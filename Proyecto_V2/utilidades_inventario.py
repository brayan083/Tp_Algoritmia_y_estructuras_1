from datetime import datetime
from inventario import cargar_inventario, guardar_inventario

def validar_producto():
    while(True):
        nombre = input("Ingrese el nombre: ")
        if Buscarpalabras(nombre) is None:
            return nombre
        print('\nEl nombre ya existe!\n')

def verificar_codigo_producto(codigo):
    inventario = cargar_inventario()
    productos = inventario['productos']
    return codigo in productos

# Función para buscar un producto por nombre o código
def Buscarpalabras(palabra):
    inventario = cargar_inventario()
    productosencontrados = [(codigo, producto) for codigo, producto in inventario['productos'].items() 
                            if codigo == palabra or producto['nombre'] == palabra]
    if productosencontrados: 
        return productosencontrados
    return None

def editar_fecha(codigo,nueva_fecha):
    inventario = cargar_inventario()
    productos = inventario['productos']

    if codigo in productos:
        productos[codigo]["fecha_vencimiento"] = nueva_fecha
        productos[codigo]["fecha_ultima_actualizacion"] = datetime.now().strftime("%Y/%d/%m") #Deberia guardar la fecha actual con la libreria datetime
        nombre_producto = productos[codigo]["fecha_ultima_actualizacion"] #guarda el nombre del producto
        guardar_inventario(inventario)
        return nombre_producto

def editar_precio(codigo,nuevo_precio):
    inventario = cargar_inventario()
    productos = inventario['productos']

    if codigo in productos:
        productos[codigo]["precio"]["valor"] = nuevo_precio
        nombre_producto = productos[codigo]["nombre"]#guarda el nombre del producto
        guardar_inventario(inventario)
        return nombre_producto

#actualiza la cantidad de un producto
def actualizar_cantidad(codigo, nueva_cantidad):
    inventario = cargar_inventario()
    productos = inventario['productos']

    if codigo in productos:
        productos[codigo]["cantidad"]["valor"] = nueva_cantidad
        nombre_producto = productos[codigo]["nombre"]  #guarda el nombre del producto
        guardar_inventario(inventario)
        return nombre_producto
    return None

def editar_nombre(codigo, nuevo_nombre):
    inventario = cargar_inventario()
    productos = inventario['productos']

    if codigo in productos:
        nombre_viejo = productos[codigo]["nombre"]  #guarda el nombre del producto
        productos[codigo]["nombre"] = nuevo_nombre
        guardar_inventario(inventario)
        return nombre_viejo
    