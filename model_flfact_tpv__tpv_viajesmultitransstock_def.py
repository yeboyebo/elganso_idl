# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration elganso_idl #
from YBLEGACY.constantes import *
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import tostring
import datetime

class elganso_idl(interna):

    def elganso_idl_getDesc(self):
        return None

    def elganso_idl_confirmapreparacion(self, params):
        res = []
        res.append("OK")
        res.append("")

        hoy = datetime.datetime.now().strftime("%d%m%Y%H%M")
        # qsatype.debug(params)

        # print(params)
        documento = ""
        codDoc = ""
        xml = ""
        doc = ""
        # {"source": "yeboyebo", "Content-Type": "application/xml", "key": "34762d577d2c6132417e5e5e2f"}
        try:
            if "key" in params and params['key'] == "34762d577d2c6132417e5e5e2f":
                if "xml" in params and params['xml'] != "":
                    xml = params['xml']
                    hoy = datetime.datetime.now().strftime("%d%m%Y%H%M")
                    root = ET.fromstring(xml)
                    tree = ET.ElementTree(root)
                    tree.write("/var/www/xmlpreparaciones/confpreparacion_" + hoy + ".xml")
                    childGeneral = root.find('int52/rub110')
                    if childGeneral:
                        if(childGeneral.find("activity_code").text != "GNS"):
                            res[0] = "KO"
                            res[1] = "rub110: activity_code erroneo"

                        elif (childGeneral.find("physical_depot_code").text != "GNS"):
                            res[0] = "KO"
                            if res[1] != "":
                                res[1] += " "
                            res[1] += "rub110: activity_code erroneo"
                        else:
                            for articulos in root.findall('int52/rub110/rub210'):
                                barcode = str(articulos.find("item_code").text)
                                if not barcode or barcode == "":
                                    res[0] = "KO"
                                    if res[1] != "":
                                        res[1] += " "
                                    res[1] += "rub210: item_code no puede estar vacío"
                                else:
                                    doc = str(articulos.find("originator_reference").text)
                                    print("________________")
                                    print(doc)
                                    if not doc or doc == "":
                                        res[0] = "KO"
                                        if res[1] != "":
                                            res[1] += " "
                                        res[1] += "rub210: originator_reference no puede estar vacío"
                                    else:
                                        existeDoc = qsatype.FLUtil.sqlSelect(u"idl_preparaciones", u"documentos", u"documentos = '" + doc + u"'")
                                        if not existeDoc:
                                            if documento == "":
                                                documento = doc
                                                fin = len(doc) - 2
                                                codDoc = doc[1:fin]
                                                # Pedidoscli
                                                if doc[0:1] == "T":
                                                    idDoc = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"idpedido", u"codigo = '" + codDoc + u"'")
                                                    if not idDoc:
                                                        documento = ""
                                                        res[0] = "KO"
                                                        if res[1] != "":
                                                            res[1] += " "
                                                        res[1] += "rub210: no se encontró el documento"
                                                    else:
                                                        idlinea = qsatype.FLUtil.sqlSelect("lineaspedidoscli", "idlinea", "barcode = '" + str(barcode) + "' and idpedido = " + str(idDoc))
                                                        if not idlinea:
                                                            res[0] = "KO"
                                                            if res[1] != "":
                                                                res[1] += " "
                                                            res[1] += "rub210: no se encontró el artículo en el documento"
                                                # Viajes
                                                if doc[0:1] == "V":
                                                    idDoc = qsatype.FLUtil.sqlSelect("tpv_viajesmultitransstock", "idviajemultitrans", "idviajemultitrans = '" + codDoc + "'")
                                                    if not idDoc:
                                                        documento = ""
                                                        res[0] = "KO"
                                                        if res[1] != "":
                                                            res[1] += " "
                                                        res[1] += "rub210: no se encontró el documento"
                                                    else:
                                                        idlinea = qsatype.FLUtil.sqlSelect("tpv_lineasmultitransstock", "idlinea", "barcode = '" + barcode + "' and idviajemultitrans = '" + str(idDoc) + "'")
                                                        if not idlinea:
                                                            res[0] = "KO"
                                                            if res[1] != "":
                                                                res[1] += " "
                                                            res[1] += "rub210: no se encontró el artículo en el documento"
                                            else:
                                                if documento != doc:
                                                    documento = ""
                                                    res[0] = "KO"
                                                    if res[1] != "":
                                                        res[1] += " "
                                                    res[1] += "rub210: originator_reference la preparación no puede pertenecer a más de un documento diferente"
                                        else:
                                            res[0] = "KO"
                                            if res[1] != "":
                                                res[1] += " "
                                            res[1] += "rub210: originator_reference ya se ha enviado anteriormente"
                    else:
                        res[0] = "KO"
                        if res[1] != "":
                            res[1] += " "
                        res[1] += "No se encontraron datos"
                else:
                    res[0] = "KO"
                    if res[1] != "":
                        res[1] += " "
                    res[1] += "No se encontró el xml"
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

        response = ET.Element("preparation_confirmation_response ")
        int52 = ET.SubElement(response, "int52")
        r110 = ET.SubElement(int52, "rub110")
        ET.SubElement(r110, "activity_code").text = "GNS"
        ET.SubElement(r110, "physical_depot_code").text = "GNS"
        ET.SubElement(r110, "status").text = res[0]
        error = ET.SubElement(r110, "error_descriptions")
        ET.SubElement(error, "error_description").text = res[1]
        xmlstring = tostring(response, 'utf-8', method="xml").decode("ISO8859-15")

        xmlstring = xmlstring.replace("'", "\\'")
        xml = str(xml).replace("'", "\\'")

        fechaActual = qsatype.FactoriaModulos.get('flfactppal').iface.dameFechaActual()
        horaActual = qsatype.FactoriaModulos.get('flfactppal').iface.dameHoraActual()
        procesar = "true"
        estado = "true"
        if res[0] == "KO":
            procesar = "false"
            estado = "false"

        if xml and xml != "":
            if not qsatype.FLUtil.sqlInsert("idl_preparaciones", ["fechapreparacion", "horapreparacion", "preparacion", "documentos", "respuesta", "estado", "procesar"], [str(fechaActual), str(horaActual), xml, doc, xmlstring, estado, procesar]):
                return False

        return xmlstring

    def elganso_idl_confirmarecepcion(self, params):
        res = []
        res.append("OK")
        res.append("")

        hoy = datetime.datetime.now().strftime("%d%m%Y%H%M")
        qsatype.debug(params)

        print(params)
        doc = ""
        xml = ""
        # {"source": "yeboyebo", "Content-Type": "application/xml", "key": "34762d577d2c6132417e5e5e2f"}
        try:
            if "key" in params and params['key'] == "34762d577d2c6132417e5e5e2f":
                print("entra key ")
                if "xml" in params and params['xml'] != "":
                    print("entra xml")
                    xml = params['xml']

                    hoy = datetime.datetime.now().strftime("%d%m%Y%H%M")
                    root = ET.fromstring(xml)
                    tree = ET.ElementTree(root)
                    tree.write("/var/www/xmlrecepciones/confrecepcion_" + hoy + ".xml")

                    childGeneral = root.find('int53/rub110')
                    if childGeneral:
                        if(childGeneral.find("activity_code").text != "GNS"):
                            res[0] = "KO"
                            res[1] = "rub110: activity_code erroneo"

                        elif (childGeneral.find("physical_depot_code").text != "GNS"):
                            res[0] = "KO"
                            if res[1] != "":
                                res[1] += " "
                            res[1] += "rub110: activity_code erroneo"
                        else:
                            childCabecera = root.find('int53/rub110/rub130')
                            doc = ""
                            if childCabecera:
                                doc = childCabecera.find("receipt_reference").text
                                if not doc or doc == "":
                                    res[0] = "KO"
                                    if res[1] != "":
                                        res[1] += " "
                                    res[1] += "rub130: receipt_reference no puede estar vacío"
                                else:
                                    fin = len(doc) - 2
                                    idDoc = 0
                                    existeDoc = qsatype.FLUtil.sqlSelect(u"idl_recepciones", u"documentos", u"documentos = '" + doc + u"'")
                                    if not existeDoc:
                                        if doc.startswith('P'):
                                            idDoc = qsatype.FLUtil.sqlSelect(u"pedidosprov", u"idpedido", u"codigo = '" + doc[1:fin] + u"'")
                                            if not idDoc:
                                                res[0] = "KO"
                                                if res[1] != "":
                                                    res[1] += " "
                                                res[1] += "rub130: no se encontró el documento"
                                        else:
                                            if doc.startswith('V'):
                                                idDoc = qsatype.FLUtil.sqlSelect("tpv_viajesmultitransstock", "idviajemultitrans", "idviajemultitrans = '" + doc[1:fin] + "'")
                                                if not idDoc:
                                                    res[0] = "KO"
                                                    if res[1] != "":
                                                        res[1] += " "
                                                    res[1] += "rub130: no se encontró el documento"
                                        # comprobar que no se haya confirmado ya
                                        if res[0] != "KO":
                                            if qsatype.FLUtil.sqlSelect("idl_recepciones", "idrecepcion", "documentos like '%" + doc + "%' and estadoprocesado != '' and estadoprocesado is not null"):
                                                res[0] = "KO"
                                                if res[1] != "":
                                                    res[1] += " "
                                                res[1] += "rub130: documento ya procesado"
                                            else:
                                                for referemcias in root.findall('int53/rub110/rub310'):
                                                    articulo = referemcias.find("item_code").text
                                                    if not articulo or articulo == "":
                                                        res[0] = "KO"
                                                        if res[1] != "":
                                                            res[1] += " "
                                                        res[1] += "rub310: item_code no puede estar vacío"

                                                    # referencia, talla = articulo.split("-")
                                                    # if talla == "T":
                                                    #    talla = "TU"
                                                    barcode = articulo
                                                    # qsatype.FLUtil.sqlSelect("atributosarticulos", "barcode", "referencia = '" + referencia + "' and talla = '" + talla + "'")
                                                    if barcode and barcode != "":
                                                        if doc.startswith('P'):
                                                            idlinea = qsatype.FLUtil.sqlSelect("lineaspedidosprov", "idlinea", "barcode = '" + str(barcode) + "' and idpedido = " + str(idDoc))
                                                            if not idlinea:
                                                                res[0] = "KO"
                                                                if res[1] != "":
                                                                    res[1] += " "
                                                                res[1] += "rub310: no se encontró el artículo en el documento"
                                                        elif doc.startswith('V'):
                                                            idlinea = qsatype.FLUtil.sqlSelect("tpv_lineasmultitransstock", "idlinea", "barcode = '" + barcode + "' and idviajemultitrans = '" + str(idDoc) + "'")
                                                            if not idlinea:
                                                                res[0] = "KO"
                                                                if res[1] != "":
                                                                    res[1] += " "
                                                                res[1] += "rub310: no se encontró el artículo en el documento"
                                                    else:
                                                        res[0] = "KO"
                                                        if res[1] != "":
                                                            res[1] += " "
                                                        res[1] += "rub310: no se encontró el artículo"

                                                    cantidad = 0
                                                    childCantidad = referemcias.find('rub340')
                                                    if childCantidad:
                                                        error = ""
                                                        if childCantidad.find("shortage_on_receipt_reason_code"):
                                                            error = childCantidad.find("shortage_on_receipt_reason_code").text
                                                            if not error or error == "":
                                                                cantidad = childCantidad.find("base_lv_quantity_confirmed").text
                                                                if not cantidad:
                                                                    res[0] = "KO"
                                                                    if res[1] != "":
                                                                        res[1] += " "
                                                                    res[1] += "rub340: base_lv_quantity_confirmed no puede estar vacío"
                                                    else:
                                                        res[0] = "KO"
                                                        if res[1] != "":
                                                            res[1] += " "
                                                        res[1] += "rub340: No se ha encontrado la cantidad"
                                    else:
                                        res[0] = "KO"
                                        if res[1] != "":
                                            res[1] += " "
                                        res[1] += "rub210: originator_reference ya se ha enviado anteriormente"
                    else:
                        res[0] = "KO"
                        if res[1] != "":
                            res[1] += " "
                        res[1] += "No se encontraron datos"
                else:
                    res[0] = "KO"
                    if res[1] != "":
                        res[1] += " "
                    # Borrar comentario
                    res[1] += "No se encontraron datos"
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

        response = ET.Element("receipt_confirmation_response")
        int53 = ET.SubElement(response, "int53")
        r110 = ET.SubElement(int53, "rub110")
        ET.SubElement(r110, "activity_code").text = "GNS"
        ET.SubElement(r110, "physical_depot_code").text = "GNS"
        ET.SubElement(r110, "status").text = res[0]
        error = ET.SubElement(r110, "error_descriptions")
        ET.SubElement(error, "error_description").text = res[1]
        xmlstring = tostring(response, 'utf-8', method="xml").decode("ISO8859-15")

        xmlstring = xmlstring.replace("'", "\\'")
        xml = str(xml).replace("'", "\\'")

        fechaActual = qsatype.FactoriaModulos.get('flfactppal').iface.dameFechaActual()
        horaActual = qsatype.FactoriaModulos.get('flfactppal').iface.dameHoraActual()
        procesar = "true"
        estado = "true"
        if res[0] == "KO":
            procesar = "false"
            estado = "false"

        if xml and xml != "":
            if not qsatype.FLUtil.sqlInsert("idl_recepciones", ["fecharecepcion", "horarecepcion", "recepcion", "documentos", "respuesta", "estado", "procesar"], [str(fechaActual), str(horaActual), xml, doc, xmlstring, estado, procesar]):
                return False

        return xmlstring

    def elganso_idl_confirmaecommerce(self, params):
        res = []
        res.append("OK")
        res.append("")

        hoy = datetime.datetime.now().strftime("%d%m%Y%H%M")
        # qsatype.debug(params)

        # print(params)
        documento = ""
        codDoc = ""
        xml = ""
        doc = ""
        # {"source": "yeboyebo", "Content-Type": "application/xml", "key": "34762d577d2c6132417e5e5e2f"}
        try:
            if "key" in params and params['key'] == "34762d577d2c6132417e5e5e2f":
                if "xml" in params and params['xml'] != "":
                    xml = params['xml']
                    hoy = datetime.datetime.now().strftime("%d%m%Y%H%M")
                    root = ET.fromstring(xml)
                    tree = ET.ElementTree(root)
                    tree.write("/var/www/xmlecommerce/confecommerce_" + hoy + ".xml")
                    childGeneral = root.find('int52/rub110')
                    if childGeneral:
                        if(childGeneral.find("activity_code").text != "GNS"):
                            res[0] = "KO"
                            res[1] = "rub110: activity_code erroneo"

                        elif (childGeneral.find("physical_depot_code").text != "GNS"):
                            res[0] = "KO"
                            if res[1] != "":
                                res[1] += " "
                            res[1] += "rub110: activity_code erroneo"
                        else:
                            for articulos in root.findall('int52/rub110/rub210'):
                                barcode = str(articulos.find("item_code").text)
                                if not barcode or barcode == "":
                                    res[0] = "KO"
                                    if res[1] != "":
                                        res[1] += " "
                                    res[1] += "rub210: item_code no puede estar vacío"
                                else:
                                    doc = str(articulos.find("originator_reference").text)
                                    print("________________")
                                    print(doc)
                                    if not doc or doc == "":
                                        res[0] = "KO"
                                        if res[1] != "":
                                            res[1] += " "
                                        res[1] += "rub210: originator_reference no puede estar vacío"
                                    else:
                                        existeDoc = qsatype.FLUtil.sqlSelect(u"idl_confirmacionpreparaciones", u"documentos", u"documentos = '" + doc + u"'")
                                        if not existeDoc:
                                            if documento == "":
                                                documento = doc
                                                fin = len(doc)
                                                codDoc = doc[1:fin]
                                                # Pedidoscli
                                                # if doc[0:1] == "T":
                                                idDoc = qsatype.FLUtil.sqlSelect(u"tpv_comandas", u"idtpv_comanda", u"codigo = '" + codDoc + u"'")
                                                if not idDoc:
                                                    documento = ""
                                                    res[0] = "KO"
                                                    if res[1] != "":
                                                        res[1] += " "
                                                    res[1] += "rub210: no se encontró el documento " + codDoc
                                                else:
                                                    idlinea = qsatype.FLUtil.sqlSelect("tpv_lineascomanda", "idtpv_linea", "barcode = '" + str(barcode) + "' and idtpv_comanda = " + str(idDoc))
                                                    if not idlinea:
                                                        res[0] = "KO"
                                                        if res[1] != "":
                                                            res[1] += " "
                                                        res[1] += "rub210: no se encontró el artículo en el documento"
                                            else:
                                                if documento != doc:
                                                    documento = ""
                                                    res[0] = "KO"
                                                    if res[1] != "":
                                                        res[1] += " "
                                                    res[1] += "rub210: originator_reference la preparación no puede pertenecer a más de un documento diferente"
                                        else:
                                            res[0] = "KO"
                                            if res[1] != "":
                                                res[1] += " "
                                            res[1] += "rub210: originator_reference ya se ha enviado anteriormente"
                    else:
                        res[0] = "KO"
                        if res[1] != "":
                            res[1] += " "
                        res[1] += "No se encontraron datos"
                else:
                    res[0] = "KO"
                    if res[1] != "":
                        res[1] += " "
                    res[1] += "No se encontró el xml"
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

        response = ET.Element("preparation_confirmation_response ")
        int52 = ET.SubElement(response, "int52")
        r110 = ET.SubElement(int52, "rub110")
        ET.SubElement(r110, "activity_code").text = "GNS"
        ET.SubElement(r110, "physical_depot_code").text = "GNS"
        ET.SubElement(r110, "status").text = res[0]
        error = ET.SubElement(r110, "error_descriptions")
        ET.SubElement(error, "error_description").text = res[1]
        xmlstring = tostring(response, 'utf-8', method="xml").decode("ISO8859-15")

        xmlstring = xmlstring.replace("'", "\\'")
        xml = str(xml).replace("'", "\\'")

        fechaActual = qsatype.FactoriaModulos.get('flfactppal').iface.dameFechaActual()
        horaActual = qsatype.FactoriaModulos.get('flfactppal').iface.dameHoraActual()
        procesar = "true"
        estado = "true"
        if res[0] == "KO":
            procesar = "false"
            estado = "false"

        if xml and xml != "":
            if not qsatype.FLUtil.sqlInsert("idl_confirmacionpreparaciones", ["fechapreparacion", "horapreparacion", "preparacion", "documentos", "respuesta", "estado", "procesar"], [str(fechaActual), str(horaActual), xml, doc, xmlstring, estado, procesar]):
                return False

        return xmlstring

    def __init__(self, context=None):
        super().__init__(context)

    def getDesc(self):
        return self.ctx.elganso_idl_getDesc()

    def confirmarecepcion(self, params):
        return self.ctx.elganso_idl_confirmarecepcion(params)

    def confirmapreparacion(self, params):
        return self.ctx.elganso_idl_confirmapreparacion(params)

    def confirmaecommerce(self, params):
        return self.ctx.elganso_idl_confirmaecommerce(params)


# @class_declaration head #
class head(elganso_idl):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration ifaceCtx #
class ifaceCtx(head):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration FormInternalObj #
class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)
