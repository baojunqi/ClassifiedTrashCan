# 0x00. 阿里云IOT SDK

## 1. 阿里云IOT环境搭建

```bash
pip install aliyun-iot-linkkit #硬件端
# amqp相关
pip install stomp.py
pip install schedule
```

## 2. 阿里云IOT连接测试

```python
```



# 0x01. 硬件环境

## 1. PCA9685

| 元件 | Board引脚 | BCM引脚 | 备注 |
| ---- | --------- | ------- | ---- |
| SDA  | 3         |         |      |
| SCL  | 5         |         |      |

## 2. MCP3008

| 元件 | Board引脚 | BCM引脚 | 备注 |
| ---- | --------- | ------- | ---- |
| VDD  | 3.3v      | 3.3v    |      |
| VREF | 3.3v      | 3.3v    |      |
| AGND | GND       | GND     |      |
| CLK  | 23        | 11      |      |
| DOUT | 21        | 9       |      |
| DIN  | 19        | 10      |      |
| CS   | 24        | 8       |      |
| DGND | GND       | GND     |      |

## 3. MQ135 GAS Sensor

| 元件 | Board引脚       | BCM引脚 | 备注                                                        |
| ---- | --------------- | ------- | ----------------------------------------------------------- |
| VCC  | 5v              |         |                                                             |
| VDD  | GND             |         |                                                             |
| A1   | MCP3008 chann 0 |         | 经过logic level converter降压为3.3v后，输入到MCP3008 chann0 |

## 4. TOF VL53L0X

| 元件           | Board引脚 | BCM引脚 | 备注 |
| -------------- | --------- | ------- | ---- |
| SDA            | 3         |         |      |
| SCL            | 5         |         |      |
| tof1 xshutdown | 13        | 27      |      |
| tof2 xshutdown | 11        | 17      |      |
| tof3 xshutdown | 16        | 23      |      |
| tof4 xshutdown | 18        | 24      |      |

## 5. HCSR-501

| 元件 | Board引脚 | BCM引脚 | 备注 |
| ---- | --------- | ------- | ---- |
| VCC  | 5v        |         |      |
| VDD  | GND       |         |      |
| DOUT | 40        | 21      |      |

## 6. DHT11

| 元件 | Board引脚 | BCM引脚 | 备注 |
| ---- | --------- | ------- | ---- |
| VCC  | 3.3v      |         |      |
| VDD  | GND       |         |      |
| DOUT | 7         | 4       |      |

## 7.HCSR-04
| 元件 | Board引脚 | BCM引脚 | 备注 |
| ---- | --------- | ------- | ---- |
| VCC  | 3.3v      |         |      |
| VDD  | GND       |         |      |
| Echo | 37        | 26      |      |
| Trig | 36        | 16      |      |

## 8. 74HC138
| 元件 | Board引脚 | BCM引脚 | 备注 |
| ---- | --------- | ------- | ---- |
| E1 | GND       |         |      |
| E2 | GND       |         |      |
| E3 | VCC   |       |      |
| A0 | 37       | 26    |      |
| A1 | 35 | 19 | |
| A2 | 33 | 13 | |
|  |           |         | |


# 0x03. Python库支持

## 1. PCA9685

### i. 开启I2C

```bash
sudo rasp-config
# 选择Interface Option
# I2C
i2cdetect -y 1
```

### ii. Adafruit_PCA9685库

```bash
sudo pip install adafruit-pca9685
```

## 2. OLED

```bash
sudo pip3 install luma.oled
```

## 3.DHT11

```bash
sudo pip3 install dht11
```

# 0x04. 语音识别

```bash
cat /proc/asound/cards 
```

![image-20211105104608156](http://imagebed-yui.oss-cn-hangzhou.aliyuncs.com/img/image-20211105104608156.png)

```bash
vim ~/.asoundrc
```

```bash
pcm.!default {
    type hw
    card 1
}

ctl.!default {
    type hw
    card 1
}
```

# 0x05. Snoyboy

