# coding: utf-8
#探査パラメータを管理するクラス
from typing import Dict


class ExploreParameters:
    def __init__(self) -> None:
        self.is_exploring = False
        self.transit_time = 2
        self.Inner_r_th = 0.0
        self.mu = 1.0
        self.sigma = 1.0
        self.Outer_r_th=3.0        
        self.height = 2.2
        self.step_limit = 10000
        self.reject_mode = 'A'
        self.marker_color = 'Green'
        self.shutter_speed = 100
        self.left_pwm_variate = 0.0
        self.right_pwm_variate = 0.0
        
    def decode_json_data(self, data: Dict) -> None:
        self.is_exploring = data['IsExploring']
        self.transit_time = data['TransitTime']
        self.Inner_r_th = data['Inner_Rth']
        self.mu = data['Mu']
        self.sigma = data['Sigma']
        self.Outer_r_th = data['Outer_Rth']        
        self.height = data['Height']
        self.step = data['CompleteStep']
        self.reject_mode = data['Reject']
        self.marker_color = data['MarkerColor']
        self.shutter_speed = data['ShutterSpeed']
        self.left_pwm_variate = data['LeftPWM']
        self.right_pwm_variate = data['RightPWM']
