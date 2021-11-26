'''
Author       : AyanamaiYui
Date         : 2021-10-25 08:37:06
LastEditTime : 2021-10-25 09:07:31
Version      : 
Description  : 
'''
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, SINCLAIR_FONT
import threading

class OLED(threading.Thread):
    # serial = i2c(port=1)
    msg = "helloworld"
    def __init__(self, i2c_addr):
        super().__init__()
        serial = i2c(port=1, address=i2c_addr)
        self.device = sh1106(serial)

        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        super().run()
        while self.__running.isSet():
            with canvas(self.device) as draw:
                draw.rectangle(self.device.bounding_box, outline="white", fill="black")
                draw.text((0, 0), self.msg, fill="white")

        self.__flag.wait()
            
    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def stop(self):
        self.__flag.set()
        self.__running.clear()



if __name__ == '__main__':
    oled = OLED(i2c_addr=0x3c)
    oled.start()
    print("helloworld")
    time.sleep(5)
    oled.msg = "I am AyanamiYui"