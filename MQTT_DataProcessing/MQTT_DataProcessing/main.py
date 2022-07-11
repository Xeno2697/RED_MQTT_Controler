from MQTTClient import MQTTClientClass as MqttClient
from DeviceInformation import DeviceInformation as DeviceInfo
from wxglade_out import MyApp
import paho.mqtt.client as mqtt
import socket
import gettext
from threading import Thread
from multiprocessing import Value
from concurrent.futures import ThreadPoolExecutor

global mqttc
mqttc = MqttClient("DataProcessingClient")

#MQTT送受信は並列処理する。GUIを動かす裏で絶えず新規Messageがないか監視し、受信を行う。
#この使用PCのIPを取得、使用しているため、変更する場合は下記の関数の第一変数を変更すること。
host = socket.gethostname()
ip = socket.gethostbyname(host)
print("This PC's IP = ",end="")
print(ip)
#以下にGUIと操作時の処理を記述
gettext.install("RED_MQTT")

thread1 = Thread(target = mqttc.run,args=(str(ip),1883))
#thread2 = threading.Thread(target=RED_MQTT.MainLoop())
thread1.start()
#thread2.start()
RED_MQTT = MyApp(False,mqttc)
RED_MQTT.MainLoop()
#thread2.join()