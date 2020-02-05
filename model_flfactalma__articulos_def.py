
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
                barcode = params['barcode']
                codTienda = params['tienda']

                if not barcode or barcode == "":
                    error = "Barcode no encontrado"
                    return self.iface.crearespuestadatosArticulo(error, precio, stock, barcode, codTienda)

                referencia = qsatype.FLUtil.sqlSelect("atributosarticulos", "referencia", "barcode = '" + barcode + "'")
                if not referencia or referencia == "":
                    error = "Referencia no encontrada"
                    return self.iface.crearespuestadatosArticulo(error, precio, stock, barcode, codTienda)

                if not codTienda or codTienda == "":
                    error = "Tienda no encontrada"
                    return self.iface.crearespuestadatosArticulo(error, precio, stock, barcode, codTienda)

                fecha = datetime.datetime.now().strftime("%d-%m-%Y")
                idEmpresa = qsatype.FLUtil.sqlSelect(u"tpv_tiendas", u"idempresa", ustr(u"codtienda = '", codTienda, u"'"))
                if not idEmpresa or idEmpresa == "" or idEmpresa == 0:
                    error = "Empresa no encontrada"
                    return self.iface.crearespuestadatosArticulo(error, precio, stock, barcode, codTienda)

                precio = str(qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.pub_damePrecioArticulo(referencia, fecha, idEmpresa, codTienda, ""))
                if not precio or precio == "":
                    error = "Precio no encontrado"
                    return self.iface.crearespuestadatosArticulo(error, precio, stock, barcode, codTienda)

                codAlmacen = qsatype.FLUtil.sqlSelect("tpv_tiendas", "codalmacen", "codtienda = '" + codTienda + "'")
                if not codAlmacen or codAlmacen == "":
                    error = "Almacén no encontrado"
                    return self.iface.crearespuestadatosArticulo(error, precio, stock, barcode, codTienda)

                stock = str(qsatype.FLUtil.sqlSelect("stocks", "disponible", "barcode = '" + barcode + "' AND codalmacen = '" + codAlmacen + "'"))
                if not stock or stock == "" or stock == "None":
                    stock = "0"
            else:
                error = "No se encontró la key"
                return self.iface.crearespuestadatosArticulo(error, precio, stock, barcode, codTienda)

        except Exception as e:
            error = "Error: " + str(e)

        return self.iface.crearespuestadatosArticulo(error, precio, stock, barcode, codTienda)

    def elganso_idl_crearespuestadatosArticulo(self, error, precio, stock, barcode, codTienda):
        response = ET.Element("articulo")

        ET.SubElement(response, "barcode").text = barcode
        ET.SubElement(response, "tienda").text = codTienda

        if error and error != "":
            ET.SubElement(response, "error").text = error
        else:
            ET.SubElement(response, "precio").text = precio
            ET.SubElement(response, "stock").text = stock

        xmlstring = tostring(response, encoding='unicode')
        xmlstring = xmlstring.replace("'", "\\'")

        return "<?xml version='1.0' encoding='UTF-8'?>" + xmlstring

    def elganso_idl_damearticulos(self, params):
        error = ""
        resXml = ""
        try:
            if "key" in params and params['key'] == "34762d577d2c6132417e5e5e2f":
                listaOutlet = qsatype.FLUtil.sqlSelect("param_parametros", "valor", "nombre = 'ALMACENES_OUTLET'")
                if not listaOutlet or listaOutlet == "":
                    error = "<?xml version='1.0' encoding='UTF-8'?><articulos><error>Se debe configurar el parámetro ALMACENES_OUTLET.</error></articulos>"
                    return error

                listaOutlet = listaOutlet.replace(",", "','")
                q = qsatype.FLSqlQuery()
                q.setSelect("a.referencia, a.descripcion, atr.barcode, atr.talla, atr.color, a.codgrupomoda, gm.descripcion, a.codtemporada, t.descripcion, a.anno, a.codgrupotc, gtc.descripcion, a.codfamilia, f.descripcion, a.codtipoprenda, tp.descripcion, a.codsubfamilia, sf.descripcion")
                q.setFrom("atributosarticulos atr INNER JOIN stocks s ON atr.barcode = s.barcode INNER JOIN articulos a ON atr.referencia = a.referencia LEFT OUTER JOIN gruposmoda gm ON a.codgrupomoda = gm.codgrupomoda LEFT OUTER JOIN temporadas t on a.codtemporada = t.codtemporada LEFT OUTER JOIN grupostc gtc ON a.codgrupotc = gtc.codgrupotc LEFT OUTER JOIN familias f ON a.codfamilia = f.codfamilia LEFT OUTER JOIN tiposprenda tp ON a.codtipoprenda = tp.codtipoprenda LEFT OUTER JOIN subfamilias sf ON a.codsubfamilia = sf.codsubfamilia")
                q.setWhere("a.referencia NOT LIKE '0000ATEMP%' AND s.codalmacen IN ('" + listaOutlet + "') AND a.nostock = FALSE AND a.sevende = TRUE AND s.disponible > 0 GROUP BY a.referencia,atr.barcode,atr.talla,a.codgrupomoda,gm.descripcion,a.codtemporada,t.descripcion,a.anno, a.codgrupotc, gtc.descripcion, a.codfamilia, f.descripcion, a.codtipoprenda, tp.descripcion, a.codsubfamilia, sf.descripcion ORDER BY a.referencia,atr.barcode,atr.talla,a.codgrupomoda,a.codtemporada,a.anno")

                if not q.exec_():
                    error = "<?xml version='1.0' encoding='UTF-8'?><articulos><error>Falló la consulta.</error></articulos>"
                    return error

                response = ET.Element("articulos")
                while q.next():
                    articulo = ET.SubElement(response, "articulo")
                    ET.SubElement(articulo, "referencia").text = q.value("a.referencia")
                    ET.SubElement(articulo, "descripcion").text = q.value("a.descripcion")
                    ET.SubElement(articulo, "barcode").text = q.value("atr.barcode")
                    ET.SubElement(articulo, "talla").text = q.value("atr.talla")
                    ET.SubElement(articulo, "color").text = q.value("atr.color")
                    ET.SubElement(articulo, "cod_grupomoda").text = q.value("a.codgrupomoda")
                    ET.SubElement(articulo, "desc_grupomoda").text = q.value("gm.descripcion")
                    ET.SubElement(articulo, "cod_grupo").text = q.value("a.codgrupotc")
                    ET.SubElement(articulo, "desc_grupo").text = q.value("gtc.descripcion")
                    ET.SubElement(articulo, "cod_familia").text = q.value("a.codfamilia")
                    ET.SubElement(articulo, "desc_familia").text = q.value("f.descripcion")
                    ET.SubElement(articulo, "cod_tipoprenda").text = q.value("a.codtipoprenda")
                    ET.SubElement(articulo, "desc_tipoprenda").text = q.value("tp.descripcion")
                    ET.SubElement(articulo, "cod_subfamilia").text = q.value("a.codsubfamilia")
                    ET.SubElement(articulo, "desc_subfamilia").text = q.value("sf.descripcion")
                    ET.SubElement(articulo, "cod_temporada").text = q.value("a.codtemporada")
                    ET.SubElement(articulo, "desc_temporada").text = q.value("t.descripcion")
                    ET.SubElement(articulo, "anno").text = q.value("a.anno")

                resXml = tostring(response, encoding='unicode')
                resXml = resXml.replace("'", "\\'")

                return "<?xml version='1.0' encoding='UTF-8'?>" + resXml
        except Exception as e:
            error = "<?xml version='1.0' encoding='UTF-8'?><articulos><error>Error: " + str(e) + "</error></articulos>"
            return error

        return ""

    def elganso_idl_damedatosarticuloporalmacen(self, params):
        error = ""
        precio = ""
        codTienda = ""
        try:
            if "key" in params and params['key'] == "34762d577d2c6132417e5e5e2f":
                codTienda = params['tienda']
                if not codTienda or codTienda == "":
                    error = "Tienda no encontrada"
                    return "<?xml version='1.0' encoding='UTF-8'?><articulos><error>" + error + "</error></articulos>"

                codAlmacen = qsatype.FLUtil.sqlSelect("tpv_tiendas", "codalmacen", "codtienda = '" + codTienda + "'")
                if not codAlmacen or codAlmacen == "":
                    error = "Almacén no encontrado"
                    return "<?xml version='1.0' encoding='UTF-8'?><articulos><error>" + error + "</error></articulos>"

                fecha = datetime.datetime.now().strftime("%d-%m-%Y")
                idEmpresa = qsatype.FLUtil.sqlSelect(u"tpv_tiendas", u"idempresa", ustr(u"codtienda = '", codTienda, u"'"))

                if not idEmpresa or idEmpresa == "" or idEmpresa == 0:
                    error = "Empresa no encontrada"
                    return "<?xml version='1.0' encoding='UTF-8'?><articulos><error>" + error + "</error></articulos>"

                q = qsatype.FLSqlQuery()
                q.setSelect("barcode, referencia, disponible")
                q.setFrom("stocks")
                q.setWhere("codalmacen = '" + codAlmacen + "' AND disponible > 0");

                if not q.exec():
                    error = "Error al obtener los articulos"
                    return "<?xml version='1.0' encoding='UTF-8'?><articulos><error>" + error + "</error></articulos>"
                response = ET.Element("articulos")
                while q.next():
                    articulo = ET.SubElement(response, "articulo")
                    ET.SubElement(articulo, "tienda").text = codTienda
                    ET.SubElement(articulo, "barcode").text = q.value("barcode")
                    ET.SubElement(articulo, "stock").text = str(q.value("disponible"))

                    referencia = q.value("referencia")
                    precio = str(qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.pub_damePrecioArticulo(referencia, fecha, idEmpresa, codTienda, ""))

                    if not precio or precio == "":
                        error = "Precio no encontrado"
                        return "<?xml version='1.0' encoding='UTF-8'?><articulos><error>" + error + "</error></articulos>"

                    ET.SubElement(articulo, "precio").text = str(precio)
            else:
                error = "No se encontró la key"
                return "<?xml version='1.0' encoding='UTF-8'?><articulos><error>" + error + "</error></articulos>"
        except Exception as e:
            error = "Error: " + str(e)
            return "<?xml version='1.0' encoding='UTF-8'?><articulos><error>" + error + "</error></articulos>"

        resXml = tostring(response, encoding='unicode')
        resXml = resXml.replace("'", "\\'")

        return "<?xml version='1.0' encoding='UTF-8'?>" + resXml


    def __init__(self, context=None):
        super().__init__(context)

    def damedatosarticulo(self, params):
        return self.ctx.elganso_idl_damedatosarticulo(params)

    def crearespuestadatosArticulo(self, error, precio, stock, barcode, codTienda):
        return self.ctx.elganso_idl_crearespuestadatosArticulo(error, precio, stock, barcode, codTienda)

    def damearticulos(self, params):
        return self.ctx.elganso_idl_damearticulos(params)

    def damedatosarticuloporalmacen(self, params):
        return self.ctx.elganso_idl_damedatosarticuloporalmacen(params)

