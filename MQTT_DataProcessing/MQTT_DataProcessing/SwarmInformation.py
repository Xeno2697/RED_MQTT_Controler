# coding: utf-8
#群ロボット全体における情報を管理するクラス

#modules defined by Users 
import ExploreParameters

class SwarmInformation:
    def __init__(self) -> None:
        self.ExplorationParameters = ExploreParameters.ExploreParameters()
        self.Entire = 0
        self.Connected = 0
        self.DisConnected = 0
        self.CenterFindingRate = 0.0
        self.AcceptRate = 0.0
        self.RejectRate = 0.0
        self.Boids = 0