import json
import os
from datetime import datetime
from tabulate import tabulate

# Ruta del archivo JSON
archivo_inventario = 'inventario_V2.json'

# Función para cargar el inventario desde el archivo JSON
def cargar_inventario():
    try:
        with open(archivo_inventario, 'r', encoding='UTF-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"productos": {}, "metadata": {}, "proveedores": {}}

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
        "categoria": "General",  #se puede cambiar esta categoria predeterminada
        "cantidad": {"valor": cantidad, "unidad": "unidad"},
        "precio": {"valor": precio, "moneda": "ARS"},
        "proveedor_id": proveedor,
        "fecha_vencimiento": fecha,
        "fecha_ultima_actualizacion": formatear(procesar_fecha("01-01-2024"))
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

# Funcion para buscar un producto
def buscar_producto(id_producto):
    inventario = cargar_inventario()
    productos = inventario['productos']
    #divide la busqueda en palabras clave
    palabras_clave = id_producto.lower().split()

    #busca productos que tengan alguna de las palabras clave en su nombre o codigo
    encontrados = {}
    for codigo, producto in productos.items():
        nombre_producto = producto['nombre'].lower()
        
        #verifica si alguna palabra clave esta en el codigo o nombre
        if any(palabra in nombre_producto for palabra in palabras_clave) or any(palabra in codigo.lower() for palabra in palabras_clave):
            encontrados[codigo] = producto

    #muestra ugerencias de busqueda si no se encuentra un resultado
    if not encontrados:
        print("No se encontró ningún producto exacto. Mostrando sugerencias similares:")
        sugerencias = {}
        #sugerencias basadas en las palabras clave
        for codigo, producto in productos.items():
            nombre_producto = producto['nombre'].lower()
            if any(palabra in nombre_producto for palabra in palabras_clave) or any(palabra in codigo.lower() for palabra in palabras_clave):
                sugerencias[codigo] = producto
        if sugerencias:
            mostrar_tabla(sugerencias)
        else:
            print("No hay productos que coincidan con la búsqueda.")
    else:
        print("Resultados de la búsqueda:")
        mostrar_tabla(encontrados)

# Funcion que muestra los productos en una tabla usando la lib tabulate y agrega paginacion
def mostrar_tabla(productos, page_size=5):
    headers = ["Código", "Nombre", "Cantidad", "Precio (ARS)", "Proveedor", "Fecha de Vencimiento"]
    datos = [[codigo, producto["nombre"], producto["cantidad"]["valor"],
              producto["precio"]["valor"], producto["proveedor_id"], producto["fecha_vencimiento"]]
             for codigo, producto in productos.items()]
    
    #paginacion
    total_paginas = (len(datos) + page_size - 1) // page_size  #calcula numero de páginas
    for page in range(total_paginas):
        inicio = page * page_size
        fin = inicio + page_size
        print(tabulate(datos[inicio:fin], headers=headers, tablefmt="grid"))
        
        if page < total_paginas - 1:
            continuar_pagina = input("Mostrar siguiente página? (s/n): ")
            if continuar_pagina.lower() != "s":
                break  
    mostrar_resumen(productos)

# Funcion que muestra un resumen de los productos encontrados
def mostrar_resumen(productos):
    total_productos = len(productos)
    valor_total = sum(producto["precio"]["valor"] * producto["cantidad"]["valor"] for producto in productos.values())
    print("\nResumen:")
    print(f"Total de productos encontrados: {total_productos}")
    print(f"Valor total de los productos: ARS {valor_total:.2f}")

# Función para buscar un producto por nombre o código
def Buscarpalabras(palabra):
    inventario = cargar_inventario()
    productosencontrados = [(codigo, producto) for codigo, producto in inventario['productos'].items() 
                            if codigo == palabra or producto['nombre'] == palabra]
    if productosencontrados: 
        return productosencontrados
    return None

# Función para actualizar la cantidad de un producto
def actualizar_cantidad(codigo, nueva_cantidad):
    inventario = cargar_inventario()
    productos = inventario['productos']

    if codigo in productos:
        productos[codigo]["cantidad"]["valor"] = nueva_cantidad
        nombre_producto = productos[codigo]["nombre"]  #guarda el nombre del producto
        guardar_inventario(inventario)
        return nombre_producto
    return None

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
    total_productos = len(inventario['productos'])
    print(f"Total de productos en el inventario: {total_productos}")

# Función para calcular el valor total del inventario
def reporte_valor_inventario():
    inventario = cargar_inventario()
    valor_total = sum(producto['precio']['valor'] * producto['cantidad']['valor'] 
                      for producto in inventario ['productos'].values())
    print(f"Valor total del inventario: ${valor_total:.2f}")

# Función para contar el número total de unidades de productos
def reporte_total_unidades():
    inventario = cargar_inventario()
    total_unidades = sum(producto['cantidad']['valor'] for producto in inventario['productos'].values())
    print(f"Total de unidades en el inventario: {total_unidades}")

# Función para mostrar productos por proveedor
def reporte_productos_por_proveedor(proveedor):
    inventario = cargar_inventario()
    #convierte el nombre del proveedor ingresado a minusculas
    proveedor = proveedor.lower()
    #filtra los productos por proveedor usando un diccionario y usando .lower() en el id del proveedor de cada producto
    productos_proveedor = {
        codigo: producto 
        for codigo, producto in inventario['productos'].items() 
        if producto['proveedor_id'].lower() == proveedor
    }

    if productos_proveedor:
        print(f"Productos del proveedor {proveedor.capitalize()}:")
        mostrar_tabla(productos_proveedor)
    else:
        print(f"No se encontraron productos del proveedor {proveedor.capitalize()}")

# Función para mostrar los productos más caros
def reporte_productos_mas_caros():
    inventario = cargar_inventario()
    productos_mas_caros = dict(sorted(inventario['productos'].items(), key=lambda x: x[1]['precio']['valor'], reverse=True)[:5])

    if productos_mas_caros:
        print(f"Top 5 productos más caros:")
        mostrar_tabla(productos_mas_caros)
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
        os.system('cls' if os.name == 'nt' else 'clear') #limpia la pantalla
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
            id_producto = input("Ingrese el código o el nombre: ")
            buscar_producto(id_producto)
            continuar()
            
        if opcion == "4":
            codigo = input("Ingrese el código: ")
            nueva_cantidad = int(input("Ingrese la nueva cantidad: "))
            nombre_producto = actualizar_cantidad(codigo, nueva_cantidad)

            if nombre_producto:
                print(f"Cantidad del producto '{nombre_producto}' actualizada a {nueva_cantidad} unidades.")
            else:
                print("Producto no encontrado")
            continuar()   
            
        if opcion == "5":
            bandera = True
            while bandera:
                menu_reportes()
                opcion_reporte = input("Ingrese una opción de reporte: ")
                os.system('cls' if os.name == 'nt' else 'clear') #limpia la pantalla
                print("")
                
                if opcion_reporte == "1":
                    reporte_total_productos()
                    continuar()
                
                elif opcion_reporte == "2":
                    reporte_valor_inventario()
                    continuar()
                
                elif opcion_reporte == "3":
                    reporte_total_unidades()
                    continuar()
                
                elif opcion_reporte == "4":
                    proveedor = input("Ingrese el nombre del proveedor: ")
                    reporte_productos_por_proveedor(proveedor)
                    continuar()
                    
                elif opcion_reporte == "5":
                    reporte_productos_mas_caros()
                    continuar()
                
                elif opcion_reporte == "-1":
                    bandera = False
                
                else:
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
