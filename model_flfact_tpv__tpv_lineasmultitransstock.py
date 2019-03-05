# @class_declaration interna_tpv_lineasmultitransstock #
import importlib

from YBUTILS.viewREST import helpers

from models.flfact_tpv import models as modelos


class interna_tpv_lineasmultitransstock(modelos.mtd_tpv_lineasmultitransstock, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_idl_tpv_lineasmultitransstock #
class elganso_idl_tpv_lineasmultitransstock(interna_tpv_lineasmultitransstock, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration tpv_lineasmultitransstock #
class tpv_lineasmultitransstock(elganso_idl_tpv_lineasmultitransstock, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfact_tpv.tpv_lineasmultitransstock_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
