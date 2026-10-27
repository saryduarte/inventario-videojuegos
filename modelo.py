class Producto:
    def __init__(self, id=None, nombre="", precio=0.0, stock=0):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def _str_(self):
        return f"[{self.id}] {self.nombre} | Precio: ${self.precio:,.2f} | Stock: {self.stock}"