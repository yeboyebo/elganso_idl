
# @class_declaration elganso_idl #
class elganso_idl(interna):

    def elganso_idl_guardadatospedidomagento(self, params):
        incrementId = ""
        status = ""
        json = ""

        try:
            if "key" in params and params['key'] == "34762d577d2c6132417e5e5e2f":

                if "json" in params:
                    json = params['json']
                else:
                    return "<?xml version='1.0' encoding='UTF-8'?><pedidos><error>No se pudo obtener el json</error></pedidos>"

                if not json or json == "":
                    return "<?xml version='1.0' encoding='UTF-8'?><pedidos><error>json vacío</error></pedidos>"

                if "increment_id" in json:
                    incrementId = json['increment_id']
                else:
                    return "<?xml version='1.0' encoding='UTF-8'?><pedidos><error>No se pudo obtener el increment_id</error></pedidos>"

                if "status" in json:
                    status = json['status']
                else:
                    return "<?xml version='1.0' encoding='UTF-8'?><pedidos><error>No se pudo obtener el status</error></pedidos>"

                if not incrementId or incrementId == "":
                    return "<?xml version='1.0' encoding='UTF-8'?><pedidos><error>increment_id vacío</error></pedidos>"

                if not status or status == "":
                    return "<?xml version='1.0' encoding='UTF-8'?><pedidos><error>status vacío</error></pedidos>"

                existePedido = qsatype.FLUtil.sqlSelect(u"eg_logpedidosweb", u"idlog", u"increment_id = '" + str(incrementId) + u"' AND estadomagento = '" + str(status) + u"'")
                if existePedido:
                    return "<?xml version='1.0' encoding='UTF-8'?><pedidos><ok>El pedido " + str(incrementId) + " ya está sincronizado</ok></pedidos>"

                now = str(qsatype.Date())
                fecha = now[:10]
                hora = now[-(8):]
                if not qsatype.FLUtil.sqlInsert("eg_logpedidosweb", ["increment_id", "estadomagento", "cuerpolog", "fechaalta", "horaalta"], [str(incrementId), str(status), str(json), fecha, hora]):
                    return "<?xml version='1.0' encoding='UTF-8'?><pedidos><error>No se pudo guardar el json</error></pedidos>"
            else:
                return "<?xml version='1.0' encoding='UTF-8'?><pedidos><error>Key incorrecta</error></pedidos>"

        except Exception as e:
            return "<?xml version='1.0' encoding='UTF-8'?><pedidos><error>Exception: " + e + "</error></pedidos>"

        return "<?xml version='1.0' encoding='UTF-8'?><pedidos><ok>Pedido guardado correctamente</ok></pedidos>"


    def __init__(self, context=None):
        super().__init__(context)


    def guardadatospedidomagento(self, params):
        return self.ctx.elganso_idl_guardadatospedidomagento(params)

