import os
from datetime import datetime
from utilidades import limpiar_consola, validar_cantidad, validar_precio, validar_fecha, input_fecha_validada, generar_codigo_unico, formatear, procesar_fecha, continuar

def test_limpiar_consola(monkeypatch):
    monkeypatch.setattr(os, 'system', lambda x: None)
    limpiar_consola()
    assert True  # If no exception is raised, the test passes

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


def test_generar_codigo_unico():
    inventario = {'productos': {'1001': {}, '1002': {}}}
    assert generar_codigo_unico(inventario) == '1003'
    inventario = {'productos': {}}
    assert generar_codigo_unico(inventario) == '1001'

def test_formatear():
    fecha = datetime.strptime("01-01-2023", "%d-%m-%Y")
    assert formatear(fecha) == "01-01-2023"

def test_procesar_fecha():
    fecha = "01-01-2023"
    assert procesar_fecha(fecha) == datetime.strptime(fecha, "%d-%m-%Y")

def test_continuar(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: None)
    monkeypatch.setattr(os, 'system', lambda x: None)
    continuar()
    assert True  # If no exception is raised, the test passes