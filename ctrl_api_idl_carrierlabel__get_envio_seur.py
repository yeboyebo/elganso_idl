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

    def start(self, data):
        print("entra en seur")
        return True
        """
        #url = data["Url_Token"]
        url = "https://servicios.apipre.seur.io/pic_token"
        #client_id = data["Client_Id"]
        client_id = "801318b4"
        client_secret = "b8ff0a3563b20754b12cef762db1495e"
        #client_secret = data["Client_Secret"]
        username = "XjfXpH3"
        password = "2AuJ9QyvD09W"

        payload = {
            'grant_type': "client_credentials",
            'client_id': client_id,
            'client_secret': client_secret
        }

        params = {
            'modal': 'true'
        }

        response = requests.post(url, data=payload)
       
        r = response.json()
        token_seur = ""
        if "access_token" in r:
            token_seur = r["access_token"]
            token_type = r["token_type"]
        print(token_seur)
        dataEnvio = {
            'serviceCode': "031",
            'productCode': "002",
            'customsGoodsCode': "C",
            'paymentType': "P",
            'sender': {
                'name': data["DatosRecogida_Nombre"],
                'ccc': data["ccc"],
                'idNumber': data["idNumber"]
            },
            'receiver': {
                'accountNumber': data["accountNumber"],
                'name': data["DatosDestinatario_Nombre"],
                'idNumber': data["idNumber"],
                'phone': data["DatosDestinatario_Telefono"],
                'contactName': data["DatosDestinatario_Nombre"],
                'email': data["DatosDestinatario_Email"],
                'address': {
                    'streetName': data["DatosDestinatario_Direccion"],
                    'cityName': data["DatosDestinatario_Poblacion"],
                    'postalCode': data["DatosDestinatario_CodPostal"],
                    'country': data["DatosDestinatario_Pais"],
                    #'pickupCentreCode': data["pickupCentreCode"]
                }
            },
            'date': data["DatosServicio_Fecha"],
            'reference': data["DatosCodigoOperacion"],
            #'observations': data["observations"],
            'parcels': [
                {
                    'weight': "10.2",
                    'width': "13",
                    'height': "4",
                    'length': "4",
                    'packReference': data["DatosCodigoOperacion"]
                }
            ]
        }
        print("Data envio" + str(dataEnvio))
        
        url = "https://servicios.apipre.seur.io/pic/v1/shipments"

        headers = {
            'Content-Type': "application/json;charset=UTF-8",
            'Authorization': token_type + " " + token_seur,
            'grant_type': "client_credentials",
            'client_id': client_id,
            'client_secret': client_secret
        }


        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Authorization": token_type + " " + token_seur
        }

        print(token_type + " " + token_seur)
        response = requests.post(url, headers=headers, json=dataEnvio)
        print(response.status_code)
        print(response.json())
        return True
        codRecogida = "047123000595220201228";
        url = "https://servicios.apiPRE.seur.io/pic/v1/labels?templateType=CUSTOM_REFERENCE&type=PDF&entity=SHIPMENTS&code=" + codRecogida
        data = {
        "token": tokenType + " " + token,
        "shipmentCode": codRecogida,
        "typeLabel": tipoEtiquetas
        }

        response = requests.post(url, data=payload)"""

# @class_declaration revoke #
class get_envio_seur(seur_postenvioseur):
    pass
