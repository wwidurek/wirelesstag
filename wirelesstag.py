import requests
import json

COOKIES = None

USERNAME = "wwidurek@gmail.com"
PASSWORD = "k4loryferM2010"

BASEURL = "https://www.mytaglist.com"

SIGNIN = BASEURL + "/ethAccount.asmx/SignIn"
GETTEMPERATURERAWDATA = BASEURL + "/ethLogs.asmx/GetTemperatureRawData"
GETTAGLIST = BASEURL + "/ethClient.asmx/GetTagList"
GETHOURLYSTATS = BASEURL + "/ethLogs.asmx/GetHourlyStats"
GETMULTITAGSTATSRAW = BASEURL + "/ethLogs.asmx/GetMultiTagStatsRaw"
GETTEMPDATA = BASEURL + "/ethLogShared.asmx/GetLatestTemperatureRawDataByUUID"

HEADERS = {
	"content-type": "application/json; charset=utf-8"
}

def login():
	global COOKIES

	data = {
		"email": USERNAME,
		"password": PASSWORD
	}
	
	r = requests.post(SIGNIN, headers=HEADERS, data=json.dumps(data))
	COOKIES = r.cookies
	
	if "set-cookie" in r.headers:
		print "Login successful"
	else:
		print "Login failed"
		return False
		
	return True

def GetTagList():
	data = {}
        tag_list = {}
	
	r = requests.post(GETTAGLIST, headers=HEADERS, cookies=COOKIES, data=json.dumps(data))
	
	response = r.json()
	for i in response:
		for tag in response[i]:
			tag_id = tag["slaveId"]
			tag_uuid = tag["uuid"]
			tag_name = tag["name"]
			tag_type = tag["tagType"]			
		
			tag_list[tag_uuid] = {'tag_id' : tag_id, 'tag_name' : tag_name, 'tag_type' : tag_type}	
					
	return tag_list

#returns current data from tag in the following format (temp,humidity,battery_volt)
def GetTagData(tag_uuid):
     data = {
             "uuid": tag_uuid 
            }

     r  = requests.post(GETTEMPDATA, headers=HEADERS, cookies=COOKIES, data=json.dumps(data)) 
     parsed_response = r.json() 
     return parsed_response["d"]["temp_degC"], parsed_response["d"]["cap"], parsed_response["d"]["battery_volts"]
	
if __name__ == "__main__":
	if login() == True:
                while 1:
 #                        GetTagList()
			for i in GetTagList():
			   print GetTagData(i) 
                        time.sleep(3600)
