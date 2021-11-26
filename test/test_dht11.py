'''
Author       : AyanamaiYui
Date         : 2021-10-27 07:43:13
LastEditTime : 2021-11-16 11:03:38
Version      : 
Description  : 
'''
import time
import dht11
import RPi.GPIO as GPIO
import threading

class DHTSensor(threading.Thread):
    def __init__(self, pin):
        super().__init__()
        self.PIN = pin
        GPIO.setup(self.PIN, GPIO.IN)
        self.temp = 0
        self.hum = 0

        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        super().run()
        while self.__running.isSet():
            dht11_data = dht11.DHT11(pin=self.PIN)
            result = dht11_data.read()
            # print(result)
            if result.is_valid():
                self.temp = result.temperature
                self.hum = result.humidity
                time.sleep(2)
                print(self.temp)
                print(self.hum)
            else:
                print(result.error_code)
                print("error")
                #直接上传阿里云事件吧

if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    dht_test = DHTSensor(10)
    dht_test.start()
    while True:
        # print("temp", dht_test.temp)
        # print("hun", dht_test.hum)
        time.sleep(2)
