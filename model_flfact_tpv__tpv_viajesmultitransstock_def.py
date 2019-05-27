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
                                        existeDoc = qsatype.FLUtil.sqlSelect(u"idl_preparaciones", u"documentos", u"documentos = '" + doc + u"'  AND estado = true")
                                        if not existeDoc:
                                            print("entra")
                                            if documento == "":
                                                documento = doc
                                                longitud = len(doc)
                                                esEcommerce = qsatype.FLUtil.sqlSelect(u"idl_ecommerce", u"codcomanda", u"codcomanda = '" + str(doc[1:longitud]) + "'")
                                                print("esEcommerce " + str(esEcommerce))
                                                if esEcommerce and esEcommerce != "":
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
                                                        res[1] += "rub210: no se encontró el documento"
                                                    else:
                                                        idlinea = qsatype.FLUtil.sqlSelect("tpv_lineascomanda", "idtpv_linea", "barcode = '" + str(barcode) + "' and idtpv_comanda = " + str(idDoc))
                                                        if not idlinea:
                                                            res[0] = "KO"
                                                            if res[1] != "":
                                                                res[1] += " "
                                                            res[1] += "rub210: no se encontró el artículo en el documento"
                                                else:
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
                                            print("else")
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
                print("false insert ")
                print(xmlstring)
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
                                    existeDoc = qsatype.FLUtil.sqlSelect(u"idl_recepciones", u"documentos", u"documentos = '" + doc + u"' AND estado = true")
                                    if not existeDoc:
                                        longitud = len(doc)
                                        esEcommerce = qsatype.FLUtil.sqlSelect(u"idl_ecommercedevoluciones", u"codcomanda", u"codcomanda = '" + str(doc[1:longitud]) + "'")
                                        if esEcommerce and esEcommerce != "":
                                            fin = len(doc)
                                            codDoc = doc[1:fin]
                                            # Pedidoscli
                                            # if doc[0:1] == "T":
                                            idDoc = qsatype.FLUtil.sqlSelect(u"tpv_comandas", u"idtpv_comanda", u"codigo = '" + codDoc + u"'")
                                            if not idDoc:
                                                res[0] = "KO"
                                                if res[1] != "":
                                                    res[1] += " "
                                                res[1] += "rub210: no se encontró el documento"
                                            else:
                                                for referemcias in root.findall('int53/rub110/rub310'):
                                                    barcode = referemcias.find("item_code").text
                                                    if not barcode or barcode == "":
                                                        res[0] = "KO"
                                                        if res[1] != "":
                                                            res[1] += " "
                                                        res[1] += "rub310: item_code no puede estar vacío"
                                                    else:
                                                        idlinea = qsatype.FLUtil.sqlSelect("tpv_lineascomanda", "idtpv_linea", "barcode = '" + str(barcode) + "' and idtpv_comanda = " + str(idDoc))
                                                        if not idlinea:
                                                            res[0] = "KO"
                                                            if res[1] != "":
                                                                res[1] += " "
                                                            res[1] += "rub210: no se encontró el artículo en el documento"
                                        else:
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

    def elganso_idl_confirmadevolucion(self, params):
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
                    tree.write("/var/www/xmldevoluciones/confdevolucion_" + hoy + ".xml")

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
                                    fin = len(doc)
                                    codDoc = doc[1:fin]
                                    idDoc = 0
                                    existeDoc = qsatype.FLUtil.sqlSelect(u"idl_confirmacionrecepciones", u"documentos", u"documentos = '" + doc + u"'")
                                    if not existeDoc:
                                        idDoc = qsatype.FLUtil.sqlSelect(u"tpv_comandas", u"idtpv_comanda", u"codigo = '" + codDoc + u"'")
                                        if not idDoc:
                                            res[0] = "KO"
                                            if res[1] != "":
                                                res[1] += " "
                                            res[1] += "rub130: no se encontró el documento"
                                        # comprobar que no se haya confirmado ya
                                        if res[0] != "KO":
                                            if qsatype.FLUtil.sqlSelect("idl_confirmacionrecepciones", "idrecepcion", "documentos like '%" + doc + "%' and estadoprocesado != '' and estadoprocesado is not null"):
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
                                                        idlinea = qsatype.FLUtil.sqlSelect("tpv_lineascomanda", "idtpv_linea", "barcode = '" + str(barcode) + "' and idtpv_comanda = " + str(idDoc))
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
            if not qsatype.FLUtil.sqlInsert("idl_confirmacionrecepciones", ["fecharecepcion", "horarecepcion", "recepcion", "documentos", "respuesta", "estado", "procesar"], [str(fechaActual), str(horaActual), xml, doc, xmlstring, estado, procesar]):
                print("sale por aqui")
                return False

        return xmlstring

    def elganso_idl_confirmafaltante(self, params):
        res = []
        res.append("OK")
        res.append("")

        hoy = datetime.datetime.now().strftime("%d%m%Y%H%M")
        # qsatype.debug(params)

        # print(params)
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
                    tree.write("/var/www/xmlfaltante/conffaltante_" + hoy + ".xml")
                    childGeneral = root.find('int50/rub110')
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
                            for articulos in root.findall('int50/rub120'):
                                doc = str(articulos.find("originator_reference").text)
                                if not doc or doc == "":
                                    res[0] = "KO"
                                    if res[1] != "":
                                        res[1] += " "
                                    res[1] += "rub120: originator_reference no puede estar vacío"
                                else:
                                    barcode = str(articulos.find("item_code").text)
                                    if not barcode or barcode == "":
                                        res[0] = "KO"
                                        if res[1] != "":
                                            res[1] += " "
                                        res[1] += "rub120: item_code no puede estar vacío"
                                    else:
                                        fin = len(doc)
                                        codDoc = doc[1:fin]
                                        # Pedidoscli
                                        # if doc[0:1] == "T":
                                        idDoc = qsatype.FLUtil.sqlSelect(u"tpv_comandas", u"idtpv_comanda", u"codigo = '" + codDoc + u"'")
                                        if not idDoc:
                                            res[0] = "KO"
                                            if res[1] != "":
                                                res[1] += " "
                                            res[1] += "rub120: no se encontró el documento " + codDoc
                                        else:
                                            idfaltante = qsatype.FLUtil.sqlSelect("idl_ecommercefaltante", "id", "barcode = '" + str(barcode) + "' and idtpv_comanda = " + str(idDoc) + " and NOT cerrada and faltante > cantconfirmada")
                                            if not idfaltante:
                                                res[0] = "KO"
                                                if res[1] != "":
                                                    res[1] += " "
                                                res[1] += "rub120: no se encontró el artículo la tabla de faltantes"
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

        response = ET.Element("faltantes_response")
        int50 = ET.SubElement(response, "int50")
        r110 = ET.SubElement(int50, "rub110")
        ET.SubElement(r110, "activity_code").text = "GNS"
        ET.SubElement(r110, "physical_depot_code").text = "GNS"
        ET.SubElement(r110, "status").text = res[0]
        ET.SubElement(r110, "originator_code").text = doc
        ET.SubElement(r110, "order_reference").text = doc
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
            if not qsatype.FLUtil.sqlInsert("idl_confirmacionfaltantes", ["fecha", "hora", "faltante", "documentos", "respuesta", "estado", "procesar"], [str(fechaActual), str(horaActual), xml, doc, xmlstring, estado, procesar]):
                return False

        return xmlstring

    # Creado por Lorena el 24/05/2019
    def elganso_idl_confirmaajustesstock(self, params):
        res = []
        res.append("OK")
        res.append("")

        ipg = []
        ipg.append("")
        ipg.append("")

        hoy = datetime.datetime.now().strftime("%d%m%Y%H%M")
        xml = ""

        # {"source": "yeboyebo", "Content-Type": "application/xml", "key": "34762d577d2c6132417e5e5e2f"}
        try:
            if "key" in params and params['key'] == "34762d577d2c6132417e5e5e2f":
                if "xml" in params and params['xml'] != "":
                    xml = params['xml']
                    hoy = datetime.datetime.now().strftime("%d%m%Y%H%M")
                    root = ET.fromstring(xml)
                    tree = ET.ElementTree(root)
                    tree.write("/var/www/xmlajustesstock/confajustesstock_" + hoy + ".xml")

                    for childGeneral in root.findall('int62/rub110'):
                        if(childGeneral.find("activity_code").text != "GNS"):
                            res[0] = "KO"
                            res[1] = "rub110: activity_code erroneo"
                            return self.iface.creaRespuesta(res, ipg, xml)

                        if (childGeneral.find("physical_depot_code").text != "GNS"):
                            res[0] = "KO"
                            if res[1] != "":
                                res[1] += " "
                            res[1] += "rub110: physical_depot_code erroneo"
                            return self.iface.creaRespuesta(res, ipg, xml)

                        ipg[0] = childGeneral.find("ipg_move_year_no").text
                        if not ipg[0] or ipg[0] == "":
                            res[0] = "KO"
                            if res[1] != "":
                                res[1] += " "
                            res[1] += "rub110: ipg_move_year_no debe estar informado"
                            return self.iface.creaRespuesta(res, ipg, xml)

                        ipg[1] = childGeneral.find("ipg_move_no").text
                        if not ipg[1] or ipg[1] == "":
                            res[0] = "KO"
                            if res[1] != "":
                                res[1] += " "
                            res[1] += "rub110: ipg_move_no debe estar informado"
                            return self.iface.creaRespuesta(res, ipg, xml)

                        barcode = str(childGeneral.find("item_code").text)
                        if not barcode or barcode == "":
                            res[0] = "KO"
                            if res[1] != "":
                                res[1] += " "
                            res[1] += "rub110: item_code debe estar informado"
                            return self.iface.creaRespuesta(res, ipg, xml)

                        existeBC = qsatype.FLUtil.sqlSelect(u"atributosarticulos", u"barcode", u"barcode = '" + barcode + u"'")
                        if not existeBC or existeBC == "":
                            res[0] = "KO"
                            if res[1] != "":
                                res[1] += " "
                            res[1] += "rub110: El artículo " + barcode + " no existe"
                            return self.iface.creaRespuesta(res, ipg, xml)

                        almacen = str(childGeneral.find("owner_code").text)
                        if not almacen or almacen == "":
                            res[0] = "KO"
                            if res[1] != "":
                                res[1] += " "
                            res[1] += "rub110: owner_code debe estar informado"
                            return self.iface.creaRespuesta(res, ipg, xml)

                        existeAlmacen = qsatype.FLUtil.sqlSelect(u"almacenesidl", u"codalmacenidl", u"codalmacenidl = '" + almacen + u"'")
                        if not existeAlmacen or existeAlmacen == "":
                            res[0] = "KO"
                            if res[1] != "":
                                res[1] += " "
                            res[1] += "rub110: El almacen " + almacen + " no existe"
                            return self.iface.creaRespuesta(res, ipg, xml)
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

        return self.iface.creaRespuesta(res, ipg, xml)

    def elganso_idl_creaRespuesta(self, res, ipg, xml):
        response = ET.Element("stock_adjustments_response")
        int62 = ET.SubElement(response, "int62")
        r110 = ET.SubElement(int62, "rub110")
        ET.SubElement(r110, "activity_code").text = "GNS"
        ET.SubElement(r110, "physical_depot_code").text = "GNS"
        ET.SubElement(r110, "ipg_move_year_no").text = ipg[0]
        ET.SubElement(r110, "ipg_move_no").text = ipg[1]
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
            doc = ipg[0] + "-" + ipg[1]
            if not qsatype.FLUtil.sqlInsert("idl_ajustesstock", ["fecha", "hora", "ajustestock", "documentos", "respuesta", "estado", "procesar"], [str(fechaActual), str(horaActual), xml, doc, xmlstring, estado, procesar]):
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

    def confirmadevolucion(self, params):
        return self.ctx.elganso_idl_confirmadevolucion(params)

    def confirmafaltante(self, params):
        return self.ctx.elganso_idl_confirmafaltante(params)

    def confirmaajustesstock(self, params):
        return self.ctx.elganso_idl_confirmaajustesstock(params)

    def creaRespuesta(self, res, ipg, xml):
        return self.ctx.elganso_idl_creaRespuesta(res, ipg, xml)


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
