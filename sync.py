import requests
import json

BigParserAccountEmail = ""
BigParserAccountPassword = ""
FileIDFromGrid = ""

url = "https://www.bigparser.com/APIServices/api/common/login"
data = {
  "emailId": BigParserAccountEmail,
  "password": BigParserAccountPassword,
  "loggedIn": True
}
data_json = json.dumps(data)
headers = {'Content-type': 'application/json'}
authId = requests.post(url, data=data_json,headers=headers).json()['authId']

url = "https://www.bigparser.com/connectors-api/api/apps/file/googleDrive/false"
data = {
	"fileIDs" : [FileIDFromGrid]
}
data_json = json.dumps(data)
headers = {'Content-type': 'application/json', 'authId':authId}

response = requests.put(url, data=data_json, headers=headers).json()

try:
	url = "https://www.bigparser.com/connectors-api/api/apps/file/googleDrive/" + response['requestId'] + "/status"
	headers = {'authId':authId}
	response = requests.get(url, headers=headers).json()
	print response
except KeyError:
	print "Your Grid is already synced up to the most recent version of your Google Sheet"