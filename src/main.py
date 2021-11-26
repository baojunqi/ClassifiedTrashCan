'''
Author       : AyanamaiYui
Date         : 2021-09-24 01:21:32
LastEditTime : 2021-11-22 07:43:18
Version      : 
Description  : 
'''

import time
import cv2
import RPi.GPIO as GPIO
import module.hardware as hardware
import module.NNmodel.predict_result as predict
import module.amqp_send as amqp
import json
from linkkit import linkkit
import random

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

PIN_DHT11 = 12

PIN_HC_SR501 = 40

PIN_HC138_Y0 = 31
PIN_HC138_Y1 = 29
PIN_HC138_Y2 = 15
PIN_HC138_Y3 = 13

TOF_KITCHEN_VCC = 38 #LOW/LOW/LOW
TOF_RECYCLABLE_VCC = 36 #LOW/LOW/HIGH
TOF_OTHERS_VCC = 32 #LOW/HIGH/LOW
TOF_HARMFUL_VCC = 11 #LOW/HIGH/HIGH
TOF_KITCHEN_STATUS = (GPIO.LOW, GPIO.LOW, GPIO.LOW)
TOF_RECYCLABLE_STATUS = (GPIO.LOW, GPIO.LOW, GPIO.HIGH)
TOF_OTHERS_STATUS = (GPIO.LOW, GPIO.HIGH, GPIO.LOW)
TOF_HARMFUL_STATUS = (GPIO.LOW, GPIO.HIGH, GPIO.HIGH)

VOLUME_KICTHEN = random.randint(10, 100)
VOLUME_RECYCLABLE = random.randint(10, 100)
VOLUME_HARMFUL = random.randint(10, 100)
VOLUME_OTHERS = random.randint(10, 100)

TEMP = random.randint(100, 200) / 10
HUM = random.randint(500, 1000) / 10

DUSTBINS_HIGH = 15

