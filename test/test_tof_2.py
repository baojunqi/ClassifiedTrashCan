'''
Author       : AyanamaiYui
Date         : 2021-10-29 06:14:21
LastEditTime : 2021-10-31 07:13:23
Version      : 
Description  : 
'''

import VL53L0X
import RPi.GPIO as GPIO
import time

A0 = 37
A1 = 35
A2 = 33

Y0 = 31 #LOW/LOW/LOW
Y1 = 29 #LOW/LOW/HIGH
Y2 = 15 #LOW/HIGH/LOW
Y3 = 13 #LOW/HIGH/HIGH

TOF0_VCC = 38 #LOW/LOW/LOW
TOF1_VCC = 36 #LOW/LOW/HIGH
TOF2_VCC = 32 #LOW/HIGH/LOW
TOF3_VCC = 11 #LOW/HIGH/HIGH

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

GPIO.setup(Y0, GPIO.IN)
GPIO.setup(Y1, GPIO.IN)
GPIO.setup(Y2, GPIO.IN)
GPIO.setup(Y3, GPIO.IN)

GPIO.setup(TOF0_VCC, GPIO.OUT)
GPIO.setup(TOF1_VCC, GPIO.OUT)
GPIO.setup(TOF2_VCC, GPIO.OUT)
GPIO.setup(TOF3_VCC, GPIO.OUT)

GPIO.setup(A0, GPIO.OUT)
GPIO.setup(A1, GPIO.OUT)
GPIO.setup(A2, GPIO.OUT)


# ENABLE Y0 and TOF0
GPIO.output(A2, GPIO.LOW)
GPIO.output(A1, GPIO.LOW)
GPIO.output(A0, GPIO.LOW)

if GPIO.input(Y0) == GPIO.LOW:
    GPIO.output(TOF0_VCC, GPIO.HIGH)
    time.sleep(1)
    tof = VL53L0X.VL53L0X(i2c_address=0x29)
    tof.open()
    time.sleep(0.5)
    tof.start_ranging()
    distance = tof.get_distance()
    time.sleep(0.5)
    tof.stop_ranging()
    tof.close()
    print("This is TOF0!!")
    print(distance)
    GPIO.output(TOF0_VCC, GPIO.LOW)
    del tof

GPIO.output(A2, GPIO.LOW)
GPIO.output(A1, GPIO.LOW)
GPIO.output(A0, GPIO.HIGH)

if GPIO.input(Y1) == GPIO.LOW:
    GPIO.output(TOF1_VCC, GPIO.HIGH)
    time.sleep(1)
    tof = VL53L0X.VL53L0X(i2c_address=0x29)
    tof.open()
    time.sleep(0.5)
    tof.start_ranging()
    distance = tof.get_distance()
    time.sleep(0.5)
    tof.stop_ranging()
    tof.close()
    print("This is TOF1!!")
    print(distance)
    GPIO.output(TOF1_VCC, GPIO.LOW)
    del tof