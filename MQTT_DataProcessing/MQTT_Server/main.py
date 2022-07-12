from MQTTClient import MQTTClientClass
from wxglade_out import MyApp
import socket
import gettext
import time
from threading import Thread
from multiprocessing import Value

mqttc = MQTTClientClass()

#MQTT送受信は並列処理する。GUIを動かす裏で絶えず新規Messageがないか監視し、受信を行う。
#この使用PCのIPを取得、使用しているため、変更する場合は下記の関数の第一変数を変更すること。
b = True
while b:
    try:
        print("Please enter your IP. If you want this PC to be the server, enter 's'.")
        ip = input("Blocker IP = ")
        port = 1883
        if ip == 's' or "":
            host = socket.gethostname()
            ip = socket.gethostbyname(host)
        print("This server's IP = ",end="")
        print(ip)
        print("port is",end="")
        print(port)
        gettext.install("RED_MQTT")
        thread1 = Thread(target = mqttc.run,args=(str(ip),1883))
        thread1.start()
        time.sleep(1)
        b = False
    except:
        print("Error! Can't connect. Maybe IP wrong?")
        b= True

    gettext.install("MQTT_SERVER")
    MQTT_SERVER = MyApp(False,mqttc)
    MQTT_SERVER.MainLoop()
    mqttc._continue = False