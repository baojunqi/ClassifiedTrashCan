'''
Author       : AyanamaiYui
Date         : 2021-10-25 09:29:40
LastEditTime : 2021-11-05 21:43:44
Version      : 
Description  : 
'''

import mq
import sys
import time
import threading

class MQSensor(threading.Thread):
    def __init__(self):
        super().__init__()
        self.mq_sensor = mq.MQ()

        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        super().run()
        while self.__running.isSet():
            perc = self.mq_sensor.MQPercentage()
            self.gas_lgp = perc["GAS_LPG"]
            self.co = perc["CO"]
            self.smoke = perc["SMOKE"]
            print(self.gas_lgp)
            time.sleep(0.1)
        
        self.__flag.wait()
            
    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def stop(self):
        self.__flag.set()
        self.__running.clear()


if __name__ == "__main__":
    mq_sensor = MQSensor()
    mq_sensor.start()
