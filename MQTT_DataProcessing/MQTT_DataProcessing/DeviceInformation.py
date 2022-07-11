# coding: utf-8
#個々のロボットの情報を管理するクラス
from typing import Dict
#modules defined by Users 
from ExploreParameters import ExploreParameters as exp

class DeviceInformation:
    
    def __init__(self, Group:str, ID:int, IsConnected:bool, Parameters:exp, BatteryLevel) -> None:
        self.Group = Group
        self.ID = ID
        self.IsConnected = IsConnected
        self.ExplorationParameters = Parameters
        self.DeviceData = [] #リストのオブジェクトはDataGainedFromDevice
        self.BatteryLevel = BatteryLevel
        
