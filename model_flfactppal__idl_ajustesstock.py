# @class_declaration interna_idl_ajustesstock #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactppal import models as modelos


class interna_idl_ajustesstock(modelos.mtd_idl_ajustesstock, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_idl_idl_ajustesstock #
class elganso_idl_idl_ajustesstock(interna_idl_ajustesstock, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration idl_ajustesstock #
class idl_ajustesstock(elganso_idl_idl_ajustesstock, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactppal.idl_ajustesstock_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
