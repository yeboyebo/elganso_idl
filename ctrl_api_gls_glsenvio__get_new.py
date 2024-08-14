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
        print("**************************** ea 0")
        if "IdCliente" not in data:
            data["IdCliente"] = "50914998-a78e-44ca-baba-230d03cde8ef"

        if "Servicio_GLS" not in data:
            data["Servicio_GLS"] = "76"

        if "Horario_GLS" not in data:
            data["Horario_GLS"] = "3"

        payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap12:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap12=\"http://www.w3.org/2003/05/soap-envelope\"><soap12:Body><GrabaServicios xmlns=\"http://www.asmred.com/\"><docIn><Servicios uidcliente=\"" + data["IdCliente"] + "\"><Recogida codrecogida=\"\"><Horarios><Fecha dia=\"" + data["DatosServicio_Fecha"] + "\"><Horario desde=\"10:00\" hasta=\"19:00\"/></Fecha></Horarios><RecogerEn><Nombre>" + data["DatosRecogida_Nombre"] + "</Nombre><Contacto>" + data["DatosRecogida_Contacto"] + "</Contacto><Direccion>" + data["DatosRecogida_Direccion"] + "</Direccion><Poblacion>" + data["DatosRecogida_Poblacion"] + "</Poblacion><Provincia>" + data["DatosRecogida_Provincia"] + "</Provincia><Pais>" + data["DatosRecogida_Pais"] + "</Pais><CP>" + data["DatosRecogida_CodPostal"] + "</CP><NIF>" + data["DatosRecogida_CifNif"] + "</NIF><Telefono>" + data["DatosRecogida_Telefono"] + "</Telefono><Email>" + data["DatosRecogida_Email"] + "</Email><Movil/></RecogerEn><Entregas><Envio><FechaPrevistaEntrega/><Portes>P</Portes><Servicio>" + data["Servicio_GLS"] + "</Servicio><Horario>" + data["Horario_GLS"] + "</Horario><PODObligatorio>N</PODObligatorio><Bultos>1</Bultos><Peso>1</Peso><Retorno>0</Retorno><Destinatario><Nombre>" + data["DatosDestinatario_Nombre"] + "</Nombre><Direccion>" + data["DatosDestinatario_Direccion"] + "</Direccion><Poblacion>" + data["DatosDestinatario_Poblacion"] + "</Poblacion><Provincia>" + data["DatosDestinatario_Provincia"] + "</Provincia><Pais>" + data["DatosDestinatario_Pais"] + "</Pais><CP>" + data["DatosDestinatario_CodPostal"] + "</CP><Telefono>" + data["DatosDestinatario_Telefono"] + "</Telefono><Movil/></Destinatario><Importes><Reembolso>0</Reembolso></Importes></Envio> </Entregas><Referencias><Referencia tipo=\"C\">" + data["DatosCodigoOperacion"] + "</Referencia> </Referencias></Recogida><Plataforma>API</Plataforma></Servicios></docIn></GrabaServicios></soap12:Body></soap12:Envelope>"
        print(str(payload))
        #print("**************************** ea OK")
        #return {"NumeroEnvio": "PRUEBA Numero Envio", "EtiquetaFile": "PRUEBA Etiqueta"}
        
        headers = {
          'Content-Type': 'text/xml; charset=utf-8'
        }

        wsdl = 'https://wsclientes.asmred.com/b2b.asmx?op=GrabaServicios'

        r = requests.request("POST", wsdl, headers=headers, data=payload)

        #print(r.content)
        root = ET.fromstring(r.content)
        codigo_recogida = ""
        error_respuesta = ""
        for codigoRecogida in root.iter('Recogida'):
            print(len(codigoRecogida.attrib))
            if len(codigoRecogida.attrib) == 1:
                codigo_recogida = str(codigoRecogida.attrib["codigo"])
            else:
                for erroresRespuesta in codigoRecogida.findall('Errores'):
                    error_respuesta = str(erroresRespuesta[0].text) 


        print("codigo recogida: " + codigo_recogida)
        print("error recogida:"+ error_respuesta)
        if codigo_recogida == "":
            if error_respuesta == "Referencia cliente duplicada":
                codigo_recogida = data["DatosCodigoOperacion"]
            else:
                return {"NumeroEnvio": "Error", "EtiquetaFile": str(error_respuesta)}

        url = "http://www.asmred.com/websrvs/printserver.asmx"

        payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap12:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap12=\"http://www.w3.org/2003/05/soap-envelope\"><soap12:Body><EtiquetaEnvio xmlns=\"http://www.asmred.com/\"><codigo>" + codigo_recogida + "</codigo><tipoEtiqueta>PDF</tipoEtiqueta></EtiquetaEnvio></soap12:Body></soap12:Envelope>"
        headers = {
          'Content-Type': 'text/xml; charset=utf-8'
        }

        r = requests.request("POST", url, headers=headers, data=payload)

        root = ET.fromstring(r.content)
        ruta = codigo_recogida + ".pdf"
        cuerpo_etiqueta = ""
        for item in root.iter('{http://www.asmred.com/}base64Binary'):
            cuerpo_etiqueta = item.text
            #print(cuerpo_etiqueta)
            file_result = open(ruta, 'wb') 
            file_result.write(b64decode(cuerpo_etiqueta, validate=True))

        etiPdf = open(ruta, "rb").read()
        etiPdf = str(base64.b64encode(etiPdf))
        #os.remove(ruta)
        print(str(codigo_recogida))
        #print(str(etiPdf))
        return {"NumeroEnvio": codigo_recogida, "EtiquetaFile": str(etiPdf)[2:len(str(etiPdf))-1]}

# @class_declaration revoke #
class get_new(gls_postenviogls):
    pass
