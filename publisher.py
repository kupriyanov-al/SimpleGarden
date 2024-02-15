

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
            'temp_on': "25",
            'temp_delta': "0.2",
            'timeRele': "21:00",
            'timeReleWork' : "30"
        }
        
    @property 
    def temp_on(self):
        return self._msgParam['temp_on']
        
    @temp_on.setter
    def temp_on(self, x):
        self._msgParam['temp_on'] = x
        
    @property    
    def temp_delta(self):
        return self._msgParam['temp_delta']
        
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
        return self._msgParam['timeReleWork']

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
        if message.topic == topic_param:
            print("запись в переменные контроллера")
            
            
            if param.msgParam!=json.loads(str(message.payload.decode())):
                print("111111111")
                print(param.msgParam)
                print(json.loads(str(message.payload.decode())))
                param.msgParam=json.loads(str(message.payload.decode()))                         
               
                msg = json.dumps(param.msgParam)
                
                result = client.publish(topic_param, msg, 0, retain=True)
                
                status = result[0]
                if status == 0:
                    print(f"данные  `{msg}` to topic {topic_param}`")
                else:
                    print(f"Failed to send message to topic {topic}")
               
            
            
  
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
    msgSendTime = MsgSendTime()

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
       
        print(f"проверка temp_on={param.timeReleWork}")
       
        # temp = random.randint(20, 30)
        temp = 1
        
        time.sleep(10)
        msg = {"temperatura": temp, "humidity": 50,
               "coolState": True, "releState": False}
        
        # ------------------------------
        val = msgSendTime.timeStampMsg(msg)
        print(f" m1 = {val} ")
       
        # ______________________________
       
        # проверка изменения сообщения
        if val != False:
            print(f" m.comparemes_____________ = {val} ")  

            # Записываем в стек
            q.put(json.dumps(val))  

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
    client.subscribe(topic_param, qos=0)
    try:
        client.loop_start()
        # client.loop_forever()
        publish(client)
    except Exception as err:
        print(f"Error loop_start: {err}")
    


if __name__ == '__main__':
    run()
    
