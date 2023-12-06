
import paho.mqtt.client as mqtt
from .procDB import recdb
import json

broker_url = "test.mosquitto.org"
broker_port = 1883


def on_connect(client, userdata, flags, rc):
   print(f"Соединение с сервером mqtt: {broker_url}")


def on_message(client, userdata, message):
   rec = json.loads(str(message.payload.decode()))
  
   # функция записи в БД
   recdb(rec['datastamp'], rec['temperatura'],
         rec['humidity'], rec['CoolState'], rec['ReleState'])
   print(rec)
   

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_url, broker_port)

client.subscribe("rasp", qos=0)

