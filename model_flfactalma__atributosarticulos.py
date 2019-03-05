# @class_declaration interna_atributosarticulos #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactalma import models as modelos


class interna_atributosarticulos(modelos.mtd_atributosarticulos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_idl_atributosarticulos #
class elganso_idl_atributosarticulos(interna_atributosarticulos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration atributosarticulos #
class atributosarticulos(elganso_idl_atributosarticulos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactalma.atributosarticulos_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
