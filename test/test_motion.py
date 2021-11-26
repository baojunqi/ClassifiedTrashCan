'''
Author       : AyanamaiYui
Date         : 2021-10-27 08:32:56
LastEditTime : 2021-10-31 07:14:37
Version      : 
Description  : 
'''
import threading
import RPi.GPIO as GPIO
class MotionSensor(threading.Thread):
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

    def stop(self):
        self.__flag.set()
        self.__running.clear()

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    motion = MotionSensor(40)
    motion.start()
