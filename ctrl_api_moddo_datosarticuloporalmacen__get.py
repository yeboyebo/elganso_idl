import json

from django.http import HttpResponse

from models.flfactalma.articulos import articulos


# @class_declaration interna_revoke #
class interna_get():
    pass


# @class_declaration flsyncppal_revoke #
class moddo_datosarticuloporalmacen(interna_get):

    @staticmethod
    def start(pk, data):
        response = articulos.damedatosarticuloporalmacen(data)
        return HttpResponse(response, content_type="application/xml")


# @class_declaration revoke #
class get(moddo_datosarticuloporalmacen):
    pass
