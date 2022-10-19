

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


print ("session_id: ",sessionID['session_id'])



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
	file = open("/var/jenkins/osm/session_id.txt", "w")
	file.write(sessionID['session_id'])
	file.close()

##############################################################################################################################
########################Create VNF Descriptor from yaml vnfd.yaml ############################################################
##############################################################################################################################


vnfdURI = "/osm/vnfpkgm/v1/vnf_packages"

vnfdURL=url+vnfdURI

print ("")

payload = "vnfd-catalog:\r\n  schema-version: '3.0'\r\n  vnfd:\r\n  - id: amf_knf2\r\n    name: amf_knf2\r\n    short-name: amf_knf2\r\n    description: KNF with KDU using a helm-chart for free5gc AMF\r\n    vendor: ACME\r\n    version: '1.0'\r\n    mgmt-interface:\r\n      cp: mgmt\r\n    connection-point:\r\n    - name: mgmt\r\n    k8s-cluster:\r\n      nets:\r\n      - id: mgmtnet\r\n        external-connection-point-ref: eth0\r\n      - id: n2-interface\r\n        external-connection-point-ref: n2-interface\r\n      - id: n26-interface\r\n        external-connection-point-ref: n6-interface\r\n    kdu:\r\n    - name: amf\r\n      helm-chart: rel16/amf\r\n"
headers = {
  'Content-Type': 'application/yaml',
  'Authorization': 'Bearer '+ token,
  #'Cookie': 'session_id=e5097c797edfecd352ae21e680dd801df6e5f29c'
  #'Cookie': sessionID['session_id']
}

response2 = requests.request("POST", vnfdURL, headers=headers, data=payload, verify=False)


if response2.status_code != 201:
	print('error: ' + str(response2.status_code))
else:
	print('Success')
	print (response2.text)
	data2 = yaml.safe_load(response2.text)
	#print (data)
	vnfId = data2['id']
	print ("vnfID: ",vnfId)
	file = open("/var/jenkins/osm//vnf_id.txt", "w")
	file.write(vnfId)
	file.close()









