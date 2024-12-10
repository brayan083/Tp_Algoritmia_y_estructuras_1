# tests/test_utilidades.py
from utilidades import validar_cantidad, validar_precio, validar_fecha

def test_validar_cantidad():
    assert validar_cantidad(5) == True
    assert validar_cantidad(0) == False
    assert validar_cantidad(-1) == False
    assert validar_cantidad("abc") == False

def test_validar_precio():
    assert validar_precio(10.5) == True
    assert validar_precio(0) == False
    assert validar_precio(-5.5) == False
    assert validar_precio("abc") == False

def test_validar_fecha():
    assert validar_fecha("01-01-2023") == True
    assert validar_fecha("31-12-2023") == True
    assert validar_fecha("31-02-2023") == False  # Fecha inválida
    assert validar_fecha("2023-01-01") == False  # Formato incorrecto
    assert validar_fecha("abc") == False  # Formato incorrecto