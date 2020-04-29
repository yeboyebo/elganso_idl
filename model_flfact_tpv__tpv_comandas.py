
# @class_declaration elganso_idl_tpv_comandas #
class elganso_idl_tpv_comandas(interna_tpv_comandas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.csr()
    def guardaDatosPedidoMagento(params):
        print(params)
        return form.iface.guardaDatosPedidoMagento(params)

