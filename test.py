# Credits to 
# Nonolk: https://github.com/nonolk/domoticz_tahoma_blind
# Madpatrick: https://github.com/MadPatrick/somfy

import requests
import json
#import Domoticz
#import DomoticzEx as Domoticz
import sys
import tahoma
import logging
import time
import os
import configparser

config = configparser.ConfigParser()
config.sections()
config.read('config.txt')
# for sect in config.sections():
    # print('Section', sect)
    # for k,v in config.items(sect):
        # print(' {} = {}'.format(k,v))
    # print()

#Variables:
pin     = config['Connection']['pin']
port    = config['Connection']['port']
token   = config['Connection']['token']
baseUrl             = f"https://gateway-{pin}.local:{port}/enduser-mobile-web/1/enduserAPI"
# pin                 = "2000-0000-0001"
# port                = "8443"
# token               = "73fde0f3cdda9a49d3d2"

print(baseUrl)

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


#Test api's
#Get verion
response = requests.request("GET", getapiversion, headers=headers, data=payload, verify=False)

#Get devices
#response = requests.request("GET", getdevices, headers=headers, data=payload, verify=False)

#Get setup
#response = requests.request("GET", getsetup, headers=headers, data=payload, verify=False)

#Get gateway
#response = requests.request("GET", getgateway, headers=headers, data=payload, verify=False)

#print (response.text)
#print (type(response.text))
#print (isinstance(response.text, str))


