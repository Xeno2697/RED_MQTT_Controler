# -*- coding: utf-8 -*-

import cv2
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('/home/pi/Red2.0-Control-Software')

# --- Local ---
import server


class FloorImage():
    
    __MyIP = server.get_my_IPaddress()
    __ImageDir = "serverImage"
    __ImageSuffix = ".png"
    FileName = ""
    
    def __init__(self) :
        if not os.path.exists(self.__ImageDir):
            os.makedirs(self.__ImageDir)
    
    def takeImage(self, Step, floorcamera_status):    
        self.FileName = str(Step)+"_floor" + self.__ImageSuffix
        try:
            floorcamera_status = floorcamera_status[-1:]
            floorCamera = cv2.VideoCapture(int(floorcamera_status))
            isSucceed, frame = floorCamera.read()
            
            if isSucceed:                
                cv2.imwrite(os.path.join(self.__ImageDir, self.FileName), frame)
                
        except Exception as e:
            print("takeImage error")
            print(e)
        
        floorCamera.release()
        return self.FileName
    
    def UploadImage(self, filename:str, Distance, Step, DegTheta):
        imageFile = open(os.path.join(self.__ImageDir, filename), "rb")
        imageFileName = str(round(Distance,1)).replace('.','-')+"_"+str(round(DegTheta,1)).replace('.','-')+"_"+str(Step)+"_"+self.__MyIP.split('.')[3] + "_floor" + self.__ImageSuffix    
        server.uploadImage(imageFile.read(), imageFileName, "FloorImage")
        imageFile.close()
        os.remove(os.path.join(self.__ImageDir, filename))

