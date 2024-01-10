import base64
import os
import json
from zeep import Client
import base64

import xml.etree.cElementTree as ET
from xml.etree.ElementTree import tostring

from django.http import HttpResponse

# @class_declaration interna_revoke #
class interna_get():
    pass


# @class_declaration flsyncppal_revoke #
class mrw_postenviomrw(interna_get):

    @staticmethod
    def start(self, data):
        requestData = {
            'DatosRecogida':{
                'Direccion':{
                    'CodigoTipoVia': data["DatosRecogida_Direccion_CodigoTipoVia"],
                    'Via': data["DatosRecogida_Direccion_Via"],
                    'Numero': data["DatosRecogida_Direccion_Numero"],
                    'Resto': data["DatosRecogida_Direccion_Resto"],
                    'CodigoPostal': data["DatosRecogida_Direccion_CodigoPostal"],
                    'Poblacion': data["DatosRecogida_Direccion_Poblacion"],
                    'Provincia': data["DatosRecogida_Direccion_Provincia"]
                },
                'Nif': data["DatosRecogida_Nif"],
                'Nombre': data["DatosRecogida_Nombre"],
                'Telefono': data["DatosRecogida_Telefono"],
                'Contacto': data["DatosRecogida_Contacto"],
                'Observaciones': data["DatosRecogida_Observaciones"]
            },
            'DatosEntrega':{
                'Direccion':{
                    'CodigoTipoVia': data["DatosEntrega_Direccion_CodigoTipoVia"],
                    'Via': data["DatosEntrega_Direccion_Via"],
                    'Numero': data["DatosEntrega_Direccion_Numero"],
                    'Resto': data["DatosEntrega_Direccion_Resto"],
                    'CodigoPostal': data["DatosEntrega_Direccion_CodigoPostal"],
                    'Poblacion': data["DatosEntrega_Direccion_Poblacion"],
                    'Provincia': data["DatosEntrega_Direccion_Provincia"]
                },
                'Nif': data["DatosEntrega_Nif"],
                'Nombre': data["DatosEntrega_Nombre"],
                'Telefono': data["DatosEntrega_Telefono"],
                'Contacto': data["DatosEntrega_Contacto"],
                'ALaAtencionDe': data["DatosEntrega_ALaAtencionDe"],
                'Observaciones': data["DatosEntrega_Observaciones"]
            },
            'DatosServicio':{
                'Fecha': data["DatosServicio_Fecha"],
                'Referencia': data["DatosServicio_Referencia"],
                'EnFranquicia': data["DatosServicio_EnFranquicia"],
                'CodigoServicio': data["DatosServicio_CodigoServicio"],
                'DescripcionServicio': data["DatosServicio_DescripcionServicio"],
                'Frecuencia': data["DatosServicio_Frecuencia"],
                'Bultos':{
                    'Referencia': data["DatosServicio_Bultos_Referencia"],
                    'Peso': data["DatosServicio_Bultos_Peso"],
                },
                'NumeroBultos': data["DatosServicio_NumeroBultos"],
                'Peso': data["DatosServicio_Peso"],
                'TipoMercancia': data["DatosServicio_TipoMercancia"],
                'ValorDeclarado': data["DatosServicio_ValorDeclarado"]
            }
        }
        
        header_value = {
            'AuthInfo':{
                'UserName': data["UserName"],
                'Password': data["Password"],
                'CodigoAbonado': data["CodigoAbonado"],
                'CodigoFranquicia':data["CodigoFranquicia"]
            }
        }
        
        # print("_________________" , str(requestData))
        
        wsdl = 'http://sagec.mrw.es/MRWEnvio.asmx?wsdl'
        client = Client(wsdl)

        response = client.service.TransmEnvio(requestData, _soapheaders=header_value)
        
        if str(response.Estado) == 0:
            return {"Error": str(response.Mensaje)}
        
        numEnvio = response.NumeroEnvio
        
        requestData = {
            'NumeroEnvio': numEnvio,
            'NumerosEtiqueta': '',
            'SeparadorNumerosEnvio': '',
            'TipoEtiquetaEnvio': '0',
            'ReportTopMargin': '1100',
            'ReportLeftMargin': '650'
        }
        
        response = client.service.EtiquetaEnvio(requestData, _soapheaders=header_value)
        
        #node = client.create_message(client.service, 'EtiquetaEnvio', requestData, _soapheaders=header_value)
        #print(ET.tostring(node))
        
        ruta = numEnvio + ".pdf"
        file_result = open(ruta, 'wb') 
        file_result.write(response.EtiquetaFile)
        
        etiPdf = open(ruta, "rb").read()
        etiPdf = str(base64.b64encode(etiPdf))
        os.remove(ruta)
        print(str(numEnvio))
        print(str(etiPdf))
        
        return {"NumeroEnvio": numEnvio, "EtiquetaFile": str(etiPdf)[2:len(str(etiPdf))-1]}

# @class_declaration revoke #
class get(mrw_postenviomrw):
    pass
