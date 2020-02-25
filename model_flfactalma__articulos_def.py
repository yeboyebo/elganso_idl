
# @class_declaration elganso_idl #
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import tostring
import datetime

class elganso_idl(flfactalma):

    def elganso_idl_damealmacenesoutlet(self):
        listaOutlet = qsatype.FLUtil.sqlSelect("param_parametros", "valor", "nombre = 'ALMACENES_OUTLET'")
        if not listaOutlet or listaOutlet == "":
            error = "<?xml version='1.0' encoding='UTF-8'?><articulos><error>Se debe configurar el parámetro ALMACENES_OUTLET.</error></articulos>"
            return ""

        listaOutlet = listaOutlet.replace(",", "','")
        return listaOutlet;


    def elganso_idl_damedatosarticulos(self, params):
        print(params)
        error = ""
        precio = ""
        barcode = ""
        codTienda = ""
        try:
            if "key" in params and params['key'] == "34762d577d2c6132417e5e5e2f":
                listaOutlet = self.iface.damealmacenesoutlet()
                if not listaOutlet or listaOutlet == "":
                    error = "Se debe configurar el parámetro ALMACENES_OUTLET."
                    return self.iface.crearespuestadatosArticulo(error, precio, stock, barcode, codTienda)

                fecha = datetime.datetime.now().strftime("%d-%m-%Y")

                if "barcode" in params:
                    barcode = params['barcode']

                if "tienda" in params:
                    codTienda = params['tienda']

                masWhere = ""
                if barcode and barcode != "None" and barcode != "":
                    print("entra if barcode")
                    masWhere += " AND s.barcode = '" + barcode + "'"

                if codTienda and codTienda != "None" and codTienda != "":
                    masWhere += " AND t.codtienda = '" + codTienda + "'"

                print(masWhere)
                q = qsatype.FLSqlQuery()
                q.setSelect("s.barcode, s.referencia, s.disponible, t.codtienda, t.idempresa")
                q.setFrom("stocks s INNER JOIN almacenes alm ON s.codalmacen = alm.codalmacen INNER JOIN tpv_tiendas t ON t.codalmacen = alm.codalmacen INNER JOIN articulos a on s.referencia = a.referencia")
                q.setWhere("a.referencia NOT LIKE '0000ATEMP%' AND s.codalmacen IN ('" + listaOutlet + "') AND a.nostock = FALSE AND a.sevende = TRUE AND s.disponible > 0" + masWhere);
                # q.setWhere("s.codalmacen IN ('" + listaOutlet + "') AND s.disponible > 0 order by t.codtienda, s.barcode");

                if not q.exec():
                    error = "Error al obtener los articulos"
                    return "<?xml version='1.0' encoding='UTF-8'?><articulos><error>" + error + "</error></articulos>"
                response = ET.Element("articulos")
                while q.next():
                    articulo = ET.SubElement(response, "articulo")
                    ET.SubElement(articulo, "tienda").text = q.value("t.codtienda")
                    ET.SubElement(articulo, "barcode").text = q.value("s.barcode")
                    ET.SubElement(articulo, "stock").text = str(q.value("s.disponible"))

                    referencia = q.value("s.referencia")
                    precio = str(qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.pub_damePrecioArticulo(referencia, fecha, q.value("t.idempresa"), q.value("t.codtienda"), ""))

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


    def elganso_idl_damearticulos(self, params):
        error = ""
        resXml = ""
        try:
            if "key" in params and params['key'] == "34762d577d2c6132417e5e5e2f":
                listaOutlet = self.iface.damealmacenesoutlet()
                if not listaOutlet or listaOutlet == "":
                    error = "<?xml version='1.0' encoding='UTF-8'?><articulos><error>Se debe configurar el parámetro ALMACENES_OUTLET.</error></articulos>"
                    return error

                q = qsatype.FLSqlQuery()
                q.setSelect("a.referencia, a.descripcion, atr.barcode, atr.talla, a.egcolor, a.codgrupomoda, gm.descripcion, a.codtemporada, t.descripcion, a.anno, a.codgrupotc, gtc.descripcion, a.codfamilia, f.descripcion, a.codtipoprenda, tp.descripcion, a.codsubfamilia, sf.descripcion, url.urls")
                q.setFrom("atributosarticulos atr INNER JOIN stocks s ON atr.barcode = s.barcode INNER JOIN articulos a ON atr.referencia = a.referencia LEFT OUTER JOIN gruposmoda gm ON a.codgrupomoda = gm.codgrupomoda LEFT OUTER JOIN temporadas t on a.codtemporada = t.codtemporada LEFT OUTER JOIN grupostc gtc ON a.codgrupotc = gtc.codgrupotc LEFT OUTER JOIN familias f ON a.codfamilia = f.codfamilia LEFT OUTER JOIN tiposprenda tp ON a.codtipoprenda = tp.codtipoprenda LEFT OUTER JOIN subfamilias sf ON a.codsubfamilia = sf.codsubfamilia LEFT OUTER JOIN eg_urlsimagenesarticulosmgt url ON a.referencia = url.referencia")
                q.setWhere("a.referencia NOT LIKE '0000ATEMP%' AND s.codalmacen IN ('" + listaOutlet + "') AND a.nostock = FALSE AND a.sevende = TRUE AND s.disponible > 0 GROUP BY a.referencia,atr.barcode,atr.talla, a.egcolor, a.codgrupomoda,gm.descripcion,a.codtemporada,t.descripcion,a.anno, a.codgrupotc, gtc.descripcion, a.codfamilia, f.descripcion, a.codtipoprenda, tp.descripcion, a.codsubfamilia, sf.descripcion, url.urls ORDER BY a.referencia,atr.barcode,atr.talla,a.codgrupomoda,a.codtemporada,a.anno")

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
                    ET.SubElement(articulo, "color").text = q.value("a.egcolor")
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
                    ET.SubElement(articulo, "urls_imagenes").text = q.value("url.urls")

                resXml = tostring(response, encoding='unicode')
                resXml = resXml.replace("'", "\\'")

                return "<?xml version='1.0' encoding='UTF-8'?>" + resXml
        except Exception as e:
            error = "<?xml version='1.0' encoding='UTF-8'?><articulos><error>Error: " + str(e) + "</error></articulos>"
            return error

        return ""


    def elganso_idl_damedatostiendas(self, params):
        error = ""
        try:
            if "key" in params and params['key'] == "34762d577d2c6132417e5e5e2f":
                listaOutlet = self.iface.damealmacenesoutlet()
                if not listaOutlet or listaOutlet == "":
                    error = "Se debe configurar el parámetro ALMACENES_OUTLET."
                    return self.iface.crearespuestadatosArticulo(error, precio, stock, barcode, codTienda)

                q = qsatype.FLSqlQuery()
                q.setSelect("t.codtienda, t.descripcion, t.dirtipovia, t.direccion, t.dirnum, t.codpostal, t.ciudad, t.provincia, t.codpais, t.telefono")
                q.setFrom("tpv_tiendas t INNER JOIN almacenes a ON a.codalmacen = t.codalmacen")
                q.setWhere("a.codalmacen IN ('" + listaOutlet + "') order by t.codtienda");

                if not q.exec():
                    error = "Error al obtener los datos de tiendas"
                    return "<?xml version='1.0' encoding='UTF-8'?><articulos><error>" + error + "</error></articulos>"
                response = ET.Element("tiendas")
                while q.next():
                    tienda = ET.SubElement(response, "tienda")
                    ET.SubElement(tienda, "codigo").text = str(q.value("t.codtienda"))
                    ET.SubElement(tienda, "descripcion").text = str(q.value("t.descripcion"))
                    direccion = ""
                    if str(q.value("t.dirtipovia")) and str(q.value("t.dirtipovia")) != "None":
                        direccion = str(q.value("t.dirtipovia")) + " "

                    direccion += str(q.value("t.direccion"))
                    if str(q.value("t.dirnum")) and str(q.value("t.dirnum")) != "None" :
                        direccion += ", " + str(q.value("t.dirnum"))

                    ET.SubElement(tienda, "direccion").text = direccion
                    ET.SubElement(tienda, "codpostal").text = str(q.value("t.codpostal"))
                    ET.SubElement(tienda, "ciudad").text = str(q.value("t.ciudad"))
                    ET.SubElement(tienda, "provincia").text = str(q.value("t.provincia"))
                    ET.SubElement(tienda, "codpais").text = str(q.value("t.codpais"))
                    ET.SubElement(tienda, "telefono").text = str(q.value("t.telefono"))
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

    def damealmacenesoutlet(self):
        return self.ctx.elganso_idl_damealmacenesoutlet()

    def damedatosarticulos(self, params):
        return self.ctx.elganso_idl_damedatosarticulos(params)

    def damearticulos(self, params):
        return self.ctx.elganso_idl_damearticulos(params)

    def damedatostiendas(self, params):
        return self.ctx.elganso_idl_damedatostiendas(params)

