#Esta clase representa un producto seleccionado por el usuario en el sistema.
class ProductoSeleccionado:
    def __init__(self, codigo: str, descripcion_base: str, unidad: str, cantidad: int):
        self.codigo = codigo
        self.unidad = int(unidad)
        self.cantidad = cantidad

        # Agregar longitud solo a productos que NO son LVL
        if "LVL" in descripcion_base.upper():
            self.descripcion = descripcion_base  # sin unidad
        else:
            self.descripcion = f"{descripcion_base} ({unidad})"

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "descripcion": self.descripcion,
            "cantidad": self.cantidad,
            "unidad": self.unidad
        }
