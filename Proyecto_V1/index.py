from datetime import datetime
import json
import os
import re
from tabulate import tabulate 
from functools import reduce

# Rutas de los archivos JSON
archivo_productos = 'Productos_V3 copy.json'
archivo_proveedores = 'Proveedores_V3.json'

# Funcion para registrar errores en un archivo de logs
def registrar_error(error):
    with open('logs.txt', 'a') as archivo_log:
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo_log.write(f"{fecha_hora} - ERROR: {error}\n")
        

# Función para cargar inventario desde los archivos JSON
def cargar_inventario():
    inventario = {}
    try:
        with open(archivo_productos, 'r', encoding='UTF-8') as file:
            inventario.update(json.load(file))
    except FileNotFoundError:
        registrar_error(FileNotFoundError)
    
    try:
        with open(archivo_proveedores, 'r', encoding='UTF-8') as file:
            inventario.update(json.load(file))
    except FileNotFoundError:
        registrar_error(FileNotFoundError)
    
    # print(inventario)
    
    return inventario

# Función para guardar el inventario en los archivos JSON
def guardar_inventario(inventario):
    try:
        with open(archivo_productos, 'w', encoding='UTF-8') as file:
            json.dump(inventario['productos'], file, indent=4)
    except IOError as e:
        registrar_error(e)
        print(f"Error al guardar los productos: {e}")
    
    try:
        with open(archivo_proveedores, 'w', encoding='UTF-8') as file:
            json.dump(inventario['proveedores'], file, indent=4)
    except IOError as e:
        registrar_error(e)
        print(f"Error al guardar los proveedores: {e}")

#crea un codigo unico para cada producto
def generar_codigo_unico(inventario):
    codigo_base = 1000
    productos = inventario.get('productos', {})

    max_codigo = max((int(codigo) for codigo in productos.keys()), default=codigo_base)
    nuevo_codigo = max_codigo + 1
    return str(nuevo_codigo)

def validar_cantidad(cantidad):
    try:
        cantidad = int(cantidad)
        if cantidad < 0:
            raise ValueError("La cantidad debe ser un número positivo")
    except ValueError as e:
        registrar_error(e)
        print(f"Error: {e}")
        return False
    return True

def validar_precio(precio):
    try:
        precio = float(precio)
        if precio < 0:
            raise ValueError("El precio debe ser un valor positivo")
    except ValueError as e:
        registrar_error(e)
        print(f"Error: {e}")
        return False
    return True

#Establece los patrones para que se reciba correctamente la fecha
def validar_formato_fecha(fecha):
    patron = r"^(0[1-9]|[12][0-9]|3[01])[-/ ](0[1-9]|1[0-2])[-/ ][0-9]{4}$"
    return bool(re.match(patron, fecha)) #Sera True si la fecha coincide con patron

def es_bisiesto(anio):
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

