from base_datos import BaseDatos
from producto_servicio import ProductoServicio

def pedir_entero(mensaje: str) -> int:
    while True:
        entrada = input(mensaje).strip()
        try:
            return int(entrada)
        except ValueError:
            print("Entrada inválida. Debe ingresar un número entero.")

def pedir_flotante(mensaje: str) -> float:
    while True:
        entrada = input(mensaje).strip()
        try:
            return float(entrada)
        except ValueError:
            print("Entrada inválida. Debe ingresar un número decimal válido.")

def mostrar_menu():
    print("\n" + "=" * 45)
    print("      SISTEMA DE INVENTARIO DE VIDEOJUEGOS   ")
    print("=" * 45)
    print("1. Registrar videojuego")
    print("2. Mostrar inventario")
    print("3. Buscar videojuego por ID")
    print("4. Actualizar videojuego")
    print("5. Eliminar videojuego")
    print("6. Vender unidades")
    print("7. Salir")
    print("=" * 45)

def main():
    BaseDatos.crear_tabla()
    servicio = ProductoServicio()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-7): ").strip()

        if opcion == "1":
            print("\n--- REGISTRAR VIDEOJUEGO ---")
            nombre = input("Nombre del videojuego: ")
            precio = pedir_flotante("Precio unitario: ")
            stock = pedir_entero("Stock inicial: ")

            exito, mensaje, _ = servicio.registrar_producto(nombre, precio, stock)
            print(mensaje)

        elif opcion == "2":
            print("\n--- INVENTARIO ACTUAL ---")
            productos = servicio.listar_inventario()
            if not productos:
                print("El inventario está actualmente vacío.")
            else:
                print(f"{'ID':<6}{'Nombre':<30}{'Precio':<15}{'Stock':<10}")
                print("-" * 61)
                for p in productos:
                    print(f"{p.id:<6}{p.nombre:<30}${p.precio:<14,.2f}{p.stock:<10}")

        elif opcion == "3":
            print("\n--- BUSCAR VIDEOJUEGO ---")
            prod_id = pedir_entero("Ingrese el ID del producto: ")
            exito, mensaje, producto = servicio.consultar_producto(prod_id)
            if exito:
                print(f"\nDatos del producto:\nID: {producto.id}\nNombre: {producto.nombre}\nPrecio: ${producto.precio:,.2f}\nStock: {producto.stock}")
            else:
                print(mensaje)

        elif opcion == "4":
            print("\n--- ACTUALIZAR VIDEOJUEGO ---")
            prod_id = pedir_entero("Ingrese el ID del producto a modificar: ")
            exito, mensaje, producto = servicio.consultar_producto(prod_id)
            if not exito:
                print(mensaje)
                continue

            print(f"Modificando: {producto.nombre}")
            nuevo_nombre = input("Nuevo nombre: ")
            nuevo_precio = pedir_flotante("Nuevo precio: ")
            nuevo_stock = pedir_entero("Nuevo stock: ")

            exito_act, mensaje_act = servicio.actualizar_producto(prod_id, nuevo_nombre, nuevo_precio, nuevo_stock)
            print(mensaje_act)

        elif opcion == "5":
            print("\n--- ELIMINAR VIDEOJUEGO ---")
            prod_id = pedir_entero("Ingrese el ID del producto a eliminar: ")
            confirmacion = input(f"¿Está seguro de eliminar el ID {prod_id}? (s/n): ").strip().lower()
            if confirmacion == 's':
                exito, mensaje = servicio.eliminar_producto(prod_id)
                print(mensaje)
            else:
                print("Operación cancelada.")

        elif opcion == "6":
            print("\n--- VENDER UNIDADES ---")
            prod_id = pedir_entero("Ingrese el ID del videojuego a vender: ")
            cantidad = pedir_entero("Cantidad de unidades vendidas: ")
            exito, mensaje = servicio.vender_producto(prod_id, cantidad)
            print(mensaje)

        elif opcion == "7":
            print("\nCerrando el sistema. ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Por favor, digite un número entre 1 y 7.")

if __name__ == "__main__":
    main()