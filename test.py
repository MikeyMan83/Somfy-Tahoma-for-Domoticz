#Variables:

pin 			    = "2017-8871-5701"
port 			    = "8443"
baseUrl 		    = f"https://gateway-{pin}.local:{port}/enduser-mobile-web/1/enduserAPI"
token			    = "62ecd0f3cdda9a49c2c1"

###API URLS
#Events    
fetchevents 	    = f"{baseUrl}/events/:listenerId/fetch" #Post
unregisterlistener  = f"{baseUrl}/events/:listenerId/unregister" #Post
registerlistener    = f"{baseUrl}/events/register" #Post

#Setup
getdevice		    = f"{baseUrl}/setup/devices/:deviceURL" #Get
getdevices		    = f"{baseUrl}/setup/devices" #Get
getdevicescontrol 	= f"{baseUrl}/setup/devices/controllables/:controllableName" #Get
getsetup		    = f"{baseUrl}/setup" #Get
getgateway		    = f"{baseUrl}/setup/gateways" #Get

#Exec
cancelexecutions 	= f"{baseUrl}/exec/current/setup" #Del
cancelspecificexec  = f"{baseUrl}/exec/current/setup/:executionId" #Del
getexecutions       = f"{baseUrl}/exec/current" #Get
getexecution	    = f"{baseUrl}/exec/current/:executionId" #Get
executeaction       = f"{baseUrl}/exec/apply" #Post


#Api version
getapiversion 	    = f"{baseUrl}/apiVersion" #Get
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
import logging
import time
import os


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
        return



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
   
#Device data? 
def get_devices(self, Devices, firstFree):
        #logging.debug("start get devices")
        #Headers = { 'Host': self.srvaddr,"Connection": "keep-alive","Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded", "Cookie": self.cookie}
        #url = self.base_url + '/enduser-mobile-web/enduserAPI/setup/devices'
        #response = requests.get(url, headers=Headers, timeout=self.timeout)
        logging.debug("get device response: url '" + str(response.url) + "' response headers: '"+str(response.headers)+"'")
        logging.debug("get device response: status '" + str(response.status_code) + "' response body: '"+str(response.json())+"'")
        if response.status_code != 200:
            logging.error("get_devices: error during get devices, status: " + str(response.status_code))
            return

        #Data = response.json()
        Data = outfile


        if (not "uiClass" in response.text):
            logging.error("get_devices: missing uiClass in response")
            logging.debug(str(Data))
            return

        self.devices = Data

        self.filtered_devices = list()
        for device in self.devices:
            logging.debug("get_devices: Device name: "+device["deviceURL"]+" Device class: "+device["uiClass"])
            if (((device["uiClass"] == "RollerShutter") or (device["uiClass"] == "ExteriorScreen") or (device["uiClass"] == "Screen") or (device["uiClass"] == "Awning") or (device["uiClass"] == "Pergola") or (device["uiClass"] == "GarageDoor") or (device["uiClass"] == "Window") or (device["uiClass"] == "VenetianBlind") or (device["uiClass"] == "ExteriorVenetianBlind")) and ((device["deviceURL"].startswith("io://")) or (device["deviceURL"].startswith("rts://")))):
                self.filtered_devices.append(device)
                print(Devices)

        logging.debug("get_devices: devices found: "+str(len(Devices))+" self.startup: "+str(self.startup))
        if (len(Devices) == 0 and self.startup):
            count = 1
            for device in self.filtered_devices:
                logging.info("get_devices: Creating device: "+device["deviceURL"])
                swtype = None

                if (device["deviceURL"].startswith("io://")):
                    if (device["uiClass"] == "Awning"):
                        swtype = 13
                    else:
                        swtype = 16
                elif (device["deviceURL"].startswith("rts://")):
                    swtype = 6

                Domoticz.Device(Name=device["deviceURL"], Unit=count, Type=244, Subtype=73, Switchtype=swtype, DeviceID=device["deviceURL"]).Create()

                if not (count in Devices):
                    logging.error("Device creation not allowed, please allow device creation")
                    Domoticz.Error("Device creation not allowed, please allow device creation")
                else:
                    logging.info("Device created: "+device["deviceURL"])
                    count += 1

        if ((len(Devices) < len(self.filtered_devices)) and len(Devices) != 0 and self.startup):
            logging.info("New device(s) detected")
            found = False

            for device in self.filtered_devices:
                for dev in Devices:
                  UnitID = Devices[dev].Unit
                  if Devices[dev].DeviceID == device["deviceURL"]:
                    found = True
                    break
                if (not found):
                 idx = firstFree
                 swtype = None

                 logging.debug("get_devices: Must create device: "+device["deviceURL"])

                 if (device["deviceURL"].startswith("io://")):
                    if (device["uiClass"] == "Awning"):
                     swtype = 13
                    else:
                     swtype = 16
                 elif (device["deviceURL"].startswith("rts://")):
                    swtype = 6

                 Domoticz.Device(Name=device["label"], Unit=idx, Type=244, Subtype=73, Switchtype=swtype, DeviceID=device["deviceURL"]).Create()

                 if not (idx in Devices):
                     logging.error("Device creation not allowed, please allow device creation")
                     Domoticz.Error("Device creation not allowed, please allow device creation")
                 else:
                     logging.info("New device created: "+device["label"])
                else:
                  found = False
        self.startup = False
        self.get_events()
