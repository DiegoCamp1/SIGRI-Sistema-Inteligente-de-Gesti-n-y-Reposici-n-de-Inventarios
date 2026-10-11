# SIGRI — Servimarsa Perú

Sistema de gestión y reposición de inventarios para el trabajo final de
Fundamentos de Programación II. Está desarrollado en Python con una interfaz
gráfica en Tkinter.

Permite registrar productos, buscar por SKU o nombre, consultar el inventario,
identificar productos críticos y generar reportes individuales y generales.
Valida las cantidades ingresadas y evita SKU duplicados.

## Funcionamiento

Cada producto tiene SKU, nombre, stock inicial, ventas, mermas, stock mínimo y
stock máximo. Ventas y mermas representan los totales de un mismo periodo.

El stock actualizado es el inicial menos ventas y mermas. Si queda en el mínimo
o por debajo, el sistema calcula cuántas unidades comprar para alcanzar el máximo.
El inventario se mantiene en memoria durante la sesión y se borra al cerrar.

## Organización

| Ubicación | Contenido |
| --- | --- |
| `modelo/` | Producto, Inventario y excepciones. |
| `reportes/` | Reporte, ReporteIndividual y ReporteGeneral. |
| `vista/` | Menú, formularios y presentación de resultados. |
| `main.py` | Inicio de la aplicación. |

Los reportes utilizan herencia y polimorfismo. Inventario recibe el reporte
seleccionado (Strategy) y Reporte define la secuencia común de generación
(Template Method).

## Requisitos y ejecución

Se necesita Python 3 con Tkinter y una pantalla gráfica. Se utiliza únicamente
la biblioteca estándar de Python; no es necesario instalar paquetes externos.

Abrir una terminal en la carpeta que contiene `main.py` y ejecutar en Windows:

```powershell
py -3 main.py
```

También se puede abrir `iniciar_windows.bat`. Si no está disponible el lanzador
`py`, usar `python main.py`. Para comprobar Tkinter, ejecutar `python -m tkinter`.
Mantener las carpetas `modelo`, `reportes` y `vista` junto a `main.py`.

## Comprobación del funcionamiento

Registrar estos productos desde el menú:

| SKU | Nombre | Inicial | Ventas | Mermas | Mínimo | Máximo |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| P001 | Leche 1 L | 80 | 45 | 5 | 35 | 100 |
| P002 | Arroz 1 kg | 80 | 40 | 5 | 35 | 100 |
| P003 | Agua 1 L | 80 | 30 | 5 | 35 | 100 |

El sistema debe calcular stocks de **30, 35 y 45**, y compras de **70, 65 y 0**
unidades, respectivamente. Estos resultados no se ingresan en el formulario.

El reporte general debe mostrar 3 productos, 2 críticos, 1 suficiente, ventas
115, mermas 15, compra 135 y porcentaje crítico 66.67 %. Los tres productos
empatan en la mayor merma, con 5 unidades.

Comprobar también la búsqueda por SKU y nombre, la selección de productos,
el rechazo de datos inválidos y SKU repetidos, y la cancelación de salida.
Con inventario vacío, los indicadores generales deben ser cero.
