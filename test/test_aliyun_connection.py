'''
Author       : AyanamaiYui
Date         : 2021-09-13 13:49:22
LastEditTime : 2021-11-13 04:23:21
Version      : 
Description  : 测试阿里云IOT连接和数据上传
'''

import time
from linkkit import linkkit

def on_thing_enable(userdata):
    print("on_thing_enable")

def on_thing_disable(userdata):
    print("on_thing_disable")

def on_connect(session_flag, rc, userdata):
    print("on_connect:%d,rc:%d,userdata:" % (session_flag, rc))

def on_disconnect(rc, userdata):
    print("on_disconnect:rc:%d,userdata:" % rc)

def on_thing_prop_post(request_id, code, data, message,userdata):
    print("on_thing_prop_post request id:%s, code:%d, data:%s message:%s" %
        (request_id, code, str(data), message))

def on_thing_call_service(self, identifier, request_id, params, userdata):
    print("on_thing_call_service: identifier:%s, request_id:%s, params:%s" % (identifier, request_id, params))
    self.linkkit.thing_answer_service(identifier, request_id, 200, {})

lk = linkkit.LinkKit(
    host_name = "cn-shanghai",
    product_key = "a1S9VRi8QDG",
    device_name = "raspberry",
    device_secret = "82b28b781c2641a71c9463ec16c16fce"
)

lk.on_connect = on_connect
lk.on_disconnect = on_disconnect
lk.on_thing_enable = on_thing_enable
lk.on_thing_disable = on_thing_disable
lk.on_thing_prop_post = on_thing_prop_post
lk.on_thing_call_service = on_thing_call_service

lk.thing_setup("/home/pi/workspace/IOTFinalProject/tsl.json")
lk.connect_async()

time.sleep(10)

prop_data = {
    "remain_volume_harmful" : 30
}


def send(prop_data):
    rc, requeset_id = lk.thing_post_property(property_data = prop_data)
    print(rc)


send(prop_data=prop_data)