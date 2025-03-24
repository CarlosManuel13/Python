import base64
import requests
import os
import json

class RaixerApi():
    
    def __init__(self,_user,_secret):
        self.user = _user
        self.secret = _secret
        self.base_url = "connections"
    
    def encodeToBase64(self):
        auth = f"{self.user}:{self.secret}"
        #ENCODE TO BASE64 for Basic Authentication
        auth_original_bytes=auth.encode("utf-8")
        encode_auth=base64.b64encode(auth_original_bytes)
        return encode_auth.decode("utf-8")
    
    def getHeaders(self):
        encode_auth=self.encodeToBase64()
        headers={"Authorization": f"Basic {encode_auth}"}
        return headers
    
    def callApi(self, endpoint, method="GET", data=None):
        url = f"https://api.raixer.com{endpoint}"
        headers=self.getHeaders()

        if method.lower() == "get":
            response = requests.get(url, headers=headers)

        elif method.lower() == "post":
            response = requests.post(url, headers=headers, data=data)

        elif method.lower() == "put":
            response = requests.put(url, headers=headers, data=data)

        elif method.lower() == "delete":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"http method {method} not supported")
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()


#class saveOptions():



if __name__ == "__main__":

    def createData(**kwargs):
        data = {
            "deviceId":kwargs.get("deviceId"),
            "doorId":kwargs.get("doorId"),
            "phoneNumber":kwargs.get("phoneNumber"),
            "authorized":kwargs.get("authorized"),
            "alias":kwargs.get("alias")
        }
        return data
    
    raixer_api_user="carlosnfq"
    raixer_api_secret="s85tf83Xqj6vAyL96hjs8755ERqb6te"
    true=str(True).lower()
    false=str(False).lower()


    deviceId=""
    doorId=""

    raixer_api = RaixerApi(raixer_api_user, raixer_api_secret) 
    phone_api_url="https://api.raixer.com/authorized-phones/v2/"
    response = raixer_api.callApi(f"/authorized-phones/device/{deviceId}")
#Guardamos la respuesta de la api en un json llamado raixer.json
    with open("./raixer_authorized_phones.json", "w") as f:
        json.dump(response,f)

# Otras Opciones
    option = input(f"<== RAIXER ==>\n[1] Create\n[2] Delete\n[3] Update")

    if option == "1":
        phone=str(34333666777)
        raixer_api.callApi(f"/authorized-phones/v2",method="POST",data=createData(
                                                                                deviceId=deviceId, 
                                                                                doorId=doorId, 
                                                                                phoneNumber=int(phone), 
                                                                                authorized=False, 
                                                                                alias="testing"))
    if option == "2":
        phone=str(34333666777)
        for user in response:
            if user["phoneNumber"] == phone:
                print(user["phoneNumber"], user["_id"])
                raixer_api.callApi(f"/authorized-phones/v2/{user["_id"]}", method="DELETE")
                break
    
    if option == "3":
        phone=str(34333666777)
        alias="Testing444"
        found=False
        for user in response:
            if user["phoneNumber"] == phone:
                found=True
                phoneId=user["_id"]
                res=raixer_api.callApi(f"/authorized-phones/v2/{phoneId}",method="put",data=createData(
                                                                                deviceId=deviceId, 
                                                                                doorId=doorId, 
                                                                                phoneNumber=int(phone), 
                                                                                authorized=False, 
                                                                                alias="testing"))
            
        try:
            if found == False:
                res=raixer_api.callApi(f"/authorized-phones/v2",method="POST",data=createData(
                                                                                    deviceId=deviceId, 
                                                                                    doorId=doorId, 
                                                                                    phoneNumber=int(phone), 
                                                                                    authorized=false, 
                                                                                    alias=alias))
                print(res)
        except requests.exceptions.HTTPError as e:
                print(f"Ha ocurrido un error {e}")
