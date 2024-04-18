
import RPi.GPIO as GPIO                 # Импортируем библиотеку по работе с GPIO
import Adafruit_DHT
import random
import json
import time
import datetime
from paho.mqtt import client as mqtt_client
import queue
from log_proc import *
# Импортируем библиотеку по работе с регулярными выражениями
from re import findall
# Импортируем библиотеку по работе с внешними процессами
from subprocess import check_output


# === Инициализация пинов ===
logger.debug('******START******')

DHT_PIN = 4
COOL_PIN = 14
RELE_PIN = 15
COOL_PROC_PIN = 23
RELE_PIN_RAIN = 18  # включение реле на полив

onTempProceccor = 60  # температура включения охлаждения процессора

GPIO.setmode(GPIO.BCM)
DHT_SENSOR = Adafruit_DHT.DHT22

# GPIO.setup(pin, GPIO.OUT, initial=0)
GPIO.setup(COOL_PIN, GPIO.OUT, initial=0)
GPIO.setup(RELE_PIN, GPIO.OUT, initial=0)
GPIO.setup(COOL_PROC_PIN, GPIO.OUT, initial=0)
GPIO.setup(RELE_PIN_RAIN, GPIO.OUT, initial=0)



# Буффер
qBuffer = queue.Queue(maxsize=10000)

# Настройка MQTT
# -------------------------
broker = 'test.mosquitto.org'
port = 1883
topic = "raspTest"
topic_param = "paramTest"
topicPrc = 'prc'
QOS = 1
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# --------------------


class ParamSetup:
    def __init__(self) -> None:
        self._msgParam = {
            'temp_on': "25",
            'temp_delta': "0.2",
            'timeRele': "21:00",
            'timeReleWork': "30"
        }

    @property
    def msgParam(self):
        return self._msgParam

    @msgParam.setter
    def msgParam(self, x):
        self._msgParam = x



class ValueRandomGen:
    # генератор случайных чисел
    def __init__(self) -> None:
        self.__temperature = 0
        self.__humidity = 0
        self.__releState = False
        self.__coolState = False
        self.__tempProc = False

    def temperature(self,min,max):
        self.__temperature = random.randint(min, max)
        return self.__temperature

    def humidity(self, min, max):
        self.__humidity = random.randint(min, max)
        return self.__humidity
    
    def releState(self):
        self.__releState =  bool(random.getrandbits(1))
        return self.__releState
    
    def coolState(self):
        self.__coolState = bool(random.getrandbits(1))
        return self.__coolState
    
    def tempProc(self, min, max):
        self.__tempProc = random.randint(min, max)
        return self.__tempProc
    
 
class MsgSendMQTT:
    def __init__(self) -> None:
        self._mesOld = {}

    def __compare(self, mesnew):
        if self._mesOld != mesnew:
            self._mesOld = mesnew.copy()
            return False
        return True

    # def timeStampMsg(self, mesnew):

        if self.__comparemes(mesnew) != True:

            now = datetime.datetime.now()
            mesnew["datastamp"] = now.strftime('%d.%m.%Y %H:%M:%S')
            return mesnew
        return False

    def sendMqtt(self, client, topic, msg, QOS):
        if self.__compare(msg) != True:
            now = datetime.datetime.now()
            msg["datastamp"] = now.strftime('%d.%m.%Y %H:%M:%S')
            
            qBuffer.put(json.dumps(msg))
            
            if client.connected_flag:
                while not qBuffer.empty():
                    msg = qBuffer.get()
                    result = client.publish(topic, msg, QOS, retain=True)
                    status = result[0]
                    if status == 0:
                        print(f"Отправлено сообщение `{msg}` to topic `{topic}`")
                    else:
                        print(f"Failed to send message to topic {topic}")
            else:
                try:
                    client.reconnect()
                    print("reconnect error...")
                except:
                    print("reconnect error...")
        



# температура процессора
def get_temp():
    # Выполняем запрос температуры
    temp = check_output(["vcgencmd", "measure_temp"]).decode()
    # Извлекаем при помощи регулярного выражения значение температуры из строки "temp=47.8'C"
    temp = float(findall('\d+\.\d+', temp)[0])
    temp = round(temp)  # округление до ближайшего целого

    return (temp)                            # Возвращаем результат


