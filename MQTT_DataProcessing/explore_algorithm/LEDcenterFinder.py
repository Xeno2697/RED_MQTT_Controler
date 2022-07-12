# -*- coding: utf-8 -*-
import math
import cv2
import numpy as np
import threading
import time
import os
import sys

# --- Local ---
from CentralRecognition import CentralRecognition
from calculation import Calc
from video import Video

class LEDCenterFinder() :
    __PRE_MARKER_FREQ = 0

    def __init__(self) :
        self.video_cap = Video()
        self.central_recognizer = CentralRecognition()
        self.calculator = Calc()

    def __judg_virtual_marker(self) :
        if len(self.MARKER_FREQ) == 1 : self.VIRTUAL_MARKER_FLAG = False
        else : self.VIRTUAL_MARKER_FLAG = True

    def __video_capture(self) :
        self.video_cap.capture(self.VIDEO_NAME)

    # Detects blinking marker
    def __marker_detection(self) :
        self.__marker_detection_img = self.central_recognizer.central_recognition(self.VIDEO_NAME, self.MARKER_FREQ, self.SEE_PRE_MARKER, self.HEIGHT_CORRECTION_FLAG, self.VIRTUAL_MARKER_FLAG)

    # Calculate the distance and angle to the blinking marker
    def __calc_distance_and_phi(self) :
        self.__distance, self.__azimuth_angle= self.calculator.get_distance_and_phi(self.__marker_detection_img, self.VIDEO_NAME, self.MARKER_FREQ, self.SEE_PRE_MARKER, self.HEIGHT_CORRECTION_FLAG, self.VIRTUAL_MARKER_FLAG, self.GYRO_ANGLES)

    # Return distance[m] and angle(phi)[deg]
    def getRTheta(self, VIDEO_NAME : int, MARKER_FREQ : str, HEIGHT_CORRECTION_FLAG : bool, GYRO_ANGLES) :
        #time.sleep(2)
        self.VIDEO_NAME = str(VIDEO_NAME)
        MARKER_FREQ = MARKER_FREQ.split(sep='_')
        self.MARKER_FREQ = [int(_) for _ in MARKER_FREQ]
        self.GYRO_ANGLES = GYRO_ANGLES
        self.__judg_virtual_marker()
        if self.MARKER_FREQ == self.__PRE_MARKER_FREQ or self.VIDEO_NAME == '0' :
        #if self.MARKER_FREQ == self.__PRE_MARKER_FREQ or self.VIDEO_NAME == '1[m]-0' :
            self.SEE_PRE_MARKER = False
        else : self.SEE_PRE_MARKER = True
        self.HEIGHT_CORRECTION_FLAG = HEIGHT_CORRECTION_FLAG

        self.__video_capture()
        self.__marker_detection()
        self.__calc_distance_and_phi()

        self.__PRE_MARKER_FREQ = self.MARKER_FREQ
        self.__azimuth_angle = np.where(self.__azimuth_angle >= 0, self.__azimuth_angle, (2 * np.pi) + self.__azimuth_angle)
        self.__distance = list((self.__distance.reshape(-1)) * 0.01)
        self.__azimuth_angle = list(np.rad2deg(self.__azimuth_angle).reshape(-1))
        return self.__distance, self.__azimuth_angle

if __name__ == '__main__' :
    x = LEDCenterFinder()
    #VIDEO_NAME = input('VIDEO NAME : ')
    VIDEO_NAME = '0'
    MARKER_FREQ = '7,9'
    GYRO_ANGLES = [0, 0]
    result = x.getRTheta(VIDEO_NAME, MARKER_FREQ, True, GYRO_ANGLES)
    print(result)
    #VIDEO_NAME = '1[m]-1'
    #MARKER_FREQ = '5,7'
    #result = x.getRTheta(VIDEO_NAME, MARKER_FREQ, True)
    #print(result)