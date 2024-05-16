# @class_declaration interna_eg_seguimientoenvios #
import importlib

from YBUTILS.viewREST import helpers

from models.flfact_tpv import models as modelos


class interna_eg_seguimientoenvios(modelos.mtd_eg_seguimientoenvios, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_idl_eg_seguimientoenvios #
class elganso_idl_eg_seguimientoenvios(interna_eg_seguimientoenvios, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration eg_seguimientoenvios #
class eg_seguimientoenvios(elganso_idl_eg_seguimientoenvios, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfact_tpv.eg_seguimientoenvios_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
