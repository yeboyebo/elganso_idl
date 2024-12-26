import base64
from base64 import b64decode

import requests

import xml.etree.cElementTree as ET
from xml.etree.ElementTree import tostring

# @class_declaration interna_revoke #
class interna_get():
    pass

# @class_declaration flsyncppal_revoke #
class gls_getetiquetagls(interna_get):

    @staticmethod
    def start(self, data):
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
            print(str(codigo_recogida))
            ruta = "/home/elganso/etiquetas/" + codigo_recogida + ".pdf"
            file_result = open(ruta, 'wb')    
            file_result.write(b64decode(cuerpo_etiqueta, validate=True))
            file_result.close()
            os.system('sshpass -p "2de01ad4" scp ' + ruta + ' root@api.elganso.com:/mnt/imgamazon/')

        if cuerpo_etiqueta == "":
            return {"NumeroEnvio": "Error", "EtiquetaFile": "No localizamos la etiqueta"}

        return {"NumeroEnvio": codigo_recogida, "EtiquetaFile": str(cuerpo_etiqueta)}

    

# @class_declaration revoke #
class get_etiqueta(gls_getetiquetagls):
    pass
