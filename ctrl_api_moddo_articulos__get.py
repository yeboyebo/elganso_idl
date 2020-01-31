import json

from django.http import HttpResponse

from models.flfactalma.articulos import articulos


# @class_declaration interna_revoke #
class interna_get():
    pass


# @class_declaration flsyncppal_revoke #
class moddo_articulos(interna_get):

    @staticmethod
    def start(pk, data):
        # params = {}
        # params["key"] = data["key"]
        response = articulos.damearticulos(data)
        # print("_________________")
        # print(response)
        return HttpResponse(response, content_type="application/xml")


# @class_declaration revoke #
class get(moddo_articulos):
    pass
