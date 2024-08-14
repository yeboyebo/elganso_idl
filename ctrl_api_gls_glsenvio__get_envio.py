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
    def start(self, data):
        if "IdCliente" not in data:
            data["IdCliente"] = "50914998-a78e-44ca-baba-230d03cde8ef"

        if "Servicio_GLS" not in data:
            data["Servicio_GLS"] = "76"

        if "Horario_GLS" not in data:
            data["Horario_GLS"] = "3"

        payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap12:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap12=\"http://www.w3.org/2003/05/soap-envelope\"><soap12:Body><GrabaServicios xmlns=\"http://www.asmred.com/\"><docIn><Servicios uidcliente=\"" + data["IdCliente"] + "\"><Envio codbarras=\"\"><Fecha>" + data["DatosServicio_Fecha"] + "</Fecha><Portes>P</Portes><Servicio>" + data["Servicio_GLS"] + "</Servicio><Horario>" + data["Horario_GLS"] + "</Horario><Bultos>1</Bultos><Peso>000000.620</Peso><Volumen>000000.011</Volumen><DNINomb>0</DNINomb><FechaPrevistaEntrega/><Retorno>0</Retorno><Pod>N</Pod><PODObligatorio>N</PODObligatorio><Aduanas><Incoterm></Incoterm></Aduanas><Remite><Nombre>" + data["DatosRecogida_Nombre"] + "</Nombre><Direccion>" + data["DatosRecogida_Direccion"] + "</Direccion><Poblacion>" + data["DatosRecogida_Poblacion"] + "</Poblacion><Provincia>" + data["DatosRecogida_Provincia"] + "</Provincia><Pais>" + data["DatosRecogida_Pais"] + "</Pais><CP>" + data["DatosRecogida_CodPostal"] + "</CP><NIF>" + data["DatosRecogida_CifNif"] + "</NIF><Telefono>" + data["DatosRecogida_Telefono"] + "</Telefono><Email>" + data["DatosRecogida_Email"] + "</Email><Movil/><Observaciones>" + data["DatosRecogida_Contacto"] + "</Observaciones></Remite><Destinatario><Nombre>" + data["DatosDestinatario_Nombre"] + "</Nombre><Direccion>" + data["DatosDestinatario_Direccion"] + "</Direccion><Poblacion>" + data["DatosDestinatario_Poblacion"] + "</Poblacion><Provincia>" + data["DatosDestinatario_Provincia"] + "</Provincia><Pais>" + data["DatosDestinatario_Pais"] + "</Pais><CP>" + data["DatosDestinatario_CodPostal"] + "</CP><Telefono>" + data["DatosDestinatario_Telefono"] + "</Telefono><Movil></Movil><ATT>" + data["DatosDestinatario_Nombre"] + "</ATT><NIF/></Destinatario><Referencias><Referencia tipo=\"C\">" + data["DatosCodigoOperacion"] + "</Referencia></Referencias><DevuelveAdicionales><Etiqueta tipo=\"PDF\"/></DevuelveAdicionales></Envio></Servicios></docIn></GrabaServicios></soap12:Body></soap12:Envelope>"
        print("XML de envio: ", str(payload))

        headers = {
          'Content-Type': 'text/xml; charset=utf-8'
        }

        #wsdl = 'https://wsclientes.asmred.com/b2b.asmx?op=TestGrabaServicios'
        wsdl = 'https://wsclientes.asmred.com/b2b.asmx?op=GrabaServicios'

        r = requests.request("POST", wsdl, headers=headers, data=payload)
       
        print(r.content)
        root = ET.fromstring(r.content)
        codigo_expedicion = ""
        etiPdf = ""
        for codresultado in root.iter('Resultado'):
            if str(codresultado.attrib["return"]) == "0":
                for codigoRecogida in root.iter('Envio'):
                    if len(codigoRecogida.attrib) >= 1:
                        codigo_expedicion = str(codigoRecogida.attrib["codexp"])
                        if codigo_expedicion == "" or codigo_expedicion == False:
                            return {"NumeroEnvio": "Error", "EtiquetaFile": "No se encuentrael código de expedición en la respuesta."}
                        for resultEtiqueta in root.iter('Etiqueta'):
                            ruta = codigo_expedicion + ".pdf"
                            file_result = open(ruta, 'wb') 
                            file_result.write(b64decode(resultEtiqueta.text, validate=True))
                            etiPdf = open(ruta, "rb").read()
                            etiPdf = str(base64.b64encode(etiPdf))
                            return {"NumeroEnvio": codigo_expedicion, "EtiquetaFile": str(etiPdf)[2:len(str(etiPdf))-1]}
                    else:
                        return {"NumeroEnvio": "Error", "EtiquetaFile": "No se encuentran los atributos en la respuesta"}
            else:
                return {"NumeroEnvio": "Error", "EtiquetaFile": str(codresultado.attrib["return"])}
        return {"NumeroEnvio": "Error", "EtiquetaFile": "No se ha podido obtener una respuesta."}

# @class_declaration revoke #
class get_envio(gls_postenviogls):
    pass
