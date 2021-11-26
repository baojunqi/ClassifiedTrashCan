'''
Author       : AyanamaiYui
Date         : 2021-10-28 08:34:39
LastEditTime : 2021-10-28 08:46:20
Version      : 
Description  : 
'''
import time
import VL53L0X

tof = VL53L0X.VL53L0X(i2c_address=0x29)
tof.open()

tof.start_ranging()

timing = tof.get_timing()

if timing < 20000:
    timing = 20000

for count in range(1, 101):
    distance = tof.get_distance()
    if distance>0:
        print("%d mm" % distance)
    time.sleep(0.5)

tof.stop_ranging()
tof.close()