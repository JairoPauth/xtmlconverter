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
st.title("📐 Custom Material XML")

# ─── Sidebar ───────────────────────────────────────────
side = st.sidebar.radio("Menu", ("ℹ️ About", "❓ Help", "⚠️ Limitations"))

if side == "ℹ️ About":
    st.sidebar.markdown(
        "This page allows you to generate structured XML files "
        "based on customized selections of construction materials. "
        "It is specially designed for engineers, technicians, or designers "
        "who work with modular structures and need to create material orders "
        "without relying on third-party software like Mitek for small projects. "
        "The main goal is to optimize time and efficiency in beam calculation projects for the New England team."
    )

elif side == "❓ Help":
    st.sidebar.markdown(
        "For support, please contact:\n\n"
        "📧 jairo.pauth@bldr.com"
    )

elif side == "⚠️ Limitations":
    st.sidebar.markdown(
        "### ⚠️ Current Limitations\n"
        "- Hangers are **not included** in this version.\n"
        "- Hangers must be added **manually** based on the project's needs.\n"
        "- Only supports a predefined list of structural materials.\n"
        "- Not integrated yet with MiTek or any external systems.\n"
        "- No automatic unit validation for custom materials beyond the default list."
    )

class MaterialDisponible:
    def __init__(self, codigo, descripcion_base):
        self.codigo = codigo
        self.descripcion = descripcion_base

# Lista de materiales disponibles
materiales = [
    MaterialDisponible("TEXT", 'TEXT LINE'),
    MaterialDisponible("76LC", 'LALLY COLUMN 3 1/2 (07 06 ft)"'),
    MaterialDisponible("80LC", 'LALLY COLUMN 3 1/2 (8ft)"'),
    MaterialDisponible("100LC", 'LALLY COLUMN 3 1/2 (10ft)"'),
    MaterialDisponible("120LC", 'LALLY COLUMN 3 1/2 (12ft)"'),
    MaterialDisponible("10x4LC", 'LALLY COLUMN 4"'),
    MaterialDisponible("76x4LC", 'LALLY COLUMN 4" 11GA'),
    MaterialDisponible("68LCP", '6" X 8" SPRINGFIELD PLATE FOR 3 -1/2" DIA.COLUMN'),
    MaterialDisponible("68LCP4", '6" X 8" SPRINGIELD PLATE FOR 4" DIA.COLUMN'),
    MaterialDisponible("V404", '3-1/2 X 3-1/2 2.1E 3100Fb PWT LVL'),
    MaterialDisponible("V406", '3-1/2 X 5-1/2 2.1E 3100Fb PWT LVL'),
    MaterialDisponible("V407", '3-1/2 X 7-1/4 2.1E 3100Fb PWT LVL'),
    MaterialDisponible("V606", '5-1/2 X 5-1/4 2.1E 3100Fb PWT LVL'),
    MaterialDisponible("V607", '5-1/4 X 7-1/4 2.1E 3100Fb PWT LVL'),
    MaterialDisponible("LV06", '1-3/4x 5-1/2 2.0E 2900Fb PWT LVL'),
    MaterialDisponible("LV07", '1-3/4x 7-1/4 2.0E 2900Fb PWT LVL 7-1/4" PWT'),
    MaterialDisponible("PWTLV", '1-1/2x 7-1/4 2.0E PWT Treated LVL Dry'),
    MaterialDisponible("LV10", '1-3/4x 9-1/2 2.0E 2900Fb PWT LVL'),
    MaterialDisponible("PWTLV10", '1-3/4x 9-1/2 2.0E PWT Treated LVL Dry'),
    MaterialDisponible("LV09", '1-3/4x 9-1/4 2.0E 2900Fb PWT LVL'),
    MaterialDisponible("PWTLV09", '1-1/2x 9-1/4 2.0E PWT Treated LVL Dry'),
    MaterialDisponible("V410", '3.5" x 9.5" 2.0E 2900Fb PWT LVL'),
    MaterialDisponible("V610", '5.25" x 9.5" 2.0E 2900Fb PWT LVL'),
    MaterialDisponible("LV11", '1-3/4x 11-1/4 2.0E 2900Fb PWT LVL'),
    MaterialDisponible("PWTLV11", '1-1/2x 11-1/4 2.0E PWT Treated LVL Dry'),
    MaterialDisponible("LV12", '1-3/4x 11-7/8 2.0E 2900Fb PWT LVL'),
    MaterialDisponible("PWTLV12", '1-3/4x 11-7/8 2.0E PWT Treated LVL Dry'),
    MaterialDisponible("LV14", '1-3/4x 14 2.0E 2900Fb PWT LVL'),
    MaterialDisponible("PWTLV14", '1-3/4x 14 2.0E PWT Treated LVL Dry'),
    MaterialDisponible("LV16", '1-3/4x 16 2.0E 2900Fb PWT LVL'),
    MaterialDisponible("PWTLV16", '1-3/4x 16 2.0E PWT Treated LVL Dry'),
    MaterialDisponible("LV18", '1-3/4x 18 2.0E 2900Fb PWT LVL'),
    MaterialDisponible("LV20", '1-3/4x 20 2.0E 2900Fb PWT LVL'),
    MaterialDisponible("LV24", '1-3/4x 24 2.0E 2900Fb PWT LVL'),
]

