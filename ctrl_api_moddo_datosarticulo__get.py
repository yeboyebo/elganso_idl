import json

from django.http import HttpResponse

from models.flfactalma.articulos import articulos


# @class_declaration interna_revoke #
class interna_get():
    pass


# @class_declaration flsyncppal_revoke #
class moddo_datosarticulo(interna_get):

    @staticmethod
    def start(pk, data):
        # params = {}
        # params["key"] = data["Key"]
        # params["barcode"] = data["barcode"]
        # params["tienda"] = data["tienda"]
        response = articulos.damedatosarticulo(data)
        # print("_________________")
        # print(response)
        return HttpResponse(response, content_type="application/xml")


# @class_declaration revoke #
class get(moddo_datosarticulo):
    pass
