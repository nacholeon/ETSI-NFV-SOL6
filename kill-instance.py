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
######################## Delete CNF from NS instance  ID          ############################################################
##############################################################################################################################


with open("/var/jenkins/osm/instance_id.txt", "r") as file:
  instanceId = file.read().replace('\n', '')
print("instance-ID: ", instanceId)
file.close()


url = "https://10.75.225.108:9999"

instanceURI1 = "/osm/nslcm/v1/ns_instances/"
instanceURI2 = "?vcaStatusRefresh=false"

instanceURL= url+instanceURI1+instanceId+instanceURI2

print (instanceURL)

payload={}

headers = {
  'Authorization': 'Bearer '+ token,
}

response4 = requests.request("DELETE", instanceURL, headers=headers, data=payload, verify=False)


if response4.status_code != 204:
	print('error: ' + str(response4.status_code))
else:
    print('Success')
    print (response4.text)
    data2 = yaml.safe_load(response4.text)
    #instanceId = data2['id']
    #print ("instance_ID: ",instanceId)
    #file = open("/var/jenkins/osm/instance_id.txt","w")
    #file.write(instanceId)
    #file.close()



