from inventario import cargar_inventario, ver_inventario
from productos import agregar_producto, borrar_producto, buscar_producto, mostrar_tabla
from proveedores import cambiar_proveedor, mostrar_proveedores, buscarProveedores
from utilidades import actualizar_cantidad, continuar, editar_fecha, editar_nombre, editar_precio, input_fecha_validada, limpiar_consola, verificar_codigo_producto
from menus import menu_opciones, menu_reportes, menu_edicion
from reportes import reporte_productos_mas_caros, reporte_productos_por_proveedor, reporte_total_productos, reporte_total_unidades, reporte_valor_inventario
import os

# Función principal del programa
def main(): 
    ...
    Start = True
    while Start:

        menu_opciones()
        
        while True:
            opcion = input("Ingrese una opción: ")
            
            if opcion == "-1":
                break
            
            if opcion.isdigit():
                break
            else:
                print("Por favor, ingrese un número válido.")
        if opcion == "-1":
            print("Gracias por usar el sistema de inventario.")
            break
                
        limpiar_consola()
        print("")                
        if opcion == "1":
            ver_inventario()
            continuar()
        
        if opcion == "2":
            agregar_producto()
            continuar()
        
        if opcion == "3": #Buscar producto
            id_producto = input("Ingrese el código o el nombre: ")
            buscar_producto(id_producto)
            continuar()
            
        if opcion == "4": #listar proveedores
            inventario = cargar_inventario()
            mostrar_proveedores(inventario["proveedores"], nav=True)
            continuar()
        
        if opcion == "5": #Buscar proveedor
            id_proveedor = input("Ingrese el código o el nombre del proveedor: ")
            buscarProveedores(id_proveedor)
            continuar()
            
        if opcion == "6":
            bandera = True
            while bandera:
                menu_reportes()
                opcion_reporte = input("Ingrese una opción de reporte: ")
                limpiar_consola()
                print("")
                
                if opcion_reporte == "1":
                    reporte_total_productos()
                    continuar()
                
                elif opcion_reporte == "2":
                    reporte_valor_inventario()
                    continuar()
                
                elif opcion_reporte == "3":
                    reporte_total_unidades()
                    continuar()
                
                elif opcion_reporte == "4":
                    proveedor = input("Ingrese el nombre o codigo del proveedor: ")
                    reporte_productos_por_proveedor(proveedor)
                    continuar()
                    
                elif opcion_reporte == "5":
                    reporte_productos_mas_caros()
                    continuar()
                
                elif opcion_reporte == "-1":
                    bandera = False
                
                else:
                    print("Opción inválida")
            continuar()
                 
        #Opcion de borrado por codigo
        if opcion == "7":
            metodo = input("Ingrese el código o nombre del producto a eliminar: ")
            borrar_producto(metodo)
        
        #Menú de opciones de edición de productos
        if opcion == "8":
            bandera = True
            while bandera:
                menu_edicion()
                opcion_editar = input("Ingrese una opción de edicion: ")
                os.system('cls' if os.name == 'nt' else 'clear') #limpia la pantalla
                print("")

                if opcion_editar == "1":
                    codigo = input("Ingrese el código: ")
                    nuevo_nombre = input("Ingrese el nuevo nombre: ")
                    nombre_producto = editar_nombre(codigo, nuevo_nombre)
                    if nombre_producto:
                        print(f"Nombre del producto '{nombre_producto}' actualizado a {nuevo_nombre}.")
                    else:
                        print("Producto no encontrado")
                    continuar()
                
                
                if opcion_editar == "2":
                    codigo = input("Ingrese el código: ")
                    nueva_cantidad = int(input("Ingrese la nueva cantidad: "))
                    nombre_producto = actualizar_cantidad(codigo, nueva_cantidad)

                    if nombre_producto:
                        print(f"Cantidad del producto '{nombre_producto}' actualizada a {nueva_cantidad} unidades.")
                    else:
                        print("Producto no encontrado")
                    continuar()

                if opcion_editar == "3":
                    codigo = input("Ingrese el código: ")
                    nuevo_precio = int(input("Ingrese el nuevo precio: "))
                    nombre_producto= editar_precio(codigo,nuevo_precio)
                    
                    if nombre_producto:
                        print(f"Precio del producto '{nombre_producto}' actualizado a ${nuevo_precio}.")
                    else:
                        print("Producto no encontrado")
                    continuar()

                if opcion_editar == "4": #Editar fecha
                    codigo = input("Ingrese el código: ")
                    nueva_fecha = input_fecha_validada()
                    nombre_producto= editar_fecha(codigo, nueva_fecha)
                    
                    if nombre_producto:
                        print(f"Fecha del producto '{nombre_producto}' actualizada a {nueva_fecha}.")
                    else:
                        print("Producto no encontrado")
                    continuar()
                
                if opcion_editar == "5": #Con formato proveedor
                    inventario = cargar_inventario()
                    mostrar_proveedores(inventario["proveedores"])
                    
                    while True:
                        codigo = input("Ingrese el código del producto: ")
                        if verificar_codigo_producto(codigo):
                            break
                        else:
                            print("Código de producto inválido. Intente nuevamente.")
                        
                    cambiar_proveedor(inventario, codigo)
                    continuar()

                elif opcion_editar == "-1":
                    bandera = False

        if opcion == "9":
            alumnos()
            continuar()

        
        if int(opcion) not in range(1, 5) and opcion != "-1":
            print("Opción inválida")

def alumnos():
    matriz = [
        ["Brayan Zorro"],
        ["Luana Kaladjian"],
        ["Gabriel Pabón"],
        ["Estefanía Sassone"]
    ]
    headers = ["Nombre del Alumno"]
    mostrar_tabla(matriz, headers)


main()