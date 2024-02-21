import random
import json
from innerClass import MsgSendTime, ParamSetup
from paho.mqtt import client as mqtt_client

broker = 'test.mosquitto.org'
port = 1883
topic = "rasp1"
topic_param = "param1"
QOS = 1
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# --------------------


def connect_mqtt(param) -> mqtt_client:

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

            if param.msgParam != json.loads(str(message.payload.decode())):
                print("111111111")
                print(param.msgParam)
                print(json.loads(str(message.payload.decode())))
                param.msgParam = json.loads(str(message.payload.decode()))

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
