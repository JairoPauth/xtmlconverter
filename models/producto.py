#Esta clase representa un producto seleccionado por el usuario en el sistema.
class ProductoSeleccionado:
    def __init__(self, codigo: str, descripcion_base: str, unidad: str, cantidad: int):
        self.codigo = codigo
        self.descripcion = f"{descripcion_base} ({unidad})"
        self.cantidad = cantidad

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "descripcion": self.descripcion,
            "cantidad": self.cantidad
        }
