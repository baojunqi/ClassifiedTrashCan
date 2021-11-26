'''
Author       : AyanamaiYui
Date         : 2021-11-16 11:04:36
LastEditTime : 2021-11-22 07:37:59
Version      : 
Description  : 
'''

import random
import numpy as np


# print(np.random.ranf)



# # 随机生成三位数，再转换成两位的小数
# temp_int = random.randint(200, 250)
# print("temp is " + str(temp_int / 10))

results_list = ["kitchen", "recyclable"]
results = results_list[random.randint(0, 1)]
print(results)