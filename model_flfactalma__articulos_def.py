
# @class_declaration elganso_idl #
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import tostring
import datetime

class elganso_idl(flfactalma):

    def elganso_idl_dameprecioarticulo(self, params):
        error = ""
        precio = ""
        stock = ""
        barcode = ""
        codTienda = ""
        try:
            if "key" in params and params['key'] == "34762d577d2c6132417e5e5e2f":
                if "xml" in params and params['xml'] != "":
                    xml = params['xml']
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


        except Exception as e:
            error = "Error: " + str(e)

        return self.iface.crearespuesta(error, precio, stock, barcode, codTienda)

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

    def dameprecioarticulo(self, params):
        return self.ctx.elganso_idl_dameprecioarticulo(params)

    def crearespuesta(self, error, precio, stock, barcode, codTienda):
        return self.ctx.elganso_idl_crearespuesta(error, precio, stock, barcode, codTienda)

