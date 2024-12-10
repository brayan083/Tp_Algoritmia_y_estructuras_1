import json
from datetime import datetime

archivo_productos = 'datos/Productos_V3.json'
archivo_proveedores = 'datos/Proveedores_V3.json'
log_file = 'datos/logs.txt'

# Funcion para registrar errores en un archivo de logs
def registrar_error(error):
    try:
        with open('log_file', 'a') as archivo_log:
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo_log.write(f"{fecha_hora} - ERROR: {error}\n")
    except Exception as e:
        print(f"No se pudo registrar el error: {e}")
        
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
                
    return inventario

# Función para guardar el inventario en los archivos JSON
def guardar_inventario(inventario):
    
    new_prod = {'productos' : inventario['productos']}
    new_prov = {'proveedores' : inventario['proveedores']}
    
    try:
        # Guardar el inventario completo en el archivo JSON
        with open(archivo_productos, 'w', encoding='UTF-8') as file:
            json.dump(new_prod, file, indent=4)
    except IOError as e:
        registrar_error(e)
        print(f"Error al guardar los productos: {e}")
        
    try:
        # Guardar el inventario completo en el archivo JSON
        with open(archivo_proveedores, 'w', encoding='UTF-8') as file:
            json.dump(new_prov, file, indent=4)
    except IOError as e:
        registrar_error(e)
        print(f"Error al guardar los proveedores: {e}")
               
from productos import mostrar_tabla

# Función para ver el inventario
def ver_inventario():
    inventario = cargar_inventario()

    if not inventario["productos"]:
        print("No hay productos en el inventario.")
    else:
        mostrar_productos(inventario["productos"])
        
def mostrar_productos(productos):
    print("Inventario actual:")
    headers_productos = ["Código", "Nombre", "Categoría", "Cantidad", "Precio (ARS)", "Proveedor", "Fecha de Vencimiento"]
    datos_productos = [[codigo, producto["nombre"], producto["categoria"], 
                        f"{producto['cantidad']['valor']} {producto['cantidad']['unidad']}",
                        f"${producto['precio']['valor']}",  # Aquí se añade el símbolo $
                        producto["proveedor_id"], producto["fecha_vencimiento"]]
                    for codigo, producto in productos.items()]
    mostrar_tabla(datos_productos, headers_productos)