output_file = json.loads(response.text)
print (json.dumps(output_file, indent=4))

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

    def onStart(self):
        if os.path.exists(Parameters["Mode5"]):
            log_dir = Parameters["Mode5"] 
        else:
            Domoticz.Status("Location {0} does not exist, logging to default location".format(Parameters["Mode5"]))
            log_dir = ""
        log_fullname = os.path.join(log_dir, self.log_filename)
        Domoticz.Status("Starting Tahoma blind plugin, logging to file {0}".format(log_fullname))
        self.logger = logging.getLogger('root')
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(2)
            DumpConfigToLog()
            logging.basicConfig(format='%(asctime)s - %(levelname)-8s - %(filename)-18s - %(message)s', filename=log_fullname,level=logging.DEBUG)
        else:
            logging.basicConfig(format='%(asctime)s - %(levelname)-8s - %(filename)-18s - %(message)s', filename=log_fullname,level=logging.INFO)
        Domoticz.Debug("os.path.exists(Parameters['Mode5']) = {}".format(os.path.exists(Parameters["Mode5"])))
        logging.info("starting plugin version "+Parameters["Version"])
        self.runCounter = int(Parameters['Mode2'])
        
        logging.debug("starting to log in")
        self.tahoma = tahoma.Tahoma()
        try:
            self.tahoma.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
        except exceptions.LoginFailure as exp:
            Domoticz.Error("Failed to login: " + str(exp))
            return
        
        if self.tahoma.logged_in:
            self.tahoma.register_listener()

        if self.tahoma.logged_in:
            self.tahoma.get_devices(Devices, firstFree())
            
        
    def onStop(self):
        logging.info("stopping plugin")
        self.heartbeat = False

    def onConnect(self, Connection, Status, Description):
        logging.debug("onConnect: Connection: '"+str(Connection)+"', Status: '"+str(Status)+"', Description: '"+str(Description)+"' self.tahoma.logged_in: '"+str(self.tahoma.logged_in)+"'")
        if (Status == 0 and not self.tahoma.logged_in):
          self.tahoma.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
        elif (self.cookie and self.tahoma.logged_in and (not self.command)):
          event_list = self.tahoma.get_events()
          self.update_devices_status(event_list)

        elif (self.command):
          event_list = self.tahoma.tahoma_command(self.json_data)
          self.update_devices_status(event_list)
          self.command = False
          self.heartbeat = False
          self.actions_serialized = []
        else:
          logging.info("Failed to connect to tahoma api")

    def onMessage(self, Connection, Data):
        Domoticz.Error("onMessage called but not implemented")
        Domoticz.Debug("onMessage data: "+str(Data))

    def onCommand(self, Unit, Command, Level, Hue):
        logging.debug("onCommand: Unit: '"+str(Unit)+"', Command: '"+str(Command)+"', Level: '"+str(Level)+"', Hue: '"+str(Hue)+"'")
        commands_serialized = []
        action = {}
        commands = {}
        params = []

        if (str(Command) == "Off"):
            commands["name"] = "close"
        elif (str(Command) == "On"):
            commands["name"] = "open"
        elif ("Set Level" in str(Command)):
            commands["name"] = "setClosure"
            tmp = 100 - int(Level)
            params.append(tmp)
            commands["parameters"] = params

        commands_serialized.append(commands)
        action["deviceURL"] = Devices[Unit].DeviceID
        action["commands"] = commands_serialized
        self.actions_serialized.append(action)
        logging.debug("preparing command: # commands: "+str(len(commands)))
        logging.debug("preparing command: # actions_serialized: "+str(len(self.actions_serialized)))
        data = {"label": "Domoticz - "+Devices[Unit].Name+" - "+commands["name"], "actions": self.actions_serialized}
        self.json_data = json.dumps(data, indent=None, sort_keys=True)

        if (not self.tahoma.logged_in):
            logging.info("Not logged in, must connect")
            self.command = True
            self.tahoma.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
            if self.tahoma.logged_in:
                self.tahoma.register_listener()

        event_list = []
        try:
            event_list = self.tahoma.tahoma_command(self.json_data)
        except (exceptions.TooManyRetries, exceptions.FailureWithErrorCode, exceptions.FailureWithoutErrorCode) as exp:
            Domoticz.Error("Failed to send command: " + str(exp))
            logging.error("Failed to send command: " + str(exp))
            return
        if event_list is not None and len(event_list) > 0:
            self.update_devices_status(event_list)
        self.heartbeat = False
        self.actions_serialized = []

    def onDisconnect(self, Connection):
        return

    def onHeartbeat(self):
        self.runCounter = self.runCounter - 1
        if self.runCounter <= 0:
            logging.debug("Poll unit")
            self.runCounter = int(Parameters['Mode2'])            

            if (self.tahoma.logged_in and (not self.tahoma.startup)):
                if (not self.tahoma.logged_in):
                    self.tahoma.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
                    if self.tahoma.logged_in:
                        self.tahoma.register_listener()
                event_list = []
                try:
                    event_list = self.tahoma.get_events()
                except (exceptions.TooManyRetries, exceptions.FailureWithErrorCode, exceptions.FailureWithoutErrorCode) as exp:
                    Domoticz.Error("Failed to request data: " + str(exp))
                    logging.error("Failed to request data: " + str(exp))
                    return
                if event_list is not None and len(event_list) > 0:
                    self.update_devices_status(event_list)
                self.heartbeat = True

            elif (self.heartbeat and (self.con_delay < self.wait_delay) and (not self.tahoma.logged_in)):
                self.con_delay +=1
                Domoticz.Status("Too many connections waiting before authenticating again")

            elif (self.heartbeat and (self.con_delay == self.wait_delay) and (not self.tahoma.logged_in)):
                if (not self.tahoma.logged_in):
                    self.tahoma.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
                    if self.tahoma.logged_in:
                        self.tahoma.register_listener()
                self.heartbeat = True
                self.con_delay = 0
        else:
            logging.debug("Polling unit in " + str(self.runCounter) + " heartbeats.")

    def update_devices_status(self, Updated_devices):
        logging.debug("updating device status self.tahoma.startup = "+str(self.tahoma.startup)+"on data: "+str(Updated_devices))
        for dev in Devices:
           logging.debug("update_devices_status: checking Domoticz device: "+Devices[dev].Name)
           for device in Updated_devices:

             if (Devices[dev].DeviceID == device["deviceURL"]) and (device["deviceURL"].startswith("io://")):
               level = 0
               status_l = False
               status = None

               if (self.tahoma.startup):
                   states = device["states"]
               else:
                   states = device["deviceStates"]
                   if (device["name"] != "DeviceStateChangedEvent"):
                       logging.debug("update_devices_status: device['name'] != DeviceStateChangedEvent: "+str(device["name"])+": breaking out")
                       break

               for state in states:
                  status_l = False

                  if ((state["name"] == "core:ClosureState") or (state["name"] == "core:DeploymentState")):
                    level = int(state["value"])
                    level = 100 - level
                    status_l = True
                    
                  if status_l:
                    if (Devices[dev].sValue):
                      int_level = int(Devices[dev].sValue)
                    else:
                      int_level = 0
                    if (level != int_level):

                      Domoticz.Status("Updating device:"+Devices[dev].Name)
                      logging.info("Updating device:"+Devices[dev].Name)
                      if (level == 0):
                        Devices[dev].Update(0,"0")
                      if (level == 100):
                        Devices[dev].Update(1,"100")
                      if (level != 0 and level != 100):
                        Devices[dev].Update(2,str(level))
        return
        
# Test entry in tahoma.py
    def test_print(self, headers=None):
        self.tahoma = tahoma.Tahoma()
        headers = self.tahoma.headers
    print(headers)

    # def test_update(self, Updated_devices=None):
        # update_devices_status(self)
    # print(device)
