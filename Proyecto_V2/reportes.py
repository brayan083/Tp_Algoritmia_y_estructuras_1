from productos import mostrar_tabla
from inventario import cargar_inventario

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
    try:
        inventario = cargar_inventario()
        if 'productos' not in inventario:
            raise KeyError("El inventario no contiene la clave 'productos'.")

        productos_mas_caros = dict(sorted(inventario['productos'].items(), key=lambda x: x[1]['precio']['valor'], reverse=True)[:5])

        if productos_mas_caros:
            print(f"Top 5 productos más caros:")
            headers_productos = ["Código", "Nombre", "Categoría", "Cantidad", "Precio (ARS)", "Proveedor", "Fecha de Vencimiento"]
            datos_productos = [[codigo, producto["nombre"], producto["categoria"],
                                f"{producto['cantidad']['valor']} {producto['cantidad']['unidad']}",
                                f"${producto['precio']['valor']}",  # Formatear el precio con el signo de $
                                producto["proveedor_id"], producto["fecha_vencimiento"]]
                               for codigo, producto in productos_mas_caros.items()]
            mostrar_tabla(datos_productos, headers_productos)
        else:
            print(f"No se encontraron productos")

    except KeyError as e:
        print(f"Error en la estructura del inventario: {e}")
    except TypeError as e:
        print(f"Error al procesar los datos del inventario: {e}")
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")