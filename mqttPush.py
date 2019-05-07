'''
Module to connect to adafruit to control NODE MCU with common feed and KEYS
'''


import os
import requests
import json
import time


__author__ = "Nyzex"

'''
Send data to nodeMCU through ADAFRUIT MQTT
'''


class FruitSent:

    def __init__(self, usename, AIOKEY,feedname):

        self.username = username
        self.AIO = AIOKEY
        self.feedname = feedname

        self.headers = header = {
        "X-AIO-Key": "{}".format(self.AIO),
        "Content-Type": "application/json"

        }

    def data_sent(self, value):

        '''
        send the 1 or 0 toggle data to adafruit api
        '''
        stateData = value
        r = requests.post("{}".format(os.eviron.get("adafruitIOv2"))+"{}/feeds/{}/data".format(self.username, self.feedname),data  = json.dumps({"value": "{}".format(stateData)}),headers = self.headers)
        return r.status_code
