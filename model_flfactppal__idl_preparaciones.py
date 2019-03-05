# @class_declaration interna_idl_preparaciones #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactppal import models as modelos


class interna_idl_preparaciones(modelos.mtd_idl_preparaciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_idl_idl_preparaciones #
class elganso_idl_idl_preparaciones(interna_idl_preparaciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration idl_preparaciones #
class idl_preparaciones(elganso_idl_idl_preparaciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactppal.idl_preparaciones_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
