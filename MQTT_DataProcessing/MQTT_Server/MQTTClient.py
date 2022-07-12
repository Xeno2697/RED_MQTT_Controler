# coding: utf-8
#データ収集のためのMQTTクライアントを管理するクラス
import sys
import os
from tkinter import Image
sys.path.append('c:/users/kaede/appdata/local/programs/python/python39/lib/site-packages')
import paho.mqtt.client as mqtt
import json
from re import A
import locale
import csv
import time
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
from DeviceInformation import DeviceInformation

#modules defined by Users 
from ExploreParameters import ExploreParameters as explo
from DataGainedFromDevice import DataGainedFromDevice
import SwarmInformation
import time

#以下は、MQTTから受信したデータを、クラス内部変数に保存するコードである・・・たぶん
class MQTTClientClass(mqtt.Client):
    
    #デバイス情報
    __DeviceInformationList = []    #リストのオブジェクトはDeviceInformation、そのなかの.DeviceDataリストにDataGainedFromDevice
    #スワーム情報
    __SwarmInformation = SwarmInformation.SwarmInformation()

    connectingIP = "Error"
    _continue = True
    
    #接続できた時に起こる処理
    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: "+str(rc))
        self.publish("DataProcessingClient/Connect", "Connect DataProcessingClient", 0, True)
        self.SubscribeTopics()

    #接続失敗時に起こる処理
    def on_connect_fail(self, mqttc, obj):
        print("Connect failed")
        
    #メッセージを受け取った時に起こる処理
    def on_message(self, mqttc, obj, msg):
        
        if("Status" in msg.topic):
            self.DataProcessingforStatus(msg.topic, msg.payload)
            
        elif("Param" in msg.topic):
            self.DataProcessingforParam(msg.topic, msg.payload)
            
        elif("Connect" in msg.topic):
            self.DataProcessingforConnect(msg.topic, msg.payload)
            
        elif("Disconnect" in msg.topic):
            self.DataProcessingforDisconnect(msg.topic, msg.payload)
            
        elif("FloorImage" in msg.topic):
            self.DataProcessingforFloorImage(msg.topic, msg.payload)
            
        elif("CeilImage" in msg.topic):
            self.DataProcessingforCeilImage(msg.topic, msg.payload)
            
        elif("DeviceData" in msg.topic):
            self.DataProcessingforDeviceData(msg.topic, msg.payload)
            
        elif("Obstacle" in msg.topic):
            self.DataProcessingforObstacle(msg.topic, msg.payload)
            
        elif("RobotStatus" in msg.topic):
            self.DataProcessingforRobotStatus(msg.topic, msg.payload)
            
    #データを送信したときに起こる処理
    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    #MQTTclientに関するログが発生した時の処理
    def on_log(self, mqttc, obj, level, string):
        print(string+"!!!!!" + str(time.time()))
    
    #クライアントを起動する際の処理
    def run(self,host : str = "192.168.4.33",port :int=1883,keepalive : int = 60):
        self.reconnect_delay_set(min_delay = 5, max_delay=10)   #再接続時の時間間隔を設定
        self.will_set("DataProcessingClient/Disconnect", "disconnect DataProcessingClient", 0, True);    #不意に切断した場合の遺言メッセージを設定
        try:            
            self.connect(host, port, keepalive)  #Brokerへの接続を試みる
            self.connectingIP = host
            
        except Exception as e:
            print("connection failed")
            print(e)        
        
        #マルチスレッド用に、定期的に処理を少し休む
        while self._continue:
            self.loop_start()
            time.sleep(0.1)
            
    
    #受け取りたいデータのトピックをBrokerに送信
    def SubscribeTopics(self):
        self.subscribe("+/Status", qos = 0)
        self.subscribe("+/+/Param", qos = 0)
        self.subscribe("+/+/Connect", qos = 0)
        self.subscribe("+/+/Disconnect", qos = 0)
        self.subscribe("+/+/FloorImage", qos = 0)
        self.subscribe("+/+/CeilImage", qos = 0)
        self.subscribe("+/+/DeviceData", qos = 0)
        self.subscribe("+/+/Obstacle", qos = 0)
        self.subscribe("+/+/RobotStatus", qos = 0)

    #トピックに応じたデータ処理
    #Status
    def DataProcessingforStatus(self, topic:str, payload):
        print("Recieved Topic:" + topic)
        
        data = json.loads(payload.decode("ascii"))
        self.__SwarmInformation.ExplorationParameters = data
        print("ExploreParameters is ",end="")
        print(self.__SwarmInformation.ExplorationParameters)
        
        #設定分布の正規分布を描画
        #self.PlotGaussPDF(self.__SwarmInformation.ExplorationParameters["Mu"], self.__SwarmInformation.ExplorationParameters["Sigma"], self.__SwarmInformation.ExplorationParameters['Outer_Rth'])
        
    #Param
    def DataProcessingforParam(self, topic:str, payload):
        print("Topic:" + topic)
        
        #Topicから対象ロボットのIPを抽出
        robotGroup = topic.split('/')[0]#Group/IP/ParamのGroup
        robotIP = topic.split('/')[1]#Group/IP/ParamのIP
        
        data = payload.decode("ascii")
        
        #DeviceInformationクラスのExplorationParametersの値をそれぞれ更新
        for device in self.__DeviceInformationList:
            
            if device.Group == robotGroup and device.ID == robotIP :
                print(device.ExplorationParameters)
                device.ExplorationParameters = data
                print(device.ExplorationParameters)
                break
         
    #Connect 同時に__DeviceInformationListに新規通信したREDを登録
    def DataProcessingforConnect(self, topic:str, payload):
        print("Topic:" + topic)
        
        #情報の抽出
        #例：connect RED 192.168.8.111
        data = payload.decode("ascii")
        ConnectedIP = data.split(' ')[2]
        ConnectedName = data.split(' ')[1]
        
        #リストの処理
        IndividualAddFlag = True
        for device in self.__DeviceInformationList:
            
            if device.Group == ConnectedName and device.ID == ConnectedIP :
                
                IndividualAddFlag = False
                device.IsConnected = True
                break
        if IndividualAddFlag :
            self.__DeviceInformationList.append(DeviceInformation(ConnectedName, ConnectedIP, True, self.__SwarmInformation.ExplorationParameters, "100"))
            
        
        for device in self.__DeviceInformationList:
            print(device.Group, device.ID, device.IsConnected, device.ExplorationParameters, device.BatteryLevel)       
        
    #Disconnect
    def DataProcessingforDisconnect(self, topic:str, payload):
        print("Topic:" + topic)
        
        #情報の抽出
        #例：disconnect RED 192.168.8.111
        data = payload.decode("ascii")
        ConnectedIP = data.split(' ')[2]
        ConnectedName = data.split(' ')[1]
        
        #リストの処理
        IndividualAddFlag = True
        for device in self.__DeviceInformationList:
            
            if device.Group == ConnectedName and device.ID == ConnectedIP :
                
                IndividualAddFlag = False
                device.IsConnected = False
                break
        if IndividualAddFlag :
            self.__DeviceInformationList.append(DeviceInformation(ConnectedName, ConnectedIP, False))
        
        for device in self.__DeviceInformationList:
            print(device.Group, device.ID, device.IsConnected)       
          
    #FloorImage
    def DataProcessingforFloorImage(self, topic:str, payload:bytes):
        print("Topic:" + topic)
        id = topic.split("/")[1]
        #データの抽出
        #Image_dict = {filename:base64.b64encode(imageData).decode('utf-8')}
        Image_dict : dict = json.loads(payload.decode("ascii"))
        for key in Image_dict.keys():
            image_data = Image_dict[key]
            LocalPath = os.path.abspath('.')+"/picture/"+id+"/floorimage/"+ key
            try:
                with open(LocalPath,mode='w') as f:
                    f.write(image_data)
            except:
                os.mkdir(os.path.abspath('.')+"/picture/"+id+"/floorimage")
                with open(LocalPath,mode='w') as f:
                    f.write(image_data)
        #保存 or DBへ蓄積　一旦保存しましょうBy鈴木
    
    #CeilImage
    def DataProcessingforCeilImage(self, topic:str, payload:bytes):
        print("Topic:" + topic)
        id = topic.split("/")[1]
        #データの抽出
        #Image_dict = {filename:base64.b64encode(imageData).decode('utf-8')}
        Image_dict : dict = json.loads(payload.decode("ascii"))
        for filename in Image_dict.keys():
            image_data = Image_dict[filename]
            LocalPath = os.path.abspath('.')+"/picture/"+id+"/ceilimage/"+ filename
            try:
                with open(LocalPath,mode='w') as f:
                    f.write(image_data)
            except:
                os.mkdir(os.path.abspath('.')+"/picture/"+id+"/ceilimage")
                with open(LocalPath,mode='w') as f:
                    f.write(image_data)
        #保存 or DBへ蓄積　一旦local保存しましょうBy鈴木
    
    #DeviceData
    def DataProcessingforDeviceData(self, topic:str, payload:bytes):
        print("Topic:" + topic)
        #DataDict = {"Group":"RED", "ID":myip, "Step":str(Step), "Distance":str(R), "Azimuth":str(Th),"TransitTime":str(TransitTime),"Accept":str(accept), "Reject":str(reject), "Boids":str(boids),"RandomRot":str(Rot),"Color":color }"color = Hz"
        datadict = json.loads(payload.decode("ascii"))
        b = True
        for i in range(len(self.__DeviceInformationList)):
            if self.__DeviceInformationList[i].ID == datadict["ID"]:
                b = False
                break
        if b:
            print("error! this id is none in list.")
        else:
            to = DataGainedFromDevice
            to.decode_json_data(datadict)
            self.__DeviceInformationList[i].DeviceData.append(to)   
        
    #Obstacle　上記のDeviceDataと分離しているのはなぜか、統合すべきなのか？
    def DataProcessingforObstacle(self, topic:str, payload:bytes):
        print("Topic:" + topic)
        datedict = json.loads(payload.decode("ascii"))
        #DataDict = {"Group":"RED", "ID":myip, "Step":Step, "ObstacleFlag_goal":ObstacleFlag_goal, "ObstacleFlag_avoidance":ObstacleFlag_avoidance, "CountTime":CountTime}
        b = True
        for i in range(len(self.__DeviceInformationList)):
            if self.__DeviceInformationList[i].ID == datedict["ID"]:
                b = False
                break
        if b:
            print("error! this id is none in list.")
        else:
            to = DataGainedFromDevice
            to.decode_json_obstacle_data(datedict)
            self.__DeviceInformationList[i].DeviceData.append(to)     
        
    #RobotStatus
    def DataProcessingforRobotStatus(self, topic:str, payload:bytes):
        print("Topic:" + topic)  
        #DataDict = {"Group":"RED", "ID":myip, "CeilCam":str(CeilCamStatus), "FloorCam":str(FloorCamStatus), "Battery":str(BatteryStatus)}
        datedict = json.loads(payload.decode("ascii"))
        search_id = datedict["ID"]
        b = True
        for i in range(len(self.__DeviceInformationList)):
            if self.__DeviceInformationList[i].ID == search_id:
                b = False
                break
        if b:
            self.__DeviceInformationList[len(self.__DeviceInformationList)] = DeviceInformation(datedict["Group"],datedict["ID"],explo(),datedict["Battery"])      
        else:
            self.__DeviceInformationList[i] = DeviceInformation(datedict["Group"],datedict["ID"],explo(),datedict["Battery"])

    #Generate GaussDisribution
    def PlotGaussPDF(self, mu, sigma, Outer_r_th):
        norm_vector = np.linspace(0, Outer_r_th + 2,1000)
        p = []
        for i in range(len(norm_vector)):
            p.append(norm.pdf(x=norm_vector[i], loc = mu, scale = sigma))
        plt.scatter(norm_vector, p)
        plt.title("Gaussian Distribution")
        plt.xlabel("R[m]")
        plt.ylabel("Probability")
        plt.savefig("DesignedGauss.png")


#mqttc = MQTTClientClass("DataProcessingClient")
#rc = mqttc.run() #MQTT起動

#print("rc: "+str(rc))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    