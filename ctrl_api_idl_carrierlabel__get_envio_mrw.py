import base64
import os
import json
from zeep import Client
import base64

import xml.etree.cElementTree as ET
from xml.etree.ElementTree import tostring

from django.http import HttpResponse

from YBLEGACY import qsatype
from YBLEGACY.constantes import *

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
                    'CodigoTipoVia': "",
                    'Via': data["DatosRecogida_Direccion"],
                    'Numero': "",
                    'Resto': "",
                    'CodigoPostal': data["DatosRecogida_CodPostal"],
                    'Poblacion': data["DatosRecogida_Poblacion"],
                    'Provincia': data["DatosRecogida_Provincia"]
                },
                'Nif': "",
                'Nombre': data["DatosRecogida_Nombre"],
                'Telefono': data["DatosRecogida_Telefono"],
                'Contacto': data["DatosRecogida_Contacto"],
                'Observaciones': ""
            },
            'DatosEntrega':{
                'Direccion':{
                    'CodigoTipoVia': "",
                    'Via': data["DatosDestinatario_Direccion"],
                    'Numero': "",
                    'Resto': "",
                    'CodigoPostal': data["DatosDestinatario_CodPostal"],
                    'Poblacion': data["DatosDestinatario_Poblacion"],
                    'Provincia': data["DatosDestinatario_Provincia"]
                },
                'Nif': "",
                'Nombre': data["DatosDestinatario_Nombre"],
                'Telefono': data["DatosDestinatario_Telefono"],
                'Contacto': data["DatosDestinatario_Email"],
                'ALaAtencionDe': "",
                'Observaciones': ""
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

        datos_ws_mrw = json.loads(str(qsatype.FLUtil.sqlSelect(u"param_parametros", u"valor", ustr(u"nombre = 'WS_IDL_MRW'"))))
        wsdl = datos_ws_mrw["url_ws_mrw"]
        client = Client(wsdl)

        response = client.service.TransmEnvio(requestData, _soapheaders=header_value)

        if str(response.Estado) == 0:
            return {"orderNumber": data["OrderNumberIDL"],"carrier": data["carrier"], "label": str(response.Mensaje), "error": True}
        
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

        ruta = numEnvio + ".pdf"
        file_result = open(ruta, 'wb') 
        file_result.write(response.EtiquetaFile)
        
        etiPdf = open(ruta, "rb").read()
        etiPdf = str(base64.b64encode(etiPdf))
        os.remove(ruta)
        print(str(numEnvio))
        print(str(etiPdf))
        return {"orderNumber": data["OrderNumberIDL"],"carrier": data["carrier"], "label": str(etiPdf)[2:len(str(etiPdf))-1], "error": False}

# @class_declaration revoke #
class get_envio_mrw(mrw_postenviomrw):
    pass
