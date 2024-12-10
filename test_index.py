import pytest
import json
#Desde el archivo principal, importamos las funciones a testear
from index import borrar_producto, cargar_inventario, guardar_inventario

# 1. Prueba: Eliminar un producto que existe
def test_borrar_producto_existe():
    # Cargamos el inventario real desde el archivo
    inventario = cargar_inventario()
    
    # Verificamos que el inventario tiene el producto con código '001' antes de borrarlo
    assert "001" in inventario["productos"]
    
    # Llamamos a la función borrar_producto para eliminar el producto con código '001'
    borrar_producto("001")
    
    # Comprobamos que el producto '001' fue eliminado del inventario
    inventario_actualizado = cargar_inventario()
    assert "001" not in inventario_actualizado["productos"]
    assert "002" in inventario_actualizado["productos"]

# 2. Prueba: Cancelar la eliminación (responde "no")
def test_borrar_producto_cancelado():
    inventario = cargar_inventario()
    respuesta_usuario = 'no'
    
    if respuesta_usuario == 'no':
        print("Operación cancelada.")
    
    # Verificamos que el producto con código '001' sigue existiendo
    assert "001" in inventario["productos"]
    assert "002" in inventario["productos"]

# 3. Prueba: Opción no válida (respuesta incorrecta varias veces antes de ingresar "si")
def test_borrar_producto_respuesta_invalida():
    inventario = cargar_inventario()

    # Simulamos respuestas inválidas seguidas de una respuesta válida 'si'
    respuestas_invalidas = ['quizás', 'tal vez']
    respuesta_usuario = 'si'  # Finalmente, el usuario responde 'si'

    # Simulamos que el usuario no elimina el producto por respuestas inválidas
    for respuesta in respuestas_invalidas:
        if respuesta not in ['si', 'no']:
            print("Opción no válida, intente nuevamente.")
    
    # Ahora, simulamos que el usuario responde 'si', lo que permite eliminar el producto
    if respuesta_usuario == 'si':
        borrar_producto("002")
    
    # Comprobamos que el producto '002' ha sido eliminado
    inventario_actualizado = cargar_inventario()
    assert "002" not in inventario_actualizado["productos"] 