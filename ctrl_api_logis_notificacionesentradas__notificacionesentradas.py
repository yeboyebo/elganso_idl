# @class_declaration interna #
from YBLEGACY import qsatype
import time

# @class_declaration interna_revoke #
class interna_get():
    pass


# @class_declaration flsyncppal_revoke #
class eg_notificacionesentradas(interna_get):

    @staticmethod
    def start(self, params):
        res = []
        res.append("OK")
        res.append("")

        documento = ""
        codDoc = ""
        notificacion = ""
        doc = ""
        estadonotificacion = ""
        # {"source": "yeboyebo", "Content-Type": "application/xml", "key": "34762d577d2c6132417e5e5e2f"}
        print(str(params))
        try:
            if "key" in params and params['key'] == "34762d577d2c6132417e5e5e2f":
                if "notificacion" in params and params['notificacion'] != "":
                    notificacion = params['notificacion']
                    documento = params['notificacion']['poNumber']
                    estadonotificacion = params['notificacion']['inboundStatus']
                    if documento and str(documento) != "":
                        existe_registro_notificacion = qsatype.FLUtil.sqlSelect("eg_notificacionesentradaslogis", "documentos", "documentos = '" + str(documento) + "' AND estadonotificacion = '" + estadonotificacion + "'")
                        if existe_registro_notificacion and str(existe_registro_notificacion) != "":
                            res[0] = "KO"
                            if res[1] != "":
                                res[1] += " "
                            res[1] += "Ya existe una notificacion para la entrada " + documento + " con el estado " + estadonotificacion

                        existe_viaje = qsatype.FLUtil.sqlSelect("tpv_viajesmultitransstock", "idviajemultitrans", "idviajemultitrans = '" + str(documento) + "'")

                        if not existe_viaje or str(existe_viaje) == "":
                            res[0] = "KO"
                            if res[1] != "":
                                res[1] += " "
                            res[1] += "No existe el viaje " + documento + " en la Base de Datos."
                            for lines in params['notificacion']['lines']:
                                existe_linea_viaje = qsatype.FLUtil.sqlSelect("tpv_lineasmultitransstock", "idlinea", "idviajemultitrans = '" + str(documento) + "' AND barcode = '" + lines["sku"] + "'")
                                print(str(existe_linea_viaje))
                                if not existe_linea_viaje or str(existe_linea_viaje) == "":
                                    res[0] = "KO"
                                    if res[1] != "":
                                        res[1] += " "
                                    res[1] += "No existe la línea con el SKU " + lines["sku"] + " en el viaje " + documento
                    else:
                        res[0] = "KO"
                        if res[1] != "":
                            res[1] += " "
                        res[1] += "El nodo poNumber está vacío."
                else:
                    res[0] = "KO"
                    if res[1] != "":
                        res[1] += " "
                    res[1] += "No se ha encontrado el JSON de la notificacion de entrada."
            else:
                res[0] = "KO"
                if res[1] != "":
                    res[1] += " "
                res[1] += "key inválida"
        except Exception as e:
            res[0] = "KO"
            if res[1] != "":
                res[1] += " "
            res[1] += "Error: " + str(e)

        
        fechaActual = qsatype.FactoriaModulos.get('flfactppal').iface.dameFechaActual()
        horaActual = qsatype.FactoriaModulos.get('flfactppal').iface.dameHoraActual()
        procesar = "true"
        estado = "true"
        if res[0] == "KO":
            procesar = "false"
            estado = "false"

        cuerpolog = str(notificacion)
        print(str(cuerpolog))
        
        cuerpolog = cuerpolog.replace("None", "\"None\"")
        cuerpolog = cuerpolog.replace("{'", "{\"")
        cuerpolog = cuerpolog.replace("'}", "\"}")
        cuerpolog = cuerpolog.replace("':", "\":")
        cuerpolog = cuerpolog.replace(": '", ": \"")
        cuerpolog = cuerpolog.replace(", '", ", \"")
        cuerpolog = cuerpolog.replace("',", "\",")
        cuerpolog = cuerpolog.replace("['", "[\"")
        cuerpolog = cuerpolog.replace("']", "\"]")
        cuerpolog = cuerpolog.replace("\\'", " ")
        cuerpolog = cuerpolog.replace("\'", " ")
        cuerpolog = cuerpolog.replace("\\xc3\\xb1", "n")
        cuerpolog = cuerpolog.replace("\\xc3\\x88", "E")
        cuerpolog = cuerpolog.replace("\\xa0", " ")
        cuerpolog = cuerpolog.replace("\\xad", "")
        cuerpolog = cuerpolog.replace("\\x81", "")
        cuerpolog = cuerpolog.replace("\\n", " ")
        cuerpolog = cuerpolog.replace("\n", " ")
        cuerpolog = cuerpolog.replace("\\x83", "")
        cuerpolog = cuerpolog.replace("\\xb1", "")
        cuerpolog = cuerpolog.replace("\\xc2", "")
        cuerpolog = cuerpolog.replace("\\xc3", "")
        cuerpolog = cuerpolog.replace("\\xf1", "n")
        cuerpolog = cuerpolog.replace("\\xed", "i")
        cuerpolog = cuerpolog.replace("\\xd3", "o")
        cuerpolog = cuerpolog.replace("\\xf3", "o")
        cuerpolog = cuerpolog.replace("\\xe1", "a")
        cuerpolog = cuerpolog.replace("\\xc1", "A")
        cuerpolog = cuerpolog.replace("\\xfa", "u")
        cuerpolog = cuerpolog.replace("\\xba", "")
        cuerpolog = cuerpolog.replace("\\xa1", "a")
        cuerpolog = cuerpolog.replace("\\xa9", "e")
        cuerpolog = cuerpolog.replace("\\xb3", "o")
        cuerpolog = cuerpolog.replace("\\x99", "")
        cuerpolog = cuerpolog.replace("\\x9a", "U")
        cuerpolog = cuerpolog.replace("\\xe2", "")
        cuerpolog = cuerpolog.replace("\\x80", "")
        cuerpolog = cuerpolog.replace("\\xb0", "o.")
        cuerpolog = cuerpolog.replace("\\x91", "N")
        cuerpolog = cuerpolog.replace("\\x93", "O")
        cuerpolog = cuerpolog.replace("\\xa2", ".")
        cuerpolog = cuerpolog.replace("\\xaa", "a.")
        cuerpolog = cuerpolog.replace("\\xa8", "e")
        cuerpolog = cuerpolog.replace("\\xa7", "c")
        cuerpolog = cuerpolog.replace("\\x8d", "I")
        cuerpolog = cuerpolog.replace("\\x89", "E")
        cuerpolog = cuerpolog.replace("\\xbc", "u")
        cuerpolog = cuerpolog.replace("\\xb7", "u")
        cuerpolog = cuerpolog.replace("\\xc4", "l")
        cuerpolog = cuerpolog.replace("\\xb2", "o")
        cuerpolog = cuerpolog.replace("\\xaf", "i")
        cuerpolog = cuerpolog.replace("\\xb4", " ")
        cuerpolog = cuerpolog.replace("\\xc3", "E")
        cuerpolog = cuerpolog.replace("\\x88", "")
        cuerpolog = cuerpolog.replace("\\x87", "s")

        print("**********************" + str(cuerpolog))

        if notificacion and notificacion != "":
            if not qsatype.FLSqlQuery().execSql("INSERT INTO eg_notificacionesentradaslogis (fechanotificacion, horanotificacion, notificacion, documentos, estado, procesar, estadonotificacion) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(str(fechaActual), str(horaActual), cuerpolog, documento, estado, procesar, estadonotificacion)):
                return {"Mensaje": "No se ha podido crear el registro de la notificacion.", "status": 0}

        return {"Mensaje": "OK", "status": 10}

# @class_declaration revoke #
class notificacionesentradas(eg_notificacionesentradas):
    pass
