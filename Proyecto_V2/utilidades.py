import os
from datetime import datetime
from inventario import cargar_inventario, guardar_inventario


def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_cantidad(cantidad):
    try:
        cantidad = int(cantidad)
        if cantidad <= 0:
            raise ValueError
        return True
    except ValueError:
        print("La cantidad debe ser un número entero positivo.")
        return False

def validar_precio(precio):
    try:
        precio = float(precio)
        if precio <= 0:
            raise ValueError
        return True
    except ValueError:
        print("El precio debe ser un número positivo.")
        return False

def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, "%d-%m-%Y")
        return True
    except ValueError:
        print("La fecha debe tener el formato DD-MM-YYYY.")
        return False
    
def validar_producto():
    while(True):
        nombre = input("Ingrese el nombre: ")
        if Buscarpalabras(nombre) is None:
            return nombre
        print('\nEl nombre ya existe!\n')
        
def input_fecha_validada():
    while True:
        fecha = input("Ingrese la fecha de vencimiento (DD-MM-YYYY): ")
        try:
            fecha_obj = datetime.strptime(fecha, "%d-%m-%Y")
            if fecha_obj < datetime.now():
                print("La fecha no puede ser anterior a la fecha actual.")
            else:
                return fecha
        except ValueError:
            print("Formato de fecha inválido. Por favor, use el formato DD-MM-YYYY.")
        
#crea un codigo unico para cada producto
def generar_codigo_unico(inventario):
    codigo_base = 1000
    productos = inventario.get('productos', {})

    max_codigo = max((int(codigo) for codigo in productos.keys()), default=codigo_base)
    nuevo_codigo = max_codigo + 1
    return str(nuevo_codigo)
        
def formatear(fecha):
    return fecha.strftime("%d-%m-%Y")

def procesar_fecha(fecha):
    return datetime.strptime(fecha, "%d-%m-%Y")

# Función para continuar con la ejecución del programa
def continuar():
    input("Presione enter para continuar...")
    os.system('cls' if os.name == 'nt' else 'clear') #limpia la pantalla para windows y mac
        
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

# Función para actualizar la cantidad de un producto !!!!!!!!!!!!!!
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

        
        
        


        