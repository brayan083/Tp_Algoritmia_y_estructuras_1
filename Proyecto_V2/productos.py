from functools import reduce
import re

from tabulate import tabulate
from inventario import cargar_inventario, guardar_inventario, registrar_error
from proveedores import seleccionar_proveedor
from utilidades import continuar, generar_codigo_unico, input_fecha_validada, limpiar_consola, validar_cantidad, validar_precio, validar_fecha, formatear, procesar_fecha, validar_producto

def agregar_producto():
    
    inventario = cargar_inventario()
    proveedores = inventario["proveedores"]
    productos = inventario["productos"]
    
    nombre = validar_producto()
    
    # Validar cantidad
    while True:
        cantidad = input("Ingrese la cantidad: ")
        if validar_cantidad(cantidad):
            cantidad = int(cantidad)
            break
    
    # Validar precio
    while True:
        precio = input("Ingrese el precio: ")
        if validar_precio(precio):
            precio = float(precio)
            break

    fecha = input_fecha_validada() #se valida la fecha de vencimiento
    
    if not proveedores:
        print("No se puede agregar el producto sin proveedores.")
        return

    proveedor_codigo = seleccionar_proveedor(proveedores, inventario)
    
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
        "fecha_vencimiento": fecha,
        "fecha_ultima_actualizacion": formatear(procesar_fecha("01-01-2024"))
    }
    
    inventario["productos"][codigo] = producto
    
    guardar_inventario(inventario)
    print(f"Producto '{nombre}' agregado exitosamente con el código {codigo}.")

def mostrar_productos(productos):
    print("Inventario actual:")
    headers_productos = ["Código", "Nombre", "Categoría", "Cantidad", "Precio (ARS)", "Proveedor", "Fecha de Vencimiento"]
    datos_productos = [[codigo, producto["nombre"], producto["categoria"], 
                        f"{producto['cantidad']['valor']} {producto['cantidad']['unidad']}",
                        f"${producto['precio']['valor']}",  # Aquí se añade el símbolo $
                        producto["proveedor_id"], producto["fecha_vencimiento"]]
                    for codigo, producto in productos.items()]
    mostrar_tabla(datos_productos, headers_productos)
    
    
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


def mostrar_tabla(datos, headers, page_size=5, navegar=True):
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

    def navegar_paginas(pagina_actual):
        mostrar_pagina(pagina_actual)
        print(f"\nPágina {pagina_actual + 1} de {total_paginas}")

        if total_paginas > 1:
            print("\nOpciones: [d] Siguiente, [a] Anterior, [b] Buscar, [o] Ordenar, [s] Salir")
            opcion = input("Seleccione una opción: ").lower()

            if opcion == 'd' and pagina_actual < total_paginas - 1:
                # Recursividad!!! Llamamos a la misma función dentro de sí misma
                navegar_paginas(pagina_actual + 1)
            elif opcion == 'a' and pagina_actual > 0:
                # Recursividad!!!
                navegar_paginas(pagina_actual - 1)
            elif opcion == 'b':
                if buscar_elemento():
                    return  # Salir de la recursión si se realizó una búsqueda
                else:
                    # Recursividad!!!
                    navegar_paginas(pagina_actual)
            elif opcion == 'o':
                ordenar_datos()
                navegar_paginas(pagina_actual)
            elif opcion == 's':
                return
            else:
                print("Opción no válida. Intente nuevamente.")
                navegar_paginas(pagina_actual)
        else:
            return

    if navegar:
        navegar_paginas(pagina_actual)
    else:
        mostrar_pagina(pagina_actual)
        