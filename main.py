# main.py
import streamlit as st
import os
from models.material import MaterialDisponible
from models.producto import ProductoSeleccionado
from models.utils.xml_exporter import generar_xml

st.set_page_config(page_title="Custom Material XML Generator", page_icon="📐")

# Mostrar banner si existe
ruta_banner = os.path.join("static", "banner_inicio.png")
if os.path.exists(ruta_banner):
    st.image(ruta_banner, use_container_width=True)

# Título visible debajo del banner
st.title("📐 Custom Material XML pruebaaaa")

# ─── Sidebar ───────────────────────────────────────────
side = st.sidebar.radio("Menu", ("ℹ️ About", "❓ Help"))

if side == "ℹ️ About":
    st.sidebar.markdown(
        "This page allows you to generate structured XML files "
        "based on customized selections of construction materials. "
        "It is specially designed for engineers, technicians, or designers "
        "who work with modular structures and need to create material orders "
        "without relying on third-party software like Mitek for small projects."
    )
elif side == "❓ Help":
    st.sidebar.markdown(
        "For support, please contact:\n\n"
        "📧 jairo.pauth@bldr.com"
    )

# Lista de materiales disponibles
materiales = [
    {"codigo": "100LC", "descripcion_base": 'LALLY COLUMN 3 1/2"'},
    {"codigo": "10x4LC", "descripcion_base": 'LALLY COLUMN 4"'},
    {"codigo": "76x4LC", "descripcion_base": 'LALLY COLUMN 4" 11GA'},
    {"codigo": "V404", "descripcion_base": '3-1/2 X 3-1/2 2.1E 3100Fb PWT LVL'},
    {"codigo": "V406", "descripcion_base": '3-1/2 X 5-1/2 2.1E 3100Fb PWT LVL'},
    {"codigo": "V606", "descripcion_base": '5-1/4 X 5-1/4 2.1E 3100Fb PWT LVL'},
    {"codigo": "V607", "descripcion_base": '5-1/4 X 7-1/4 2.1E 3100Fb PWT LVL'},
    {"codigo": "LV07", "descripcion_base": '1-3/4x 7-1/4 2.0E 2900Fb PWT LVL 7-1/4\" PWT'},
    {"codigo": "PWTLV", "descripcion_base": '1-1/2x 7-1/4 2.0E PWT Treated LVL Dry'},
    {"codigo": "LV10", "descripcion_base": '1-3/4x 9-1/2 2.0E 2900Fb PWT LVL'},
    {"codigo": "PWTLV10", "descripcion_base": '1-3/4x 9-1/2 2.0E PWT Treated LVL Dry'},
    {"codigo": "LV09", "descripcion_base": '1-3/4x 9-1/4 2.0E 2900Fb PWT LVL'},
    {"codigo": "PWTLV09", "descripcion_base": '1-1/2x 9-1/4 2.0E PWT Treated LVL Dry'},
    {"codigo": "V410", "descripcion_base": '3.5\" x 9.5\" 2.0E 2900Fb PWT LVL'},
    {"codigo": "V610", "descripcion_base": '5.25\" x 9.5\" 2.0E 2900Fb PWT LVL'},
    {"codigo": "LV11", "descripcion_base": '1-3/4x 11-1/4 2.0E 2900Fb PWT LVL'},
    {"codigo": "PWTLV11", "descripcion_base": '1-1/2x 11-1/4 2.0E PWT Treated LVL Dry'},
    {"codigo": "LV12", "descripcion_base": '1-3/4x 11-7/8 2.0E 2900Fb PWT LVL'},
    {"codigo": "PWTLV12", "descripcion_base": '1-3/4x 11-7/8 2.0E PWT Treated LVL Dry'},
    {"codigo": "LV14", "descripcion_base": '1-3/4x 14 2.0E 2900Fb PWT LVL'},
    {"codigo": "PWTLV14", "descripcion_base": '1-3/4x 14 2.0E PWT Treated LVL Dry'},
    {"codigo": "LV16", "descripcion_base": '1-3/4x 16 2.0E 2900Fb PWT LVL'},
    {"codigo": "PWTLV16", "descripcion_base": '1-3/4x 16 2.0E PWT Treated LVL Dry'},
    {"codigo": "LV18", "descripcion_base": '1-3/4x 18 2.0E 2900Fb PWT LVL'},
    {"codigo": "LV20", "descripcion_base": '1-3/4x 20 2.0E 2900Fb PWT LVL'},
    {"codigo": "LV24", "descripcion_base": '1-3/4x 24 2.0E 2900Fb PWT LVL'}
]

if 'productos' not in st.session_state:
    st.session_state.productos = []

st.subheader("Add Product")

material_opcion = st.selectbox("Select material:", materiales)
unidad_input = st.text_input("Enter the lenght in feet (example: 2, 6, 10...)")
cantidad = st.number_input("Quantity", min_value=1, value=1, step=1)

# Validación
valid_unidad = False
unidad_limpia = ""

if st.button("Add to Order"):
    try:
        unidad_limpia = unidad_input.strip().replace("'", "").replace('"', "")
        unidad_valor = int(unidad_limpia)
        if unidad_valor % 2 != 0 or unidad_valor <= 0:
            st.error("Unit must be a positive multiple of 2 (e.g., 2, 4, 6, 8).")
        else:
            valid_unidad = True
    except ValueError:
        st.error("Unit must be a whole number in feet (e.g., 2, 4, 6, 8).")

    if valid_unidad:
        unidad_str = f"{unidad_valor}' 0\""
        producto = ProductoSeleccionado(
            codigo=material_opcion.codigo,
            descripcion_base=material_opcion.descripcion_base,
            unidad=unidad_str,
            cantidad=cantidad
        )
        st.session_state.productos.append(producto)
        st.success("Product added.")

# ─── Lista actual ───────────────────────────────────────────
st.subheader("Current Order")
if st.session_state.productos:
    for p in st.session_state.productos:
        st.write(f"{p.cantidad} x {p.codigo} - {p.descripcion}") #p.cantidad con la p. para evitar confusión con la cantidad
else:
    st.write("No products added yet.")

# ─── Exportar XML ───────────────────────────────────────────
if st.button("Generate XML"):
    path = generar_xml(st.session_state.productos)
    with open(path, "rb") as file:
        st.download_button("Download XML", file, file_name=path, mime="application/xml")

# ─── Nuevo Pedido / Reset ────────────────────────────────────
if 'reset_feedback' not in st.session_state:
    st.session_state.reset_feedback = None  # puede ser "cleared" o "empty"

if st.button("🆕 New Order"):
    if st.session_state.productos:
        st.session_state.productos = []
        st.session_state.reset_feedback = "cleared"
        st.rerun()
    else:
        st.session_state.reset_feedback = "empty"

# Mostrar feedback después de presionar el botón
if st.session_state.reset_feedback == "cleared":
    st.success("Order cleared. Ready for a new one.")
elif st.session_state.reset_feedback == "empty":
    st.info("There's nothing to clear.")