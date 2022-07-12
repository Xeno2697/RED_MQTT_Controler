import cv2
import numpy as np
import os
import socket

class Calc():
    # Height from floor to Upper marker[cm]
    __H1 = 280

    # Height from floor to Lower marker[cm]
    __H2 = 200

    # Distance between markers
    __H = __H1 - __H2

    # Number of markers on one pole
    NUM_MARKER = 2

    __MARK_DIR = 'mark/'
    __MARK_EXT = '.png'

    __PRE_MARKER_FREQ = 0

    def __init__(self) :
        self.__get_myIP()
        self.__get_calib_coefficient()
        if not os.path.exists(self.__MARK_DIR) :
            os.makedirs(self.__MARK_DIR)

    def __get_myIP(self) :
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        self.__myIP = s.getsockname()[0]
        self.__myIP = '192.168.1.200'
        s.close()

    def __get_calib_coefficient(self) :
        calib_txt = np.loadtxt('/home/pi/Red2.0-Control-Software/explore_algorithm/calibration.txt', delimiter=',', skiprows=1, dtype='str')
        #calib_txt = np.loadtxt('calibration.txt', delimiter=',', skiprows=1, dtype='str')
        index = np.where(calib_txt == self.__myIP)[0]
        row = calib_txt[index].reshape(10)
        row = np.delete(row, 0).astype(np.float32)
        self.__Cx = row[0]
        self.__Cy = row[1]
        self.__a0 = row[2]
        self.__a2 = row[3]
        self.__a3 = row[4]
        self.__a4 = row[5]
        self.__c = row[6]
        self.__d = row[7]
        self.__e = row[8]
        self.__C = np.array([self.__Cx, self.__Cy])
        self.__A = np.array([[self.__c, self.__d], [self.__e, 1]])

    def __get_center_point(self, result) :
        result = result.reshape(result.shape[:2])
        result = result.astype(bool)
        index = np.array(np.where(result == True))
        marker_center = np.sum(index, axis=1) / index.shape[1]
        marker_center = np.roll(marker_center, 1)
        return marker_center

    def __get_difference_from_the_center_point(self, marker_center) :
        u_prime = np.zeros(shape=(2, 1))
        u_prime = (marker_center - self.__C).reshape(2, 1)
        u_prime_prime = np.matmul(np.linalg.inv(self.__A), u_prime)
        r = np.sqrt(u_prime_prime[0]**2 + u_prime_prime[1]**2)[0]
        return r, u_prime_prime

    def __get_z(self, r) :
        z = \
            self.__a0 + \
            self.__a2 * r ** 2 + \
            self.__a3 * r ** 3 + \
            self.__a4 * r ** 4
        z *= -1
        #incidence_angle = (np.pi / 2) - np.arctan2(z, r)
        #self.incidence_angle = np.append(self.incidence_angle, incidence_angle.reshape(1, 1), axis=0)
        return z

    def __posture_angle_correction(self, u_prime_prime, z, roll, pitch) :
        rot = np.array([[0, 1], [-1, 0]])
        rot_point = np.matmul(rot, u_prime_prime)
        x = rot_point[0]
        y = rot_point[1]
        z = z
        p = np.empty(shape=(3, 1))
        p[0, 0] = x[0]
        p[1, 0] = y[0]
        p[2, 0] = z
        Rx = np.empty(shape=(3, 3))
        Ry = np.empty(shape=(3, 3))
        Rx = np.array([[1, 0, 0], [0, np.cos(roll), -np.sin(roll)], [0, np.sin(roll), np.cos(roll)]])
        Ry = np.array([[np.cos(pitch), 0, np.sin(pitch)], [0, 1, 0], [-np.sin(pitch), 0, np.cos(pitch)]])
        p_prime = np.matmul(np.matmul(Ry, Rx), p)
        return p_prime

    def __get_incidence_angle(self, p) :
        incidence_angle = (np.pi / 2) - np.arctan2(p[2], np.sqrt(p[0]**2 + p[1]**2))
        #print(np.rad2deg(incidence_angle))
        self.incidence_angle = np.append(self.incidence_angle, incidence_angle.reshape(1, 1), axis=0)

    def __get_azimuth_angle(self, p) :
        azimuth_angle = np.arctan2(p[1], p[0])
        self.azimuth_angle = np.append(self.azimuth_angle, azimuth_angle.reshape(1, 1), axis=0)

    def __get_distance(self, p) :
        rad = np.arctan2(p[2], np.sqrt(p[0]**2 + p[1]**2))
        distance = self.__H1 / np.tan(rad)
        self.distance = np.append(self.distance, distance.reshape(1, 1), axis=0)

    def __calc_height_correction_distance(self) :
        theta = np.abs(np.diff(self.incidence_angle, axis=0))
        tmp = (self.__H * np.sin(self.incidence_angle[0])) / np.sin(theta)
        distance = tmp * np.sin(self.incidence_angle[1])
        return distance

    def __calc_height_correction_azimuth_angle(self) :
        azimuth_angle = np.sum(self.azimuth_angle, axis=0) / self.azimuth_angle.shape[0]
        return azimuth_angle

    def draw_marker(self, num, result, marker_center) :
        self.marker_detection_img = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        cv2.circle(self.marker_detection_img, center=(tuple(marker_center.astype(np.int))), radius=50, color=(0, 255, 0), thickness=5, lineType=cv2.LINE_4, shift=0)
        tmp = cv2.imread(os.path.join(self.__MARK_DIR, 'tmp' + self.__MARK_EXT))
        output = cv2.addWeighted(self.marker_detection_img, 0.5, tmp, 0.5, 0)
        cv2.imwrite(os.path.join(self.__MARK_DIR, self.VIDEO_NAME + '-' + str(self.MARKER_FREQ + num) + self.__MARK_EXT), output)

    def __each_get_distance_and_phi(self) :
        if not self.HEIGHT_CORRECTION : self.NUM_MARKER = 1
        else : self.NUM_MARKER = 2
        for _ in range(self.NUM_MARKER) :
            marker_center = self.__get_center_point(self.result[_])
            r, u_prime_prime = self.__get_difference_from_the_center_point(marker_center)
            z = self.__get_z(r)
            p_prime = self.__posture_angle_correction(u_prime_prime, z, np.deg2rad(self.roll), np.deg2rad(self.pitch))
            self.__get_incidence_angle(p_prime)
            self.__get_azimuth_angle(p_prime)
            self.__get_distance(p_prime)
            self.draw_marker(_, self.result[_], marker_center)
        if self.HEIGHT_CORRECTION :
            self.calc_distance = np.append(self.calc_distance, self.__calc_height_correction_distance().reshape(1,1), axis=0)
            self.calc_azimuth_angle = np.append(self.calc_azimuth_angle, self.__calc_height_correction_azimuth_angle().reshape(1,1), axis=0)
        else :
            self.calc_distance = np.append(self.calc_distance, self.distance, axis=0)
            self.calc_azimuth_angle = np.append(self.calc_azimuth_angle, self.azimuth_angle, axis=0)

    def __get_distance_and_phi(self) :
        for freq in self.CURRENT_MARKER_FREQ :
            self.distance = np.empty(shape=(0, 1))
            self.incidence_angle = np.empty(shape=(0, 1))
            self.azimuth_angle = np.empty(shape=(0, 1))
            self.MARKER_FREQ = freq
            self.__each_get_distance_and_phi()
            if self.HEIGHT_CORRECTION : self.result = np.delete(self.result, obj=0, axis=0)
            self.result = np.delete(self.result, obj=0, axis=0)
        if not self.VIRTUAL_MARKER :
            return self.calc_distance, self.calc_azimuth_angle

    def __get_virtual_marker_estValue(self) :
        self.__get_distance_and_phi()
        x0 = self.calc_distance[0] * np.cos(self.calc_azimuth_angle[0])
        y0 = self.calc_distance[0] * np.sin(self.calc_azimuth_angle[0])
        x1 = self.calc_distance[1] * np.cos(self.calc_azimuth_angle[1])
        y1 = self.calc_distance[1] * np.sin(self.calc_azimuth_angle[1])
        xm = (x0 + x1) / 2
        ym = (y0 + y1) / 2
        rm = np.sqrt(xm**2 + ym**2)
        rad = np.arctan2(ym, xm)
        return rm, rad

    def get_distance_and_phi(self, result, VIDEO_NAME, MARKER_FREQ, SEE_PRE_MARKER : bool, HEIGHT_CORRECTION : bool, VIRTUAL_MARKER : bool, GYRO_ANGLES) :
        self.result = result
        self.VIDEO_NAME = VIDEO_NAME
        self.CURRENT_MARKER_FREQ = MARKER_FREQ
        self.HEIGHT_CORRECTION = HEIGHT_CORRECTION
        self.VIRTUAL_MARKER = VIRTUAL_MARKER
        self.SEE_PRE_MARKER = SEE_PRE_MARKER
        self.roll = GYRO_ANGLES[0]
        self.pitch = GYRO_ANGLES[1]

        self.calc_distance = np.empty(shape=(0, 1))
        self.calc_azimuth_angle = np.empty(shape=(0, 1))
        self.result_distance = np.empty(shape=(0, 1))
        self.result_azimuth_angle = np.empty(shape=(0, 1))
        self.debug = False

        if self.SEE_PRE_MARKER :
            #print('~~~~~ SEE_PRE_MARKER ~~~~~')
            for _ in range(2) :
                if _ == 0 :
                    self.CURRENT_MARKER_FREQ = self.__PRE_MARKER_FREQ
                    self.VIRTUAL_MARKER = self.PRE_VIRTUAL_MARKER
                else :
                    self.CURRENT_MARKER_FREQ = MARKER_FREQ
                    self.VIRTUAL_MARKER = VIRTUAL_MARKER
                if self.VIRTUAL_MARKER :
                    #print('START SEE VIRTUAL MARKER')
                    self.debug = True
                    self.calc_distance = np.empty(shape=(0, 1))
                    self.calc_azimuth_angle = np.empty(shape=(0, 1))
                    distance, azimuth_angle = self.__get_virtual_marker_estValue()
                    #print('END SEE VIRTUAL MARKER')

                else :
                    #print('START SEE NORMAL MARKER')
                    self.calc_distance = np.empty(shape=(0, 1))
                    self.calc_azimuth_angle = np.empty(shape=(0, 1))
                    distance, azimuth_angle = self.__get_distance_and_phi()
                    #print('FINISH SEE NORMAL MARKER')

                self.result_distance = np.append(self.result_distance, distance.reshape(1,1), axis=0)
                self.result_azimuth_angle = np.append(self.result_azimuth_angle, azimuth_angle.reshape(1,1), axis=0)


        else :
            #print('~~~~~ NOT SEE_PRE_MARKER ~~~~~')
            if VIRTUAL_MARKER :
                #print('START SEE VIRTUAL MARKER')
                self.calc_distance = np.empty(shape=(0, 1))
                self.calc_azimuth_angle = np.empty(shape=(0, 1))
                distance, azimuth_angle = self.__get_virtual_marker_estValue()
                #print('END SEE VIRTUAL MARKER')

            else :
                #print('START SEE NORMAL MARKER')
                self.calc_distance = np.empty(shape=(0, 1))
                self.calc_azimuth_angle = np.empty(shape=(0, 1))
                distance, azimuth_angle = self.__get_distance_and_phi()
                #print('FINISH SEE NORMAL MARKER')

            self.result_distance = np.append(self.result_distance, distance.reshape(1, 1), axis=0)
            self.result_azimuth_angle = np.append(self.result_azimuth_angle, azimuth_angle.reshape(1, 1), axis=0)

        os.remove(os.path.join(self.__MARK_DIR, 'tmp' + self.__MARK_EXT))

        ##print('self.distance : ' + str(self.distance))
        ##print('self.azimuth_angle : ' + str(np.rad2deg(self.azimuth_angle)))
        ##print('self.incidence_angle : ' + str(self.incidence_angle))
        ##print('self.calc_distance : ' + str(self.calc_distance))
        ##print('self.calc_azimuth_angle : ' + str(np.rad2deg(self.calc_azimuth_angle)))
        #print('self.result_distance : ' + str(self.result_distance))
        #print('self.result_azimuth_angle : ' + str(np.rad2deg(self.result_azimuth_angle)))

        self.__PRE_MARKER_FREQ = MARKER_FREQ
        self.PRE_VIRTUAL_MARKER = self.VIRTUAL_MARKER

        return self.result_distance, self.result_azimuth_angle