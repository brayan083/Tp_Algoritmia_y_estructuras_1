# Lista para almacenar los productos
inventario = []

# Set para almacenar los códigos de productos únicos
codigos_unicos = set()

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
    if codigo in codigos_unicos:
        print("Error: El código del producto ya existe.")
        return
    
    dia, mes, anio = fecha.split("-")
    new_date = (dia, mes, anio)
    
    producto = {
        "codigo": codigo,
        "nombre": nombre.capitalize(),
        "cantidad": cantidad,
        "precio": precio,
        "fecha": new_date,
        "proveedor": proveedor.capitalize()
    }
    inventario.append(producto)
    codigos_unicos.add(codigo)

# Función para buscar un producto
def buscar_producto(codigo):
    ...
    for producto in inventario:
        if producto["codigo"] == codigo:
            return producto
    return None

# Función para buscar un producto por nombre o código
def Buscarpalabras(palabra):
    productosencontrados = [producto for producto in inventario if producto['nombre'] == palabra or producto["codigo"] == palabra]
    if productosencontrados: 
        return productosencontrados
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
    
# Función para contar el número total de productos en el inventario
def reporte_total_productos():
    total_productos = len(inventario)
    print(f"Total de productos en el inventario: {total_productos}")

# Función para calcular el valor total del inventario
def reporte_valor_inventario():
    valor_total = sum(producto['precio'] * producto['cantidad'] for producto in inventario)
    print(f"Valor total del inventario: ${valor_total:.2f}")

# Función para contar el número total de unidades de productos
def reporte_total_unidades():
    total_unidades = sum(producto['cantidad'] for producto in inventario)
    print(f"Total de unidades en el inventario: {total_unidades}")

# Función para mostrar productos por proveedor
def reporte_productos_por_proveedor(proveedor):
    productos_proveedor = [producto for producto in inventario if producto['proveedor'] == proveedor]
    if productos_proveedor:
        print(f"Productos del proveedor {proveedor}:")
        for producto in productos_proveedor:
            print(f"Código: {producto['codigo']}, Nombre: {producto['nombre']}, Cantidad: {producto['cantidad']}, Precio: {producto['precio']}")
    else:
        print(f"No se encontraron productos del proveedor {proveedor}")

# Función para mostrar los productos más caros
def reporte_productos_mas_caros():
    productos_mas_caros = sorted(inventario, key=precio_producto, reverse=True)[:5]
    if productos_mas_caros:
        print(f"Top 5 productos más caros:")
        for producto in productos_mas_caros:
            print(f"Código: {producto['codigo']}, Nombre: {producto['nombre']}, Precio: {producto['precio']}")
    else:
        print(f"No se encontraron productos")

def precio_producto(producto):
    return producto['precio']


# Función para mostrar el menú de opciones por pantalla
def menu_opciones():
    print("\n --------------------------------")
    print("| Menú                           |")
    print("| 1. Ver inventario              |")
    print("| 2. Agregar producto            |")
    print("| 3. Buscar producto             |")
    print("| 4. Actualizar cantidad         |")
    print("| 5. Reportes                    |")
    print("| 6. Borrar producto             |")
    print("| -1. Salir                      |")
    print(" --------------------------------\n")

# Función para mostrar el submenú de reportes
def menu_reportes():
    print("\n --------------------------------")
    print("| Reportes                       |")
    print("| 1. Total de productos          |")
    print("| 2. Valor total del inventario  |")
    print("| 3. Total de unidades           |")
    print("| 4. Productos por proveedor     |")
    print("| 5. Top 5 Productos más caros   |")
    print("| -1. Volver al menú principal   |")
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
        
        if opcion == "3": #Buscar producto
            codigo = input("Ingrese el código: ")
            producto = Buscarpalabras(codigo) #me devuelve una lista con los productosencontrados
            #
            # print(producto) #imprime lista
            if producto: #?
                print(f"Producto encontrado:")
                for i in producto: #va pasando i por i agarrando diccionarios completos
                    for clave,valor in i.items(): #agarra el diccionario de i en esa posicion y la muestra
                        print(f"{clave.capitalize()}: {valor}")
                continuar()
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
            
        if opcion == "5":
            bandera = True
            while bandera:
                menu_reportes()
                opcion_reporte = input("Ingrese una opción de reporte: ")
                print("")
                
                if opcion_reporte == "1":
                    reporte_total_productos()
                    continuar()
                
                if opcion_reporte == "2":
                    reporte_valor_inventario()
                    continuar()
                
                if opcion_reporte == "3":
                    reporte_total_unidades()
                    continuar()
                
                if opcion_reporte == "4":
                    proveedor = input("Ingrese el nombre del proveedor: ")
                    reporte_productos_por_proveedor(proveedor)
                    continuar()
                    
                if opcion_reporte == "5":
                    reporte_productos_mas_caros()
                    continuar()
                
                if opcion_reporte == "-1":
                    bandera = False
                
                if int(opcion_reporte) not in range(1, 4) and opcion_reporte != "-1":
                    print("Opción inválida")

        
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

# Estructura de datos de ejemplo:
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