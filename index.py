from datetime import datetime
import json
import os
from tabulate import tabulate 

# Ruta del archivo JSON
archivo_inventario = 'inventario_V2.json'

# Función para cargar e inventario desde el archivo JSON
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

    if not inventario["productos"]:
        print("No hay productos en el inventario.")
        return
    
    print("Inventario actual:")
    headers_productos = ["Código", "Nombre", "Categoría", "Cantidad", "Precio (ARS)", "Proveedor", "Fecha de Vencimiento"]
    datos_productos = [[codigo, producto["nombre"], producto["categoria"], 
                        f"{producto['cantidad']['valor']} {producto['cantidad']['unidad']}",
                        producto["precio"]["valor"], producto["proveedor_id"], producto["fecha_vencimiento"]]
                       for codigo, producto in inventario["productos"].items()]
    mostrar_tabla(datos_productos, headers_productos)

    print("\nMetadatos del inventario:")
    headers_metadatos = ["Metadatos", "Valores"]
    datos_metadatos = [
        ["Versión", inventario['metadata'].get('version', 'N/A')],
        ["Última actualización", inventario['metadata'].get('ultima_actualizacion', 'N/A')],
        ["Total de productos", inventario['metadata'].get('total_productos', 0)],
        ["Total de proveedores", inventario['metadata'].get('total_proveedores', 0)],
        ["Valor total del inventario (ARS)", inventario['metadata'].get('valor_total_inventario', 0.0)]
    ]
    mostrar_tabla(datos_metadatos, headers_metadatos)

    print("\nInformación de proveedores:")
    headers_proveedores = ["ID", "Nombre", "Dirección", "Teléfono", "Email"]
    datos_proveedores = [[prov_id, proveedor["nombre"], proveedor["direccion"], proveedor["telefono"], proveedor["email"]]
                         for prov_id, proveedor in inventario["proveedores"].items()]
    mostrar_tabla(datos_proveedores, headers_proveedores)

def mostrar_proveedores():
    inventario = cargar_inventario()
    proveedores = inventario.get("proveedores", {})
    
    if not proveedores:
        print("No hay proveedores registrados.")
        return None

    return proveedores

#Da el formato al proveedor
def crear_nombre_proveedor(codigo_proveedor,inventario ):
    return f"PROV{len(inventario['proveedores']) + 1:03}"

def agregar_nuevo_proveedor(inventario):
    print("\n--- Agregar Nuevo Proveedor ---")
    nombre_proveedor = input("Nombre del proveedor: ").strip()
    direccion = input("Dirección del proveedor: ").strip()
    telefono = input("Teléfono del proveedor: ").strip()
    email = input("Email del proveedor: ").strip()

    #crea un codigo para el proveedor
    codigo_proveedor = crear_nombre_proveedor(codigo_proveedor,inventario)

    #agrega el nuevo proveedor al inventario
    inventario["proveedores"][codigo_proveedor] = {
        "nombre": nombre_proveedor,
        "direccion": direccion,
        "telefono": telefono,
        "email": email
    }
    guardar_inventario(inventario)

    print(f"Proveedor '{nombre_proveedor}' agregado exitosamente con el código {codigo_proveedor}.")
    
    return codigo_proveedor, nombre_proveedor

def seleccionar_proveedor(proveedores, inventario):
    while True:
        print("\nProveedores disponibles:")
        for codigo, datos in proveedores.items():
            print(f"Código: {codigo} - Nombre: {datos['nombre']}")
        
        print("\nIngrese el código del proveedor elegido o escriba '1' para agregar un nuevo proveedor:")
        codigo_proveedor = input("Código del proveedor: ").strip().upper()

        if codigo_proveedor in proveedores:
            return codigo_proveedor, proveedores[codigo_proveedor]["nombre"]
        elif codigo_proveedor == "1" or codigo_proveedor == 1:
            return agregar_nuevo_proveedor(inventario)
        else:
            print("Código inválido. Intente nuevamente.")

