from utilidades import validar_cantidad, validar_precio, validar_fecha, generar_codigo_unico

def test_validar_cantidad():
    #success
    assert validar_cantidad(10) == True, "Error, 10 es una cantidad valida"
    
    #error
    assert validar_cantidad(0) == False, "Error, 0 no una catidad valida"
    assert validar_cantidad(-5) == False, "Error, -5 no es una cantidad valida porque es un nro negativo"
    assert validar_cantidad("abc") == False, "Error, no se permiten strings"


def test_validar_precio():
    #success
    assert validar_precio(15.5) == True, "Error, 15.5 es valido"
    
    #error
    assert validar_precio(0) == False, "Error, 0 no es un precio valido"
    assert validar_precio(-10.98) == False, "Error, -10.98 no es un precio valido porque es un nro negativo"
    assert validar_precio("abc") == False, "Error, no se permiten strings"

def test_validar_fecha():
    #success
    assert validar_fecha("25-12-2024") == True, "Error, '27-12-2024' es una fecha valida"
    
    #error
    assert validar_fecha("2024-12-25") == False, "Error, '2024-12-25' no es un formato de fecha valido"
    assert validar_fecha("abc-def-ghi") == False, "Error, 'abcd-ef-gh' no es un formato de fecha valido"
    assert validar_fecha("31-02-2024") == False, "Error, '28-02-2024' no es una fecha valida ya que no es una fecha mayor o igual a la fecha actual"

def test_generar_codigo_unico():

    #Caso 1: inventario con productos
    inventario = {
        'productos': {
            '1001': {'nombre': 'Arroz'},
            '1002': {'nombre': 'Harina'},
            '1003': {'nombre': 'Aceite'}
        }
    }
    #El codigo siguiente debe ser 1004
    assert generar_codigo_unico(inventario) == '1004', "Error, el codigo generado debería ser 1004"

    #Caso 2: inventario vacío
    inventario_vacio = {
        'productos': {}
    }
    #El codigo siguiente debe ser 1001, porque el valor base es 1000 y le sumamos 1
    assert generar_codigo_unico(inventario_vacio) == '1001', "Error, el codigo generado debe ser 1001"

    #Caso 3: inventario con un solo producto y codigo 1000
    inventario_con_producto_base = {
        'productos': {
            '1000': {'nombre': 'Cafe'}
        }
    }
    #El codigo siguiente debe ser 1001
    assert generar_codigo_unico(inventario_con_producto_base) == '1001', "Error, el codigo generado debe ser 1001"
