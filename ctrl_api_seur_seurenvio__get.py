import base64
from base64 import b64decode
import os
import json

import requests
#import aspose.words as aw

import xml.etree.cElementTree as ET
from xml.etree.ElementTree import tostring
from django.http import HttpResponse

import xmltodict

# @class_declaration interna_revoke #
class interna_get():
    pass


# @class_declaration flsyncppal_revoke #
class seur_postenvioseur(interna_get):

    def start(self, dataws):

        url = dataws["Url_Token"]
        print("URL PRE: " + str(url))
        client_id = dataws["Client_Id"]
        client_secret = dataws["Client_Secret"]
        username = dataws["User_Name"]
        password = dataws["Password"]

        payload = {
            'grant_type': "password",
            'client_id': client_id,
            'client_secret': client_secret,
            'username': username,
            'password': password
        }

        headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'incap_ses_1777_2392811=kV4ReI/SrH2QcpgrmCypGPqejWkAAAAAdH37ZvKcVNh3tnX7N8RKdQ==; visid_incap_2392811=qKjeFPpyRNifBh2Q6ffYHgWd92gAAAAAQUIPAAAAAAAZGZ9Af8mxZkNW0WY0u+ej; 8a001cb98b95ca7ca8dee5d504821ceb=433f15149fb3e956ab217471b246a3fd; incap_ses_267_2392811=xz09Q7sUVEcYPLKTmpO0A62gjWkAAAAADUbzjYRVNEi0oil0cWyE7Q==; visid_incap_2392811=fGlA8qiqT0iXAytTvbyxmxAZ1WgAAAAAQUIPAAAAAADwQyK2btWKHwozntb2B4Y5; 8a001cb98b95ca7ca8dee5d504821ceb=433f15149fb3e956ab217471b246a3fd'
        }

        response = requests.post(url, headers=headers, data=payload)
        print(response.text)
        r = response.json()

        token_seur = ""
        token_type = ""
        if "access_token" in r:
            token_seur = r["access_token"]
            token_type = r["token_type"]

        if not token_seur or token_seur == "":
            return {"Error": "Error", "EtiquetaFile": "No se ha podido obtener etiqueta"}

        dataEnvio = {
            'serviceCode': "31",
            'productCode': "2",
            'customsGoodsCode': "C",
            'paymentType': "P",
            "eti": False,
            "eci": False,
            "dSat": False,
            'sender': {
                'name': dataws["sender_name"],
                'ccc': dataws["ccc"],
                'idNumber': dataws["idNumber"],
                "phone": "99999999",
                "contactName": "ATT_CLIE_ORI",
                "address":{
                "streetName": "DIRE_ORI",
                "postalCode": "19001",
                "country": "ES",
                "cityName": "GUADALAJARA"
                }
            },
            'receiver': {
                'name': dataws["name"],
                'idNumber': dataws["idNumber"],
                'phone': dataws["phone"],
                'contactName': dataws["name"],
                'email': dataws["email"],
                'address': {
                    'streetName': dataws["streetName"],
                    'cityName': dataws["cityName"],
                    'postalCode': dataws["postalCode"],
                    'country': dataws["country"]
                }
            },
            'date': dataws["date"],
            'reference': dataws["reference"],
            'observations': dataws["observations"],
            'parcels': [
                {
                    'weight': "10.2",
                    'width': "13",
                    'height': "4",
                    'length': "4",
                    'packReference': dataws["reference"]
                }
            ]
        }
        
        url = dataws["Url_Shipment"]
        print("URL SHIPMENT PRE: " + str(url))

        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": token_type + " " + token_seur
        }


        response = requests.post(url, headers=headers, json=dataEnvio)
        print(response.text)
        dataResponse = response.json()

        if "data" in dataResponse:
            print("entra")
            if "shipmentCode" in dataResponse["data"]:
                print(dataResponse["data"]["shipmentCode"])
                codRecogida = str(dataResponse["data"]["shipmentCode"])
                print("codRecogida: " + str(codRecogida))
                url = "https://servicios.apipre.seur.io/pic/v1/labels?code=" + str(codRecogida) + "&type=PDF&entity=SHIPMENTS"

                payload = {}
                headers = {
                    "Authorization": token_type + " " + token_seur,
                    "shipmentCode": codRecogida,
                    "typeLabel": "PDF"
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                print(response.text)
                dataResponse = response.json()
                if "data" in dataResponse:
                    if "pdf" in dataResponse["data"][0]:
                        ruta = codRecogida + ".pdf"
                        file_result = open(ruta, 'wb')    
                        file_result.write(b64decode(dataResponse["data"][0]["pdf"], validate=True))
                        file_result.close()
                        os.system('scp ' + ruta + ' root@api.elganso.com:/mnt/imgamazon/')
                        return {"NumeroEnvio": codRecogida, "EtiquetaFile": str(dataResponse["data"][0]["pdf"])}
        elif "errors" in dataResponse:
            return {"Error": str(dataResponse["errors"][0]["status"]), "EtiquetaFile": str(dataResponse["errors"][0]["detail"])}
        else:
            return {"Error": "Error", "EtiquetaFile": "No se ha podido obtener etiqueta"}



# @class_declaration revoke #
class get(seur_postenvioseur):
    pass
