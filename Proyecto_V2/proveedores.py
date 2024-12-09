from datetime import datetime
from inventario import cargar_inventario, guardar_inventario

def seleccionar_proveedor(proveedores, inventario):
    while True:
        print("\n--- Proveedores disponibles ---")
        proveedores_lista = list(proveedores.items())
        for i, (codigo, datos) in enumerate(proveedores_lista, start=1):
            print(f"{i}. {datos['nombre']}")
        
        print("\nIngrese el número del proveedor elegido o escriba 'n' para agregar un nuevo proveedor:")
        seleccion = input("Selección: ").strip()

        if seleccion == "n":
            codigo_proveedor = agregar_nuevo_proveedor(inventario)
            return codigo_proveedor
        elif seleccion.isdigit() and 1 <= int(seleccion) <= len(proveedores_lista):
            indice = int(seleccion) - 1
            codigo_proveedor, datos = proveedores_lista[indice]
            return codigo_proveedor
        else:
            print("Selección inválida. Intente nuevamente.")

def crear_nombre_proveedor(inventario):
    return f"PROV{len(inventario['proveedores']) + 1:03}"

def agregar_nuevo_proveedor(inventario):
    print("\n--- Agregar Nuevo Proveedor ---")
    nombre_proveedor = input("Nombre del proveedor: ").strip()
    direccion = input("Dirección del proveedor: ").strip()
    telefono = input("Teléfono del proveedor: ").strip()
    email = input("Email del proveedor: ").strip()

    # Crea un código para el proveedor
    codigo_proveedor = crear_nombre_proveedor(inventario)

    # Agrega el nuevo proveedor al inventario
    inventario["proveedores"][codigo_proveedor] = {
        "nombre": nombre_proveedor,
        "direccion": direccion,
        "telefono": telefono,
        "email": email
    }

    guardar_inventario(inventario)  # Guarda el inventario actualizado
    return codigo_proveedor

def mostrar_proveedores(proveedores, nav=False):
    # Aquí puedes importar mostrar_tabla justo antes de usarla
    from productos import mostrar_tabla
    
    print("\nInformación de proveedores:")
    headers_proveedores = ["ID", "Nombre", "Dirección", "Teléfono", "Email"]
    datos_proveedores = [[prov_id, proveedor["nombre"], proveedor["direccion"], proveedor["telefono"], proveedor["email"]]
                         for prov_id, proveedor in proveedores.items()]
    mostrar_tabla(datos_proveedores, headers_proveedores, navegar=nav)
    
def buscarProveedores(id_proveedor):
    # Aquí puedes importar mostrar_tabla justo antes de usarla
    from productos import mostrar_tabla
    
    inventario = cargar_inventario()
    proveedores = inventario.get("proveedores", {})

    if not proveedores:
        print("No hay proveedores registrados.")
        return

    palabras_clave = id_proveedor.lower().split() #busca por palabras clave

    #muestra los proveedores que coincidan con las palabras clave
    encontrados = {}
    for codigo, proveedor in proveedores.items():
        nombre_proveedor = proveedor["nombre"].lower()
        if any(palabra in nombre_proveedor for palabra in palabras_clave) or any(palabra in codigo.lower() for palabra in palabras_clave):
            encontrados[codigo] = proveedor

    if not encontrados:
        print("No se encontró ningún proveedor que coincida con la búsqueda.")
    else:
        print("\nResultados de la búsqueda:")
        headers_proveedores = ["Código", "Nombre", "Dirección", "Teléfono", "Email"]
        datos_encontrados = [[codigo, proveedor["nombre"], proveedor["direccion"], proveedor["telefono"], proveedor["email"]]
                             for codigo, proveedor in encontrados.items()]
        
        mostrar_tabla(datos_encontrados, headers_proveedores)
        

def cambiar_proveedor(inventario, codigo_producto):
    lista_proveedores = []
    productos = inventario['productos']
    proveedores = inventario['proveedores']
    
    for codigo_proveedor, datos in proveedores.items():
        lista_proveedores.append(codigo_proveedor)
    
    print('')
    while True:
        print("Proveedores disponibles:")
        i = 0
        for codigo_proveedor, datos in proveedores.items():
            i += 1
            print(f"{i}) Código: {codigo_proveedor} - Nombre: {datos['nombre']}") # muestra un menú enumerado
                    
        numero = int(input('Ingrese el numero: ')) #selecciona un proveedor
        if numero in range(1, len(lista_proveedores)+1):
            productos[codigo_producto]["proveedor_id"] = lista_proveedores[numero-1]
            productos[codigo_producto]["fecha_ultima_actualizacion"] = datetime.now().strftime("%Y/%d/%m")
            guardar_inventario(inventario)
            print('El proveedor del PRODUCTO se cambió correctamente')
            return
        else:
            print('Numero inválido!')