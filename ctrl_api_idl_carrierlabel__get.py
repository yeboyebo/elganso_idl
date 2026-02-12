import base64
from base64 import b64decode
import os
import json

from YBLEGACY import qsatype
from YBLEGACY.constantes import *

import requests

import xml.etree.cElementTree as ET
from xml.etree.ElementTree import tostring
from django.http import HttpResponse

import xmltodict

import datetime as dt


# @class_declaration interna_revoke #
class interna_get():
    pass


# @class_declaration flsyncppal_revoke #
class idl_carrierlabel(interna_get):

    @staticmethod
    def start(self, data):
        # Preguntar si el servicio y horario va a ir junto en el nodo "service".
        # El idClient de GLS para las devoluciones, ¿Es el mismo?
        # Cuando sea una devolución con UPS, necesitamos las credenciales, ya que cuando se envía, en el WS se necesita un ShipperNumber

        data = idl_carrierlabel.controlcaracteres(data)
        datos_idl = idl_carrierlabel.damedatosidl()

        codigo_pedido = str(data["orderNumber"])[1:]
        respuesta_ws = {}
        if str(data["carrier"]) == "GLS":
            datos_ws_gls = json.loads(str(qsatype.FLUtil.sqlSelect(u"param_parametros", u"valor", ustr(u"nombre = 'WS_IDL_GLS'"))))
            datosEnvio = idl_carrierlabel.damedatosenviogls(datos_idl, data, codigo_pedido)
            headers = {}
            r = requests.request("POST", datos_ws_gls["url_ws_ybyb_gls"], headers=headers, data=datosEnvio)
            respuesta_ws = r.content
        elif str(data["carrier"]) == "UPS":
            datosEnvio = idl_carrierlabel.damedatosenvioups(datos_idl, data, codigo_pedido)
            headers = {}
            r = requests.request("POST", datosEnvio["Url_Ws"], headers=headers, data=datosEnvio)
            respuesta_ws = r.content
        elif str(data["carrier"]) == "MRW":
            datos_ws_mrw = json.loads(str(qsatype.FLUtil.sqlSelect(u"param_parametros", u"valor", ustr(u"nombre = 'WS_IDL_MRW'"))))
            datosEnvio = idl_carrierlabel.damedatosenviomrw(datos_idl, data, codigo_pedido)
            headers = {}
            r = requests.request("POST", datos_ws_mrw["url_ws_ybyb_mrw"], headers=headers, data=datosEnvio)
            respuesta_ws = r.content
        elif str(data["carrier"]) == "SEUR":
            datos_ws_seur = json.loads(str(qsatype.FLUtil.sqlSelect(u"param_parametros", u"valor", ustr(u"nombre = 'WS_SEUR'"))))
            datosEnvio = idl_carrierlabel.damedatosenvioseur(datos_idl, data, codigo_pedido)
            headers = {}
            r = requests.request("POST", datos_ws_seur["url_ws_ybyb_seur"], headers=headers, data=datosEnvio)
            respuesta_ws = r.content
        
        try:
            idl_carrierlabel.guardarpeticion(respuesta_ws, data, codigo_pedido)
        except Exception as e:
           print(e)

        return json.loads(respuesta_ws.decode("utf-8"))

    @staticmethod
    def controlcaracteres(data):

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
        return data

    @staticmethod
    def damedatosidl():
        datos_idl = {}
        datos_idl["nombre"] = "TEST IDLogistic"
        datos_idl["direccion"] = qsatype.FLUtil.sqlSelect(u"almacenes", u"direccion", ustr(u"codalmacen = 'AWEB'"))
        datos_idl["ciudad"] = qsatype.FLUtil.sqlSelect(u"almacenes", u"poblacion", ustr(u"codalmacen = 'AWEB'"))
        datos_idl["provincia"] = qsatype.FLUtil.sqlSelect(u"almacenes", u"provincia", ustr(u"codalmacen = 'AWEB'"))
        datos_idl["pais"] = qsatype.FLUtil.sqlSelect(u"almacenes", u"codpais", ustr(u"codalmacen = 'AWEB'"))
        datos_idl["codpostal"] = qsatype.FLUtil.sqlSelect(u"almacenes", u"codpostal", ustr(u"codalmacen = 'AWEB'"))
        datos_idl["cifnif"] = ""
        datos_idl["telefono"] = qsatype.FLUtil.sqlSelect(u"almacenes", u"telefono", ustr(u"codalmacen = 'AWEB'"))
        datos_idl["email"] = qsatype.FLUtil.sqlSelect(u"almacenes", u"email", ustr(u"codalmacen = 'AWEB'"))
        return datos_idl

    @staticmethod
    def damedatosenviogls(datos_idl, data, codigo_pedido):
        datosEnvio = {
            "DatosRecogida_Nombre": datos_idl["nombre"],
            "DatosRecogida_Contacto": datos_idl["nombre"],
            "DatosRecogida_Direccion": datos_idl["direccion"],
            "DatosRecogida_Poblacion": datos_idl["ciudad"],
            "DatosRecogida_Provincia": datos_idl["provincia"],
            "DatosRecogida_Pais": datos_idl["pais"],
            "DatosRecogida_CodPostal": datos_idl["codpostal"],
            "DatosRecogida_CifNif": datos_idl["cifnif"],
            "DatosRecogida_Telefono": datos_idl["telefono"],
            "DatosRecogida_Email": datos_idl["email"],
            "DatosDestinatario_Nombre": data["deliveryName"],
            "DatosDestinatario_Direccion": data["deliveryAddress"],
            "DatosDestinatario_Poblacion": data["deliveryCity"],
            "DatosDestinatario_Provincia": data["deliveryProvince"],
            "DatosDestinatario_Pais": data["deliveryCountry"],
            "DatosDestinatario_CodPostal": data["deliveryZipcode"],
            "DatosDestinatario_Email": data["deliveryEmail"],
            "DatosDestinatario_Telefono": data["deliveryPhone"],
            "DatosServicio_Fecha": dt.date.today(),
            "DatosCodigoOperacion": "IDL" + codigo_pedido[4:] + codigo_pedido[:7],
            "DatosCodPedido": codigo_pedido,
            "IdCliente": "606aded3-54c8-43c9-a1e2-e7a24ec4a0d8",
            "Servicio_GLS": data["service"],
            "Horario_GLS": "",
            "Bultos": "1",
            "OrderNumberIDL": str(data["orderNumber"]),
            "carrier": str(data["carrier"]),
            "Retorno_GLS": "0"
        }
        if str(data["pickupReturn"]).lower() == "true":
            datosEnvio = {
                "DatosRecogida_Nombre": datos_idl["nombre"],
                "DatosRecogida_Contacto": datos_idl["nombre"],
                "DatosRecogida_Direccion": datos_idl["direccion"],
                "DatosRecogida_Poblacion": datos_idl["ciudad"],
                "DatosRecogida_Provincia": datos_idl["provincia"],
                "DatosRecogida_Pais": datos_idl["pais"],
                "DatosRecogida_CodPostal": datos_idl["codpostal"],
                "DatosRecogida_CifNif": datos_idl["cifnif"],
                "DatosRecogida_Telefono": datos_idl["telefono"],
                "DatosRecogida_Email": datos_idl["email"],
                "DatosDestinatario_Nombre": data["deliveryName"],
                "DatosDestinatario_Direccion": data["deliveryAddress"],
                "DatosDestinatario_Poblacion": data["deliveryCity"],
                "DatosDestinatario_Provincia": data["deliveryProvince"],
                "DatosDestinatario_Pais": data["deliveryCountry"],
                "DatosDestinatario_CodPostal": data["deliveryZipcode"],
                "DatosDestinatario_Email": data["deliveryEmail"],
                "DatosDestinatario_Telefono": data["deliveryPhone"],
                "DatosServicio_Fecha": dt.date.today(),
                "DatosCodigoOperacion": "IDL" + codigo_pedido[4:] + codigo_pedido[:7],
                "DatosCodPedido": codigo_pedido,
                "IdCliente": "606aded3-54c8-43c9-a1e2-e7a24ec4a0d8",
                "Servicio_GLS": data["service"],
                "Horario_GLS": "",
                "Bultos": "1",
                "OrderNumberIDL": str(data["orderNumber"]),
                "carrier": str(data["carrier"]),
                "Retorno_GLS": "1"
            }

        return datosEnvio

    @staticmethod
    def damedatosenvioups(datos_idl, data, codigo_pedido):

        credenciales_ups = qsatype.FLUtil.sqlSelect(u"param_parametros", u"valor", ustr(u"nombre = 'CREDENCIALES_UPS'"))

        jUps = json.loads(str(credenciales_ups))

        datosEnvio = {
            "Url_Token": jUps["url_token"],
            "Url_Etiqueta": jUps["url_etiqueta"],
            "Client_Id": jUps["client_id"],
            "Client_Secret": jUps["client_secret"],
            "Merchant_Id": jUps["merchant_id"],
            "Url_Ws": jUps["url_ws_ybyb_ups"],
            "DatosRecogida_Nombre": datos_idl["nombre"],
            "DatosRecogida_Contacto": datos_idl["nombre"],
            "DatosRecogida_Direccion": datos_idl["direccion"],
            "DatosRecogida_Poblacion": datos_idl["ciudad"],
            "DatosRecogida_Provincia": datos_idl["provincia"],
            "DatosRecogida_Pais": datos_idl["pais"],
            "DatosRecogida_CodPostal": datos_idl["codpostal"],
            "DatosRecogida_CifNif": datos_idl["cifnif"],
            "DatosRecogida_Telefono": datos_idl["telefono"],
            "DatosRecogida_Email": datos_idl["email"],
            "DatosDestinatario_Nombre": data["deliveryName"],
            "DatosDestinatario_Direccion": data["deliveryAddress"],
            "DatosDestinatario_Poblacion": data["deliveryCity"],
            "DatosDestinatario_Provincia": data["deliveryProvince"],
            "DatosDestinatario_Pais": data["deliveryCountry"],
            "DatosDestinatario_CodPostal": data["deliveryZipcode"],
            "DatosDestinatario_Email": data["deliveryEmail"],
            "DatosDestinatario_Telefono": data["deliveryPhone"],
            "DatosServicio_Fecha": dt.date.today(),
            "DatosCodigoOperacion": "IDL" + codigo_pedido[4:] + codigo_pedido[:7],
            "DatosCodPedido": codigo_pedido,
            "Bultos": "1",
            "OrderNumberIDL": str(data["orderNumber"]),
            "carrier": str(data["carrier"])
            }

        return datosEnvio

    @staticmethod
    def damedatosenviomrw(datos_idl, data, codigo_pedido):
        datosEnvio = {
            "UserName":"02666ELGANSO",
            "Password":"02666ELGANSO",
            "CodigoAbonado":"066413",
            "CodigoFranquicia":"02665",
            "DatosRecogida_Nombre": datos_idl["nombre"],
            "DatosRecogida_Contacto": datos_idl["nombre"],
            "DatosRecogida_Direccion": datos_idl["direccion"],
            "DatosRecogida_Poblacion": datos_idl["ciudad"],
            "DatosRecogida_Provincia": datos_idl["provincia"],
            "DatosRecogida_Pais": datos_idl["pais"],
            "DatosRecogida_CodPostal": datos_idl["codpostal"],
            "DatosRecogida_CifNif": datos_idl["cifnif"],
            "DatosRecogida_Telefono": datos_idl["telefono"],
            "DatosRecogida_Email": datos_idl["email"],
            "DatosDestinatario_Nombre": data["deliveryName"],
            "DatosDestinatario_Direccion": data["deliveryAddress"],
            "DatosDestinatario_Poblacion": data["deliveryCity"],
            "DatosDestinatario_Provincia": data["deliveryProvince"],
            "DatosDestinatario_Pais": data["deliveryCountry"],
            "DatosDestinatario_CodPostal": data["deliveryZipcode"],
            "DatosDestinatario_Email": data["deliveryEmail"],
            "DatosDestinatario_Telefono": data["deliveryPhone"],
            "DatosServicio_Fecha": dt.date.today(),
            "DatosServicio_Referencia": "IDL" + codigo_pedido[4:] + codigo_pedido[:7],
            "DatosCodPedido": codigo_pedido,
            "DatosServicio_EnFranquicia":"N",
            "DatosServicio_CodigoServicio":"0205",
            "DatosServicio_DescripcionServicio":"",
            "DatosServicio_Frecuencia":"1",
            "DatosServicio_Bultos_Referencia":"1",
            "DatosServicio_Bultos_Peso":"1",
            "DatosServicio_NumeroBultos":"1",
            "DatosServicio_Peso":"1",
            "DatosServicio_TipoMercancia":"BJV",
            "DatosServicio_ValorDeclarado":"10",
            "Bultos": "1",
            "OrderNumberIDL": str(data["orderNumber"]),
            "carrier": str(data["carrier"])
            }
        

        return datosEnvio

    @staticmethod
    def damedatosenvioseur(datos_idl, data, codigo_pedido):
        datosEnvio = {
            "DatosRecogida_Nombre": datos_idl["nombre"],
            "DatosRecogida_Contacto": datos_idl["nombre"],
            "DatosRecogida_Direccion": datos_idl["direccion"],
            "DatosRecogida_Poblacion": datos_idl["ciudad"],
            "DatosRecogida_Provincia": datos_idl["provincia"],
            "DatosRecogida_Pais": datos_idl["pais"],
            "DatosRecogida_CodPostal": datos_idl["codpostal"],
            "DatosRecogida_CifNif": datos_idl["cifnif"],
            "DatosRecogida_Telefono": datos_idl["telefono"],
            "DatosRecogida_Email": datos_idl["email"],
            "DatosDestinatario_Nombre": data["deliveryName"],
            "DatosDestinatario_Direccion": data["deliveryAddress"],
            "DatosDestinatario_Poblacion": data["deliveryCity"],
            "DatosDestinatario_Provincia": data["deliveryProvince"],
            "DatosDestinatario_Pais": data["deliveryCountry"],
            "DatosDestinatario_CodPostal": data["deliveryZipcode"],
            "DatosDestinatario_Email": data["deliveryEmail"],
            "DatosDestinatario_Telefono": data["deliveryPhone"],
            "DatosServicio_Fecha": dt.date.today(),
            "DatosCodigoOperacion": "IDL" + codigo_pedido[4:] + codigo_pedido[:7],
            "DatosCodPedido": codigo_pedido,
            "ccc": datos_idl["nombre"],
            "idNumber": datos_idl["nombre"],
            "accountNumber": datos_idl["nombre"]
        }
        if str(data["pickupReturn"]).lower() == "true":
            datosEnvio = {
                "DatosRecogida_Nombre": datos_idl["nombre"],
                "DatosRecogida_Contacto": datos_idl["nombre"],
                "DatosRecogida_Direccion": datos_idl["direccion"],
                "DatosRecogida_Poblacion": datos_idl["ciudad"],
                "DatosRecogida_Provincia": datos_idl["provincia"],
                "DatosRecogida_Pais": datos_idl["pais"],
                "DatosRecogida_CodPostal": datos_idl["codpostal"],
                "DatosRecogida_CifNif": datos_idl["cifnif"],
                "DatosRecogida_Telefono": datos_idl["telefono"],
                "DatosRecogida_Email": datos_idl["email"],
                "DatosDestinatario_Nombre": data["deliveryName"],
                "DatosDestinatario_Direccion": data["deliveryAddress"],
                "DatosDestinatario_Poblacion": data["deliveryCity"],
                "DatosDestinatario_Provincia": data["deliveryProvince"],
                "DatosDestinatario_Pais": data["deliveryCountry"],
                "DatosDestinatario_CodPostal": data["deliveryZipcode"],
                "DatosDestinatario_Email": data["deliveryEmail"],
                "DatosDestinatario_Telefono": data["deliveryPhone"],
                "DatosServicio_Fecha": dt.date.today(),
                "DatosCodigoOperacion": "IDL" + codigo_pedido[4:] + codigo_pedido[:7],
                "DatosCodPedido": codigo_pedido
            }

        return datosEnvio

    @staticmethod
    def guardarpeticion(respuesta_ws, data, codigo_pedido):
        fechaActual = qsatype.FactoriaModulos.get('flfactppal').iface.dameFechaActual()
        horaActual = qsatype.FactoriaModulos.get('flfactppal').iface.dameHoraActual()
        idecommerce = qsatype.FLUtil.sqlSelect(u"idl_ecommerce", u"id", ustr(u"codcomanda = '" + codigo_pedido + "'"))
        if not idecommerce or str(idecommerce) == "None":
            idecommerce = 1
        idtpv_comanda = qsatype.FLUtil.sqlSelect(u"tpv_comandas", u"idtpv_comanda", ustr(u"codigo = '" + codigo_pedido + "'"))
        if not idtpv_comanda or str(idtpv_comanda) == "None":
            idtpv_comanda = 1

        qsatype.FLSqlQuery().execSql("INSERT INTO eg_shippinglabel (transportista, idecommerce, idtpv_comanda, codcomanda, shippinglabel, peticionidl, respuestapeticion, fechapeticion, horapeticion) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(str(data["carrier"]), idecommerce, idtpv_comanda, str(codigo_pedido), str(json.loads(respuesta_ws.decode("utf-8"))["label"]), str(data).replace("'", "\""), str(respuesta_ws).replace("'", "\""), str(fechaActual), str(horaActual)))

        return True

# @class_declaration revoke #
class get(idl_carrierlabel):
    pass
