

import random
import json
import time, datetime
from paho.mqtt import client as mqtt_client
import queue

# Буффер
q = queue.Queue()

# Настройка MQTT
# -------------------------
broker = 'test.mosquitto.org'
port = 1883
topic = "rasp1"
QOS = 1
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# --------------------


# температура включения вентилятора
temp_on = 25
# изменение температуры для отключения вентилятора
temp_delta = 0.2

class ParamSetup:
    def __init__(self) -> None:
        self._temp_on = 25
        self._temp_delta = 0.2
        
    @property 
    def temp_on(self):
        return self._temp_on
        
    @temp_on.setter
    def temp_on(self, x):
        self._temp_on = x
        
    @property    
    def temp_delta(self):
        return self._temp_delta
        
    @temp_delta.setter
    def temp_delta(self, x):
        self._temp_delta = x
        

param = ParamSetup()


# сравнение двух сообщений для исключения отправки данных без изменений
def compare_dict(dect, dect_old):
    # if msg is None or dict_msg is None:
    if dect == dect_old:
        return True
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
        if message.topic == "param":
            print("запись в переменные контроллера")
            param.temp_on = json.loads(
                str(message.payload.decode()))["temp_on"]
            param.temp_delta = json.loads(str(message.payload.decode()))["temp_delta"]
            print(f"запись в переменные контроллера temp_on={param.temp_on}")
            
  
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




def publish(client):
    mes_old={}

# ---------------------------    
    msg = { 
           'temp_on' : param.temp_on,
           'temp_delta' : temp_delta
    }
    msg = json.dumps(msg)
    result = client.publish("param", msg, QOS, retain=True)
    status = result[0]
    if status == 0:
        print(f"параметры отправлены  `{msg}` to topic `param`")
    else:
        print(f"Failed to send message to topic {topic}")
 #---------------------------------   
    
    while True:
       
        temp = random.randint(20, 30)
        # temp = 1
        
        time.sleep(10)
        msg = {"temperatura": temp, "humidity": 50,
               "coolState": True, "releState": False}
       
        # проверка изменения сообщения
        if not compare_dict(msg, mes_old):
            mes_old = msg.copy()

            now = datetime.datetime.now()
            msg["datastamp"] = now.strftime('%d.%m.%Y %H:%M:%S')
            msg = json.dumps(msg)
       
            # Записываем в стек
            q.put(msg)  

            print(f"connected_flag={client.connected_flag}")
        
            if client.connected_flag:
                while not q.empty():
                    msg=q.get()
                    result = client.publish(topic, msg, QOS)
                    status = result[0]
                    if status == 0:
                        print(f"Отправлено сообщение `{msg}` to topic `{topic}`") 
                    else:
                        print(f"Failed to send message to topic {topic}")
                    time.sleep(0.5)
            else:
                try:
                    client.reconnect()
                except:
                    print("reconnect error...")
            
def run():
    client = connect_mqtt()
    client.subscribe("param", qos=0)
    try:
        client.loop_start()
        # client.loop_forever()
        publish(client)
    except Exception as err:
        print(f"Error loop_start: {err}")
    


if __name__ == '__main__':
    run()
    
