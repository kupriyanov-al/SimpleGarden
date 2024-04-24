

import random
import json
import time
import datetime
from paho.mqtt import client as mqtt_client
import queue
from log_proc import *
import statistics


import collections


logger.debug('**************')

# Буффер
qBuffer = queue.Queue(maxsize=10000)

# Настройка MQTT
# -------------------------
broker = 'test.mosquitto.org'
port = 1883
topic = "raspT"
topic_param = "paramT"
topicPrc = 'prcT'
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

    def temperature(self, min, max):
        self.__temperature = random.randint(min, max)
        return self.__temperature

    def humidity(self, min, max):
        self.__humidity = random.randint(min, max)
        return 50
        # return self.__humidity

    def releState(self):
        self.__releState = bool(random.getrandbits(1))
        return False
        # return self.__releState

    def coolState(self):
        self.__coolState = bool(random.getrandbits(1))
        # return self.__coolState
        return False

    def tempProc(self, min, max):
        self.__tempProc = random.randint(min, max)
        return self.__tempProc


class MsgSendMQTT:
    def __init__(self) -> None:
        self._mesOld = {}
        self.__counter = 0

    def __compare(self, mesnew):
        if self._mesOld != mesnew:
            self._mesOld = mesnew.copy()
            return False
        return True

    def sendMqtt(self, client, topic, msg, QOS):
        print(self.__counter)
        if self.__compare(msg) != True or self.__counter == 10:
            self.__counter = 0
            now = datetime.datetime.now()
            msg["datastamp"] = now.strftime('%d.%m.%Y %H:%M:%S')

            qBuffer.put(json.dumps(msg))

            if client.connected_flag:
                while not qBuffer.empty():
                    msg = qBuffer.get()
                    result = client.publish(topic, msg, QOS, retain=True)
                    status = result[0]
                    if status == 0:
                        print(
                            f"Отправлено сообщение `{msg}` to topic `{topic}`")
                    else:
                        print(f"Failed to send message to topic {topic}")
            else:
                try:
                    client.reconnect()
                    print("reconnect error...")
                except:
                    print("reconnect error...")
        else:
            self.__counter += 1


param = ParamSetup()
valTestGen = ValueRandomGen()
contrval = MsgSendMQTT()
prc = MsgSendMQTT()
paramSend = MsgSendMQTT()


dq = collections.deque(maxlen=5)


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
    # отправляем настройки контроллера всем клиентам
    paramSend.sendMqtt(client, topic_param, param.msgParam, QOS)

    while True:

        # сгенерированные случайные данные
        temperature = valTestGen.temperature(20, 22)
        humidity = valTestGen.humidity(60, 100)
        releState = valTestGen.releState()
        coolState = valTestGen.coolState()
        tempProc = valTestGen.tempProc(30, 40)
        
        
        # среднее арифм
        dq.append(temperature)
        print(f"очередь - {list(dq)}")
        res_mean = statistics.mean(list(dq))
        print(f"среднее арифм - {res_mean}")


        

        msg = {"temperatura": temperature, "humidity": humidity,
               "coolState": releState, "releState": coolState}

        msgTempProc = {"tempProc": tempProc}

        print(f"параметры - {param.msgParam['temp_delta']}")

        contrval.sendMqtt(client, topic, msg, QOS)
        prc.sendMqtt(client, topicPrc, msgTempProc, QOS)

        print(f"temp-{msg}")
        time.sleep(5)


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
