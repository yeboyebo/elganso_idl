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
        print("entra en gls : ", data)
        if "DatosDestinatario_Email" not in data:
            data["DatosDestinatario_Email"] = ""
        
        if "Bultos" not in data:
            data["Bultos"] = "1"

        incotermGLS = ""
        if "Incoterm_GLS" in data:
            if str(data["Incoterm_GLS"]) != "None" and str(data["Incoterm_GLS"]) != "":
                incotermGLS = data["Incoterm_GLS"]

        observaciones = ""
        if "esParcelShop" in data:
            if data["esParcelShop"]:
                observaciones = "<Observaciones>" + data["obsParcelShop"] + "</Observaciones><Codigo>" + data["codParcelShop"] + "</Codigo>"

        """if "DatosDestinatario_Pais" in data:
            if data["DatosDestinatario_Pais"] == "NO":
                incotermGLS = "20"""

        payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap12:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap12=\"http://www.w3.org/2003/05/soap-envelope\"><soap12:Body><GrabaServicios xmlns=\"http://www.asmred.com/\"><docIn><Servicios uidcliente=\"" + data["IdCliente"] + "\"><Envio codbarras=\"\"><Fecha>" + data["DatosServicio_Fecha"] + "</Fecha><Portes>P</Portes><Servicio>" + data["Servicio_GLS"] + "</Servicio><Horario>" + data["Horario_GLS"] + "</Horario><Bultos>" + data["Bultos"] + "</Bultos><Peso>000000.620</Peso><Volumen>000000.011</Volumen><DNINomb>0</DNINomb><FechaPrevistaEntrega/><Retorno>0</Retorno><Pod>N</Pod><PODObligatorio>N</PODObligatorio><Aduanas><Incoterm>" + incotermGLS + "</Incoterm></Aduanas><Remite><Nombre>" + data["DatosRecogida_Nombre"] + "</Nombre><Direccion>" + data["DatosRecogida_Direccion"] + "</Direccion><Poblacion>" + data["DatosRecogida_Poblacion"] + "</Poblacion><Provincia>" + data["DatosRecogida_Provincia"] + "</Provincia><Pais>" + data["DatosRecogida_Pais"] + "</Pais><CP>" + data["DatosRecogida_CodPostal"] + "</CP><NIF>" + data["DatosRecogida_CifNif"] + "</NIF><Telefono>" + data["DatosRecogida_Telefono"] + "</Telefono><Movil>" + data["DatosRecogida_Telefono"] + "</Movil><Email>" + data["DatosRecogida_Email"] + "</Email><Observaciones>" + data["DatosCodPedido"] + " - " + data["DatosRecogida_Contacto"] + "</Observaciones></Remite><Destinatario><Nombre>" + data["DatosDestinatario_Nombre"] + "</Nombre><Direccion>" + data["DatosDestinatario_Direccion"] + "</Direccion><Poblacion>" + data["DatosDestinatario_Poblacion"] + "</Poblacion><Provincia>" + data["DatosDestinatario_Provincia"] + "</Provincia><Pais>" + data["DatosDestinatario_Pais"] + "</Pais><CP>" + data["DatosDestinatario_CodPostal"] + "</CP><Telefono>" + data["DatosDestinatario_Telefono"] + "</Telefono><Movil>" + data["DatosDestinatario_Telefono"] + "</Movil><Email>" + data["DatosDestinatario_Email"] + "</Email><ATT>" + data["DatosCodPedido"] + " - " +  data["DatosDestinatario_Nombre"] + "</ATT><NIF/>" + observaciones + "</Destinatario><Referencias><Referencia tipo=\"C\">" + data["DatosCodigoOperacion"] + "</Referencia></Referencias><DevuelveAdicionales><Etiqueta tipo=\"PDF\"/></DevuelveAdicionales></Envio></Servicios></docIn></GrabaServicios></soap12:Body></soap12:Envelope>"


        headers = {
          'Content-Type': 'text/xml; charset=utf-8'
        }

        #print(str(payload.encode("utf8")))
        
        wsdl = 'https://wsclientes.asmred.com/b2b.asmx?op=TestGrabaServicios'
        r = requests.request("POST", wsdl, headers=headers, data=payload)
        root = ET.fromstring(r.content)
        codigo_expedicion = ""
        etiPdf = ""
        for codresultado in root.iter('Resultado'):
            if str(codresultado.attrib["return"]) == "0":
                for codigoRecogida in root.iter('Envio'):
                    if len(codigoRecogida.attrib) >= 1:
                        codigo_expedicion = str(codigoRecogida.attrib["codexp"])
                        if codigo_expedicion == "" or codigo_expedicion == False:
                            return {"orderNumber": data["OrderNumberIDL"],"carrier": data["carrier"], "label": "", "error": True}
                        for resultEtiqueta in root.iter('Etiqueta'):
                            ruta = codigo_expedicion + ".pdf"
                            file_result = open(ruta, 'wb')
                            file_result.write(b64decode(resultEtiqueta.text, validate=True))
                            etiPdf = open(ruta, "rb").read()
                            etiPdf = str(base64.b64encode(etiPdf))
                            return {"orderNumber": data["OrderNumberIDL"],"carrier": data["carrier"], "label": str(etiPdf)[2:len(str(etiPdf))-1], "error": False}
                    else:
                        return {"orderNumber": data["OrderNumberIDL"],"carrier": data["carrier"], "label": "", "error": True}
            else:
                if str(codresultado.attrib["return"]) == "70" or str(codresultado.attrib["return"]) == "-70":
                    url = "http://www.asmred.com/websrvs/printserver.asmx"
                    codigo_recogida = data["DatosCodigoOperacion"]

                    payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap12:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap12=\"http://www.w3.org/2003/05/soap-envelope\"><soap12:Body><EtiquetaEnvio xmlns=\"http://www.asmred.com/\"><codigo>" + codigo_recogida + "</codigo><tipoEtiqueta>PDF</tipoEtiqueta></EtiquetaEnvio></soap12:Body></soap12:Envelope>"
                    headers = {
                        'Content-Type': 'text/xml; charset=utf-8'
                    }

                    r = requests.request("POST", url, headers=headers, data=payload)

                    root = ET.fromstring(r.content)
                    cuerpo_etiqueta = ""
                    for item in root.iter('{http://www.asmred.com/}base64Binary'):
                        cuerpo_etiqueta = item.text
                        ruta = codigo_recogida + ".pdf"
                        file_result = open(ruta, 'wb')
                        file_result.write(b64decode(cuerpo_etiqueta, validate=True))
                        etiPdf = open(ruta, "rb").read()
                        etiPdf = str(base64.b64encode(etiPdf))
                        return {"orderNumber": data["OrderNumberIDL"],"carrier": data["carrier"], "label": str(etiPdf)[2:len(str(etiPdf))-1], "error": False}
        return {"orderNumber": data["OrderNumberIDL"],"carrier": data["carrier"], "label": "", "error": True}

# @class_declaration revoke #
class get_envio(gls_postenviogls):
    pass
