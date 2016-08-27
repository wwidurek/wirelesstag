import requests
import json
from decimal import Decimal


_USERNAME = ""
_PASSWORD = ""

_BASEURL = "https://www.mytaglist.com"

_SIGNIN = _BASEURL + "/ethAccount.asmx/SignIn"
_ISSIGNED = _BASEURL + "/ethAccount.asmx/IsSignedIn"
_GETTAGLIST = _BASEURL + "/ethClient.asmx/GetTagList"
_GETTEMPDATA = _BASEURL + "/ethLogShared.asmx/GetLatestTemperatureRawDataByUUID"

_HEADERS = {
	"content-type": "application/json; charset=utf-8"
}

_DECIMALS = 1

class ClientAuth:
    """

    Request authentication and return authentication cookie. If cookie requested and not already logged in, it will log in again.

    """ 
    def __init__(self, username=_USERNAME,
                       password=_PASSWORD):
        
       postParams = {
             "email": username,
             "password": password
             }

       r = requests.post(_SIGNIN, headers=_HEADERS, data=json.dumps(postParams))
       self._accessCookie = r.cookies 
       self._username = username
       self._password = password
       
       r = requests.post(_ISSIGNED, headers=_HEADERS,cookies=self._accessCookie)
       response = r.json()
       if response['d']!=True:
          raise ValueError('Incorrect Login operation')
      
    @property
    def accessCookie(self):
      #if not signed in, sign in and return cookie

       r = requests.post(_ISSIGNED, headers=_HEADERS)
       response = r.json()
       if response['d']=='TRUE':
          return self._accessCookie 
       else:
            postParams = {
              "email": self._username,
              "password": self._password
             }

            r = requests.post(_SIGNIN, headers=_HEADERS, data=json.dumps(postParams))

            self._accessCookie = r.cookies
            return self._accessCookie

       return self._accessCookie

class WirelessTagData:
   """
   Retrieves data from Wireless senors available
   """    


   def __init__(self,authData):
      self.getAuthToken = authData.accessCookie
   #   self._TagList = self.getTagsList()


   @property
   def tagList(self):
        self._tagList = {}
        cookies = self.getAuthToken
        r = requests.post(_GETTAGLIST, headers=_HEADERS, cookies=cookies)

        response = r.json()
        for i in response:
                for tag in response[i]:
                        tag_id = tag["slaveId"]
                        tag_uuid = tag["uuid"]
                        tag_name = tag["name"]
                        tag_type = tag["tagType"]

                        self._tagList[tag_uuid] = {'tag_id' : tag_id, 'tag_name' : tag_name, 'tag_type' : tag_type}

        return self._tagList
  

   def getTemperature(self,uuid=""):
        """
        If no UUID provided, it will take the first sensor discovered
        """
   
        if uuid=="":
           uuid = self.tagList.keys()[0]
        data = {
             "uuid": uuid
             }
        cookies = self.getAuthToken

        r  = requests.post(_GETTEMPDATA, headers=_HEADERS, cookies=cookies, data=json.dumps(data))
        parsed_response = r.json()
        temp = Decimal(float(parsed_response["d"]["temp_degC"]))
        rounded_temp = round(temp,_DECIMALS)
        return rounded_temp 


   def getHumidity(self,uuid=""):
        """
        If no UUID provided, it will take the first sensor discovered
        """

        if uuid=="":
           uuid = self.tagList.keys()[0]
        data = {
             "uuid": uuid
             }
        cookies = self.getAuthToken

        r  = requests.post(_GETTEMPDATA, headers=_HEADERS, cookies=cookies, data=json.dumps(data))
        parsed_response = r.json()
        return parsed_response["d"]["cap"]

   def getBatteryVolt(self,uuid=""):
        """
        If no UUID provided, it will take the first sensor discovered
        """

        if uuid=="":
           uuid = self.tagList.keys()[0]
        data = {
             "uuid": uuid
             }
        cookies = self.getAuthToken

        r  = requests.post(_GETTEMPDATA, headers=_HEADERS, cookies=cookies, data=json.dumps(data))
        parsed_response = r.json()
        return parsed_response["d"]["battery_volts"]

