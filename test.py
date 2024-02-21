

import random
import json
import time

from paho.mqtt import client as mqtt_client
import queue
from innerClass import MsgSendTime, ParamSetup
from mqtt_ph import *

# Буффер
q = queue.Queue()

# Настройка MQTT
# -------------------------


param = ParamSetup()







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
 # ---------------------------------

    while True:

        print(f"проверка temp_on={param.timeReleWork}")

        temp = random.randint(20, 30)
        temp = temp*1.23

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
                    msg = q.get()
                    result = client.publish(topic, msg, QOS)
                    status = result[0]
                    if status == 0:
                        print(
                            f"Отправлено сообщение `{msg}` to topic `{topic}`")
                    else:
                        print(f"Failed to send message to topic {topic}")
                    time.sleep(0.5)
            else:
                try:
                    client.reconnect()
                except:
                    print("reconnect error...")


def run():
    client = connect_mqtt(param)
    client.subscribe(topic_param, qos=0)
    try:
        client.loop_start()
        # client.loop_forever()
        publish(client)
    except Exception as err:
        print(f"Error loop_start: {err}")


if __name__ == '__main__':
    run()
