
# @class_declaration idl_articulos #
class elganso_idl_articulos(flfactalma_articulos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.csr()
    def damedatosarticulo(params):
        return form.iface.damedatosarticulo(params)

    @helpers.decoradores.csr()
    def damearticulos(params):
        return form.iface.damearticulos(params)

    @helpers.decoradores.csr()
    def damedatosarticulos(params):
        return form.iface.damedatosarticulos(params)

    @helpers.decoradores.csr()
    def damedatosarticuloporalmacen(params):
        return form.iface.damedatosarticuloporalmacen(params)

    @helpers.decoradores.csr()
    def damedatostiendas(params):
        return form.iface.damedatostiendas(params)

