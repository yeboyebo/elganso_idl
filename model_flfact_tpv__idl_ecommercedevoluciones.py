# @class_declaration interna_idl_ecommercedevoluciones #
import importlib

from YBUTILS.viewREST import helpers

from models.flfact_tpv import models as modelos


class interna_idl_ecommercedevoluciones(modelos.mtd_idl_ecommercedevoluciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_idl_idl_ecommercedevoluciones #
class elganso_idl_idl_ecommercedevoluciones(interna_idl_ecommercedevoluciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration idl_ecommercedevoluciones #
class idl_ecommercedevoluciones(elganso_idl_idl_ecommercedevoluciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfact_tpv.idl_ecommercedevoluciones_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
