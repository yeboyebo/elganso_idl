import base64
from base64 import b64decode
import os
import json

import requests
#import aspose.words as aw

from YBLEGACY import qsatype
from YBLEGACY.constantes import *

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
				"Name": data["DatosRecogida_Nombre"][0:35],
				"AttentionName": data["DatosRecogida_Nombre"][0:35],
				"TaxIdentificationNumber": "",
				"Phone": {
				  "Number": data["DatosRecogida_Telefono"],
				  "Extension": " "
				},
				"ShipperNumber": merchant_id,
				"FaxNumber": "",
				"Address": {
				  "AddressLine": [
					 data["DatosRecogida_Direccion"][0:35]
				  ],
				  "City": data["DatosRecogida_Poblacion"],
				  "StateProvinceCode": ups_postenvioups.get_provincia_ups(data["DatosRecogida_Provincia"]),
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
				  "StateProvinceCode": ups_postenvioups.get_provincia_ups(data["DatosDestinatario_Provincia"]),
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
				  "StateProvinceCode": ups_postenvioups.get_provincia_ups(data["DatosRecogida_Provincia"]),
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
				"Code": "PDF",
				"Description": "PDF"
			  },
			  "HTTPUserAgent": "Mozilla/4.5",
			  "LanguageCode": "esp"
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
		if "ShipmentResponse" in dataResponse:
			if "ShipmentResults" in dataResponse["ShipmentResponse"]:
				if "PackageResults" in dataResponse["ShipmentResponse"]["ShipmentResults"]:
					if "ShippingLabel" in dataResponse["ShipmentResponse"]["ShipmentResults"]["PackageResults"]:
						if "GraphicImage" in dataResponse["ShipmentResponse"]["ShipmentResults"]["PackageResults"]["ShippingLabel"]:
							cuerpo_etiqueta = dataResponse["ShipmentResponse"]["ShipmentResults"]["PackageResults"]["ShippingLabel"]["GraphicImage"]

		if cuerpo_etiqueta == "":
			return {"orderNumber": data["OrderNumberIDL"],"carrier": data["carrier"], "label": str(json.loads(response.text)), "error": True}

		codigo_recogida = data["DatosCodigoOperacion"]
		ruta = "/home/jesusz/" + codigo_recogida + ".pdf"
		file_result = open(ruta, 'wb')
		file_result.write(b64decode(cuerpo_etiqueta, validate=True))
		etiPdf = open(ruta, "rb").read()
		etiPdf = str(base64.b64encode(etiPdf))
		os.remove(ruta)
		return {"orderNumber": data["OrderNumberIDL"],"carrier": data["carrier"], "label": str(etiPdf)[2:len(str(etiPdf))-1], "error": False}

	@staticmethod
	def get_provincia_ups(provincia):

		provincias_ups = qsatype.FLUtil.sqlSelect(u"param_parametros", u"valor", ustr(u"nombre = 'PROVINCIAS_UPS'"))

		jUps = json.loads(str(provincias_ups))
		if "provincias" in jUps:
			for prov in jUps["provincias"]:
				nombre = prov["nombre"]
				if nombre.lower() == provincia.lower():
					codProvincia = prov["codigo"]

		return codProvincia

# @class_declaration revoke #
class get_envio_ups(ups_postenvioups):
	pass
