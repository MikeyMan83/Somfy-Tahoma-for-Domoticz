#Variables:

pin 			= "2111-8111-5111"
port 			= "8443"
baseUrl 		= f"https://gateway-{pin}.local:{port}/enduser-mobile-web/1/enduserAPI"
token			= "62abc0d3efgh9b49d2e1"
    
getapiversion 	= f"{baseUrl}/apiVersion"
getdevices		= f"{baseUrl}/setup/devices"
getsetup		= f"{baseUrl}/setup"
getgateway		= f"{baseUrl}/setup/gateways"

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

#Get verion
#response = requests.request("GET", getapiversion, headers=headers, data=payload, verify=False)

#Get devices
# response = requests.request("GET", getdevices, headers=headers, data=payload, verify=False)

#Get setup
#response = requests.request("GET", getsetup, headers=headers, data=payload, verify=False)

#Get gateway
response = requests.request("GET", getgateway, headers=headers, data=payload, verify=False)

print(response.json())


