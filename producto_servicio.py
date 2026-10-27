from modelo import Producto
from producto_dao import ProductoDAO

class ProductoServicio:
    def __init__(self):
        self.dao = ProductoDAO()

    def registrar_producto(self, nombre: str, precio: float, stock: int):
        nombre_limpio = nombre.strip()
        if not nombre_limpio:
            return False, "Error: El nombre del videojuego no puede estar vacío.", None
        if precio <= 0:
            return False, "Error: El precio debe ser un número mayor a cero.", None
        if stock < 0:
            return False, "Error: La cantidad de stock inicial no puede ser negativa.", None

        nuevo_producto = Producto(nombre=nombre_limpio, precio=precio, stock=stock)
        nuevo_id = self.dao.insertar(nuevo_producto)
        nuevo_producto.id = nuevo_id
        return True, f"Videojuego '{nuevo_producto.nombre}' registrado con éxito con el ID {nuevo_id}.", nuevo_producto

    def listar_inventario(self):
        productos = self.dao.listar_todos()
        return productos

    def consultar_producto(self, producto_id: int):
        if producto_id <= 0:
            return False, "Error: El ID debe ser un número entero positivo.", None

        producto = self.dao.buscar_por_id(producto_id)
        if not producto:
            return False, f"El videojuego con ID {producto_id} no existe en el sistema.", None
        return True, "Producto encontrado.", producto

    def actualizar_producto(self, producto_id: int, nuevo_nombre: str, nuevo_precio: float, nuevo_stock: int):
        exito, msg, producto_existente = self.consultar_producto(producto_id)
        if not exito:
            return False, msg

        nombre_limpio = nuevo_nombre.strip()
        if not nombre_limpio:
            return False, "Error: El nombre no puede estar vacío."
        if nuevo_precio <= 0:
            return False, "Error: El precio debe ser mayor a cero."
        if nuevo_stock < 0:
            return False, "Error: El stock no puede ser negativo."

        producto_existente.nombre = nombre_limpio
        producto_existente.precio = nuevo_precio
        producto_existente.stock = nuevo_stock

        if self.dao.actualizar(producto_existente):
            return True, f"Videojuego con ID {producto_id} actualizado con éxito."
        return False, "No se pudo actualizar el registro en la base de datos."

    def eliminar_producto(self, producto_id: int):
        exito, msg, _ = self.consultar_producto(producto_id)
        if not exito:
            return False, msg

        if self.dao.eliminar(producto_id):
            return True, f"Videojuego con ID {producto_id} eliminado exitosamente."
        return False, "No se pudo eliminar el registro de la base de datos."

    def vender_producto(self, producto_id: int, cantidad: int):
        if cantidad <= 0:
            return False, "Error: La cantidad a vender debe ser mayor a cero."

        exito, msg, producto = self.consultar_producto(producto_id)
        if not exito:
            return False, msg

        if cantidad > producto.stock:
            return False, f"Venta rechazada: Stock insuficiente. Hay {producto.stock} unidades disponibles e intentaste vender {cantidad}."

        nuevo_stock = producto.stock - cantidad
        if self.dao.actualizar_stock(producto_id, nuevo_stock):
            return True, f"Venta exitosa: Se vendieron {cantidad} unidad(es). Stock restante: {nuevo_stock}."
        return False, "No se pudo procesar la venta en la base de datos."