st.subheader("Add Item to Order")

# ─── Selección de Material ───────────────────────────────────────────
# NUEVO: usamos st.session_state para mantener la selección entre recargas
if 'material_opcion' not in st.session_state:
    st.session_state.material_opcion = materiales[0]  # default al primero de la lista

# NUEVO: selectbox con key para recordar la opción seleccionada
material_opcion = st.selectbox(
    "Select Material or Insert Narrative",
    materiales,
    format_func=lambda m: m.descripcion,
    key="material_select"  # clave para mantener la selección
)

# ─── Manejo de Text Line ─────────────────────────────────────────────
if material_opcion.codigo == "TEXT":
    texto_narrativo = st.text_input("Enter text Line")
    
    # Usamos el mismo botón que ya tenías
    if st.button("Add to Order"):
        if texto_narrativo.strip():
            producto_texto = ProductoSeleccionado(
                codigo="",  # sin código
                descripcion_base=texto_narrativo,
                unidad="0",
                cantidad=0,
                es_texto=True
            )
            # NUEVO: inicializa lista si no existe
            if 'productos' not in st.session_state:
                st.session_state.productos = []
            st.session_state.productos.append(producto_texto)
            st.success("Narrative line added.")
        else:
            st.warning("Please enter some text.")

# ─── Manejo de Productos Normales ────────────────────────────────────
else:
    unidad_input = st.text_input("Enter the length in feet (example: 10...)")
    cantidad = st.number_input("Quantity", min_value=1, value=1, step=1)

    # Usamos el mismo botón que ya tenías
    if st.button("Add to Order"):
        try:
            unidad_valor = int(unidad_input.strip())
            if unidad_valor <= 0 or unidad_valor % 2 != 0:
                st.write("⚠️ Unit must be a positive multiple of 2 (e.g., 8, 10).")
            else:
                producto = ProductoSeleccionado(
                    codigo=material_opcion.codigo,
                    descripcion_base=material_opcion.descripcion,
                    unidad=unidad_valor,
                    cantidad=cantidad
                )
                # NUEVO: inicializa lista si no existe
                if 'productos' not in st.session_state:
                    st.session_state.productos = []
                st.session_state.productos.append(producto)
                st.success("Product added.")
        except ValueError:
            st.write("⚠️ Unit must be a whole number in feet (e.g., 2, 4, 6, 8).")


# ─── Lista actual ───────────────────────────────────────────
# Asegurarse de que 'productos' exista
if 'productos' not in st.session_state:
    st.session_state.productos = []

# Luego puedes usarlo sin error
st.subheader("Current Order")
if st.session_state.productos:
    for p in st.session_state.productos:
        if getattr(p, "es_texto", False):
            st.markdown(f"📝 *{p.descripcion}*")
        else:
            st.write(f"{p.cantidad} x {p.codigo} - {p.descripcion}")
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