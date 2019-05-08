# @class_declaration interna_idl_confirmacionpreparaciones #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactppal import models as modelos


class interna_idl_confirmacionpreparaciones(modelos.mtd_idl_confirmacionpreparaciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_idl_idl_confirmacionpreparaciones #
class elganso_idl_idl_confirmacionpreparaciones(interna_idl_confirmacionpreparaciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration idl_confirmacionpreparaciones #
class idl_confirmacionpreparaciones(elganso_idl_idl_confirmacionpreparaciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactppal.idl_confirmacionpreparaciones_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
