<h1  align="center"> Sistema de inventario </h1>

<p align="center">
  <a href="https://code.visualstudio.com/">
    <img src="https://badgen.net/badge/ide/VisualStudioCode/blue" alt="VS Badge"/></a>
  <a href="https://www.python.org/">
    <img src="https://badgen.net/badge/language/python/yellow" alt="Python Badge"/></a>
  <a href="https://pypi.org/project/tabulate/">
    <img src="https://badgen.net/badge/library/tabulate/cyan" alt="Tabulate Badge"/></a>
</p>

## Descripción de los archivos 📂

- **main.py**: Archivo principal que ejecuta el programa.
- **inventario.py**: Funciones relacionadas con la carga y guardado del inventario.
- **proveedores.py**: Funciones relacionadas con la gestión de proveedores.
- **productos.py**: Funciones relacionadas con la gestión de productos.
- **utilidades.py**: Funciones auxiliares y utilidades generales.
- **datos/**: Carpeta que contiene los archivos JSON de productos y proveedores.

<p> Este proyecto implementa un sistema de inventario utilizando Python que permite a los usuarios gestionar productos, proveedores y datos del inventario, almacenados en un archivo JSON; además permite generar reportes utilizando los datos del inventario. </p>

## Funcionalidades 🔍
<ul>
  <li><strong>Ver inventario</strong>: muestra todos los productos disponibles con sus propiedades.</li>
  <li><strong>Agregar producto</strong>: permite agregar productos nuevos al inventario.</li>
  <li><strong>Borrar producto</strong>: permite borrar un producto del inventario.</li>
  <li><strong>Buscar producto</strong>: facilita la búsqueda de productos específicos por su nombre o codigo.</li>
  <li><strong>Buscar proveedor</strong>: facilita la búsqueda de proveedores específicos por su nombre o codigo.</li>
  <li><strong>Actualizar cantidad</strong>: modifica la cantidad disponible de un producto.</li>
  <li><strong>Generar Reportes</strong>: permite generar los siguientes tipos de reportes para obtener información del inventario: 
  <ul>
    <li>Total de productos</li>
    <li>Valor Total del inventario</li>
    <li>Total de unidades</li>
    <li>Productos por proveedor</li>
    <li>Top 5 productos más caros</li>
  </ul> </li>
</ul>

## Ejecucion Local 💻

#### Pasos para ejecutar este proyecto en tu entorno local:

 **1.** Instala [Visual Studio Code](https://code.visualstudio.com/Download) si no lo tienes instalado.

 **2.** Instala Python 3 visitando la pagina oficial y siguiendo los pasos indicados en la misma: https://www.python.org/downloads/.

 **3.** Clona el repositorio con el comando: `git clone <enlace a repositorio>`.

 **4.** Instala las dependencias necesarias ejecutando: `pip3 install <nombre_paquete>`.

 **5.** Ejecuta el archivo index.py con la opcion ejecutar del IDE utilizado o con el comando `python index.py` para poder utilizar el programa.
