'''
Author       : AyanamaiYui
Date         : 2021-09-13 21:58:24
LastEditTime : 2021-11-14 02:23:09
Version      : 
Description  : 
'''
# encoding=utf-8

import time
import sys
import hashlib
import hmac
import base64
import stomp
import ssl
import schedule
import threading
import pymysql
import json


def update_database(remain_volume, bin_type):
    db = pymysql.connect(host='127.0.0.1', 
                            port=3306,
                            user = '',
                            password='',
                            database="")
    cursor = db.cursor()
    # 获取devices_id和devices_type
    SELECT_DEVICES_ID = "SELECT * FROM apps_devices WHERE DevicesType = '%s'" % (bin_type)
    cursor.execute(SELECT_DEVICES_ID)
    data = cursor.fetchone()
    dustbin_id = data[0]
    dusbtin_type = data[1]
    now_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())  
    # 更新
    UPDATE_VOLUME = "UPDATE apps_devices SET VolumeRemain = %s, Time = '%s' WHERE DevicesType = '%s'" % (remain_volume, now_time, bin_type)
    # 插入log_volume
    INSERT_LOG_VOLUME = "INSERT INTO apps_logvolume(DevicesId, DevicesType, VolumeRemain, LogTime) VALUES ('%s', '%s', '%s', '%s')" % (dustbin_id, dusbtin_type, remain_volume, now_time) 
    # 插入log_putrubbish
    INSERT_PUT_RUBBISH = "INSERT INTO apps_logputrubbish(DevicesId, DevicesType, VolumeRemain, PutTime) VALUES ('%s', '%s', '%s', '%s')" % (dustbin_id, dusbtin_type, remain_volume, now_time)
    cursor.execute(UPDATE_VOLUME)
    db.commit()
    cursor.execute(INSERT_LOG_VOLUME)
    db.commit()
    cursor.execute(INSERT_PUT_RUBBISH)
    db.commit()
    db.close()

def insert_envrionment_database(temp, hum, aqi):
    db = pymysql.connect(host='127.0.0.1', 
                            port=3306,
                            user = '',
                            password='',
                            database="")
    cursor = db.cursor()
    now_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())  
    INSERT_LOG_ENVIRONMENT = "INSERT INTO apps_environment(Temperature, Humidity, AirQuality, Time, Dustbin) VALUES ('%d', '%d', '%d', '%s', '%s')" % (temp, hum, aqi, now_time, "bin1") 
    cursor.execute(INSERT_LOG_ENVIRONMENT)
    db.commit()
    db.close()

def connect_and_subscribe(conn):
    accessKey = ""
    accessSecret = ""
    consumerGroupId = ""
    # iotInstanceId：实例ID。
    # iotInstanceId = "${YourIotInstanceId}"
    clientId = ""
    # 签名方法：支持hmacmd5，hmacsha1和hmacsha256。
    signMethod = "hmacsha1"
    timestamp = current_time_millis()
    # userName组装方法，请参见AMQP客户端接入说明文档。
    # 若使用二进制传输，则userName需要添加encode=base64参数，服务端会将消息体base64编码后再推送。具体添加方法请参见下一章节“二进制消息体说明”。
    username = clientId + "|authMode=aksign" + ",signMethod=" + signMethod \
                    + ",timestamp=" + timestamp + ",authId=" + accessKey \
                    + ",consumerGroupId=" + consumerGroupId + "|"
    signContent = "authId=" + accessKey + "&timestamp=" + timestamp
    # 计算签名，password组装方法，请参见AMQP客户端接入说明文档。
    password = do_sign(accessSecret.encode("utf-8"), signContent.encode("utf-8"))
    
    conn.set_listener('', MyListener(conn))
    conn.connect(username, password, wait=True)
    # 清除历史连接检查任务，新建连接检查任务
    schedule.clear('conn-check')
    schedule.every(1).seconds.do(do_check,conn).tag('conn-check')

class MyListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        # print('received a message "%s"' % frame.body)
        response_data = json.loads(frame.body)
        # print(type(response_data))
        print(response_data)
        # print(response_data["items"])

        
        if "items" in response_data:
            if "remain_volume_harmful" in response_data["items"]:
                update_database(response_data["items"]["remain_volume_harmful"]["value"], "bin1_harmful1")

            elif "remain_volume_kitchen" in response_data["items"]:
                update_database(response_data["items"]["remain_volume_kitchen"]["value"], "bin1_kitchen1")

            elif "remain_volume_others" in response_data["items"]:
                update_database(response_data["items"]["remain_volume_others"]["value"], "bin1_others")

            elif "remain_volume_recyable" in response_data["items"]:
                update_database(response_data["items"]["remain_volume_recyable"]["value"], "bin1_recyable")

            elif "Humidity" and "Temperature" and "AQI" in response_data["items"]:
                insert_envrionment_database(response_data["items"]["temperature"]["value"], response_data["items"]["Humidity"]["value"], response_data["items"]["AQI"]["value"])

        elif "identifier" in response_data:
            if response_data["identifier"] == "log_dustbin_broken":
                pass

    def on_heartbeat_timeout(self):
        print('on_heartbeat_timeout')

    def on_connected(self, headers):
        print("successfully connected")
        conn.subscribe(destination='/topic/#', id=1, ack='auto')
        print("successfully subscribe")

    def on_disconnected(self):
        print('disconnected')
        connect_and_subscribe(self.conn)

def current_time_millis():
    return str(int(round(time.time() * 1000)))

def do_sign(secret, sign_content):
    m = hmac.new(secret, sign_content, digestmod=hashlib.sha1)
    return base64.b64encode(m.digest()).decode("utf-8")

# 检查连接，如果未连接则重新建连
def do_check(conn):
    print('check connection, is_connected: %s', conn.is_connected())
    if (not conn.is_connected()):
        try:
            connect_and_subscribe(conn)
        except Exception as e:
            print('disconnected, ', e)

# 定时任务方法，检查连接状态
def connection_check_timer():
    while 1:
        schedule.run_pending()
        time.sleep(10)

#  接入域名，请参见AMQP客户端接入说明文档。这里直接填入域名，不需要带amqps://前缀
conn = stomp.Connection([('1650947015949971.iot-amqp.cn-shanghai.aliyuncs.com', 61614)])
conn.set_ssl(for_hosts=[('1650947015949971.iot-amqp.cn-shanghai.aliyuncs.com', 61614)], ssl_version=ssl.PROTOCOL_TLS)

try:
    connect_and_subscribe(conn)
except Exception as e:
    print('connecting failed')
    raise e
    
# 异步线程运行定时任务，检查连接状态
thread = threading.Thread(target=connection_check_timer)
thread.start()
