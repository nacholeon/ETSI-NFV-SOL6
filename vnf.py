

import requests
import json
import yaml



###### Generate Auth Token ###############
#url = "https://10.75.225.108:9999/osm/admin/v1/tokens"
url = "https://10.75.225.108:9999"
authURI="/osm/admin/v1/tokens"


authURL=url+authURI

print (authURL)

payload = json.dumps({
  "username": "admin",
  "password": "admin",
  "project_id": "admin"
})

headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", authURL, headers=headers, data=payload, verify=False)

#print (response.cookies)

sessionID =  requests.utils.dict_from_cookiejar(response.cookies)

#cookies_dictionary = session.get_dict()


#print ("session_id: ",sessionID['session_id'])



if response.status_code != 200:
	print('error: ' + str(response.status_code))
else:
	print('Success')
	#print (response.text)
	data = yaml.safe_load(response.text)
	#print (data)
	token2 = data['id']
	print ("token: ",token2)
	print ("session_id", sessionID)


##############################################################################################################################
########################Upload VNF Descriptor tar gzip           ############################################################
##############################################################################################################################

with open("/var/jenkins/osm/vnf_id.txt", "r") as file:
    vnfID = file.read().replace('\n', '')
print (vnfID)

vnfURI1 = "/osm/vnfpkgm/v1/vnf_packages/"
vnfURI2 = "/package_content"
vnfURL = url+vnfURI1+vnfID+vnfURI2

print (vnfURL)

payload = open("/var/jenkins/osm/amf2_knf.tar.gz", 'rb').read()

headers = {
  'Content-Type': 'application/zip',
  'Authorization': 'Bearer ' + token2
}

response2 = requests.request("PUT", vnfURL, headers=headers, data=payload, verify=False)


if response2.status_code != 204:
	print('error: ' + str(response2.status_code))
else:
	print('Success')
	print (response2.text)
	#data = yaml.safe_load(response.text)
	#print (data)
	#token = data['id']
	#print (token)






