#Variables:

pin 			= "2111-8111-5111"
port 			= "8443"
baseUrl 		= f"https://gateway-{pin}.local:{port}/enduser-mobile-web/1/enduserAPI"
token			= "62abc0d3efgh9b49d2e1"
    
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

output_file = json.dumps(response.text, indent=4)

with open('response.json', 'w') as outfile:
   outfile.write(output_file)