def cambiar_proveedor(proveedores, inventario, codigo_producto):
    lista_proveedores = []
    productos = inventario['productos']
    
    for codigo_proveedor, datos in proveedores.items():
        lista_proveedores.append(codigo_proveedor)
    
    print('')
    while True:
        print("\nProveedores disponibles:")
        i = 0
        for codigo_proveedor, datos in proveedores.items():
            i += 1
            print(f"{i}) Código: {codigo_proveedor} - Nombre: {datos['nombre']}")
                    
        numero = int(input('Ingrese el numero: '))
        if numero in range(1, len(lista_proveedores)+1):
            productos[codigo_producto]["proveedor_id"] = lista_proveedores[numero-1]
            productos[codigo_producto]["fecha_ultima_actualizacion"] = datetime.now().strftime("%Y/%d/%m")
            guardar_inventario(inventario)
            print('El proveedor del PRODUCTO se cambió correctamente')
            return
        else:
            print('Numero inválido!')

def agregar_producto(nombre, cantidad, precio, fecha):
    inventario = cargar_inventario()
    proveedores = mostrar_proveedores()
    if not proveedores:
        print("No se puede agregar el producto sin proveedores.")
        return

    proveedor_codigo, proveedor_nombre = seleccionar_proveedor(proveedores, inventario)
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
        "proveedor_id": proveedor_codigo,
        "proveedor_nombre": proveedor_nombre,
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

def procesar_fecha(fecha): #No usar esta (se usa en es_fecha_valida)
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
    palabras_clave = id_producto.lower().split() #divide la busqueda en palabras clave

    headers_productos = ["Código", "Nombre", "Categoría", "Cantidad", "Precio (ARS)", "Proveedor", "Fecha de Vencimiento"]

    #busca productos que tengan alguna de las palabras clave en su nombre o codigo
    encontrados = {}
    for codigo, producto in productos.items():
        nombre_producto = producto['nombre'].lower()
        
        #verifica si alguna palabra clave esta en el codigo o nombre
        if any(palabra in nombre_producto for palabra in palabras_clave) or any(palabra in codigo.lower() for palabra in palabras_clave):
            encontrados[codigo] = producto

    #muestra sugerencias de busqueda si no se encuentra un resultado
    if not encontrados:
        print("No se encontró ningún producto exacto. Mostrando sugerencias similares:")
        sugerencias = {}
        #sugerencias basadas en las palabras clave
        for codigo, producto in productos.items():
            nombre_producto = producto['nombre'].lower()
            if any(palabra in nombre_producto for palabra in palabras_clave) or any(palabra in codigo.lower() for palabra in palabras_clave):
                sugerencias[codigo] = producto
        if sugerencias:
            datos_sugerencias = [[codigo, producto["nombre"], producto["categoria"], 
                                  f"{producto['cantidad']['valor']} {producto['cantidad']['unidad']}",
                                  producto["precio"]["valor"], producto["proveedor_id"], producto["fecha_vencimiento"]]
                                 for codigo, producto in sugerencias.items()]
            mostrar_tabla(datos_sugerencias, headers_productos)
            mostrar_resumen(sugerencias)
        else:
            print("No hay productos que coincidan con la búsqueda.")
    else:
        print("Resultados de la búsqueda:")
        datos_encontrados = [[codigo, producto["nombre"], producto["categoria"], 
                              f"{producto['cantidad']['valor']} {producto['cantidad']['unidad']}",
                              producto["precio"]["valor"], producto["proveedor_id"], producto["fecha_vencimiento"]]
                             for codigo, producto in encontrados.items()]
        mostrar_tabla(datos_encontrados, headers_productos)
        mostrar_resumen(encontrados)

# Funcion que muestra los productos en una tabla usando la lib tabulate y agrega paginacion
def mostrar_tabla(datos, headers, page_size=5): 
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

# Función para actualizar la cantidad de un producto                                                                        !!!!!!!!!!!!!!
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
def editar_nombre(codigo, nuevo_nombre):
    inventario = cargar_inventario()
    productos = inventario['productos']

    if codigo in productos:
        nombre_viejo = productos[codigo]["nombre"]  #guarda el nombre del producto
        productos[codigo]["nombre"] = nuevo_nombre
        guardar_inventario(inventario)
        return nombre_viejo

def editar_precio(codigo,nuevo_precio):
    inventario = cargar_inventario()
    productos = inventario['productos']

    if codigo in productos:
        productos[codigo]["precio"]["valor"] = nuevo_precio
        nombre_producto = productos[codigo]["nombre"]#guarda el nombre del producto
        guardar_inventario(inventario)
        return nombre_producto
    
