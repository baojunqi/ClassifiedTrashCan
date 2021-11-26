'''
Author       : AyanamaiYui
Date         : 2021-10-28 04:34:41
LastEditTime : 2021-10-28 10:53:25
Version      : 
Description  : 
'''

A0 = 37
A1 = 35
A2 = 33


import RPi.GPIO as GPIO
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(A0, GPIO.OUT)
GPIO.setup(A1, GPIO.OUT)
GPIO.setup(A2, GPIO.OUT)

GPIO.output(A2, GPIO.LOW)
GPIO.output(A1, GPIO.LOW)
GPIO.output(A0, GPIO.LOW)
while True:
    pass
