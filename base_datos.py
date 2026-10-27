import sqlite3

class BaseDatos:
    DB_NAME = "inventario_videojuegos.db"

    @classmethod
    def obtener_conexion(cls):
        """Retorna una nueva conexión a la base de datos SQLite."""
        conexion = sqlite3.connect(cls.DB_NAME)
        return conexion

    @classmethod
    def crear_tabla(cls):
        """Crea la tabla productos si no existe."""
        conexion = cls.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                stock INTEGER NOT NULL
            )
        """)
        conexion.commit()
        conexion.close()