# Температура и влажность
def get_temp_hum():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        if (0 < humidity < 100) and (0 < humidity < 100):
            temperature = round(temperature, 2)
            humidity = round(humidity, 1)
            DHT = {'humidity': humidity, 'temperature': temperature}
            return DHT
    return False


def connect_mqtt() -> mqtt_client:
    
    def on_connect(client, userdata, flags, rc):
        print(f"on_connect flags={flags} , rc={rc}")
        
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.connected_flag = True
        else:
            print("Failed to connect, return code ", rc)
            client.reconnect()

    def on_publish(client, userdata, mid):
        print(f"on_publish mid={mid}")
         
    def on_disconnect(client, userdata, rc):
        client.connected_flag = False
        if rc != 0:
            print("Unexpected disconnection. Reconnecting...")
            try:
                client.reconnect()
            except:
              print("Disconnected")
        else:
            print("Disconnected successfully")
 
    
    def on_message(client, userdata, message):
        if message.topic == topic_param:
            logger.debug('*******запись в переменные контроллера*******')

            if param.msgParam != json.loads(str(message.payload.decode())):
                param.msgParam = json.loads(str(message.payload.decode()))
                paramSend.sendMqtt(client, topic_param, param.msgParam, QOS)

           
            
            
  
    client = mqtt_client.Client(client_id, clean_session=False)

    client.connected_flag = True
    
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(broker, port)  # 
    
    return client


def publish(client):
    
    ReleState = False
    CoolState = False
    CoolProcState = False
    
    # отправляем настройки контроллера всем клиентам
    paramSend.sendMqtt(client, topic_param, param.msgParam, QOS)
    
    while True:
        
        tempProc = get_temp()  # температура процессора
        
        if tempProc > onTempProceccor and not CoolProcState or tempProc < onTempProceccor - 5 and CoolProcState:
            CoolProcState = not CoolProcState         # Меняем статус состояния
            # Задаем новый статус пину управления
            GPIO.output(COOL_PROC_PIN, CoolProcState)
        
        msgTempProc = {"tempProc": tempProc}
        msgProcMqtt.sendMqtt(client, topicPrc, msgTempProc, QOS)
        
        temp_on = float(param.msgParam['temp_on'])
        temp_delta = float(param.msgParam['temp_delta'])
        timeRele = param.msgParam['timeRele']
        timeReleWork = float(param.msgParam['timeReleWork'])
        

        DHT = get_temp_hum()
        if DHT == False:
            continue

        if DHT['temperature'] > temp_on and not CoolState or DHT['temperature'] < temp_on-temp_delta and CoolState:
            CoolState = not CoolState
            GPIO.output(COOL_PIN, CoolState)

        
        time_obj = time.strptime(timeRele, "%H:%M")  # преобразование времени в объект

        now = datetime.datetime.now()
        todayon = now.replace(hour=time_obj.tm_hour,
                              minute=time_obj.tm_min, second=0, microsecond=0)
        seconds = (now - todayon).total_seconds()
        if now >= todayon and seconds < timeReleWork and not ReleState or now > todayon and seconds > timeReleWork and ReleState:
            ReleState = not ReleState
            GPIO.output(RELE_PIN, ReleState)
           
        
        temperature = round(DHT['temperature'] /1)*1
        humidity = round(DHT['humidity']/10)*10
        
        msg = {"temperatura": temperature, "humidity": humidity,
               "coolState": CoolState, "releState": ReleState}
        
        msgMqtt.sendMqtt(client, topic, msg, QOS)
        
        
        time.sleep(10)


param = ParamSetup()
valTestGen = ValueRandomGen()
msgMqtt = MsgSendMQTT()
msgProcMqtt = MsgSendMQTT()
paramSend = MsgSendMQTT()

def run():
    client = connect_mqtt()
    client.subscribe(topic_param, qos=0)
    try:
        client.loop_start()
        # client.loop_forever()
        publish(client)
    except Exception as err:
        print(f"Error loop_start: {err}")
    


if __name__ == '__main__':
    run()
    
