from MQTTClient import MQTTClientClass
from wxglade_out import MyApp
import socket
import gettext
from threading import Thread
from multiprocessing import Value

mqttc = MQTTClientClass()

#MQTT送受信は並列処理する。GUIを動かす裏で絶えず新規Messageがないか監視し、受信を行う。
#この使用PCのIPを取得、使用しているため、変更する場合は下記の関数の第一変数を変更すること。
print("Please enter your IP. If you want this PC to be the server, enter 's'.")
ip = input("Blocker IP = ")
if ip == 's' or None:
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    print("This server's IP = ",end="")
    print(ip)

#以下にGUIと操作時の処理を記述
gettext.install("RED_MQTT")

thread1 = Thread(target = mqttc.run,args=(str(ip),1883))
#thread2 = threading.Thread(target=RED_MQTT.MainLoop())
thread1.start()
#thread2.start()
RED_MQTT = MyApp(False,mqttc)
RED_MQTT.MainLoop()
mqttc._continue = False
#thread2.join()