#!/usr/bin/env python3
# coding: utf-8
import sys
import time
import VL53L0X
import pigpio


class DistanceSensor:
    # GPIO for shutdown pin of sensors
    __left_sensor_pin = 4
    __right_sensor_pin = 17

    # Output elias
    __HIGH = 1
    __LOW = 0

    # Distance limit
    __distance_limit = 50

    def __init__(self, gpio: pigpio.pi) -> None:
        self.__gpio = gpio

        # Setup GPIO for shutdown pins on each VL53L0X
        self.__gpio.set_mode(self.__left_sensor_pin, pigpio.OUTPUT)
        self.__gpio.set_mode(self.__right_sensor_pin, pigpio.OUTPUT)

        # Set all shutdown pins low to turn off each VL53L0X
        self.__gpio.write(self.__left_sensor_pin, self.__LOW)
        self.__gpio.write(self.__right_sensor_pin, self.__LOW)
        
        # Keep all low for 500 ms or so to make sure they reset
        time.sleep(0.5)

        # Create one object per VL53L0X passing the address to give to each
        self.__left_sensor = VL53L0X.VL53L0X(address=0x2B)
        self.__right_sensor = VL53L0X.VL53L0X(address=0x2D)

        # Set shutdown pin high for the left VL53L0X then call to start ranging
        self.__gpio.write(self.__left_sensor_pin, self.__HIGH)
        time.sleep(0.5)
        self.__left_sensor.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

        # Set shutdown pin high for the left VL53L0X then call to start ranging
        self.__gpio.write(self.__right_sensor_pin, self.__HIGH)
        time.sleep(0.5)
        self.__right_sensor.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

        # Get timing
        self.timing = self.__left_sensor.get_timing()
        if self.timing < 20000:
            self.timing = 20000

    def get_distance(self):
        left_distance = self.__left_sensor.get_distance()
        right_distance = self.__right_sensor.get_distance()

        if left_distance > 0:
            # print('left sensor - {} mm, {} cm'.format(left_distance, left_distance / 10))
            pass
        else:
            # print('left sensor - Error')
            left_distance = -1

        if right_distance > 0:
            # print('right sensor - {} mm, {} cm'.format(right_distance, right_distance / 10))
            pass
        else:
            # print('right sensor - Error')
            right_distance = -1

        time.sleep(self.timing / 1000000.0)

        return left_distance, right_distance

    def obstacle_monitoring(self):
        left, right = self.get_distance()
        # When one side throws error 
        if left == -1:
            if right < self.__distance_limit:
                print("Right: {} mm".format(right))
                raise FindObstacle
            else:
                return
        elif right == -1:
            if left < self.__distance_limit:
                print("Left: {} mm".format(left))
                raise FindObstacle
            else:
                return

        # When both sensor does not throw error
        if left < self.__distance_limit or right < self.__distance_limit:
            print("Right: {} mm, Left: {} mm".format(right, left))
            raise FindObstacle

        return


class FindObstacle(Exception):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return 'Find Obstacle!'


if __name__ == '__main__':
    gpio = pigpio.pi()
    distance_sensor = DistanceSensor(gpio)
    while True:
        try:
            distance_sensor.obstacle_monitoring()
        except FindObstacle as e:
            print(e)
            continue
        except KeyboardInterrupt:
            sys.exit()
        finally:
            time.sleep(1.0)
