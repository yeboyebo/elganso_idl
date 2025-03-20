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
        print(data)

        oCaracteres = {}
        oCaracteres["Á"] = "A"
        oCaracteres["É"] = "E"
        oCaracteres["Í"] = "I"
        oCaracteres["Ó"] = "O"
        oCaracteres["Ú"] = "U"
        oCaracteres["á"] = "a"
        oCaracteres["é"] = "e"
        oCaracteres["í"] = "i"
        oCaracteres["ó"] = "o"
        oCaracteres["ú"] = "u"
        oCaracteres["ñ"] = "n"
        oCaracteres["Ñ"] = "N"
        oCaracteres["À"] = "A"
        oCaracteres["È"] = "E"
        oCaracteres["Ì"] = "I"
        oCaracteres["Ò"] = "O"
        oCaracteres["Ù"] = "U"
        oCaracteres["à"] = "a"
        oCaracteres["è"] = "e"
        oCaracteres["ì"] = "i"
        oCaracteres["ò"] = "o"
        oCaracteres["ù"] = "u"
        oCaracteres["Â"] = "A"
        oCaracteres["Ê"] = "E"
        oCaracteres["Î"] = "I"
        oCaracteres["Ô"] = "O"
        oCaracteres["Û"] = "U"
        oCaracteres["â"] = "a"
        oCaracteres["ê"] = "e"
        oCaracteres["î"] = "i"
        oCaracteres["ô"] = "o"
        oCaracteres["û"] = "u"
        oCaracteres["Ä"] = "A"
        oCaracteres["Ë"] = "E"
        oCaracteres["Ï"] = "I"
        oCaracteres["Ö"] = "O"
        oCaracteres["Ü"] = "U"
        oCaracteres["ä"] = "a"
        oCaracteres["ë"] = "e"
        oCaracteres["ï"] = "i"
        oCaracteres["ö"] = "o"
        oCaracteres["ü"] = "u"
        oCaracteres["ü"] = "u"
        oCaracteres["ç"] = "c"
        oCaracteres["Ç"] = "C"
        oCaracteres[";"] = ""
        oCaracteres["'"] = ""
        oCaracteres[","] = ""
        oCaracteres["\""] = ""
        oCaracteres["\r\n"] = " "
        oCaracteres["\r"] = " "
        oCaracteres["\n"] = " "
        oCaracteres["\t"] = " "

        for datos in data:
            for c in oCaracteres:
                cadena = str(data[datos])
                cadena = cadena.replace(c, oCaracteres[c])
                data[datos] = cadena

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

        payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap12:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap12=\"http://www.w3.org/2003/05/soap-envelope\"><soap12:Body><GrabaServicios xmlns=\"http://www.asmred.com/\"><docIn><Servicios uidcliente=\"" + data["IdCliente"] + "\"><Envio codbarras=\"\"><Fecha>" + data["DatosServicio_Fecha"] + "</Fecha><Portes>P</Portes><Servicio>" + data["Servicio_GLS"] + "</Servicio><Horario>" + data["Horario_GLS"] + "</Horario><Bultos>" + data["Bultos"] + "</Bultos><Peso>000000.620</Peso><Volumen>000000.011</Volumen><DNINomb>0</DNINomb><FechaPrevistaEntrega/><Retorno>0</Retorno><Pod>N</Pod><PODObligatorio>N</PODObligatorio><Aduanas><Incoterm>" + incotermGLS + "</Incoterm></Aduanas><Remite><Nombre>" + data["DatosRecogida_Nombre"] + "</Nombre><Direccion>" + data["DatosRecogida_Direccion"] + "</Direccion><Poblacion>" + data["DatosRecogida_Poblacion"] + "</Poblacion><Provincia>" + data["DatosRecogida_Provincia"] + "</Provincia><Pais>" + data["DatosRecogida_Pais"] + "</Pais><CP>" + data["DatosRecogida_CodPostal"] + "</CP><NIF>" + data["DatosRecogida_CifNif"] + "</NIF><Telefono>" + data["DatosRecogida_Telefono"] + "</Telefono><Movil>" + data["DatosRecogida_Telefono"] + "</Movil><Email>" + data["DatosRecogida_Email"] + "</Email><Observaciones>" + data["DatosCodPedido"] + " - " + data["DatosRecogida_Contacto"] + "</Observaciones></Remite><Destinatario><Nombre>" + data["DatosDestinatario_Nombre"] + "</Nombre><Direccion>" + data["DatosDestinatario_Direccion"] + "</Direccion><Poblacion>" + data["DatosDestinatario_Poblacion"] + "</Poblacion><Provincia>" + data["DatosDestinatario_Provincia"] + "</Provincia><Pais>" + data["DatosDestinatario_Pais"] + "</Pais><CP>" + data["DatosDestinatario_CodPostal"] + "</CP><Telefono>" + data["DatosDestinatario_Telefono"] + "</Telefono><Movil>" + data["DatosDestinatario_Telefono"] + "</Movil><Email>" + data["DatosDestinatario_Email"] + "</Email><ATT>" + data["DatosCodPedido"] + " - " +  data["DatosDestinatario_Nombre"] + "</ATT><NIF/>" + observaciones + "</Destinatario><Referencias><Referencia tipo=\"C\">" + data["DatosCodigoOperacion"] + "</Referencia></Referencias><DevuelveAdicionales><Etiqueta tipo=\"PDF\"/></DevuelveAdicionales></Envio></Servicios></docIn></GrabaServicios></soap12:Body></soap12:Envelope>"
        #print(str(payload))

        headers = {
          'Content-Type': 'text/xml; charset=utf-8'
        }

        print(str(payload.encode("utf8")))
        wsdl = 'https://wsclientes.asmred.com/b2b.asmx?op=GrabaServicios'

        r = requests.request("POST", wsdl, headers=headers, data=payload)

        print(str(r.content))
       
        root = ET.fromstring(r.content)
        codigo_expedicion = ""
        etiPdf = ""
        for codresultado in root.iter('Resultado'):
            if str(codresultado.attrib["return"]) == "0":
                for codigoRecogida in root.iter('Envio'):
                    if len(codigoRecogida.attrib) >= 1:
                        codigo_expedicion = str(codigoRecogida.attrib["codexp"])
                        if codigo_expedicion == "" or codigo_expedicion == False:
                            return {"NumeroEnvio": "Error", "EtiquetaFile": "No se encuentra el código de expedición en la respuesta."}
                        for resultEtiqueta in root.iter('Etiqueta'):
                            ruta = codigo_expedicion + ".pdf"
                            file_result = open(ruta, 'wb')
                            file_result.write(b64decode(resultEtiqueta.text, validate=True))
                            os.system('scp ' + ruta + ' root@api.elganso.com:/mnt/imgamazon/')
                            return {"NumeroEnvio": codigo_expedicion, "EtiquetaFile": str(resultEtiqueta.text)}
                    else:
                        return {"NumeroEnvio": "Error", "EtiquetaFile": "No se encuentran los atributos en la respuesta"}
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
                        os.system('scp ' + ruta + ' root@api.elganso.com:/mnt/imgamazon/')
                    return {"NumeroEnvio": codigo_recogida, "EtiquetaFile": str(cuerpo_etiqueta)}

                return {"NumeroEnvio": "Error", "EtiquetaFile": str(codresultado.attrib["return"])}
        return {"NumeroEnvio": "Error", "EtiquetaFile": "No se ha podido obtener una respuesta."}

# @class_declaration revoke #
class get_envio(gls_postenviogls):
    pass
