from productos import agregar_producto
from unittest.mock import patch

inventarioDeTest = {
    'productos': {},
    'proveedores': {
        'PROV001': {'nombre': 'Granix'},
        'PROV002': {'nombre': 'Molinos'}
    }
}

def cargar_inventario():
    return inventarioDeTest

def guardar_inventario(inventario):
    global inventarioDeTest
    inventarioDeTest = inventario  #guarda el inventario simulado

#funciones de validación simuladas
def validar_producto():
    return "Harina"

def validar_cantidad(cantidad):
    return cantidad.isdigit() and int(cantidad) > 0

def validar_precio(precio):
    try:
        float(precio)
        return True
    except ValueError:
        return False

def input_fecha_validada():
    return "12-11-2025"

def seleccionar_proveedor(proveedores, inventario):
    return 'PROV001'

def generar_codigo_unico(inventario):
    return '1001'

def formatear(fecha):
    return fecha

def procesar_fecha(fecha):
    return fecha

def validar_fecha(fecha):
    return True

# Test para agregar_producto
def test_agregar_producto():
    with patch('builtins.input', side_effect=['10', '15.0']):  # Simulamos las entradas del usuario
        agregar_producto()
    
    inventario = cargar_inventario()
    assert '1001' in inventario['productos'], "Error: El producto no fue agregado."
    assert inventario['productos']['1001']['nombre'] == 'Harina', "Error: El nombre del producto es incorrecto."
    assert inventario['productos']['1001']['cantidad']['valor'] == 10, "Error: La cantidad es incorrecta."
    assert inventario['productos']['1001']['precio']['valor'] == 15.0, "Error: El precio es incorrecto."
    assert inventario['productos']['1001']['proveedor_id'] == 'PROV001', "Error: El proveedor es incorrecto."
    assert inventario['productos']['1001']['fecha_vencimiento'] == '12-12-2025', "Error: La fecha de vencimiento es incorrecta."
