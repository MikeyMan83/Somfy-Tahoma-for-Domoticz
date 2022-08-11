Credits to 




#Variables:

pin                 = "2017-8871-5701"
port                = "8443"
baseUrl             = f"https://gateway-{pin}.local:{port}/enduser-mobile-web/1/enduserAPI"
token               = "62ecd0f3cdda9a49c2c1"

###API URLS
#Events    
fetchevents         = f"{baseUrl}/events/:listenerId/fetch" #Post
unregisterlistener  = f"{baseUrl}/events/:listenerId/unregister" #Post
registerlistener    = f"{baseUrl}/events/register" #Post

#Setup
getdevice           = f"{baseUrl}/setup/devices/:deviceURL" #Get
getdevices          = f"{baseUrl}/setup/devices" #Get
getdevicescontrol   = f"{baseUrl}/setup/devices/controllables/:controllableName" #Get
getsetup            = f"{baseUrl}/setup" #Get
getgateway          = f"{baseUrl}/setup/gateways" #Get

#Exec
cancelexecutions    = f"{baseUrl}/exec/current/setup" #Del
cancelspecificexec  = f"{baseUrl}/exec/current/setup/:executionId" #Del
getexecutions       = f"{baseUrl}/exec/current" #Get
getexecution        = f"{baseUrl}/exec/current/:executionId" #Get
executeaction       = f"{baseUrl}/exec/apply" #Post


#Api version
getapiversion       = f"{baseUrl}/apiVersion" #Get
### API Urls

payload={}
headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
        
        
#Print variable output
#print(f"Pin = {pin}")
#print(f"Port = {port}")
#print(f"URL = {baseUrl}")
#print(f"Token = {token}")
#print(f"Headers = {headers}")


import requests
import json
#import Domoticz
#import DomoticzEx as Domoticz
import sys
import tahoma
import logging
import time
import os




#Get verion
#response = requests.request("GET", getapiversion, headers=headers, data=payload, verify=False)

#Get devices
response = requests.request("GET", getdevices, headers=headers, data=payload, verify=False)

#Get setup
#response = requests.request("GET", getsetup, headers=headers, data=payload, verify=False)

#Get gateway
#response = requests.request("GET", getgateway, headers=headers, data=payload, verify=False)

#print (response.text)
#print (type(response.text))
#print (isinstance(response.text, str))


output_file = json.loads(response.text)
#print (json.dumps(output_file, indent=4))

with open('response.json', 'w', encoding='utf-8') as outfile:
    json.dump(output_file, outfile, indent=4)

class BasePlugin:
    def __init__(self):
        self.heartbeat = False
        self.devices = None
        self.heartbeat_delay = 1
        self.con_delay = 0
        self.wait_delay = 30
        self.json_data = None
        self.command = False
        self.refresh = True
        self.actions_serialized = []
        self.logger = None
        self.log_filename = "somfy.log"
        self.headers = headers
        return
# Test entry in tahoma.py
    def test_print(self, headers=None):
        self.tahoma = tahoma.Tahoma()
        headers = self.tahoma.headers
    print(headers)

