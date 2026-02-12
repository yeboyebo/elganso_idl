# @class_declaration interna #
from YBLEGACY import qsatype
import time

# @class_declaration interna_revoke #
class interna_get():
    pass


# @class_declaration flsyncppal_revoke #
class eg_creatarjetafidelizacion(interna_get):

    @staticmethod
    def start(self, data):
        try:
            if "passwd" in data and data["passwd"] == "bUqfqBMnoH":
                print(1)
                time.sleep(3)
                print(2)
                if "email" not in data:
                    return {"Error": "No se ha introducido el email de la Tarjeta.", "status": 0}

                if "codtarjetapuntos" not in data:
                    return {"Error": "No se ha encontrado el código de la Tarjeta.", "status": 0}
                
                email = str(data['email']).lower()
                #cifnif = str(data['cifnif']).lower()
                telefono = str(data['telefono']).lower()

                existe_tarjeta_email = qsatype.FLUtil.sqlSelect("tpv_tarjetaspuntos", "codtarjetapuntos", "LOWER(email) = '" + str(email) + "' AND codtarjetapuntos <> '" + str(data['codtarjetapuntos']) + "'")

                if existe_tarjeta_email:
                    return {"Error": "Ya existe la tarjeta " + existe_tarjeta_email + " con el email " + str(email) + " en Central.", "status": 0}

                """existe_tarjeta_cifnif = qsatype.FLUtil.sqlSelect("tpv_tarjetaspuntos", "codtarjetapuntos", "((lower(cifnif) = '" + cifnif + "') OR ('0' || lower(cifnif) = '" + cifnif + "')) AND codtarjetapuntos <> '" + str(data['codtarjetapuntos']) + "'")
                if existe_tarjeta_cifnif:
                    return {"Error": "Ya existe la tarjeta " + existe_tarjeta_cifnif + " con el cifnif " + str(cifnif) + " en Central.", "status": 0}"""

                existe_tarjeta_telefono = qsatype.FLUtil.sqlSelect("tpv_tarjetaspuntos", "codtarjetapuntos", "lower(telefono) = '" + telefono + "' AND codtarjetapuntos <> '" + str(data['codtarjetapuntos']) + "'")
                if existe_tarjeta_telefono:
                    return {"Error": "Ya existe la tarjeta " + existe_tarjeta_telefono + " con el telefono " + str(telefono) + " en Central.", "status": 0}
                
                if not qsatype.FLSqlQuery().execSql("INSERT INTO tpv_tarjetaspuntos (direccion, sexo, fechanacimiento, codbarrastarjeta, dtoespecial, horaalta, horamod, activa, codtarjetapuntos, codpais, email, saldopuntos, cifnif, dtopor, topemensual, deempleado, eg_emailbienvenida, nombre, anulada, telefono, suscritocrm, saldopuntossinc, fechaalta, codpostal, fechamod, ciudad, sincronizada, idusuarioalta, provincia, idprovincia, idusuariomod) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}', '{}', '{}', {}, '{}', '{}', '{}', '{}', {}, '{}', '{}', '{}', {}, {}, '{}', '{}', '{}', '{}', {}, '{}', '{}', '{}', '{}')".format(data['direccion'],  data['sexo'], data['fechanacimiento'], data['codtarjetapuntos'], data['dtoespecial'], data['horaalta'], data['horamod'], True, data['codtarjetapuntos'], data['codpais'], email, 0, data['cifnif'], data['dtopor'], data['topemensual'], data['deempleado'], False, data['nombre'], data['anulada'], data['telefono'], True, 0, data['fechaalta'], data['codpostal'], data['fechamod'], data['ciudad'], True, data['idusuarioalta'], data['provincia'], data['idprovincia'], data['idusuarioalta'])):
                    return {"Error": "No se ha podido crear la Tarjeta de Fidelizacion en Central. Contacte con Soporte.", "status": 0}


                return {"CodTarjetaPuntos": data['codtarjetapuntos']}

        except Exception as e:
            return {"Error": "Error inesperado al crear la Tarjeta de Fidelizacion", "status": -2}

        return True

# @class_declaration revoke #
class creatarjetafidelizacion(eg_creatarjetafidelizacion):
    pass
