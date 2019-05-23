# @class_declaration interna_idl_confirmacionfaltantes #
import importlib

from YBUTILS.viewREST import helpers

from models.flfact_tpv import models as modelos


class interna_idl_confirmacionfaltantes(modelos.mtd_idl_confirmacionfaltantes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_idl_idl_confirmacionfaltantes #
class elganso_idl_idl_confirmacionfaltantes(interna_idl_confirmacionfaltantes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration idl_confirmacionfaltantes #
class idl_confirmacionfaltantes(elganso_idl_idl_confirmacionfaltantes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfact_tpv.idl_confirmacionfaltantes_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
