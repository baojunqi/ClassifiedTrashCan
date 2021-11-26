'''
Author       : AyanamaiYui
Date         : 2021-11-13 08:18:20
LastEditTime : 2021-11-22 07:24:33
Version      : 
Description  : 
'''

from IOTFinalProject.src.module.hardware import Servo
import time

# 45中间

# 1 Kicthen 90kai 178guan

servo0 = Servo(1)
# servo1 = Servo(5)

# servo0.position = 90
# servo1.position = 90

# servo0.run()
# servo1.run()


# servo1.position = 30
servo0.position = 180
servo0.run()
# time.sleep(2)
# del servo0
# servo1.run()