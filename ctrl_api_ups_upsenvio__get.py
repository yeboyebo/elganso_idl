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
class ups_postenvioups(interna_get):

    def start(self, data):
        url = data["Url_Token"]
        client_id = data["Client_Id"]
        client_secret = data["Client_Secret"]
        merchant_id = data["Merchant_Id"]
        accountName = "ACTURUS CAPITAL, S.L."
        if data["DatosRecogida_Pais"] == "FR":
            merchant_id = "R77R81"
            accountName = "ACTURUS FRANCE SAS"


        payload = "grant_type=client_credentials"

        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'x-merchant-id': merchant_id
        }

        response = requests.post(url, data=payload, headers=headers, auth=(client_id,client_secret))

        r = response.json()
        token_ups = ""
        if "access_token" in r:
            token_ups = r["access_token"]

        payload = {
          "ShipmentRequest": {
            "Request": {
              "SubVersion": "1801",
              "RequestOption": "nonvalidate",
              "TransactionReference": {
                "CustomerContext": ""
              }
            },
            "Shipment": {
              "Description": "Ship WS",
              "Shipper": {
                "Name": accountName,
                "AttentionName": "Logistica El Ganso",
                "TaxIdentificationNumber": "",
                "Phone": {
                  "Number": "916326464",
                  "Extension": " "
                },
                "ShipperNumber": merchant_id,
                "FaxNumber": "",
                "Address": {
                  "AddressLine": [
                     data["DatosRecogida_Direccion"][0:35]
                  ],
                  "City": data["DatosRecogida_Poblacion"],
                  "StateProvinceCode": data["DatosRecogida_Provincia"],
                  "PostalCode": data["DatosRecogida_CodPostal"],
                  "CountryCode": data["DatosRecogida_Pais"]
                }
              },
              "ShipTo": {
                "Name": data["DatosDestinatario_Nombre"][0:35],
                "AttentionName": data["DatosDestinatario_Nombre"][0:35],
                "Phone": {
                  "Number": data["DatosDestinatario_Telefono"]
                },
                "Address": {
                  "AddressLine": [
                    data["DatosDestinatario_Direccion"][0:35]
                  ],
                  "City": data["DatosDestinatario_Poblacion"],
                  "StateProvinceCode": data["DatosDestinatario_Provincia"],
                  "PostalCode": data["DatosDestinatario_CodPostal"],
                  "CountryCode": data["DatosDestinatario_Pais"]
                },
                "Residential": " "
              },
              "ShipFrom": {
                "Name": data["DatosRecogida_Nombre"],
                "AttentionName": data["DatosRecogida_Contacto"],
                "Phone": {
                  "Number": data["DatosRecogida_Telefono"]
                },
                "FaxNumber": "",
                "Address": {
                  "AddressLine": [
                    data["DatosRecogida_Direccion"]
                  ],
                  "City": data["DatosRecogida_Poblacion"],
                  "StateProvinceCode": data["DatosRecogida_Provincia"],
                  "PostalCode": data["DatosRecogida_CodPostal"],
                  "CountryCode": data["DatosRecogida_Pais"]
                }
              },
              "PaymentInformation": {
                "ShipmentCharge": {
                  "Type": "01",
                  "BillShipper": {"AccountNumber": merchant_id}
                }
              },
              "ReferenceNumber": {
                "Value": data["DatosCodigoOperacion"]
              },
              "Service": {
                "Code": "65",
                "Description": "UPS Saver"
              },
              "Package": {
                "Description": " ",
                "Packaging": {
                  "Code": "02",
                  "Description": "Customer Supplied"
                },
                "PackageWeight": {
                  "UnitOfMeasurement": {
                    "Code": "KGS",
                    "Description": ""
                  },
                  "Weight": "1"
                }
              }
            },
            "LabelSpecification": {
              "LabelImageFormat": {
                "Code": "GIF",
                "Description": "GIF"
              },
              "HTTPUserAgent": "Mozilla/4.5"
            }
          }
        }

        if data["DatosRecogida_Pais"] == "FR":
            payload["ShipmentRequest"]["Shipment"]["PaymentInformation"] = {
                "ShipmentCharge": {
                    "Type": "01",
                    "BillThirdParty": {
                        "AccountNumber": data["Merchant_Id"],
                        "Address":{
                            "PostalCode":"28660",
                            "CountryCode": "ES"
                        }
                    }
                }
            }

        aPaisesUE = ['AT','BE','BG','CZ','DE','DK','EE','FI','FR','GB','GG','GR','HR','HU','IE','IT','JE','LI','LT','LU','LV','MC','NL','NO','PL','PT','RO','SE','SI','SK','SM','ES']

        for pais in aPaisesUE:
            if data["DatosDestinatario_Pais"] == pais:
                print(str(pais))
                payload["ShipmentRequest"]["Shipment"]["Service"] = {
                    "Code": "11",
                    "Description": "UPS Standard"
                }

        print(str(json.dumps(payload)))

        headers = {
          "Content-Type": "application/json",
          "transId": "string",
          "transactionSrc": "testing",
          "Authorization": "Bearer " + token_ups
        }

        url = data["Url_Etiqueta"]
        response = requests.post(url, json=payload, headers=headers)
        
        cuerpo_etiqueta = ""
        dataResponse = response.json()
        print(str(response.text))
        if "ShipmentResponse" in dataResponse:
            if "ShipmentResults" in dataResponse["ShipmentResponse"]:
                if "PackageResults" in dataResponse["ShipmentResponse"]["ShipmentResults"]:
                    if "ShippingLabel" in dataResponse["ShipmentResponse"]["ShipmentResults"]["PackageResults"]:
                        if "GraphicImage" in dataResponse["ShipmentResponse"]["ShipmentResults"]["PackageResults"]["ShippingLabel"]:
                            cuerpo_etiqueta = dataResponse["ShipmentResponse"]["ShipmentResults"]["PackageResults"]["ShippingLabel"]["GraphicImage"] 
        print(cuerpo_etiqueta)

        if cuerpo_etiqueta == "":
            return {"NumeroEnvio": "Error", "EtiquetaFile": str(response.text)}

        codigo_recogida = data["DatosCodigoOperacion"]
        print(str(codigo_recogida))
        ruta = "/home/elganso/etiquetas/" + codigo_recogida + ".gif"
        file_result = open(ruta, 'wb')    
        file_result.write(b64decode(cuerpo_etiqueta, validate=True))
        file_result.close()
        os.system('sshpass -p "2de01ad4" scp ' + ruta + ' root@api.elganso.com:/mnt/imgamazon/')

        return {"NumeroEnvio": codigo_recogida, "EtiquetaFile": str(cuerpo_etiqueta)}

# @class_declaration revoke #
class get(ups_postenvioups):
    pass
