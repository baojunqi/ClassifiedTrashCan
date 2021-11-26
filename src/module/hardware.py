'''
Author       : AyanamaiYui
Date         : 2021-09-24 01:21:43
LastEditTime : 2021-11-22 07:44:49
Version      : 
Description  : Hardware Module 
'''


import random
from tkinter import font
from VL53L0X import VL53L0X
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

import amqp_send
import threading
import time
import Adafruit_PCA9685
import dht11
import RPi.GPIO as GPIO
import mq
import sys

class Servo():
    '''
    author       : AyanamaiYui
    param         {*}
    return        {*}
    description  : 
    '''
    
    def __init__(self, chann):
        #默认地址0x40
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)
        self.position = 0
        self.channel = chann

    #2^12精度  角度转换成数值  
    #position输入的角度值(0--180)  
    #pulsewidth高电平占空时间(0.5ms--2.5ms)   
    #/1000将us转换为ms  #20ms时基脉冲(50HZ)  
    #pulse_width=((angle*11)+500)/1000;  
    #将角度转化为500(0.5)<-->2480(2.5)的脉宽值(高电平时间)   postion=180时  pulse_width=2480us(2.5ms)  
    #date/4096=pulse_width/20 ->有上pulse_width的计算结果得date=4096*( ((angle*11)+500)/1000 )/20   -->int date=4096((postion*11)+500)/20000;  
    def set_servo_angle(self):
        angle = int(4096*((self.position * 11) + 500) / 20000)          #输入角度转换成12^精度的数值
        self.pwm.set_pwm(self.channel, 0, angle)                    #进行四舍五入运算 date=int(4096*((angle*11)+500)/(20000)+0.5

    def run(self):
        try:
            #0-180°固定位置旋转
            self.set_servo_angle()
        except KeyboardInterrupt:
            self.pwm.software_reset()
            sys.exit()

class EnvironmentSensor(threading.Thread):
    '''
    author       : AyanamaiYui
    param         {*}
    return        {*}
    description  : 
    '''
    def __init__(self, pin, sender):
        super().__init__()
        # self.sender = amqp_send.AMQPSender()
        self.PIN = pin
        self.sender = sender
        self.temp = 0
        self.hum = 0

        self.mq_sensor = mq.MQ()
        self.co = ""
        self.gas_lgp = ""
        self.smoke = ""

        
    def run(self):
        super().run()
        while True:   
            dht11_data = dht11.DHT11(pin=self.PIN)
            result = dht11_data.read()
            if result.is_valid():
                self.temp = result.temperature
                self.hum = result.humidity
            
            perc = self.mq_sensor.MQPercentage()
            self.gas_lgp = perc["GAS_LPG"]
            self.co = perc["CO"]
            self.smoke = perc["SMOKE"]

            if self.gas_lgp < 10 and self.co < 10 and self.smoke < 10:
                self.aqi = 1
            
            elif self.gas_lgp < 50 and self.co < 50 and self.smoke < 50:
                self.aqi = 2

            else:
                self.aqi = 3

            if TEMP != 0 and HUM != 0:
                data = {
                    "temperature": temp,
                    "Humidity": hum,
                    "AQI": self.aqi,
                }
                time.sleep(10)
                self.sender.send_property(prop_data=data)
            else:
                data = {
                    "temperature": 15,
                    "Humidity": 60,
                    "AQI": self.aqi,
                }
                time.sleep(10)
                self.sender.send_property(prop_data=data)
            

#线程
class OLED(threading.Thread):
    '''
    author       : AyanamaiYui
    param         {*}
    return        {*}
    description  : 
    '''
    def __init__(self, i2c_addr):
        super().__init__()
        serial = i2c(port=1, address=i2c_addr)
        self.device = sh1106(serial)

        self.temp = ""
        self.hum = ""
        self.volume_kitchen = ""
        self.volume_others = ""
        self.volume_recyclable = ""
        self.volume_harmful = ""
        self.co = ""
        self.lpg = ""
        self.smoke = ""

    def run(self):
        super().run()
        # while self.__running.isSet():
        while True:
            with canvas(self.device) as draw:
                draw.rectangle(self.device.bounding_box, outline="white", fill="black")
                draw.text((0, 0), "Hum:" + self.hum, fill="white")
                draw.text((0, 10), "Tem:" + self.temp, fill="white")
                draw.text((50, 0), "CO:" + self.co, fill="white", align="right")
                draw.text((50, 10), "LPG:" + self.lpg, fill="white", align="right")
                draw.text((70, 20), "SMOKE:" + self.smoke, fill="white", align="right")
                draw.text((0, 40), "Kic V:" + self.volume_kitchen, fill="white")
                draw.text((0, 50), "Rec V:" + self.volume_recyclable, fill="white")
                draw.text((70, 40), "Har V:" + self.volume_harmful, fill="white")
                draw.text((70, 50), "Oth V:" + self.volume_others, fill="white")



class MotionSensor(threading.Thread):
    '''
    author       : AyanamaiYui
    param         {
        pin_out: HC SR501 Dout Pin
        }
    return        {*}
    description  : 
    '''
    def __init__(self, pin_out):
        super().__init__()
        self.OUT = pin_out
        self.is_human = False
        GPIO.setup(self.OUT, GPIO.IN)

        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        while self.__running.isSet():
            if GPIO.input(self.OUT) == 1:
                self.is_human = True
                self.__flag.wait()
            else:
                self.is_human = False

    def pause(self):
        self.__flag.clear()
        self.is_human = False

    def resume(self):
        self.__flag.set()
        self.is_human = False

    def stop(self):
        self.__flag.set()
        self.is_human = False
        self.__running.clear()



class TOFSensor():
    '''
    author       : AyanamaiYui
    param         {
        hc138_output: RPi output to hc138 to control 138 chip select.
        tof_vcc: mutli TOF VCC pin, controlled by 74hc138
        hc138_input:  Tuple. 74hc138 pin input to RPi. should be GPIO.LOW to contorl the TOF start.
        }
    return        {*}
    description  : 
    '''
    def __init__(self, hc138_output, tof_vcc, hc138_input) -> None:
        
        self.distance = 0
        self.A0 = 37
        self.A1 = 35
        self.A2 = 33
        self.A0_STATUS = hc138_input[0]
        self.A1_STATUS = hc138_input[1]
        self.A2_STATUS = hc138_input[2]
        self.HC138_OUTPUT = hc138_output
        self.TOF_VCC = tof_vcc

        GPIO.setup(self.HC138_OUTPUT, GPIO.IN)
        GPIO.setup(self.TOF_VCC, GPIO.OUT)
        GPIO.setup(self.A0, GPIO.OUT)
        GPIO.setup(self.A1, GPIO.OUT)
        GPIO.setup(self.A2, GPIO.OUT)

    def start(self):
        GPIO.output(self.A2, self.A2_STATUS)
        GPIO.output(self.A1, self.A2_STATUS)
        GPIO.output(self.A0, self.A2_STATUS)

        if GPIO.input(self.HC138_OUTPUT) == GPIO.LOW:
            GPIO.output(self.TOF_VCC, GPIO.HIGH)
            time.sleep(1)
            tof = VL53L0X(i2c_address = 0x29)
            tof.open()
            time.sleep(0.5)
            tof.start_ranging()
            self.distance = tof.get_distance()
            time.sleep(0.5)
            tof.stop_ranging()
            tof.close()

        return self.distance
            
            
    def __del__(self):
        GPIO.output(self.TOF_VCC, GPIO.LOW)