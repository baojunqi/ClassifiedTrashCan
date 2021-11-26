'''
Author       : AyanamaiYui
Date         : 2021-10-27 04:16:04
LastEditTime : 2021-11-05 16:44:02
Version      : 
Description  : 
'''
import threading
import time
from RPi import GPIO
import VL53L0X

class TOFSensor():
    # def __init__(self, A2_status, A1_status, A0_status):
    def __init__(self, gpio_status) -> None:
        
        print(gpio_status)
        self.distance = 0
        self.E3 = 31
        self.A0 = 37
        self.A1 = 35
        self.A2 = 33
        self.A0_STATUS = gpio_status[0]
        self.A1_STATUS = gpio_status[1]
        self.A2_STATUS = gpio_status[2]

        GPIO.setup(self.A0, GPIO.OUT)
        GPIO.setup(self.A1, GPIO.OUT)
        GPIO.setup(self.A2, GPIO.OUT)
        GPIO.setup(self.E3, GPIO.OUT)


        GPIO.output(self.E3, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(self.A2, self.A2_STATUS)
        GPIO.output(self.A1, self.A1_STATUS)
        GPIO.output(self.A0, self.A0_STATUS)


    def tof_start_ranging(self):
        tof = VL53L0X.VL53L0X(i2c_address=0x29)
        time.sleep(1)
        tof.open()
        tof.start_ranging()
        self.distance = tof.get_distance()
        time.sleep(0.5)
        tof.stop_ranging()
        tof.close()
        print(self.distance)

    def __del__(self):
        GPIO.output(self.E3, GPIO.LOW)

        


if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    TOF_1 = (GPIO.LOW, GPIO.LOW, GPIO.LOW)

    tof1 = TOFSensor(TOF_1)
    tof1.tof_start_ranging()
    # del tof1
    # time.sleep(3)
    # tof2 = TOFSensor(GPIO.LOW, GPIO.LOW, GPIO.HIGH)
    # tof2.tof_start_ranging()
    # del tof2
    # GPIO.cleanup()