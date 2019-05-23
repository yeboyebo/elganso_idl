# @class_declaration interna_idl_ecommerce #
import importlib

from YBUTILS.viewREST import helpers

from models.flfact_tpv import models as modelos


class interna_idl_ecommerce(modelos.mtd_idl_ecommerce, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_idl_idl_ecommerce #
class elganso_idl_idl_ecommerce(interna_idl_ecommerce, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration idl_ecommerce #
class idl_ecommerce(elganso_idl_idl_ecommerce, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfact_tpv.idl_ecommerce_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
