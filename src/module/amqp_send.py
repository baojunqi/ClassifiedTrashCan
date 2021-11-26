'''
Author       : AyanamaiYui
Date         : 2021-11-10 05:42:16
LastEditTime : 2021-11-13 16:24:28
Version      : 
Description  : 
'''

import time
from urllib import request
from linkkit import linkkit

class AMQPSender():
    def __init__(self) -> None:
        self.lk = linkkit.LinkKit(
            host_name = "",
            product_key = "",
            device_name = "",
            device_secret = ""
        )

        self.lk.on_connect = self.on_connect
        self.lk.on_disconnect = self.on_disconnect
        self.lk.on_thing_enable = self.on_thing_enable
        self.lk.on_thing_disable = self.on_thing_disable
        self.lk.on_thing_prop_post = self.on_thing_prop_post
        self.lk.on_thing_call_service = self.on_thing_call_service
        self.lk.on_thing_event_post = self.on_thing_event_post

        self.lk.thing_setup("/home/pi/workspace/IOTFinalProject/tsl.json")
        self.lk.connect_async()
        
        

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
    
    def on_thing_event_post(self, event, request_id, code, data, message, userdata):
        print("on_thing_event_post event:%s,request id:%s, code:%d, data:%s, message:%s" %
        (event, request_id, code, str(data), message))
        
    def send_property(self, prop_data):
        rc, request_id = self.lk.thing_post_property(property_data=prop_data)
        return rc

    def send_event(self, event_tuple):
        '''
        prop_data = ()
        '''
        rc, request_id = self.lk.thing_trigger_event(event_tuple=event_tuple)
        return rc


if __name__ == "__main__":
    sender = AMQPSender()
    time.sleep(5)
    # event = {
    #     "log_put_rubbish_record": 1
    # }
    # sender.send_event(("log_put_rubbish", event))
    
    data = {
        "remain_volume_harmful": 69
    }
    time.sleep(2)
    while True:
        rc = sender.send_property(prop_data=data)
        print(rc)
        time.sleep(1)