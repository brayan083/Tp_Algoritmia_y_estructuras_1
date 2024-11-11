import json
import os
from datetime import datetime

# Ruta del archivo JSON
archivo_inventario = 'inventario_V2.json'

# Función para cargar el inventario desde el archivo JSON
def cargar_inventario():
    try:
        with open(archivo_inventario, 'r', encoding='UTF-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"productos": {}, "metadata": {}, "proveedores": {}} #"productos": {}, "proveedores": {}, "metadata": {"total_productos": 0}

#Función para guardar el inventario en el archivo JSON
def guardar_inventario(inventario):
    try:
        with open(archivo_inventario, 'w', encoding='UTF-8') as file:
            json.dump(inventario, file, indent=4)
    except IOError as e:
        print(f"Error al guardar el inventario: {e}")

#crea un codigo unico para cada producto
def generar_codigo_unico(inventario):
    codigo_base = 1000
    total_productos = inventario['metadata'].get("total_productos", 0)
    return str(codigo_base + total_productos + 1)

# Función para validar campos del producto
def validar_campos(cantidad, precio, fecha):
    try:
        cantidad = int(cantidad)
        if cantidad < 0:
            raise ValueError("La cantidad debe ser un número positivo")
    except ValueError as e:
        print(f"Error: {e}")
        return False

    try:
        precio = float(precio)
        if precio < 0:
            raise ValueError("El precio debe ser un valor positivo")
    except ValueError as e:
        print(f"Error: {e}")
        return False

    if not es_fecha_valida(fecha):
        print("Error: La fecha de vencimiento es inválida")
        return False

    return True

#Función para ver el inventario
def ver_inventario(cargar_inventario):
    inventario = cargar_inventario()
    print("Inventario actual:")
    for codigo, producto in inventario["productos"].items():
        print(f"Código: {codigo}")
        print(f"Nombre: {producto['nombre']}")
        print(f"Categoría: {producto['categoria']}")
        print(f"Cantidad: {producto['cantidad']['valor']} {producto['cantidad']['unidad']}")
        print(f"Precio: {producto['precio']['valor']} {producto['precio']['moneda']}")
        print(f"Proveedor ID: {producto['proveedor_id']}")
        print(f"Fecha de vencimiento: {producto['fecha_vencimiento']}")
        print(f"Última actualización: {producto['fecha_ultima_actualizacion']}")
        print("-" * 30)

    print("\nMetadatos del inventario:")
    print(f"Versión: {inventario['metadata']['version']}")
    print(f"Última actualización: {inventario['metadata']['ultima_actualizacion']}")
    print(f"Total de productos: {inventario['metadata']['total_productos']}")
    print(f"Total de proveedores: {inventario['metadata']['total_proveedores']}")
    print(f"Valor total del inventario: {inventario['metadata']['valor_total_inventario']} {inventario['productos'][next(iter(inventario['productos']))]['precio']['moneda']}")

    print("\nInformación de proveedores:")
    for prov_id, proveedor in inventario["proveedores"].items():
        print(f"ID: {prov_id}")
        print(f"Nombre: {proveedor['nombre']}")
        print(f"Dirección: {proveedor['direccion']}")
        print(f"Teléfono: {proveedor['telefono']}")
        print(f"Email: {proveedor['email']}")
        print("-" * 30)

def agregar_producto(nombre, cantidad, precio, proveedor, fecha):
    inventario = cargar_inventario()
    
    #crea un codigo unico para cada prod
    codigo = generar_codigo_unico(inventario)
    
    #validar precio y cantidad
    if not validar_campos(cantidad, precio, fecha):
        return
    
    if not es_fecha_valida(fecha):
        print("La fecha de vencimiento no es válida.")
        return
    
    #formatea la fecha de vencimiento
    fecha = formatear(procesar_fecha(fecha))
    
    producto = {
        "nombre": nombre.capitalize(),
        "categoria": "General",  # Puedes cambiar esta categoría predeterminada si es necesario
        "cantidad": {"valor": cantidad, "unidad": "unidad"},  # Asumimos "unidad" como predeterminada
        "precio": {"valor": precio, "moneda": "ARS"},  # Asumimos USD como moneda predeterminada
        "proveedor_id": proveedor,
        "fecha_vencimiento": fecha,
        "fecha_ultima_actualizacion": formatear(procesar_fecha("01-01-2024"))  # Asignar fecha de actualización
    }
    
    inventario["productos"][codigo] = producto
    
    inventario["metadata"]["total_productos"] = len(inventario["productos"])
    
    guardar_inventario(inventario)
    print(f"Producto '{nombre}' agregado exitosamente con el código {codigo}.")

def es_bisiesto(anio):
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

def es_fecha_valida(fecha):
    dia, mes, anio = procesar_fecha(fecha)
    dia = int(dia)
    mes = int(mes)
    anio = int(anio)

    dias_por_mes = [31, 29 if es_bisiesto(anio) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if not (1 <= mes <= 12):
        return False

    if not (1 <= dia <= dias_por_mes[mes - 1]):
        return False

    return True

def procesar_fecha(fecha):
    if fecha.find('-') != -1:
        dia, mes, anio = fecha.split("-")
    elif fecha.find('/') != -1:
        dia, mes, anio = fecha.split("/")
    elif fecha.find(' ') != -1:
        dia, mes, anio = fecha.split(" ")

    return (dia, mes, anio)

def formatear(valor):
    if isinstance(valor, tuple): #isinstance compara el tipo de "valor" con el tipo tupla
        return f'{valor[0]}-{valor[1]}-{valor[2]}'#si coincide entra y la formatea a un valor de tipo fecha
    return f'{valor}'

# Función para buscar un producto
def buscar_producto(codigo):
    ...
    inventario = cargar_inventario()
    for producto in inventario:
        if producto["codigo"] == codigo:
            return producto
    return None

# Función para buscar un producto por nombre o código
def Buscarpalabras(palabra):
    inventario = cargar_inventario()
    productosencontrados = [(codigo, producto) for codigo, producto in inventario['productos'].items() if codigo == palabra or producto['nombre'] == palabra]
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
def borrar_producto(dato): 
    inventario = cargar_inventario()
    
    producto_eliminar = Buscarpalabras(dato)
    if producto_eliminar == None:
        print("Producto no encontrado")
        continuar()
        return
    
    confirmar = int(input(f"¿Desea eliminar el producto {producto_eliminar}? 1 para SI, 2 para NO: "))
    if confirmar == 1:
        inventario_nuevo = []
        for producto in inventario:
            if producto["codigo"] != dato and producto["nombre"] != dato:
                inventario_nuevo.append(producto)
        inventario[:] = inventario_nuevo
        continuar()
    
# Función para contar el número total de productos en el inventario
def reporte_total_productos():
    inventario = cargar_inventario()
    total_productos = len(inventario)
    print(f"Total de productos en el inventario: {total_productos}")

# Función para calcular el valor total del inventario
def reporte_valor_inventario():
    inventario = cargar_inventario()
    valor_total = sum(producto['precio'] * producto['cantidad'] for producto in inventario)
    print(f"Valor total del inventario: ${valor_total:.2f}")

# Función para contar el número total de unidades de productos
def reporte_total_unidades():
    inventario = cargar_inventario()
    total_unidades = sum(producto['cantidad'] for producto in inventario)
    print(f"Total de unidades en el inventario: {total_unidades}")

# Función para mostrar productos por proveedor
def reporte_productos_por_proveedor(proveedor):
    inventario = cargar_inventario()
    productos_proveedor = [producto for producto in inventario if producto['proveedor'] == proveedor]
    if productos_proveedor:
        print(f"Productos del proveedor {proveedor}:")
        for producto in productos_proveedor:
            print(f"Código: {producto['codigo']}, Nombre: {producto['nombre']}, Cantidad: {producto['cantidad']}, Precio: {producto['precio']}")
    else:
        print(f"No se encontraron productos del proveedor {proveedor}")

# Función para mostrar los productos más caros
def reporte_productos_mas_caros():
    inventario = cargar_inventario()
    productos_mas_caros = sorted(inventario, key=precio_producto, reverse=True)[:5]
    if productos_mas_caros:
        print(f"Top 5 productos más caros:")
        for producto in productos_mas_caros:
            print(f"Código: {producto['codigo']}, Nombre: {producto['nombre']}, Precio: {producto['precio']}")
    else:
        print(f"No se encontraron productos")

def precio_producto(producto):
    return producto['precio']

def validar_producto():
    while(True):
        nombre = input("Ingrese el nombre: ")
        if Buscarpalabras(nombre) is None:
            return nombre
        print('\nEl nombre ya existe!\n')

def validar_fecha():
    while(True):
        fecha = input("Ingrese la fecha de vencimiento (DD-MM-YYYY): ")
        if es_fecha_valida(fecha):
            return fecha
        print('\nLa fecha es invalida!\n')

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
    os.system('cls' if os.name == 'nt' else 'clear') #limpia la pantalla para windows y mac

# Función principal del programa
def main(): 
    ...
    Start = True
    while Start:

        menu_opciones()
        opcion = input("Ingrese una opción: ")
        os.system('cls') #limpia la pantalla
        print("")
                        
        if opcion == "1":
            ver_inventario(cargar_inventario)
            continuar()
        
        if opcion == "2":
            nombre = validar_producto()
            cantidad = int(input("Ingrese la cantidad: "))
            precio = float(input("Ingrese el precio: "))
            fecha = validar_fecha() #se valida la fecha de vencimiento
            proveedor = input("Ingrese el nombre del Proveedor: ")
            agregar_producto(nombre, cantidad, precio, proveedor, fecha) #Codigo no se envia
            continuar()
        
        if opcion == "3": #Buscar producto
            codigo = input("Ingrese el código o el nombre: ")
            producto = Buscarpalabras(codigo) #me devuelve una lista con los productosencontrados
            if producto: 
                print(f"Producto encontrado:")
                #print(producto)
                for clave, valor in producto: #va pasando i por i agarrando diccionarios completos
                    #for clave,valor in i: #agarra el diccionario de i en esa posicion y la muestra
                        print(f"{clave.capitalize()}:")
                        for subclave, subvalor in valor.items():
                            print(f"  {subclave.capitalize()}: {subvalor}")  # Agregar sangría para mejor legibilidad
                        print()  # Salto de línea después de cada grupo de subclaves
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
                os.system('cls') #limpia la pantalla
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
                
                if int(opcion_reporte) not in range(1, 5) and opcion_reporte != "-1":
                    print("Opción inválida")
            
            continuar()
                 
        #Opcion de borrado por codigo
        if opcion == "6":
            metodo = input("Ingrese el código o nombre del producto a eliminar: ")
            borrar_producto(metodo)
           
        # Op 
        if opcion == "-1":
            Start = False
            print("Saliendo del programa... ¡Hasta luego!")
        
        if int(opcion) not in range(1, 5) and opcion != "-1":
            print("Opción inválida")
            
main()
