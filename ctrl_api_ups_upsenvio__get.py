import base64
from base64 import b64decode
import os
import json

import requests

import xml.etree.cElementTree as ET
from xml.etree.ElementTree import tostring
from django.http import HttpResponse

import xmltodict

# @class_declaration interna_revoke #
class interna_get():
    pass


# @class_declaration flsyncppal_revoke #
class gls_postenviogls(interna_get):

    @staticmethod
    def getTockenUps(self, data):
        url = "https://wwwcie.ups.com/security/v1/oauth/token"

        payload = {
          "grant_type": "client_credentials"
        }

        headers = {
          "Content-Type": "application/x-www-form-urlencoded",
          "x-merchant-id": "string"
        }

        response = requests.post(url, data=payload, headers=headers, auth=('<username>','<password>'))

        data = response.json()
        print(data)

    @staticmethod
    def start(self, data):
        print(self.getTockenUps(data))
        return True
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
              "Description": "Ship WS test",
              "Shipper": {
                "Name": "ShipperName",
                "AttentionName": "ShipperZs Attn Name",
                "TaxIdentificationNumber": "123456",
                "Phone": {
                  "Number": "1115554758",
                  "Extension": " "
                },
                "ShipperNumber": " ",
                "FaxNumber": "8002222222",
                "Address": {
                  "AddressLine": [
                    "2311 York Rd"
                  ],
                  "City": "Timonium",
                  "StateProvinceCode": "MD",
                  "PostalCode": "21093",
                  "CountryCode": "US"
                }
              },
              "ShipTo": {
                "Name": "Happy Dog Pet Supply",
                "AttentionName": "1160b_74",
                "Phone": {
                  "Number": "9225377171"
                },
                "Address": {
                  "AddressLine": [
                    "123 Main St"
                  ],
                  "City": "timonium",
                  "StateProvinceCode": "MD",
                  "PostalCode": "21030",
                  "CountryCode": "US"
                },
                "Residential": " "
              },
              "ShipFrom": {
                "Name": "T and T Designs",
                "AttentionName": "1160b_74",
                "Phone": {
                  "Number": "1234567890"
                },
                "FaxNumber": "1234567890",
                "Address": {
                  "AddressLine": [
                    "2311 York Rd"
                  ],
                  "City": "Alpharetta",
                  "StateProvinceCode": "GA",
                  "PostalCode": "30005",
                  "CountryCode": "US"
                }
              },
              "PaymentInformation": {
                "ShipmentCharge": {
                  "Type": "01",
                  "BillShipper": {
                    "AccountNumber": " "
                  }
                }
              },
              "Service": {
                "Code": "03",
                "Description": "Express"
              },
              "Package": {
                "Description": " ",
                "Packaging": {
                  "Code": "02",
                  "Description": "Nails"
                },
                "Dimensions": {
                  "UnitOfMeasurement": {
                    "Code": "IN",
                    "Description": "Inches"
                  },
                  "Length": "10",
                  "Width": "30",
                  "Height": "45"
                },
                "PackageWeight": {
                  "UnitOfMeasurement": {
                    "Code": "LBS",
                    "Description": "Pounds"
                  },
                  "Weight": "5"
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

    headers = {
      "Content-Type": "application/json",
      "transId": "string",
      "transactionSrc": "testing",
      "Authorization": "Bearer <YOUR_TOKEN_HERE>"
    }

    response = requests.post(url, json=payload, headers=headers, params=query)

    data = response.json()
    print(data)

# @class_declaration revoke #
class get(gls_postenviogls):
    pass
