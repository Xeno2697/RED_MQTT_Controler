import sys
import time
import math
import numpy as np
import threading
import pigpio
import WheelControl
import MotorControl
import DistanceSensor
import imu_ekf as fcn
import mpu6050


class GyroScope:
    def __init__(self, gpio, wheel, left_motor, right_motor):
        self.sensor = mpu6050.mpu6050(0x68)
        self.gpio = gpio
        self.wheel = wheel
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.__distance_sensor = DistanceSensor.DistanceSensor(gpio)
        self.__find_obstacle_twice = False
        self.gyro_data = 0,0,0
        self.accel_data = 0,0,0
        self.angles = [0,0,0]

    def accel(self):
        accel_x, accel_y, accel_z = self.sensor.get_accel_data().values()
        return -accel_y, -accel_x, -accel_z

    def gyro(self):
        gyro_x, gyro_y, gyro_z = self.sensor.get_gyro_data().values()
        return -gyro_y*math.pi/180, -gyro_x*math.pi/180, -gyro_z*math.pi/180

    def gyro_deg(self):
        gyro_x, gyro_y, gyro_z = self.sensor.get_gyro_data().values()
        return -gyro_y, -gyro_x, -gyro_z

    def roll_a(self, y, z):
        return math.atan2(y, z)

    def pitch_a(self, x, y, z):
        return -math.atan2(x, math.copysign(1, z)*math.sqrt(y*y+z*z))

    def roll_g(self, dt, roll, pitch, x, y, z):
        return x*dt+y*dt*math.sin(roll)*math.tan(pitch)+z*dt*math.cos(roll)*math.tan(pitch)

    def pitch_g(self, dt, roll, y, z):
        return y*dt*math.cos(roll)-z*dt*math.sin(roll)

    def offset_accel(self):
        x0=0
        y0=0
        z0=0
        for i in range(1,100):
            x, y, z = self.accel()
            x0 += x
            y0 += y
            z0 += z
        return x0/100, y0/100, z0/100-9.80665

    def offset_gyro(self):
        x0=0
        y0=0
        z0=0
        for i in range(1,100):
            x, y, z = self.gyro()
            x0 += x
            y0 += y
            z0 += z
        return x0/100, y0/100, z0/100

    def accel_true(self,x,y,z):
        accel_x, accel_y, accel_z = self.sensor.get_accel_data().values()
        return -accel_y-x, -accel_x-y, -accel_z-z

    def gyro_true(self,x,y,z):
        gyro_x, gyro_y, gyro_z = self.sensor.get_gyro_data().values()
        return -gyro_y*math.pi/180-x, -gyro_x*math.pi/180-y, -gyro_z*math.pi/180-z

    def gyro_deg_true(self,x,y,z):
        gyro_x, gyro_y, gyro_z = self.sensor.get_gyro_data().values()
        return -gyro_y-x, -gyro_x-y, -gyro_z-z

    def returning(self):#????????????
        while True:
            accel_x, accel_y, accel_z = self.accel()
            #print(accel_z)
            if accel_z < 0:
                self.wheel.forward_pwm(100)
                time.sleep(0.1)
            else:
                accel_x, accel_y, accel_z = self.accel()
                print(accel_z)
                if accel_z < 0:
                    self.wheel.forward_pwm(100)
                    time.sleep(0.1)
                else:
                    break
        self.wheel.stop_gently()
        print("finish!")

    def forward_g(self, duty_L: int, duty_R:int):
        a = 10 #???????????????
        self.left_motor.backward_rotation_pwm(duty_L)
        self.right_motor.forward_rotation_pwm(duty_R)
        time.sleep(0.1)
        self.gyro_x, self.gyro_y, self.gyro_z = self.gyro()
        duty_L += int(a*self.gyro_z)
        duty_R -= int(a*self.gyro_z)
        if duty_L > 80:
            duty_L = 80
        if duty_L < 60:
            duty_L = 60
        if duty_R > 80:
            duty_R = 80
        if duty_R < 60:
            duty_R = 60
        self.left_motor.backward_rotation_pwm(duty_L)
        self.right_motor.forward_rotation_pwm(duty_R)
        return duty_L, duty_R

    def forward_sec(self, seconds: float):
        loop_count = seconds / 0.1
        time_start = time.perf_counter()
        obstacle_flag = 0
        forward_time = 0
        duty_L = 70
        duty_R = 70
        for i in range(int(loop_count / 2)):
            try:
                # ???????????????????????????
                # ???????????????????????????????????????????????????threading???????????????????????????
                self.__distance_sensor.obstacle_monitoring()
                duty_L, duty_R = self.forward_g(duty_L,duty_R)
                print('Duty:{0},{1}'.format(duty_L, duty_R))
            except DistanceSensor.FindObstacle:
                if not self.__find_obstacle_twice:
                    self.__find_obstacle_twice = True
                    continue
                print("Find obstacle!")
                time_end = time.perf_counter()
                forward_time = time_end - time_start
                obstacle_flag = 1
                self.__find_obstacle_twice = False
                
                self.wheel.stop()
                """
                # ?????????????????????????????????
                if random.random() < 0.5:
                    self.pivot_turn_left_deg(90)
                else:
                    self.pivot_turn_right_deg(90)
                    break
                # ????????????
                """
                # ??????????????????
                self.wheel.turn_right_sec(0.5)
                self.wheel.stop()
                self.wheel.turn_left_sec(0.5)
                self.wheel.stop()
                
                time.sleep(0.5)
                break
                # ????????????
                
        
        if obstacle_flag == 0:
            time_end = time.perf_counter()
            self.wheel.stop_gently()
            
            forward_time = time_end - time_start
            
        return obstacle_flag, forward_time

    def ekf(self):

        accel0 = np.zeros((3,))
        gyro0 = np.zeros((3,))

        for i in range(1,100):
            accel = self.accel()
            gyro = self.gyro()
            accel0 = accel0 + np.array(accel)
            gyro0 = gyro0 + np.array(gyro)
        gyro0 = gyro0/100
        accel0 = accel0/100 + ([0,0,-9.80665])

        x0 = np.zeros((2,))

        x = x0
        P = np.zeros((2,2))
        Ts = 1.0/10.0
        Yaw = 0
        Tri = np.zeros((2,3))

        c = np.array([[1,0],[0,1]])
        q = np.array([[1.74E-3*Ts*Ts,0],[0,1.74E-3*Ts*Ts]])
        b = np.array([[1,0],[0,1]])
        r = np.array([[1*Ts*Ts,0],[0,1*Ts*Ts]])
        Cgy = np.eye(3,3)*1.74E-3*Ts*Ts
        while(True):
            t_estimate_Attitude0 = time.perf_counter()
            self.accel_data = self.accel()
            self.gyro_data = self.gyro()

            self.accel_data = np.array(self.accel_data)-accel0
            self.gyro_data = np.array(self.gyro_data)-gyro0

            Tri = fcn.get_Trigonometrxic(x)
            J = fcn.Jacobian_forprocessvariance2(Tri)
            Jt = J.transpose()
            x,P = fcn.Kalman_filer2(x,fcn.get_angle_acc(self.accel_data),self.gyro_data,c,b,q,r,P,Ts,Tri)
            Yaw = Yaw + (Tri[1,1]/Tri[0,0]*self.gyro_data[1]+Tri[1,0]/Tri[0,0]*self.gyro_data[2])*Ts
            self.angles[:] = np.array([(x[0])* 57.296,(x[1])* 57.296],Yaw * 57.296)
            #print("Roll:{0:0.3f},Pitch:{1:0.3f}".format((x[0])* 57.296,(x[1])* 57.296))
            time.sleep(Ts-time.perf_counter()+t_estimate_Attitude0)

    def cf(self):

        dt = 1.0/20
        k = 0.95
        offset_a = self.offset_accel()
        offset_g = self.offset_gyro()

        accel_x, accel_y, accel_z = self.accel_true(*offset_a)
        self.angles[0] = self.roll_a(accel_y, accel_z)
        self.angles[1] = self.pitch_a(accel_x, accel_y, accel_z)
        gyro_x, gyro_y, gyro_z = self.gyro_true(*offset_g)
        while True:
            T = time.perf_counter()
            roll_g = self.roll_g(dt, self.angles[0], self.angles[1], gyro_x, gyro_y, gyro_z)
            pitch_g = self.pitch_g(dt, self.angles[0], gyro_y, gyro_z)
            try:
                accel_x, accel_y, accel_z = self.accel_true(*offset_a)
            except Exception as e:
                print(e)
                continue
            else:
                roll_a = self.roll_a(accel_y, accel_z)
                pitch_a = self.pitch_a(accel_x, accel_y, accel_z)
                self.angles[0] = k*(self.angles[0]+roll_g)+(1-k)*roll_a*57.296
                self.angles[1] = k*(self.angles[1]+pitch_g)+(1-k)*pitch_a*57.296
                #print("Eular Angles (deg)({0:0.3f},{1:0.3f})".format(self.angles[0], self.angles[1]))
                try:
                    gyro_x, gyro_y, gyro_z = self.gyro_true(*offset_g)
                except Exception as e:
                    print(e)
                    continue
                else:
                    dt = time.perf_counter()-T


    def pivot_turn_right_deg_g(self, degree: float) -> None:
        degree_n = 0.0 #offset
        dt = 0.0
        start = time.perf_counter()
        self.wheel.pivot_turn_right()
        while degree_n < degree:
            dt = time.perf_counter()-start
            start = time.perf_counter()
            gyro_x, gyro_y, gyro_z = self.gyro()
            if gyro_z > -4.3:
                gyro_z = -4.3
            degree_n -= (gyro_z)*1.4*dt*57.2958
        self.wheel.stop()

    def pivot_turn_left_deg_g(self, degree: float) -> None:
        degree_n = 0.0
        dt = 0.0
        start = time.perf_counter()
        self.wheel.pivot_turn_left()
        while degree_n < degree:
            dt = time.perf_counter()-start
            start = time.perf_counter()
            gyro_x, gyro_y, gyro_z = self.gyro()
            if gyro_z < 4.3:
                gyro_z = 4.3
            degree_n += (gyro_z)*1.4*dt*57.2958
        self.wheel.stop()

    def thread(self):
        th = threading.Thread(target=self.cf)
        th.setDaemon(True)
        th.start()

    def jugde(self):#????????????
        self.accel_x, self.accel_y, self.accel_z = self.accel()
        if self.accel_z < 0:
            raise Judge

        return

class Judge(Exception):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return 'Inverted'


if __name__ == '__main__':
    gpio = pigpio.pi()
    wheel = WheelControl.Wheel(gpio)
    left_motor = MotorControl.BD6231(gpio, 27, 22)
    right_motor = MotorControl.BD6231(gpio, 19, 26)
    gyroscope = GyroScope(gpio, wheel,left_motor,right_motor)
    gyroscope.pivot_turn_left_deg_g(360)
    time.sleep(1)
    gyroscope.thread()
    time.sleep(3)
    while True:
        accel_x, accel_y, accel_z = gyroscope.accel()
        print("Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})"
            .format(accel_x, accel_y, accel_z))
        gyro_x, gyro_y, gyro_z = gyroscope.gyro()
        print("Gyroscope (rad/sec): ({0:0.3f},{1:0.3f},{2:0.3f})"
            .format(gyro_x, gyro_y, gyro_z))
        print("Eular angles (deg): ({0:0.3f},{1:0.3f})"
            .format(gyroscope.angles[0], gyroscope.angles[1]))
        try:
            gyroscope.jugde()
        except Judge as  e:
            print(e)
            #gyroscope.returning()
            continue
        except KeyboardInterrupt:
            sys.exit()
        finally:
            time.sleep(1.0)
