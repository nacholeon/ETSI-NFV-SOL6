

import requests
import json
import yaml

###### Generate Auth Token ###############
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
	token = data['id']
	print ("token: ",token)
	print ("session_id", sessionID)


##############################################################################################################################
########################Upload NS  Descriptor YAML           ############################################################
##############################################################################################################################

nsURI = "/osm/nsd/v1/ns_descriptors"

payload2 = "nsd-catalog:\r\n    nsd:\r\n    -   id: amf_ns2\r\n        name: amf_ns2\r\n        short-name: amf_ns2\r\n        description: NS consisting of a KNF amf_knf connected to mgmt network\r\n        vendor: ACME\r\n        version: '1.1'\r\n        constituent-vnfd:\r\n        -   member-vnf-index: amf\r\n            vnfd-id-ref: amf_knf\r\n        vld:\r\n        -   id: mgmtnet\r\n            name: mgmtnet\r\n            type: ELAN\r\n            mgmt-network: true\r\n            vim-network-name: mgmt\r\n            vnfd-connection-point-ref:\r\n            -   member-vnf-index-ref: amf\r\n                vnfd-id-ref: amf_knf\r\n                vnfd-connection-point-ref: mgmt\r\n\r\n"
headers2 = {
  'Content-Type': 'application/yaml',
  'Authorization': 'Bearer ' + token
}
url2 = url+nsURI

response2 = requests.request("POST", url2, headers=headers2, data=payload2, verify=False)


if response2.status_code != 201:
	print('error: ' + str(response2.status_code))
else:
	print('Success')
	print (response2.text)
	data = yaml.safe_load(response2.text)
	#print (data)
	nsId = data['id']
	print (nsId)
	file = open("/var/jenkins/osm/ns_id.txt", "w")
	file.write(nsId)
	file.close()



##############################################################################################################################
########################Upload NS Package tar gzip           ############################################################
##############################################################################################################################


nsdURI1 = "/osm/nsd/v1/ns_descriptors/"
nsdURI2 = "/nsd_content"
nsdURL = url+nsdURI1+nsId+nsdURI2

print (nsdURL)

payload = open("/var/jenkins/osm/amf_ns2.tar.gz", 'rb').read()

headers = {
  'Content-Type': 'application/zip',
  'Authorization': 'Bearer ' + token
}

response3 = requests.request("PUT", nsdURL, headers=headers, data=payload, verify=False)


if response3.status_code != 204:
	print('error: ' + str(response3.status_code))
else:
	print('Success')
	print (response3.text)
	#data = yaml.safe_load(response.text)
	#print (data)
	#token = data['id']
	#print (token)






