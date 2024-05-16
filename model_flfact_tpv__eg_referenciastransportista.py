# @class_declaration interna_eg_referenciastransportista #
import importlib

from YBUTILS.viewREST import helpers

from models.flfact_tpv import models as modelos


class interna_eg_referenciastransportista(modelos.mtd_eg_referenciastransportista, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration elganso_idl_eg_referenciastransportista #
class elganso_idl_eg_referenciastransportista(interna_eg_referenciastransportista, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration eg_referenciastransportista #
class eg_referenciastransportista(elganso_idl_eg_referenciastransportista, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfact_tpv.eg_referenciastransportista_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
