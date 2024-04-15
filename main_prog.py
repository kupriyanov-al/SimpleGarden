
import RPi.GPIO as GPIO                 # Импортируем библиотеку по работе с GPIO
import Adafruit_DHT
import random
import json
import time, datetime
from paho.mqtt import client as mqtt_client
import queue
from log_proc import *
from re import findall                      # Импортируем библиотеку по работе с регулярными выражениями
from subprocess import check_output         # Импортируем библиотеку по работе с внешними процессами


 # === Инициализация пинов ===
logger.debug('******START******')

DHT_PIN = 4
COOL_PIN = 14 
RELE_PIN = 15
COOL_PROC_PIN = 23
RELE_PIN_RAIN = 18 # включение реле на полив 


GPIO.setmode(GPIO.BCM)
DHT_SENSOR = Adafruit_DHT.DHT22
               
#GPIO.setup(pin, GPIO.OUT, initial=0)
GPIO.setup(COOL_PIN, GPIO.OUT, initial=0)
GPIO.setup(RELE_PIN, GPIO.OUT, initial=0)
GPIO.setup(COOL_PROC_PIN, GPIO.OUT, initial=0)
GPIO.setup(RELE_PIN_RAIN, GPIO.OUT, initial=0)

# Буффер
q = queue.Queue()

# Настройка MQTT
# -------------------------
broker = 'test.mosquitto.org'
port = 1883
topic = "rasp1"
topic_param = "param1"
QOS = 1
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# --------------------



class MsgSendTime:
    def __init__(self) -> None:
        self._mesOld = {}
        
    def __comparemes(self, mesnew):
        if self._mesOld != mesnew:
            self._mesOld = mesnew.copy()
            return False
        return True
        

    
    def timeStampMsg(self, mesnew):
        
        if self.__comparemes(mesnew) !=True:
            
            now = datetime.datetime.now()
            mesnew["datastamp"] = now.strftime('%d.%m.%Y %H:%M:%S')
            return mesnew
        return False
    

class ParamSetup:
    def __init__(self) -> None:
        self._msgParam = {
            'temp_on': 25,
            'temp_delta': 0.2,
            'timeRele': "22:23",
            'timeReleWork' : 30
        }
        
    @property 
    def temp_on(self):
        return float(self._msgParam['temp_on'])
        
    @temp_on.setter
    def temp_on(self, x):
        self._msgParam['temp_on'] = x
        
    @property    
    def temp_delta(self):
        return float(self._msgParam['temp_delta'])
        
    @temp_delta.setter
    def temp_delta(self, x):
        self._msgParam['temp_delta'] = x
        
    @property 
    def timeRele(self):
        return self._msgParam['timeRele']
        
    @timeRele.setter
    def timeRele(self, x):
        self._msgParam['timeRele'] = x
        
    @property
    def timeReleWork(self):
        return float(self._msgParam['timeReleWork'])

    @timeReleWork.setter
    def timeReleWork(self, x):
        self._msgParam['timeReleWork'] = x
    
    @property    
    def msgParam(self):
        return self._msgParam 
        
    @msgParam.setter
    def msgParam(self, x):
        self._msgParam  = x
        

param = ParamSetup()

# температура процессора
def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode()    # Выполняем запрос температуры
    temp = float(findall('\d+\.\d+', temp)[0])                   # Извлекаем при помощи регулярного выражения значение температуры из строки "temp=47.8'C"
    return(temp)                            # Возвращаем результат




