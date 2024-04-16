
import paho.mqtt.client as mqtt
from .procDB import RecDB #recdb

import json

broker_url = "test.mosquitto.org"
broker_port = 1883
topic = "raspTest"

def on_connect(client, userdata, flags, rc):
   print(f"Соединение с сервером mqtt: {broker_url}")
   if rc == 0:
        print(
           f"Соединение OK: {rc}")
        try:
            client.subscribe(topic, qos=0)
        except:
            print("err!")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(
            f"Unexpected MQTT disconnection. Will auto-reconnect. Status connection: {rc}")
        try:
            client.reconnect()
        except:
            print("err!")
        

def on_message(client, userdata, message):
   rec = json.loads(str(message.payload.decode()))
  
   # функция записи в БД в модуле procDB
#    recdb(rec['datastamp'], rec['temperatura'],
#          rec['humidity'], rec['coolState'], rec['releState'])
#    print(rec)
   
   RecDB.record(rec['datastamp'], rec['temperatura'],
                rec['humidity'], rec['coolState'], rec['releState'])
   
   
   
   

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connect(broker_url, broker_port)

client.subscribe(topic, qos=0)