def editar_fecha(codigo,nueva_fecha):
    inventario = cargar_inventario()
    productos = inventario['productos']

    if codigo in productos:
        productos[codigo]["fecha_vencimiento"] = nueva_fecha
        productos[codigo]["fecha_ultima_actualizacion"] = datetime.now().strftime("%Y/%d/%m") #Deberia guardar la fecha actual con la libreria datetime
        nombre_producto = productos[codigo]["fecha_ultima_actualizacion"] #guarda el nombre del producto
        guardar_inventario(inventario)
        return nombre_producto
    
def editar_proveedor(codigo,nuevo_proveedor):
    inventario = cargar_inventario()
    productos = inventario['productos']

    if codigo in productos:
        productos[codigo]["proveedor_id"] = nuevo_proveedor
        nombre_producto = productos[codigo]["nombre"] #guarda el nombre del producto
        guardar_inventario(inventario)
        return nombre_producto

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
    print("| 7. Editar producto             |")
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

# Funcion para mostrar el submenu de edicion (del producto)
def menu_edicion():
    print("\n --------------------------------")
    print("| Menú Edición                   |")
    print("| 1. Nombre del producto         |")
    print("| 2. Cantidad                    |")
    print("| 3. Precio                      |")
    print("| 4. Fecha                       |")
    print("| 5. Proveedor                   |")
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
            agregar_producto(nombre, cantidad, precio, fecha)
            continuar()
        
        if opcion == "3": #Buscar producto
            id_producto = input("Ingrese el código o el nombre: ")
            buscar_producto(id_producto)
            continuar()
            
        if opcion == "4": #Eliminar esta funcion                                                                                  !!!!!!!!!
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
        
        #Menú de opciones de edición de productos
        if opcion == "7":
            bandera = True
            while bandera:
                menu_edicion()
                opcion_editar = input("Ingrese una opción de edicion: ")
                os.system('cls' if os.name == 'nt' else 'clear') #limpia la pantalla
                print("")

                if opcion_editar == "1":
                    codigo = input("Ingrese el código: ")
                    nuevo_nombre = input("Ingrese el nuevo nombre: ")
                    nombre_producto = editar_nombre(codigo, nuevo_nombre)
                    if nombre_producto:
                        print(f"Nombre del producto '{nombre_producto}' actualizado a {nuevo_nombre}.")
                    else:
                        print("Producto no encontrado")
                    continuar()
                
                
                if opcion_editar == "2":
                    codigo = input("Ingrese el código: ")
                    nueva_cantidad = int(input("Ingrese la nueva cantidad: "))
                    nombre_producto = actualizar_cantidad(codigo, nueva_cantidad)

                    if nombre_producto:
                        print(f"Cantidad del producto '{nombre_producto}' actualizada a {nueva_cantidad} unidades.")
                    else:
                        print("Producto no encontrado")
                    continuar()

                if opcion_editar=="3":
                    codigo = input("Ingrese el código: ")
                    nuevo_precio = int(input("Ingrese el nuevo precio: "))
                    nombre_producto= editar_precio(codigo,nuevo_precio)
                    
                    if nombre_producto:
                        print(f"Precio del producto '{nombre_producto}' actualizado a ${nuevo_precio}.")
                    else:
                        print("Producto no encontrado")
                    continuar()

                if opcion_editar=="4": #Editar fecha
                    codigo = input("Ingrese el código: ")
                    nueva_fecha = validar_fecha()
                    nombre_producto= editar_fecha(codigo, nueva_fecha)
                    
                    if nombre_producto:
                        print(f"Fecha del producto '{nombre_producto}' actualizada a {nueva_fecha}.")
                    else:
                        print("Producto no encontrado")
                    continuar()
                
                if opcion_editar=="5": #Con formato proveedor
                    inventario = cargar_inventario()
                    proveedores = mostrar_proveedores()
                    codigo = input("Ingrese el código del producto: ")
                    cambiar_proveedor(proveedores, inventario, codigo)
                    continuar()

                elif opcion_editar == "-1":
                    bandera = False

           
        # Op 
        if opcion == "-1":
            Start = False
            print("Saliendo del programa... ¡Hasta luego!")
        
        if int(opcion) not in range(1, 5) and opcion != "-1":
            print("Opción inválida")


main()