def connect_mqtt() -> mqtt_client:
    
    def on_connect(client, userdata, flags, rc):        
        if rc == 0:            
            logger.debug('Connected to MQTT Broker!')
            client.connected_flag = True
        else:
            logger.debug("Failed to connect, return code ", rc)
            client.reconnect()

    def on_publish(client, userdata, mid):
        print(f"on_publish mid={mid}")
         
    def on_disconnect(client, userdata, rc):
        client.connected_flag = False
        if rc != 0:
            logger.debug("Unexpected disconnection. Reconnecting...")
            try:
                client.reconnect()
            except:
              logger.debug("Disconnected")
        else:
            logger.debug("Disconnected successfully")
 
    
    def on_message(client, userdata, message):
        if message.topic == topic_param:            
            if param.msgParam!=json.loads(str(message.payload.decode())):
               
                print(param.msgParam)
                print(json.loads(str(message.payload.decode())))
                param.msgParam=json.loads(str(message.payload.decode()))                         
               
                msg = json.dumps(param.msgParam)
                
                result = client.publish(topic_param, msg, 0, retain=True)
                
                status = result[0]
                if status == 0:
                    logger.debug(f"send pub {msg} to topic {topic_param}")
                else:
                    logger.debug(f"Failed to send message to topic {topic}")
                    
  
    client = mqtt_client.Client(client_id, clean_session=False)

    client.connected_flag = True
    # client.reconnect_delay_set(min_delay=1, max_delay=120)
    # client.reconnect_max_delay_set(maximum_delay=300)
    
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(broker, port)  # 
    
    return client


def get_temp_hum():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        if (0 < humidity < 100) and (0 < humidity < 100): 
            temperature = round(temperature,2)
            humidity = round(humidity,1)
            DHT={'humidity':humidity,'temperature':temperature}        
            return DHT
    return False

def publish(client):
    msgSendTime = MsgSendTime()
    ReleState = False
    CoolState = False
    CoolProcState = False
# ---------------------------    

    # msg = json.dumps(param.msgParam)
    # result = client.publish(topic_param, msg, 0, retain=True)
    # status = result[0]
    # if status == 0:
    #     print(f"параметры отправлены  `{msg}` to topic {topic_param}`")
    # else:
    #     print(f"Failed to send message to topic {topic}")
 #---------------------------------   
    
    while True:
        temp = 1        
        time.sleep(10)

        tempProc = get_temp()
        
        if tempProc > 60 and not CoolProcState or tempProc < 60 - 10 and CoolProcState:
            CoolProcState = not CoolProcState         # Меняем статус состояния
            GPIO.output(COOL_PROC_PIN, CoolProcState) # Задаем новый статус пину управления

        
        print(tempProc)

        DHT=get_temp_hum()
        if DHT == False:
            continue
              
        if DHT['temperature']>param.temp_on and not CoolState or DHT['temperature']<param.temp_on-param.temp_delta and CoolState:
            CoolState=not CoolState
            GPIO.output(COOL_PIN, CoolState)
               
        
        time_obj = time.strptime(param.timeRele, "%H:%M") # преобразование времени в объект 

        now = datetime.datetime.now()
        todayon = now.replace(hour = time_obj.tm_hour, minute=time_obj.tm_min, second =0, microsecond =0)
        seconds = (now  - todayon).total_seconds()
        if now >= todayon and seconds < param.timeReleWork and not ReleState or now > todayon and seconds > param.timeReleWork and ReleState:
            ReleState = not ReleState
            GPIO.output(RELE_PIN, ReleState)
            #print(ReleState)
         
        temperature = round(DHT['temperature'] /0.5)*0.5
        
        
        #temperature = round(DHT['temperature'] ,3)
        
        humidity = round(DHT['humidity']/10)*10
        
        # temperature = DHT['temperature'] 
        # humidity = DHT['humidity']
            
        msg = {"temperatura": temperature, "humidity": humidity, "coolState": CoolState, "releState": ReleState}

        val = msgSendTime.timeStampMsg(msg)

        # проверка изменения сообщения
        if val != False:           

            # Записываем в стек
            q.put(json.dumps(val))  
        
            if client.connected_flag:
                while not q.empty():
                    msg=q.get()
                    result = client.publish(topic, msg, QOS, retain=True)
                    status = result[0]
                    if status == 0:
                        logger.debug(f"Send MQTT message {msg} to topic {topic}")
                    else:
                        logger.debug(f"Failed to send message to topic {topic}")
                    time.sleep(0.5)
            else:
                try:
                    client.reconnect()
                except:
                    logger.error("reconnect error...")
            
def run():
    client = connect_mqtt()
    client.subscribe(topic_param, qos=0)
    try:
        client.loop_start()
        # client.loop_forever()
        publish(client)
    except Exception as err:
        logger.error(f"Error loop_start: {err}")
    


if __name__ == '__main__':
    run()
    
