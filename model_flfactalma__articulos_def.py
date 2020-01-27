
# @class_declaration elganso_idl #
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import tostring
import datetime

class elganso_idl(flfactalma):

    def elganso_idl_damedatosarticulo(self, params):
        error = ""
        precio = ""
        stock = ""
        barcode = ""
        codTienda = ""
        try:
            if "key" in params and params['key'] == "34762d577d2c6132417e5e5e2f":
                if "xml" in params and params['xml'] != "":
                    xml = params['xml']
                    print(xml)
                    root = ET.fromstring(xml)

                    barcode = root.find("barcode").text
                    codTienda = root.find("tienda").text

                    if not barcode or barcode == "":
                        error = "Barcode no encontrado"
                        return self.iface.crearespuesta(error, precio, stock, barcode, codTienda)

                    referencia = qsatype.FLUtil.sqlSelect("atributosarticulos", "referencia", "barcode = '" + barcode + "'")
                    if not referencia or referencia == "":
                        error = "Referencia no encontrada"
                        return self.iface.crearespuesta(error, precio, stock, barcode, codTienda)

                    if not codTienda or codTienda == "":
                        error = "Tienda no encontrada"
                        return self.iface.crearespuesta(error, precio, stock, barcode, codTienda)

                    fecha = datetime.datetime.now().strftime("%d-%m-%Y")
                    idEmpresa = qsatype.FLUtil.sqlSelect(u"tpv_tiendas", u"idempresa", ustr(u"codtienda = '", codTienda, u"'"))
                    if not idEmpresa or idEmpresa == "" or idEmpresa == 0:
                        error = "Empresa no encontrada"
                        return self.iface.crearespuesta(error, precio, stock, barcode, codTienda)

                    precio = str(qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.pub_damePrecioArticulo(referencia, fecha, idEmpresa, codTienda, ""))
                    if not precio or precio == "":
                        error = "Precio no encontrado"
                        return self.iface.crearespuesta(error, precio, stock, barcode, codTienda)

                    codAlmacen = qsatype.FLUtil.sqlSelect("tpv_tiendas", "codalmacen", "codtienda = '" + codTienda + "'")
                    if not codAlmacen or codAlmacen == "":
                        error = "Almacén no encontrado"
                        return self.iface.crearespuesta(error, precio, stock, barcode, codTienda)

                    stock = str(qsatype.FLUtil.sqlSelect("stocks", "disponible", "barcode = '" + barcode + "' AND codalmacen = '" + codAlmacen + "'"))
                    if not stock or stock == "" or stock == "None":
                        stock = "0"
                else:
                    error = "No se encontró el xml"
                    return self.iface.crearespuesta(error, precio, stock, barcode, codTienda)
            else:
                error = "No se encontró la key"
                return self.iface.crearespuesta(error, precio, stock, barcode, codTienda)

        except Exception as e:
            error = "Error: " + str(e)

        return self.iface.crearespuesta(error, precio, stock, barcode, codTienda)

    def elganso_idl_damearticulos(self, params):
        error = "";
        resXml = "";
        try:
            if "key" in params and params['key'] == "34762d577d2c6132417e5e5e2f":
                listaOutlet = qsatype.FLUtil.sqlSelect("param_parametros", "valor", "nombre = 'ALMACENES_OUTLET'")
                if not listaOutlet or listaOutlet == "":
                    error = "<articulos><error>Se debe configurar el parámetro ALMACENES_OUTLET.</error></articulos>"
                    return error

                listaOutlet = listaOutlet.replace(",", "','")

                q = qsatype.FLSqlQuery()
                q.setSelect("a.referencia, a.descripcion, atr.barcode, atr.talla, a.codgrupomoda, a.codtemporada, a.anno")
                q.setFrom("atributosarticulos atr INNER JOIN stocks s ON atr.barcode = s.barcode INNER JOIN articulos a ON atr.referencia = a.referencia")
                q.setWhere("s.codalmacen IN ('" + listaOutlet + "') AND a.sevende = TRUE AND s.disponible > 0 GROUP BY a.referencia,atr.barcode,atr.talla,a.codgrupomoda,a.codtemporada,a.anno ORDER BY a.referencia,atr.barcode,atr.talla,a.codgrupomoda,a.codtemporada,a.anno")

                if not q.exec_():
                    error = "<articulos><error>Falló la consulta.</error></articulos>"
                    return error

                response = ET.Element("articulos")
                while q.next():
                    articulo = ET.SubElement(response, "articulo")
                    ET.SubElement(articulo, "referencia").text = q.value("a.referencia")
                    ET.SubElement(articulo, "descripcion").text = q.value("a.descripcion")
                    ET.SubElement(articulo, "barcode").text = q.value("atr.barcode")
                    ET.SubElement(articulo, "talla").text = q.value("atr.talla")
                    ET.SubElement(articulo, "grupomoda").text = q.value("a.codgrupomoda")
                    ET.SubElement(articulo, "temporada").text = q.value("a.codtemporada")
                    ET.SubElement(articulo, "anno").text = q.value("a.anno")

                resXml = tostring(response, 'utf-8', method="xml").decode("ISO8859-15")
                resXml = resXml.replace("'", "\\'")
                return resXml
        except Exception as e:
            error = "<articulos><error>Error: " + str(e) + "</error></articulos>"
            return error

        return ""

    def elganso_idl_crearespuesta(self, error, precio, stock, barcode, codTienda):
        response = ET.Element("articulo")

        ET.SubElement(response, "barcode").text = barcode
        ET.SubElement(response, "tienda").text = codTienda
        ET.SubElement(response, "error").text = error
        ET.SubElement(response, "precio").text = precio
        ET.SubElement(response, "stock").text = stock

        xmlstring = tostring(response, 'utf-8', method="xml").decode("ISO8859-15")
        xmlstring = xmlstring.replace("'", "\\'")

        return xmlstring

    def __init__(self, context=None):
        super().__init__(context)

    def damedatosarticulo(self, params):
        return self.ctx.elganso_idl_damedatosarticulo(params)

    def damearticulos(self, params):
        return self.ctx.elganso_idl_damearticulos(params)

    def crearespuesta(self, error, precio, stock, barcode, codTienda):
        return self.ctx.elganso_idl_crearespuesta(error, precio, stock, barcode, codTienda)

