
#Esta clase representa un material disponible en el sistema.
class MaterialDisponible:
    def __init__(self, codigo: str, descripcion_base: str):
        self.codigo = codigo
        self.descripcion_base = descripcion_base

    def __str__(self):
        return f"{self.codigo} - {self.descripcion_base}"