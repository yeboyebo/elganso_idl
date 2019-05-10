# @class_declaration interna_idl_confirmacionrecepciones #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactppal import models as modelos


class interna_idl_confirmacionrecepciones(modelos.mtd_idl_confirmacionrecepciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_idl_idl_confirmacionrecepciones #
class elganso_idl_idl_confirmacionrecepciones(interna_idl_confirmacionrecepciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration idl_confirmacionrecepciones #
class idl_confirmacionrecepciones(elganso_idl_idl_confirmacionrecepciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactppal.idl_confirmacionrecepciones_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