if __name__ == "__main__":

    sender = amqp.AMQPSender()
    
    tof_kitchen = hardware.TOFSensor(hc138_output = PIN_HC138_Y0, 
                              tof_vcc = TOF_KITCHEN_VCC, 
                              hc138_input = TOF_KITCHEN_STATUS)

    tof_recyclable = hardware.TOFSensor(hc138_output = PIN_HC138_Y1, 
                              tof_vcc = TOF_RECYCLABLE_VCC, 
                              hc138_input = TOF_RECYCLABLE_STATUS)

    tof_others = hardware.TOFSensor(hc138_output = PIN_HC138_Y2, 
                              tof_vcc = TOF_OTHERS_VCC, 
                              hc138_input = TOF_OTHERS_STATUS)

    tof_harmful = hardware.TOFSensor(hc138_output = PIN_HC138_Y3, 
                              tof_vcc = TOF_HARMFUL_VCC, 
                              hc138_input = TOF_HARMFUL_STATUS)

    servo_kitchen = hardware.Servo(chann=0)
    servo_recyclable = hardware.Servo(chann=1)
    servo_others = hardware.Servo(chann=2)
    servo_harmful = hardware.Servo(chann=3)

    servo_push_horizontal = hardware.Servo(chann = 4)
    servo_push_vertical = hardware.Servo(chann = 5)

    
    servo_push_vertical.position = 180
    servo_push_horizontal.position = 90

    servo_kitchen.position = 180
    servo_harmful.position = 180
    servo_others.position = 180
    servo_recyclable.position = 180

    servo_push_vertical.run()
    servo_push_horizontal.run()

    servo_harmful.run()
    servo_kitchen.run()
    servo_others.run()
    servo_recyclable.run()

    motion_sensor = hardware.MotionSensor(pin_out=PIN_HC_SR501)
    oled_sensor = hardware.OLED(i2c_addr=0x3c)
    environment_sensor = hardware.EnvironmentSensor(pin=PIN_DHT11, sender=sender)

    environment_sensor.start()
    motion_sensor.start()
    oled_sensor.start()
    
    while True:
        oled_sensor.co = str(environment_sensor.co)
        oled_sensor.smoke = str(environment_sensor.smoke)
        oled_sensor.lpg = str(environment_sensor.gas_lgp)
        oled_sensor.temp = str(environment_sensor.temp)
        oled_sensor.hum = str(environment_sensor.hum)
        oled_sensor.volume_harmful = str(VOLUME_HARMFUL) + "%"
        oled_sensor.volume_kitchen = str(VOLUME_KICTHEN) + "%"
        oled_sensor.volume_others = str(VOLUME_OTHERS) + "%"
        oled_sensor.volume_recyclable = str(VOLUME_RECYCLABLE) + "%"


        # 检测是否有人
        if motion_sensor.is_human:
        # if True:
            motion_sensor.pause()
            print("someone coming!")
            time.sleep(5)
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            img_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())                
            img_name = '/home/pi/workspace/IOTFinalProject/image/original/' + img_time + '.jpg'
            cv2.imwrite(img_name, frame)
            cap.release()
            results = predict.detect(img_name)
            
            print(results)

            # 厨余垃圾
            if results == "kitchen":

                if VOLUME_KICTHEN < 10:
                    continue
                else:
                    servo_kitchen.position = 60
                    servo_kitchen.run()

                    time.sleep(3)

                    servo_push_horizontal.position = 110
                    servo_push_horizontal.run()
                    time.sleep(2)
                    servo_push_vertical.position = 150
                    servo_push_vertical.run()
                    
                    time.sleep(2)
                    servo_push_vertical.position = 180
                    servo_push_horizontal.position = 90
                    servo_push_vertical.run()
                    time.sleep(1) 
                    servo_push_horizontal.run()
                    time.sleep(2)
                    servo_kitchen.position = 180
                    servo_kitchen.run()


                    distance_mm = tof_kitchen.start()

                    distance_cm = distance_mm / 10
                    print(distance_cm)

                    remain_volume = distance_cm / DUSTBINS_HIGH * 100
                    remain_volume = round(remain_volume, 2)
                    VOLUME_KICTHEN = remain_volume
                    prop_data = {
                        "remain_volume_kitchen": int(remain_volume),
                    }
                    # time.sleep()
                    sender.send_property(prop_data=prop_data)
                    print("upload!")
                    time.sleep(5)

                    print(remain_volume)

            elif results == "others":
                if VOLUME_OTHERS < 10:
                    break
                else:

                    # 开盖
                    servo_others.position = 60
                    servo_others.run()

                    time.sleep(3)

                    # 水平位移
                    servo_push_horizontal.position = 180
                    servo_push_horizontal.run()
                    time.sleep(2)

                    # 垂直位移，倒垃圾
                    servo_push_vertical.position = 150
                    servo_push_vertical.run()
                    
                    time.sleep(2)
                    # 复位
                    servo_push_vertical.position = 180
                    servo_push_horizontal.position = 90
                    servo_push_horizontal.run()
                    time.sleep(1)
                    servo_push_vertical.run()
                    time.sleep(2)
                    # 关盖
                    servo_others.position = 180
                    servo_others.run()


                    distance_mm = tof_others.start()

                    distance_cm = distance_mm / 10
                    print(distance_cm)

                    remain_volume = distance_cm / DUSTBINS_HIGH * 100
                    remain_volume = round(remain_volume, 2)
                    VOLUME_OTHERS = remain_volume
                    prop_data = {
                        "remain_volume_others": int(remain_volume),
                    }
                    # time.sleep()
                    sender.send_property(prop_data=prop_data)
                    print("upload!")
                    time.sleep(5)

                    print(remain_volume)

            elif results == "recyclable":
                if VOLUME_OTHERS < 10:
                    break
                else:

                    # 开盖
                    servo_recyclable.position = 60
                    servo_recyclable.run()

                    time.sleep(3)

                    # 水平位移
                    servo_push_horizontal.position = 70
                    servo_push_horizontal.run()
                    time.sleep(2)

                    # 垂直位移，倒垃圾
                    servo_push_vertical.position = 150
                    servo_push_vertical.run()
                    
                    time.sleep(2)
                    # 复位
                    servo_push_vertical.position = 180
                    servo_push_horizontal.position = 90

                    servo_push_vertical.run()
                    time.sleep(1)
                    servo_push_horizontal.run()
                    
                    
                    time.sleep(2)
                    # 关盖
                    servo_recyclable.position = 180
                    servo_recyclable.run()


                    distance_mm = tof_recyclable.start()

                    distance_cm = distance_mm / 10
                    print(distance_cm)

                    remain_volume = distance_cm / DUSTBINS_HIGH * 100
                    remain_volume = round(remain_volume, 2)
                    VOLUME_OTHERS = remain_volume
                    prop_data = {
                        "remain_volume_recyclable": int(remain_volume),
                    }
                    # time.sleep()
                    sender.send_property(prop_data=prop_data)
                    print("upload!")
                    time.sleep(5)

                    print(remain_volume)
            
            elif results == "harmful":
                if VOLUME_HARMFUL < 10:
                    break
                else:

                    # 开盖
                    servo_harmful.position = 60
                    servo_harmful.run()

                    time.sleep(3)

                    # 水平位移
                    servo_push_horizontal.position = 0
                    servo_push_horizontal.run()
                    time.sleep(2)

                    # 垂直位移，倒垃圾
                    servo_push_vertical.position = 150
                    servo_push_vertical.run()
                    
                    time.sleep(2)
                    # 复位
                    servo_push_vertical.position = 180
                    servo_push_horizontal.position = 90
                    servo_push_horizontal.run()
                    time.sleep(1)
                    servo_push_vertical.run()
                    time.sleep(2)
                    # 关盖
                    servo_harmful.position = 180
                    servo_harmful.run()

                    distance_mm = tof_harmful.start()

                    distance_cm = distance_mm / 10
                    print(distance_cm)

                    remain_volume = distance_cm / DUSTBINS_HIGH * 100
                    remain_volume = round(remain_volume, 2)
                    VOLUME_HARMFUL = remain_volume
                    prop_data = {
                        "remain_volume_others": int(remain_volume),
                    }
                    # time.sleep()
                    sender.send_property(prop_data=prop_data)
                    print("upload!")
                    time.sleep(5)

                    print(remain_volume)
            motion_sensor.resume()