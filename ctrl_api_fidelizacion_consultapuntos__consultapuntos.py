# @class_declaration interna #
from YBLEGACY import qsatype
from YBLEGACY.constantes import *
import time

# @class_declaration interna_revoke #
class interna_get():
    pass


# @class_declaration flsyncppal_revoke #
class eg_consultapuntos(interna_get):

    @staticmethod
    def start(self, data):
        try:
            # return {"Error": "Ahora no es posible realizar la consulta de puntos", "status": 0}
            # print("entro en consultapuntos: " + str(qsatype.Date()))
            if "passwd" in data and data["passwd"] == "bUqfqBMnoH":

                if "email" not in data:
                    return {"Error": "Formato Incorrecto", "status": 0}
                email = str(data['email']).lower()
                # print("saldo de consultapuntos: " + str(email))
                existe_tarjeta = qsatype.FLUtil.sqlSelect(u"tpv_tarjetaspuntos", u"codtarjetapuntos", ustr(u"lower(email) = '", email, u"'"))

                if not existe_tarjeta:
                    if qsatype.FLUtil.sqlSelect(u"eg_logtarjetasweb", u"email", ustr(u"lower(email) = '", email, u"'")):
                        if not qsatype.FLUtil.sqlSelect(u"eg_logtarjetasweb", "procesado", ustr(u"lower(email) = '", email, u"'")):
                            return {"Error": "Petición realizada, pendiente de creación", "status": 2}
                    return {"Error": "No se ha encontrado la tarjeta.", "status": 1}

                es_empleado = qsatype.FLUtil.sqlSelect(u"tpv_tarjetaspuntos", u"deempleado", ustr(u"lower(email) = '", email, u"' AND codtarjetapuntos = '", existe_tarjeta, u"'"))
                es_dtoespecial = qsatype.FLUtil.sqlSelect(u"tpv_tarjetaspuntos", u"dtoespecial", ustr(u"lower(email) = '", email, u"' AND codtarjetapuntos = '", existe_tarjeta, u"'"))
                dtopor = ""
                if es_dtoespecial:
                    dtopor = qsatype.FLUtil.sqlSelect(u"tpv_tarjetaspuntos", u"dtopor", ustr(u"lower(email) = '", email, u"' AND codtarjetapuntos = '", existe_tarjeta, u"'"))

                saldopuntos = qsatype.FLUtil.sqlSelect(u"tpv_tarjetaspuntos", u"ROUND(CAST(saldopuntos AS NUMERIC),2)", ustr(u"lower(email) = '", email, u"' AND codtarjetapuntos = '", existe_tarjeta, u"'"))
                
                # print("saldo de consultapuntos: " + str(qsatype.Date()))
                return {"saldoPuntos": saldopuntos, "email": email, "codtarjetapuntos": existe_tarjeta, "esempleado": es_empleado, "esdtoespecial": es_dtoespecial, "dtopor": dtopor}
            else:
                return {"Error": "Petición Incorrecta", "status": -1}
        except Exception as e:
            qsatype.debug(ustr(u"Error inesperado consulta de puntos: ", e))
            return {"Error": data, "status": -2}
        return False

# @class_declaration revoke #
class consultapuntos(eg_consultapuntos):
    pass
