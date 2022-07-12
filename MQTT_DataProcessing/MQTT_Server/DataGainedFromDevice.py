# coding: utf-8
#送信されてきたデータを管理するクラス
from typing import Dict


class DataGainedFromDevice:
    def __init__(self) -> None:
        self.Step = 0
        self.distance_from_center = 0.0
        self.azimuth_to_center = 0.0
        self.random_transit_time = 0.0
        self.practical_transit_time = 0.0
        self.practical_rotate_angle = 0.0
        self.ObstacleFlag_goal = 0.0
        self.ObstacleFlag_avoidance = 0.0
        self.detected_marker_color = ""
        self.Decision = 0   #reject:0, accept:1, boids:2
        
        

    def decode_json_data(self, data: Dict) -> None:
        self.Step = data['Step']
        self.distance_from_center = data['Distance']
        self.azimuth_to_center = data['Azimuth']
        self.practical_rotate_angle = data['Rotation']
        self.practical_transit_time = data['TransitTime']
        self.detected_marker_color = data['MarkerColor']
        self.Accept = data['Decision']
        
    def decode_json_obstacle_data(self, data: Dict) -> None:
        self.Step = data['Step']
        self.practical_transit_time = data['Counttime']
        self.ObstacleFlag_goal = data['ObstacleFlag_goal']
        self.ObstacleFlag_avoidance = data['ObstacleFlag_avoidance']

