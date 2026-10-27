from base_datos import BaseDatos
from modelo import Producto

class ProductoDAO:

    def insertar(self, producto: Producto) -> int:
        conexion = BaseDatos.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
            (producto.nombre, producto.precio, producto.stock)
        )
        conexion.commit()
        nuevo_id = cursor.lastrowid
        conexion.close()
        return nuevo_id

    def listar_todos(self) -> list:
        conexion = BaseDatos.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, precio, stock FROM productos ORDER BY id ASC")
        filas = cursor.fetchall()
        conexion.close()

        productos = []
        for fila in filas:
            productos.append(Producto(id=fila[0], nombre=fila[1], precio=fila[2], stock=fila[3]))
        return productos

    def buscar_por_id(self, producto_id: int):
        conexion = BaseDatos.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id, nombre, precio, stock FROM productos WHERE id = ?",
            (producto_id,)
        )
        fila = cursor.fetchone()
        conexion.close()

        if fila:
            return Producto(id=fila[0], nombre=fila[1], precio=fila[2], stock=fila[3])
        return None

    def actualizar(self, producto: Producto) -> bool:
        conexion = BaseDatos.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE id = ?",
            (producto.nombre, producto.precio, producto.stock, producto.id)
        )
        conexion.commit()
        filas_afectadas = cursor.rowcount
        conexion.close()
        return filas_afectadas > 0

    def actualizar_stock(self, producto_id: int, nuevo_stock: int) -> bool:
        conexion = BaseDatos.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE productos SET stock = ? WHERE id = ?",
            (nuevo_stock, producto_id)
        )
        conexion.commit()
        filas_afectadas = cursor.rowcount
        conexion.close()
        return filas_afectadas > 0

    def eliminar(self, producto_id: int) -> bool:
        conexion = BaseDatos.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        conexion.close()
        return filas_afectadas > 0