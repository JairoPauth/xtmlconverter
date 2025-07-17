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
        # Si es una línea de texto, crear un OrderLine de tipo TEXT y saltar el resto
        if getattr(p, "es_texto", False):
            line = ET.SubElement(orden, "OrderLine", TypeCode="SECTIONSTART")
            ET.SubElement(line, "LineNumber").text = str(line_number)
            ET.SubElement(line, "Narrative").text = p.descripcion
            line_number += 1
            continue  # saltamos al siguiente elemento

        # Producto normal
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
            amount = int(p.unidad) * int(p.cantidad)
            tally = f"{p.cantidad}/{p.unidad}"
        else:
            uom = getattr(p, 'uom', 'EA')
            amount = p.cantidad
            tally = None

        quantity = ET.SubElement(line, "Quantity", UOMCode=uom)
        ET.SubElement(quantity, "Amount").text = str(amount)
        if tally:
            ET.SubElement(quantity, "Tally").text = tally

        line_number += 1

    section_end = ET.SubElement(orden, "OrderLine", TypeCode="SECTIONEND")
    ET.SubElement(section_end, "LineNumber").text = str(line_number)
    ET.SubElement(section_end, "Narrative").text = "End of Material Selection"

    order_total = ET.SubElement(orden, "OrderTotal")
    ET.SubElement(order_total, "GoodsValue")

    tree = ET.ElementTree(orden)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    return output_file