def validar_fecha(fecha):
    if not validar_formato_fecha(fecha):  #Busca validar el formato
        return False
    
    dia, mes, anio = procesar_fecha(fecha)
    try:
        dia = int(dia)
        mes = int(mes)
        anio = int(anio)
    except ValueError:
        registrar_error(ValueError)
        return False


    dias_por_mes = [31, 29 if es_bisiesto(anio) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if not (1 <= mes <= 12):
        return False
    if not (1 <= dia <= dias_por_mes[mes - 1]):
        return False
    
    #validar que la fecha no sea anterior a la fecha actual
    try:
        fecha_vencimiento = datetime(anio, mes, dia)
        fecha_actual = datetime.now()
        if fecha_vencimiento < fecha_actual:
            return False
    except ValueError:
        return False

    return True

# Función para ver el inventario
def ver_inventario():
    inventario = cargar_inventario()

    if not inventario["productos"]:
        print("No hay productos en el inventario.")
    else:
        mostrar_productos(inventario["productos"])

    # mostrar_metadatos(inventario.get("metadata", {}))
    
# def mostrar_metadatos(metadata):
#     print("\nMetadatos del inventario:")
#     headers_metadatos = ["Metadatos", "Valores"]
#     datos_metadatos = [
#         ["Versión", metadata.get('version', 'N/A')],
#         ["Última actualización", metadata.get('ultima_actualizacion', 'N/A')],
#         ["Total de productos", metadata.get('total_productos', 0)],
#         ["Total de proveedores", metadata.get('total_proveedores', 0)],
#         ["Valor total del inventario (ARS)", f"${metadata.get('valor_total_inventario', 0.0):.2f}"]
#     ]
#     mostrar_tabla(datos_metadatos, headers_metadatos)    

# Función para limpiar la consola
def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

# Función que muestra los datos en una tabla usando la librería tabulate y agrega paginación e interactividad
def mostrar_tabla(datos, headers, page_size=5):
    def mostrar_pagina(pagina):
        limpiar_consola()
        inicio = pagina * page_size
        fin = inicio + page_size
        print(tabulate(datos[inicio:fin], headers=headers, tablefmt="grid"))

    def buscar_elemento():
        termino = input("Ingrese el término de búsqueda: ").lower()
        resultados = [fila for fila in datos if any(termino in str(celda).lower() for celda in fila)]
        if resultados:
            limpiar_consola()
            print("\nResultados de la búsqueda:")
            print(tabulate(resultados, headers=headers, tablefmt="grid"))
            return True  # Indica que se realizó una búsqueda
        else:
            print("No se encontraron resultados.")
            return False  # Indica que no se encontraron resultados

    def ordenar_datos():
        print("Seleccione la columna para ordenar:")
        for i, header in enumerate(headers):
            print(f"{i + 1}. {header}")
        opcion = int(input("Ingrese el número de la columna: ")) - 1
        if 0 <= opcion < len(headers):
            # Convertir a número si es la columna de cantidad o precio
            if headers[opcion] in ["Cantidad", "Precio (ARS)"]:
                datos.sort(key=lambda x: float(re.sub(r'[^\d.]', '', x[opcion])))
            else:
                datos.sort(key=lambda x: x[opcion])
        else:
            print("Opción no válida.")

    total_paginas = (len(datos) + page_size - 1) // page_size  # calcula número de páginas
    pagina_actual = 0

    while True:
        mostrar_pagina(pagina_actual)
        print(f"\nPágina {pagina_actual + 1} de {total_paginas}")

        if total_paginas > 1:
            print("\nOpciones: [d] Siguiente, [a] Anterior, [b] Buscar, [o] Ordenar, [s] Salir")
            opcion = input("Seleccione una opción: ").lower()

            if opcion == 'd' and pagina_actual < total_paginas - 1:
                pagina_actual += 1
            elif opcion == 'a' and pagina_actual > 0:
                pagina_actual -= 1
            elif opcion == 'b':
                if buscar_elemento():
                    break  # Salir del bucle si se realizó una búsqueda
            elif opcion == 'o':
                ordenar_datos()
            elif opcion == 's':
                break
            else:
                print("Opción no válida. Intente nuevamente.")
        else:
            break

def mostrar_productos(productos):
    print("Inventario actual:")
    headers_productos = ["Código", "Nombre", "Categoría", "Cantidad", "Precio (ARS)", "Proveedor", "Fecha de Vencimiento"]
    datos_productos = [[codigo, producto["nombre"], producto["categoria"], 
                        f"{producto['cantidad']['valor']} {producto['cantidad']['unidad']}",
                        f"${producto['precio']['valor']}",  # Aquí se añade el símbolo $
                        producto["proveedor_id"], producto["fecha_vencimiento"]]
                    for codigo, producto in productos.items()]
    mostrar_tabla(datos_productos, headers_productos)


def mostrar_proveedores():
    inventario = cargar_inventario()
    proveedores = inventario.get("proveedores", {})
    
    if not proveedores:
        print("No hay proveedores registrados.")
        return None

    return proveedores

#Da el formato al proveedor
def crear_nombre_proveedor(inventario): #codigo_proveedor,
    return f"PROV{len(inventario['proveedores']) + 1:03}"

def seleccionar_proveedor(proveedores, inventario):
    while True:
        print("\n--- Proveedores disponibles ---")
        for codigo, datos in proveedores.items():
            print(f"Código: {codigo} - Nombre: {datos['nombre']}")
        
        print("\nIngrese el código del proveedor elegido o escriba '1' para agregar un nuevo proveedor:")
        codigo_proveedor = input("Código del proveedor: ").strip().upper()

        if codigo_proveedor in proveedores:
            return codigo_proveedor, proveedores[codigo_proveedor]["nombre"]
        elif codigo_proveedor == "1":
            codigo_proveedor, nombre_proveedor = agregar_nuevo_proveedor(inventario)
            return codigo_proveedor, nombre_proveedor
        else:
            print("Código inválido. Intente nuevamente.")

def agregar_nuevo_proveedor(inventario):
    print("\n--- Agregar Nuevo Proveedor ---")
    nombre_proveedor = input("Nombre del proveedor: ").strip()
    direccion = input("Dirección del proveedor: ").strip()
    telefono = input("Teléfono del proveedor: ").strip()
    email = input("Email del proveedor: ").strip()

    #crea un codigo para el proveedor
    codigo_proveedor = crear_nombre_proveedor(inventario) #codigo_proveedor,
    # Crea un código para el proveedor
    codigo_proveedor = crear_nombre_proveedor(inventario)

    # Agrega el nuevo proveedor al inventario
    inventario["proveedores"][codigo_proveedor] = {
        "nombre": nombre_proveedor,
        "direccion": direccion,
        "telefono": telefono,
        "email": email
    }
    guardar_inventario(inventario)

    print(f"Proveedor '{nombre_proveedor}' agregado exitosamente con el código {codigo_proveedor}.")
    
    return codigo_proveedor, nombre_proveedor

def buscarProveedores(id_proveedor):
    inventario = cargar_inventario()
    proveedores = inventario.get("proveedores", {})

    if not proveedores:
        print("No hay proveedores registrados.")
        return

    palabras_clave = id_proveedor.lower().split() #busca por palabras clave

    #muestra los proveedores que coincidan con las palabras clave
    encontrados = {}
    for codigo, proveedor in proveedores.items():
        nombre_proveedor = proveedor["nombre"].lower()
        if any(palabra in nombre_proveedor for palabra in palabras_clave) or any(palabra in codigo.lower() for palabra in palabras_clave):
            encontrados[codigo] = proveedor

    if not encontrados:
        print("No se encontró ningún proveedor que coincida con la búsqueda.")
    else:
        print("\nResultados de la búsqueda:")
        headers_proveedores = ["Código", "Nombre", "Dirección", "Teléfono", "Email"]
        datos_encontrados = [[codigo, proveedor["nombre"], proveedor["direccion"], proveedor["telefono"], proveedor["email"]]
                             for codigo, proveedor in encontrados.items()]
        
        mostrar_tabla(datos_encontrados, headers_proveedores)

        
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
            print(f"{i}) Código: {codigo_proveedor} - Nombre: {datos['nombre']}") # muestra un menú enumerado
                    
        numero = int(input('Ingrese el numero: ')) #selecciona un proveedor
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
    proveedores = inventario["proveedores"]
    productos = inventario["productos"]
    
    if not proveedores:
        print("No se puede agregar el producto sin proveedores.")
        return

    proveedor_codigo, _ = seleccionar_proveedor(proveedores, inventario)
    #crea un codigo unico para cada prod
    proveedor_codigo, proveedor_nombre = seleccionar_proveedor(proveedores, inventario)
    
    # Crea un código único para cada producto
    codigo = generar_codigo_unico(inventario)
    if codigo in productos:
        print(f"Error: El código {codigo} ya existe. No se puede agregar el producto.")
        return
    
    if not validar_cantidad(cantidad):
        return
    
    if not validar_precio(precio):
        return
    
    if not validar_fecha(fecha):
        print("La fecha de vencimiento no es válida.")
        return
    
    # Formatea la fecha de vencimiento
    fecha = formatear(procesar_fecha(fecha))
    
    producto = {
        "nombre": nombre.capitalize(),
        "categoria": "General",  # Se puede cambiar esta categoría predeterminada
        "cantidad": {"valor": cantidad, "unidad": "unidad"},
        "precio": {"valor": precio, "moneda": "ARS"},
        "proveedor_id": proveedor_codigo,
        #"proveedor_nombre": proveedor_nombre,
        "fecha_vencimiento": fecha,
        "fecha_ultima_actualizacion": formatear(procesar_fecha("01-01-2024"))
    }
    
    inventario["productos"][codigo] = producto
    inventario["metadata"]["total_productos"] = len(inventario["productos"])
    
    guardar_inventario(inventario)
    print(f"Producto '{nombre}' agregado exitosamente con el código {codigo}.")


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
    palabras_clave = id_producto.lower().split()  # Divide la búsqueda en palabras clave
    #define los encabezados que se usarán en la tabla al mostrar resultados
    headers_productos = ["Código", "Nombre", "Categoría", "Cantidad", "Precio (ARS)", "Proveedor", "Fecha de Vencimiento"]

    # Filtra los productos que coinciden con las palabras clave en nombre o código
    encontrados = dict(filter(
        lambda item: any(palabra in item[1]['nombre'].lower() for palabra in palabras_clave) or 
                     any(palabra in item[0].lower() for palabra in palabras_clave),
        productos.items()
    ))

    # Muestra sugerencias de búsqueda si no se encuentra un resultado
    if not encontrados:
        print("No se encontró ningún producto exacto. Muestra sugerencias similares:")
        sugerencias = dict(filter(
            lambda item: any(palabra in item[1]['nombre'].lower() for palabra in palabras_clave) or 
                         any(palabra in item[0].lower() for palabra in palabras_clave),
            productos.items()
        ))

        if sugerencias:
            # Usa map para transformar los datos de las sugerencias a la tabla
            datos_sugerencias = list(map(
                lambda item: [item[0], item[1]["nombre"], item[1]["categoria"],
                              f"{item[1]['cantidad']['valor']} {item[1]['cantidad']['unidad']}",
                              item[1]["precio"]["valor"], item[1]["proveedor_id"], item[1]["fecha_vencimiento"]],
                sugerencias.items()
            ))

            # Usa reduce para calcular un resumen (ejemplo: sumar cantidades totales de los productos)
            resumen_sugerencias = reduce(
                lambda acc, item: acc + item[1]['cantidad']['valor'], 
                sugerencias.items(), 0)
            print(f"Total de unidades sugeridas: {resumen_sugerencias}")

            mostrar_tabla(datos_sugerencias, headers_productos)
            mostrar_resumen(sugerencias)
        else:
            print("No hay productos que coincidan con la búsqueda.")
    else:
        print("Resultados de la búsqueda:")
        # Usa map para transformar los datos encontrados a la tabla
        datos_encontrados = list(map(
            lambda item: [item[0], item[1]["nombre"], item[1]["categoria"],
                          f"{item[1]['cantidad']['valor']} {item[1]['cantidad']['unidad']}",
                          item[1]["precio"]["valor"], item[1]["proveedor_id"], item[1]["fecha_vencimiento"]],
            encontrados.items()
        ))

        # Usa reduce para calcular un resumen (ejemplo: sumar el valor total de los productos encontrados)
        resumen_encontrados = reduce(
            lambda acc, item: acc + (item[1]["precio"]["valor"] * item[1]["cantidad"]["valor"]),
            encontrados.items(), 0
        )
        print(f"Valor total de los productos encontrados: {resumen_encontrados} ARS")

        mostrar_tabla(datos_encontrados, headers_productos)
        mostrar_resumen(encontrados)

# Funcion que muestra un resumen de los productos encontrados
def mostrar_resumen(productos):
    total_productos = len(productos)
    valor_total = sum(producto["precio"]["valor"] * producto["cantidad"]["valor"] for producto in productos.values())
    print("\nResumen:")
    print(f"Total de productos encontrados: {total_productos}")
    print(f"Valor total de los productos: ARS {valor_total:.2f} \n")

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
def borrar_producto(producto_codigo):
    try:
        inventario = cargar_inventario()
        productos = inventario.get("productos", {}) # Verificar si el producto existe en los productos
        
    
        if producto_codigo in productos:
            producto = productos[producto_codigo]
            nombre_producto = producto["nombre"]
            comprobar = True
            while comprobar:
                validar_borrado = input(f"¿Esta seguro de querer borrar este producto: {nombre_producto}? (si o no) \n Escriba su opcion aqui: ")
                validar_borrado = validar_borrado.lower()
                if validar_borrado == 'si':
                    comprobar = False
                else:
                    if validar_borrado == 'no':
                        return
            del productos[producto_codigo]
            print(f"Producto: {producto['nombre']} borrado exitosamente.")
            inventario["metadata"]["total_productos"] = len(inventario["productos"])
            guardar_inventario(inventario)
        else:
            print("Producto no encontrado en el inventario.")
    
    except ValueError as e:
        registrar_error(e)
        print(f"Respuesta erronea: {e}")
    except KeyError as e:
        registrar_error(e)
        print(f"Error al procesar el inventario: {e}")
    except Exception as e:
        registrar_error(e)
        print(f"Error inesperado: {e}")
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
    proveedor = proveedor.lower()#convierte el nombre del proveedor a minusculas

    #filtra los productos por nombre o codigo proveedor usando un diccionario y usando .lower() en el id del proveedor de cada producto
    proveedores_por_nombre = {
        datos['nombre'].lower(): prov_id
        for prov_id, datos in inventario['proveedores'].items()
    }
    proveedores_por_codigo = {
        prov_id.lower(): prov_id
        for prov_id in inventario['proveedores'].keys()
    }

    #verifica si se busca al proveedor por nombre o por codigo
    proveedor_id = proveedores_por_codigo.get(proveedor) or proveedores_por_nombre.get(proveedor)

    if not proveedor_id:
        print(f"No se encontró un proveedor con el nombre '{proveedor.capitalize()}'.")
        return
    
    productos_proveedor = {
        codigo: producto 
        for codigo, producto in inventario['productos'].items() 
        if producto['proveedor_id'].lower() == proveedor_id.lower()
    }

    if productos_proveedor:
        print(f"Productos del proveedor {proveedor.capitalize()} ({proveedor_id}):")
        headers = ["Código", "Nombre", "Categoría", "Cantidad", "Precio (ARS)", "Fecha de Vencimiento"]
        datos = [
            [
                codigo,
                producto["nombre"],
                producto["categoria"],
                f"{producto['cantidad']['valor']} {producto['cantidad']['unidad']}",
                f"${producto['precio']['valor']}",
                producto["fecha_vencimiento"],
            ]
            for codigo, producto in productos_proveedor.items()
        ]
        mostrar_tabla(datos, headers)
    else:
        print(f"No se encontraron productos del proveedor {proveedor.capitalize()} ({proveedor_id}).")

# Función para mostrar los productos más caros
def reporte_productos_mas_caros():
    inventario = cargar_inventario()
    productos_mas_caros = dict(sorted(inventario['productos'].items(), key=lambda x: x[1]['precio']['valor'], reverse=True)[:5])

    if productos_mas_caros:
        print(f"Top 5 productos más caros:")
        headers_productos = ["Código", "Nombre", "Categoría", "Cantidad", "Precio (ARS)", "Proveedor", "Fecha de Vencimiento"]
        datos_productos = [[codigo, producto["nombre"], producto["categoria"],
                            f"{producto['cantidad']['valor']} {producto['cantidad']['unidad']}",
                            producto["precio"]["valor"], producto["proveedor_id"], producto["fecha_vencimiento"]]
                           for codigo, producto in productos_mas_caros.items()]
        mostrar_tabla(datos_productos, headers_productos)
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

def input_fecha_validada():
    while(True):
        fecha = input("Ingrese la fecha de vencimiento (DD-MM-YYYY): ")
        if validar_fecha(fecha):
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
    print("| 4. Buscar proveedor            |")
    print("| 5. Reportes                    |")
    print("| 6. Borrar producto             |")
    print("| 7. Editar producto             |")
    print("| 8. Ver autores                 |")
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
    
def alumnos():
    matriz = [
        ["Brayan Zorro"],
        ["Luana Kaladjian"],
        ["Gabriel Pabón"],
        ["Estefanía Sassone"]
    ]
    headers = ["Nombre del Alumno"]
    mostrar_tabla(matriz, headers)


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
            ver_inventario()
            continuar()
        
        if opcion == "2": #agregar producto
            nombre = validar_producto()
            cantidad = int(input("Ingrese la cantidad: "))
            precio = float(input("Ingrese el precio: "))
            fecha = input_fecha_validada() #se valida la fecha de vencimiento
            agregar_producto(nombre, cantidad, precio, fecha)
            continuar()
        
        if opcion == "3": #Buscar producto
            id_producto = input("Ingrese el código o el nombre: ")
            buscar_producto(id_producto)
            continuar()
        
        if opcion == "4": #Buscar proveedor
            id_proveedor = input("Ingrese el código o el nombre del proveedor: ")
            buscarProveedores(id_proveedor)
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
                    proveedor = input("Ingrese el nombre o codigo del proveedor: ")
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
                    nueva_fecha = input_fecha_validada()
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

        if opcion=="8":
            alumnos()
            continuar()

        #Opcion que permite salir del programa 
        if opcion == "-1":
            Start = False
            print("Saliendo del programa... ¡Hasta luego!")
        
        if int(opcion) not in range(1, 5) and opcion != "-1":
            print("Opción inválida")


main()
