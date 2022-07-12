import server
from time import sleep
import random

N=0
saitaku = 0
kikyaku = 0
Judge = 0
R = 0
Rbe = 0
findCentre = 1
CompleteStep = 100

server.initialize()

while True:
    #sleep(0.5)
    isExploring, speed, mue, sigma, Approach_Rth, Repulsion_Rth, Height, Kikyaku, MarkerColor ,shutterspeed,_,_= server.getStatus()
    print(isExploring)
    print(MarkerColor)
    #sleep(0.5)
    
    
    
    
    
    #CompleteStep回になったら自動で停止
    if N == CompleteStep:
        
        N = 0
        while isExploring:
            isExploring,_,_,_,_,_,_,_,_,_,_,_ = server.getStatus()
            sleep(1)
            
    if isExploring:
        print(N)
        print("moveeee")
        
        #sleep(1)
        
        #距離を出す
        R=round(random.uniform(15,24),1)
        """
        if N==0:
            R=0.4
        elif N==1:
            R=0.0
        elif N==2:
            R=0.9
        """
        #R=1.0
        print(R,Rbe)
        #中心を認識した or しない
        #findCentre = random.randint(0,1)
        print("findCentre:"+str(findCentre))
        if findCentre ==0:
            R=0
        
        Boids = 0
        
        #採択 or 棄却
        print(Approach_Rth)
        if R < Approach_Rth:
            if mue > 0:
                Judge = random.randint(0,1)
                if R==0:
                    saitaku=saitaku+1
                    print("採択")
                    #server.uploadDeviceData2(N+1,1,0,0)
                elif Judge == 1:
                    saitaku = saitaku + 1
                    print("採択")
                    #server.uploadDeviceData2(N+1,1,0,0)
                else:
                    kikyaku = kikyaku + 1
                    print("棄却")
                    #server.uploadDeviceData2(N+1,0,1,0)
                
                print(saitaku,kikyaku)
                print("mue>0")
            else:
                Judge = random.randint(0,1)
                if R==0:
                    saitaku=saitaku+1
                    print("採択")
                    #server.uploadDeviceData2(N+1,1,0,0)
                elif Judge == 1:
                    saitaku = saitaku + 1
                    print("採択")
                    #server.uploadDeviceData2(N+1,1,0,0)
                else:
                    kikyaku = kikyaku + 1
                    print("棄却")
                    #server.uploadDeviceData2(N+1,0,1,0)
                
                print(saitaku,kikyaku)
                print("mue=0")
        else:
            Boids=1
            
        print("boids:"+str(Boids))
        #Boidsした or しない
        if Boids==1:
            print("boids")      
                
        Rbe = R
        
        #if findCentre == 1:
        #    
        #    server.uploadDeviceData1(N+1,R,0,MarkerColor)
        #    
        #    
        #else:
        #    
        #    server.uploadDeviceData1(N+1,-1,0,MarkerColor)
        #    
        """
        if N+1==1:
            server.uploadBatteryStatus(N+1,5)
        elif N+1==10:
            server.uploadBatteryStatus(N+1,4)
        elif N+1==15:
            server.uploadBatteryStatus(N+1,3)
        elif N+1==20:
            server.uploadBatteryStatus(N+1,2)
        elif N+1==25:
            server.uploadBatteryStatus(N+1,1)
        elif N+1==30:
            server.uploadBatteryStatus(N+1,"warning")
        """
            
        #N = N + 1 #ステップ数
        #採択，棄却，Boidsのデータをサーバに送信
        if Boids == 1:
            server.uploadDeviceData1(N+1,R,0,MarkerColor, 0, 0, Boids)
        else:
            
            if Judge==1:
                server.uploadDeviceData1(N+1,R,0,MarkerColor, 1, 0, Boids)
            else:
                server.uploadDeviceData1(N+1,R,0,MarkerColor, 0, 1, Boids)
        print()
        N = N + 1 #ステップ数
        sleep(3)
        
        server.uploadDeviceData2(N, random.randint(0,1), round(random.uniform(3,4),1))
        
    else:
        # 探査しないときは一秒待つ
        sleep(1)
        N = 0
        #server.uploadSteps(N)
        