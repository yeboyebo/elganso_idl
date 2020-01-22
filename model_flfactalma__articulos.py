
# @class_declaration idl_articulos #
class elganso_idl_articulos(flfactalma_articulos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.csr()
    def dameprecioarticulo(params):
        return form.iface.dameprecioarticulo(params)

