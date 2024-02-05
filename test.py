

import random
import json
import time, datetime
from paho.mqtt import client as mqtt_client


flag_connected = 0

broker = 'test.mosquitto.org'
port = 1883
topic = "rasp"
# generate client ID with pub prefix randomly
#client_id = f'python-mqtt-{random.randint(0, 100)}'



def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    global flag_connected
    flag_connected = 1
    return client

# сравнение двух сообщений для исключения отправки данных без изменений


def compare_dict(dect, dect_old):
    # if msg is None or dict_msg is None:
    if dect == dect_old:
        return True
    return False


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Unexpected MQTT disconnection. Will auto-reconnect. Statuc{rc}")
        global flag_connected
        flag_connected = 0


def publish(client):
    msg_count = 0
    mes_old={} 
    
    
    while True:
        time.sleep(100)
        # msg = f"messages: {msg_count}"
        # now = datetime.datetime.now()
        msg = {"temperatura": random.randint(20, 35), "humidity": 50, "coolState": True, "releState": False}
        # msg = {"temperatura": 50, "humidity": 100, "coolState": True, "releState": False}
        
        # msg = sendfull(msg)
        # print(mes)
        
        if flag_connected:
            print("connect")
            
        else:
            print("disconnect")
        
        if not compare_dict(msg, mes_old):
            mes_old = msg.copy()
           
            
            now = datetime.datetime.now()
            msg["datastamp"] = now.strftime('%d.%m.%Y %H:%M:%S')
            msg = json.dumps(msg)
            result = client.publish(topic, msg)

           
            
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic} status:{status}" )
                client.reconnect()
        
       
   


def run():
    client = connect_mqtt()
    global flag_connected
    
    client.on_disconnect = on_disconnect
    publish(client)
    
    client.loop_forever(timeout=1.0, max_packets=1,
                         retry_first_connection=False)

    # client.loop_start()
    # publish(client)
    # client.loop_stop()

if __name__ == '__main__':
    run()
    