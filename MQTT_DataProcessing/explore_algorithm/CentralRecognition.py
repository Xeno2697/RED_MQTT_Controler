# -*- coding:utf-8 -*-
import cv2
import numpy as np
import os
import time

# --- Local ---
import calculation
from FrameDivision import FrameDivision

class CentralRecognition() :

    __OUTPUT_DIR = 'output/'
    __IMG_EXT = '.png'

    # Sampling points
    __N = 32

    # FPS
    __dt = 1 / 30

    # Window Function
    __win = np.hanning(__N).astype(np.float32)

    # Frequency Axis
    __freq = np.linspace(0, 1.0 / __dt, __N)
    '''
    [ 0.          0.96774194  1.93548387  2.90322581  3.87096774  4.83870968
    5.80645161  6.77419355  7.74193548  8.70967742  9.67741935 10.64516129
    11.61290323 12.58064516 13.5483871  14.51612903 15.48387097 16.4516129
    17.41935484 18.38709677 19.35483871 20.32258065 21.29032258 22.25806452
    23.22580645 24.19354839 25.16129032 26.12903226 27.09677419 28.06451613
    29.03225806 30.        ]
    '''

    # Frequency Infimum (__freq[2] = 1.93[Hz])
    __freq_infimum = 2

    # Number of markers on one pole
    NUM_MARKER = 2

    # Flag Default(False) or BackgroundSubtractorCNT(True)
    __flag_backgroundSubtractor = True

    # Output BackgroundSubtractorCNT Video
    __flag_video = False

    __PRE_MARKER_FREQ = 0

    def __init__(self) :
        self.frame_divider = FrameDivision()
        self.fgbg = cv2.bgsegm.createBackgroundSubtractorCNT(minPixelStability=0, maxPixelStability = 30 * 1)
        if not os.path.exists(self.__OUTPUT_DIR) :
            os.makedirs(self.__OUTPUT_DIR)

    def __getFrames(self) :
        self.frames = self.frame_divider.Frame_Division(self.VIDEO_NAME)

    def __frames2gray_img(self) :
        self.img = np.array([cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) for frame in self.frames])
        self.img_size = self.img.shape[1:]
        self.output = np.zeros((self.img.shape[1], self.img.shape[2]), dtype=np.uint8)
        self.result = np.empty(shape=(0, self.img.shape[1], self.img.shape[2]), dtype=np.uint8)

    def __backgroundSubtractorCNT(self):
        self.fgmask = np.array([self.fgbg.apply(_) for _ in self.img])
        if self.__flag_video :
            self.__output_backgroundSubtractorVideo()
        self.valid_area = (np.sum(self.fgmask, axis=0) * 255) / self.fgmask.max()
        self.valid_area = self.valid_area.astype(bool)
        self.masked_img = self.img[:, self.valid_area == True]

    def __output_backgroundSubtractorVideo(self) :
        # Set Video Writer
        fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
        video  = cv2.VideoWriter('video.mp4', fourcc, 30.0, tuple(np.roll(self.img_size, 1)), 0)

        for i in range(self.__N):
            video.write(self.fgmask[i])

        video.release()

    def __window_func(self) :
        # Default
        if not self.__flag_backgroundSubtractor :
            self.img = self.img.transpose(1, 2, 0)
            self.img = self.img * np.hanning(self.__N)
            self.img = self.img.transpose(2, 0, 1)

        # BackgroundSubtractorCNT
        else :
            self.masked_img = self.masked_img.T * self.__win

        self.acf = 1/(self.__win.sum()/self.__N)

    def __fft(self) :
        # Default
        if not self.__flag_backgroundSubtractor :
             self.fft_signal = np.fft.fft(self.img, axis=0)

        # BackgroundSubtractorCNT
        else :
            self.masked_img = self.masked_img.transpose(1, 0)
            self.fft_signal = np.fft.fft(self.masked_img, axis=0)

    def __normalize(self) :
        self.fft_signal_amp = self.acf * np.abs(self.fft_signal)
        self.fft_signal_amp = self.fft_signal_amp / (self.__N / 2)

        # Default
        if not self.__flag_backgroundSubtractor :
            self.fft_signal_amp[0, :, :] /= 2

        # BackgroundSubtractorCNT
        else :
            self.fft_signal_amp[0, :] /= 2

    def __bpf(self, MARKER_FREQ) :
        # Default
        if not self.__flag_backgroundSubtractor :
            self.fft_signal_amp_argmax = np.argmax(self.fft_signal_amp[self.__freq_infimum:int(self.__N/2), :, :], axis=0)
            self.fft_signal_amp_max = np.max(self.fft_signal_amp[self.__freq_infimum:int(self.__N/2)], axis=0)

        # BackgroundSubtractorCNT
        else :
            self.fft_signal_amp_argmax = np.argmax(self.fft_signal_amp[self.__freq_infimum:int(self.__N/2), :], axis=0)
            self.fft_signal_amp_max = np.max(self.fft_signal_amp[self.__freq_infimum:int(self.__N/2)], axis=0)

        self.fft_signal_amp_max_filtered = self.fft_signal_amp_max[self.__freq_infimum + self.fft_signal_amp_argmax == (self.MARKER_FREQ + MARKER_FREQ)]

    def __binarization(self, MARKER_FREQ) :
        self.fft_signal_amp_max_filtered[self.fft_signal_amp_max_filtered.max() > self.fft_signal_amp_max_filtered] = 0
        self.fft_signal_amp_max_filtered[self.fft_signal_amp_max_filtered.max() <= self.fft_signal_amp_max_filtered] = 255

        if not self.__flag_backgroundSubtractor :
            self.output[self.__freq_infimum + self.fft_signal_amp_argmax == (self.MARKER_FREQ + MARKER_FREQ)] = self.fft_signal_amp_max_filtered

        else :
            self.fft_signal_amp_max[self.__freq_infimum + self.fft_signal_amp_argmax == (self.MARKER_FREQ + MARKER_FREQ)] = self.fft_signal_amp_max_filtered
            self.fft_signal_amp_max[self.__freq_infimum + self.fft_signal_amp_argmax != (self.MARKER_FREQ + MARKER_FREQ)] = 0
            self.output[self.valid_area == True] = self.fft_signal_amp_max

        self.result = np.vstack((self.result, self.output.reshape(1, self.img.shape[1], self.img.shape[2])))

    def __output_result(self, MARKER_FREQ) :
        cv2.imwrite(os.path.join(self.__OUTPUT_DIR, self.VIDEO_NAME + '-' + str(self.MARKER_FREQ + MARKER_FREQ) + self.__IMG_EXT), self.output)

    def __each_detect_marker_pole(self) :
        if not self.HEIGHT_CORRECTION : self.NUM_MARKER = 1
        else : self.NUM_MARKER = 2
        for _ in range(self.NUM_MARKER) :
            # numpy.fft.fftfreq版に書き換えたら以下のif分を削除
            #if self.MARKER_FREQ == 7 and _ == 1 : _ += 1
            self.__bpf(_)
            self.__binarization(_)
            self.__output_result(_)

    def __detect_marker_pole(self) :
        for freq in self.CURRENT_MARKER_FREQ :
            self.MARKER_FREQ = int(freq)
            self.__each_detect_marker_pole()

    def __detect_marker_pole_with_premarker(self) :
        self.MARKER_FREQ = int(self.__PRE_MARKER_FREQ[0])
        self.__each_detect_marker_pole()

        if self.PRE_VIRTUAL_MARKER :
            self.MARKER_FREQ = int(self.__PRE_MARKER_FREQ[1])
            self.__each_detect_marker_pole()

        self.MARKER_FREQ = int(self.CURRENT_MARKER_FREQ[0])
        self.__each_detect_marker_pole()

        if self.VIRTUAL_MARKER_FLAG :
            self.MARKER_FREQ = int(self.CURRENT_MARKER_FREQ[1])
            self.__each_detect_marker_pole()


    def central_recognition(self, VIDEO_NAME : str, MARKER_FREQ : int, SEE_PRE_MARKER : bool, HEIGHT_CORRECTION : bool, VIRTUAL_MARKER_FLAG : bool) :
        self.VIDEO_NAME = VIDEO_NAME
        self.CURRENT_MARKER_FREQ = MARKER_FREQ
        self.HEIGHT_CORRECTION = HEIGHT_CORRECTION
        self.VIRTUAL_MARKER_FLAG = VIRTUAL_MARKER_FLAG
        self.__getFrames()
        self.__frames2gray_img()
        if self.__flag_backgroundSubtractor :
            self.__backgroundSubtractorCNT()
        self.__window_func()
        self.__fft()
        self.__normalize()

        if not SEE_PRE_MARKER :
            self.__detect_marker_pole()
        else :
            self.__detect_marker_pole_with_premarker()
        self.__PRE_MARKER_FREQ = MARKER_FREQ
        self.PRE_VIRTUAL_MARKER = VIRTUAL_MARKER_FLAG
        return self.result

    def __del__(self):
        del self.frame_divider

if __name__=="__main__":
    start_time = time.time()
    centralRecognizer = CentralRecognition()
    VIDEO_NAME = input('Enter The Video file name (The Video Exists In The Video Folder.)')
    centralRecognizer.central_recognition(VIDEO_NAME, 'Green')
    print(time.time() - start_time)