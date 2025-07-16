#Esta clase representa un producto seleccionado por el usuario en el sistema.
class ProductoSeleccionado:
    def __init__(self, codigo: str, descripcion_base: str, unidad: str = "0", cantidad: int = 0, es_texto: bool = False):
        self.codigo = codigo
        self.unidad = int(unidad) if unidad.isdigit() else 0
        self.cantidad = cantidad
        self.es_texto = es_texto

        # Agregar longitud solo a productos que NO son LVL y si no es texto
        if es_texto:
            self.descripcion = descripcion_base
        elif "LVL" in descripcion_base.upper():
            self.descripcion = descripcion_base  # sin unidad
        else:
            self.descripcion = f"{descripcion_base} ({unidad})"

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "descripcion": self.descripcion,
            "cantidad": self.cantidad,
            "unidad": self.unidad,
            "es_texto": self.es_texto
        }