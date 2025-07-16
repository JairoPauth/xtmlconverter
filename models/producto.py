#Esta clase representa un producto seleccionado por el usuario en el sistema.
class ProductoSeleccionado:
    def __init__(self, codigo: str, descripcion_base: str, unidad="0", cantidad: int = 0, es_texto: bool = False):
        self.codigo = codigo

        if isinstance(unidad, str) and unidad.isdigit():
            self.unidad = int(unidad)
        elif isinstance(unidad, int):
            self.unidad = unidad
        else:
            self.unidad = 0

        self.cantidad = cantidad
        self.es_texto = es_texto

        if es_texto:
            self.descripcion = descripcion_base
        elif "LVL" in descripcion_base.upper():
            self.descripcion = descripcion_base
        else:
            self.descripcion = f"{descripcion_base} ({self.unidad})"

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "descripcion": self.descripcion,
            "cantidad": self.cantidad,
            "unidad": self.unidad,
            "es_texto": self.es_texto
        }