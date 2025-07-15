# Este módulo se encarga de generar un archivo XML con la estructura requerida para una orden de compra.
import xml.etree.ElementTree as ET  # Importamos el módulo para manejar XML
from datetime import date  # Esta librería nos permite trabajar con fechas
import re

def generar_xml(productos: list, output_file="orden.xml"):
    orden = ET.Element("Order")

    order_head = ET.SubElement(orden, "OrderHead")
    parameters = ET.SubElement(order_head, "Parameters")
    ET.SubElement(parameters, "Language").text = "en-GB"
    ET.SubElement(parameters, "DecimalSeparator").text = "."
    ET.SubElement(parameters, "Precision").text = "2"
    ET.SubElement(order_head, "OrderType", Code="PUQ").text = "Quote"
    order_currency = ET.SubElement(order_head, "OrderCurrency")
    ET.SubElement(order_currency, "Currency", Code="USD")
    ET.SubElement(orden, "OrderDate").text = str(date.today())

    section_start = ET.SubElement(orden, "OrderLine", TypeCode="SECTIONSTART")
    ET.SubElement(section_start, "LineNumber").text = "1"
    ET.SubElement(section_start, "Narrative").text = "MATERIAL SELECTION"

    line_number = 2
    for p in productos:
        line = ET.SubElement(orden, "OrderLine", TypeCode="GDS")
        ET.SubElement(line, "LineNumber").text = str(line_number)

        extensions = ET.SubElement(line, "Extensions")
        ET.SubElement(extensions, "ProductType").text = "CUSTOM MATERIAL"

        product = ET.SubElement(line, "Product")
        ET.SubElement(product, "SuppliersProductCode").text = p.codigo
        ET.SubElement(product, "Description").text = p.descripcion

        # Lógica especial para LVL
        if "LVL" in p.descripcion.upper():
            uom = "LF"
            # Extrae el primer número entero de la unidad, sin importar el formato
            try:
                unidad_str = str(p.unidad)
                # Log para depuración
                # print(f"DEBUG unidad: {unidad_str}")
                match = re.search(r"\d+", unidad_str)
                if match:
                    amount = int(match.group())
                else:
                    amount = 1
            except Exception as e:
                # print(f"Error parseando unidad: {e}")
                amount = 1
        else:
            uom = getattr(p, 'uom', 'EA')
            amount = p.cantidad

        quantity = ET.SubElement(line, "Quantity", UOMCode=uom)
        ET.SubElement(quantity, "Amount").text = str(amount)

        line_number += 1

    section_end = ET.SubElement(orden, "OrderLine", TypeCode="SECTIONEND")
    ET.SubElement(section_end, "LineNumber").text = str(line_number)
    ET.SubElement(section_end, "Narrative").text = "MATERIAL SELECTION"

    order_total = ET.SubElement(orden, "OrderTotal")
    ET.SubElement(order_total, "GoodsValue")

    tree = ET.ElementTree(orden)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    return output_file
