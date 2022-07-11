import json
from tkinter import E
from types import ModuleType
import sys
#sys.path.append("/home/pi/.local/python3.7/site-package")
import paho.mqtt.client as mqtt
import threading
import socket
import random

global data
data={'IsExploring':False, 'TransitTime':3, 'Mu':1.0, 'Sigma':0.0, 'Inner_Rth':3.0, 'Outer_Rth':3.0, 'Height':3.0, 'Reject':'A', 'MarkerColor':'Green', 'Height_Correction':True,'ShutterSpeed':100, 'LeftPWM':0,'RightPWM':0}

def get_myip_address():
    ip_address = '';
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

myip=get_myip_address()
myip="192.168.8.202"

def search():
    #将来的にここでIPアドレスを検索
    return '192.168.0.176'

def initialize():

    #メッセージが届いたときの処理
    def on_message(client, userdata, msg):
        #msg.topicにトピック名がmsg.payloadに届いたデータ本体が入っている
        #トピックによって条件分岐し、それぞれのバラメータを代入
        if msg.topic =="RED/Status":
            global data
            data = json.loads(str(msg.payload)[2:len(str(msg.payload))-1])
            
            print(getStatus())
        elif msg.topic == "RED/"+myip+"/Param":
            #global data
            data = json.loads(str(msg.payload)[2:len(str(msg.payload))-1])
            
            print(getStatus())

    #サーバに接続できた時の処理（MQTT）
    def on_connect(client, userdata, flag, rc):
        #接続できた旨表示
        print("connected OK.")
        
        client.publish("RED/"+myip+"/Connect","connect RED "+myip,0,True)
        client.publish("RED/"+myip+"/connect","connect RED "+myip,0,True)
        #subするトピックを設定
        client.subscribe("RED/Status",qos=1)
        client.subscribe("RED/"+myip+"/Param",qos=1)

    #サーバが切断したときの処理（MQTT）
    def on_disconnect(client, userdata, flag, rc=-1):
        if rc != 0:
            print("Unexpected disconnection.")
            global data
            data['IsExploring']=False
    
    global client
    client = mqtt.Client("RED(" + myip + ")") #クラスのインスタンスの作成。()の中身はクライアントネームで自分のIPアドレスとした。

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.will_set("RED/"+myip+"/disconnect", "disconnect RED " + myip, 0, True);
    client.reconnect_delay_set(min_delay = 5, max_delay=10)   #再接続時の時間間隔を設定
    
    try:
        client.connect("192.168.4.33", 1883, 60)
    except Exception as e:
        print("connection failed")
        print(e)
    
    threading.Thread(target = client.loop_forever).start()
    
    # Not found.
    #return '192.168.0.176'

def getStatus():

    return(data['IsExploring'], data['TransitTime'], data['Mu'], data['Sigma'] ,data['Inner_Rth'],data['Outer_Rth'] ,data['Height'], data['Reject'],data["MarkerColor"], data['ShutterSpeed'],data["LeftPWM"],data["RightPWM"])


def uploadImage(imageData, filename):
    #引数の型：binary, string サーバに画像をアップロードする関数

    try:
        
        client.publish("RED/" + myip + "/Image/filename",filename, 0)
        client.publish("RED/" + myip + "/Image/imageData",imageData, 0)
        print("send filename and imageData")

    except Exception as e:
        print("Upload error(image)")
        print(e)
        
def uploadDeviceData(Step, R, Th, saitaku, kikyaku, boids):
    try:
        #client.publish("RED/" + myip + "/DeviceData",str(Step) +" "+ str(R) +" "+str(saitaku) +" "+ str(kikyaku) +" "+str(boids) +" "+" RED "+myip , 0)
        #print("upload DeviceData")
        #dict -> json形式にする
        DataDict = {"Group":"RED", "ID":myip, "Step":str(Step), "Distance":str(R), "Azimuth":str(Th)}
        DataJson = json.dumps(DataDict)
        client.publish("RED/" + myip + "/DeviceData",DataJson, 0)
        print("upload DeviceData")
    
    except Exception as e:
        print("upload error(DeviceData)")
        print(e)
        
def uploadBatteryStatus(Step,level):
    try:
        #dict -> json形式にする
        DataDict = {"Group":"RED", "ID":myip, "Step":str(Step), "Battery":str(level)}
        DataJson = json.dumps(DataDict)
        client.publish("RED/" + myip + "/Battery",DataJson, 0)
        print("upload DeviceData")
    
    except Exception as e:
        print("upload error(Step)")
        print(e)
        
def uploadDeviceData1(Step, R, Th,color, saitaku, kikyaku, boids):
    try:
        #dict -> json形式にする
        DataDict = {"Group":"RED", "ID":myip, "Step":str(Step), "Distance":str(R), "Azimuth":str(Th),"Color":color,"Accept":str(saitaku), "Reject":str(kikyaku), "Boids":str(boids)}
        DataJson = json.dumps(DataDict)
        client.publish("RED/" + myip + "/DeviceData",DataJson, 0)
        print("upload DeviceData")
    
    except Exception as e:
        print("upload error(DeviceData)")
        print(e)
        
#採択，棄却，Boidsのデータをサーバに送信
def uploadDeviceData2(Step, collision, untilTime):
    try:
        #dict -> json形式にする
        DataDict = {"Group":"RED", "ID":myip, "Step":str(Step), "ObstacleFlag":str(collision), "CountTime":str(untilTime)}
        DataJson = json.dumps(DataDict)
        client.publish("RED/" + myip + "/Obstacle",DataJson , 0)
        print("upload DeviceData")
    
    except Exception as e:
        print("upload error(DeviceData)")
        print(e)

if __name__ == '__main__':
    print(initialize())
    