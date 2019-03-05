# @class_declaration interna_idl_recepciones #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactppal import models as modelos


class interna_idl_recepciones(modelos.mtd_idl_recepciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_idl_idl_recepciones #
class elganso_idl_idl_recepciones(interna_idl_recepciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration idl_recepciones #
class idl_recepciones(elganso_idl_idl_recepciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactppal.idl_recepciones_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
