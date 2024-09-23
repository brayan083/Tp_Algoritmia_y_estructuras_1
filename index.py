# Lista para almacenar los productos
inventario = []

# Función para ver el inventario
def ver_inventario():
    ...
    print("Inventario:")
    print("")
    for producto in inventario:
        print(f"Código: {producto['codigo']}")
        print(f"Nombre: {producto['nombre']}")
        print(f"Cantidad: {producto['cantidad']}")
        print(f"Precio: {producto['precio']}")
        print(f"Fecha: {producto['fecha'][0]}-{producto['fecha'][1]}-{producto['fecha'][2]}")
        print(f"Proveedor: {producto['proveedor']}")
        print("---------")

# Función para agregar un producto
def agregar_producto(codigo, nombre, cantidad, precio, proveedor, fecha):
    ...
    dia, mes, anio = fecha.split("-")
    new_date = (dia, mes, anio)
    
    producto = {
        "codigo": codigo,
        "nombre": nombre,
        "cantidad": cantidad,
        "precio": precio,
        "fecha": new_date,
        "proveedor": proveedor
    }
    inventario.append(producto)

# Función para buscar un producto
def buscar_producto(codigo):
    ...
    for producto in inventario:
        if producto["codigo"] == codigo:
            return producto
    return None

# Función para actualizar la cantidad de un producto
def actualizar_cantidad(codigo, nueva_cantidad):
    ...
    producto = buscar_producto(codigo)
    if producto:
        producto["cantidad"] = nueva_cantidad
        return True
    return False


#Funcion para borrar un producto
def borrar_producto(codigo):
    inventario_nuevo = []
    for producto in inventario:
        if producto["codigo"] != codigo:
            inventario_nuevo.append(producto)
    inventario[:] = inventario_nuevo
    continuar()

# Función para mostrar el menú de opciones por pantalla
def menu_opciones():
    print("\n --------------------------------")
    print("| Menú                           |")
    print("| 1. Ver inventario              |")
    print("| 2. Agregar producto            |")
    print("| 3. Buscar producto             |")
    print("| 4. Actualizar cantidad         |")
    print("| 6. Borrar producto             |")
    print("| -1. Salir                      |")
    print(" --------------------------------\n")

# Función para continuar con la ejecución del programa
def continuar():
    input("Presione enter para continuar...")

# Función principal del programa
def main(): 
    ...
    agregar_producto("002", "Leche", 30, 29.99, 'La serenisima', "02-01-2024")
    agregar_producto("001", "Pan", 50, 15.99, 'Arcor', "01-01-2024")
    Start = True
    while Start:

        menu_opciones()
        opcion = input("Ingrese una opción: ")
        print("")
                        
        if opcion == "1":
            ver_inventario()
            continuar()
        
        if opcion == "2":
            codigo = input("Ingrese el código: ")
            nombre = input("Ingrese el nombre: ")
            cantidad = int(input("Ingrese la cantidad: "))
            precio = float(input("Ingrese el precio: "))
            fecha = input("Ingrese la fecha de vencimiento (DD-MM-YYYY): ")
            proveedor = input("Ingrese el nombre del Proveedor: ")
            agregar_producto(codigo, nombre, cantidad, precio, proveedor, fecha)
            continuar()
            
        if opcion == "3":
            codigo = input("Ingrese el código: ")
            producto = buscar_producto(codigo)
            if producto:
                print(f"Producto encontrado: {producto['nombre']}")
            else:
                print("Producto no encontrado")
            continuar()
        
        if opcion == "4":
            codigo = input("Ingrese el código: ")
            nueva_cantidad = int(input("Ingrese la nueva cantidad: "))
            if actualizar_cantidad(codigo, nueva_cantidad):
                print("Cantidad actualizada")
            else:
                print("Producto no encontrado")
            continuar()    
        
        #Opcion de borrado por codigo
        if opcion == "6":
            codigo = input("Ingrese el código: ")
            borrar_producto(codigo)
            
        if opcion == "-1":
            Start = False
            print("Saliendo del programa... ¡Hasta luego!")
        
        if int(opcion) not in range(1, 5) and opcion != "-1":
            print("Opción inválida")
            
main()

# Estructura de datos:
# [
#     {
#         'codigo': '3', 
#         'nombre': 'pan', 
#         'cantidad': 12, 
#         'precio': 20.0,
#         'proveedor': 'Panaderia UADE'
#     },
#     {
#         'codigo': '2', 
#         'nombre': 'leche', 
#         'cantidad': 5, 
#         'precio': 15.0,
#         'proveedor': 'UADE cuando es epoca de parcial'
#     }
# ]