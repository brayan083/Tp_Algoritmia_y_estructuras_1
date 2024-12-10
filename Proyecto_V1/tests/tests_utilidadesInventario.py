from datetime import datetime
from index import validar_producto, Buscarpalabras, editar_fecha, editar_precio, actualizar_cantidad, editar_nombre

def cargar_inventario(): #inventario de ejemplo
    return {
        'productos': {
            '1001': {'nombre': 'Arroz'},
            '1002': {'nombre': 'Harina'},
            '1003': {'nombre': 'Aceite'}
        }
    }

def test_validar_producto():
    #Nombre que ya existe
    resultado = validar_producto('Arroz')
    assert resultado is None, f"Error: {resultado}"

    #Nombre que no existe
    resultado = validar_producto('naranja')
    assert resultado == 'naranja', f"Error: {resultado}"

"""   
def test_verificar_codigo_producto():
    #codigo que existe
    resultado = verificar_codigo_producto('1001')
    assert resultado is True, f"Error: {resultado}"

    #codigo no existe
    resultado = verificar_codigo_producto('1004')
    assert resultado is False, f"Error: {resultado}"

"""
def test_buscar_palabras():
    #buscar por codigo
    resultado = Buscarpalabras('001')
    assert resultado == [('1001', {'nombre': 'Arroz'})], f"Error: {resultado}"

    #buscar por nombre
    resultado = Buscarpalabras('Galletitas')
    assert resultado == [('002', {'nombre': 'Galletitas'})], f"Error: {resultado}"

    #buscar un producto que no existe
    resultado = Buscarpalabras('Galletitas')
    assert resultado is None, f"Error: {resultado}"

    #buscar por codigo que no existe
    resultado = Buscarpalabras('1004')
    assert resultado is None, f"Error: {resultado}"

    #buscar por nombre que no existe
    resultado = Buscarpalabras('pera')
    assert resultado is None, f"Error: {resultado}"

inventarioDeTest = {
    'productos': {
        '1001': {'nombre': 'cereal', 'cantidad': {'valor': 21, 'unidad': 'unidad'},'precio': {'valor': 2700.50, 'moneda': 'ARS'}, 'proveedor_id': 'PROV001','fecha_vencimiento': '12/10/2025', 'fecha_ultima_actualizacion': '10/12/2024'},
        '1002': {'nombre': 'pan', 'cantidad': {'valor': 21, 'unidad': 'unidad'},'precio': {'valor': 1200.0, 'moneda': 'ARS'}, 'proveedor_id': 'PROV002', 'fecha_vencimiento': '2025/02/01', 'fecha_ultima_actualizacion': '10/12/2024'},
    }
}

def cargar_inventario():
    return inventarioDeTest

def guardar_inventario(inventario):
    global inventarioDeTest
    inventarioDeTest = inventario  #se guarda el inventario simulado

def test_editar_fecha():
    #Editar la fecha de un producto existente
    codigo = '1001'
    nueva_fecha = '10/11/2025'
    resultado = editar_fecha(codigo, nueva_fecha)
    
    #verificar que el nombre del producto devuelto sea la fecha de última actualización
    assert resultado == datetime.now().strftime("%Y/%d/%m"), f"Error: {resultado}"

    #verifica que la fecha de vencimiento se haya actualizado correctamente
    inventario = cargar_inventario()
    assert inventario['productos'][codigo]['fecha_vencimiento'] == nueva_fecha, f"Error: {inventario['productos'][codigo]['fecha_vencimiento']}"

    #verificar que la fecha de ultima actualización se haya actualizado correctamente
    assert inventario['productos'][codigo]['fecha_ultima_actualizacion'] == datetime.now().strftime("%Y/%d/%m"), f"Error: {inventario['productos'][codigo]['fecha_ultima_actualizacion']}"

    #Intentar editar un producto que no existe
    codigo_inexistente = '003'
    resultado = editar_fecha(codigo_inexistente, nueva_fecha)
    assert resultado is None, f"Error: {resultado}"

def test_editar_precio():
    #Editar el precio de un producto existente
    codigo = '1001'
    nuevo_precio = 2890.50
    
    resultado = editar_precio(codigo, nuevo_precio)
    
    #Verificar que el nombre del producto sea correcto
    assert resultado == 'cereal', f"Error: {resultado}"

    #Verificar que el precio se haya actualizado
    inventario = cargar_inventario()
    assert inventario['productos'][codigo]['precio']['valor'] == nuevo_precio, f"Error: {inventario['productos'][codigo]['precio']['valor']}"

    #Intentar editar un producto que no existe
    codigo_inexistente = '1009'
    resultado = editar_precio(codigo_inexistente, nuevo_precio)
    assert resultado is None, f"Error: {resultado}"

def test_actualizar_cantidad():
    # actualizar la cantidad de un producto existente
    codigo = '1001'
    nueva_cantidad = 30
    
    resultado = actualizar_cantidad(codigo, nueva_cantidad)
    
    #Verificar que el nombre del producto que retorna sea correcto
    assert resultado == 'Arroz', f"Error: {resultado}"

    #verificar que la cantidad se haya actualizado correctamente
    inventario = cargar_inventario()
    assert inventario['productos'][codigo]['cantidad']['valor'] == nueva_cantidad, f"Error: {inventario['productos'][codigo]['cantidad']['valor']}"

    #intenta actualizar la cantidad de un producto inexistente
    codigo_inexistente = '1009'
    resultado = actualizar_cantidad(codigo_inexistente, nueva_cantidad)
    assert resultado is None, f"Error: {resultado}"


def test_editar_nombre():
    #editar el nombre de un producto existente
    codigo = '1001'
    nuevo_nombre = 'Fideos'
    
    resultado = editar_nombre(codigo, nuevo_nombre)
    
    #verificar que el nombre viejo que devuelve sea correcto
    assert resultado == 'Arroz', f"Error: {resultado}"

    #verifica que el nombre se haya actualizado correctamente
    inventario = cargar_inventario()
    assert inventario['productos'][codigo]['nombre'] == nuevo_nombre, f"Error: {inventario['productos'][codigo]['nombre']}"

    #intentar editar el nombre de un producto inexistente
    codigo_inexistente = '1009'
    resultado = editar_nombre(codigo_inexistente, nuevo_nombre)
    assert resultado is None, f"Error: {resultado}"
