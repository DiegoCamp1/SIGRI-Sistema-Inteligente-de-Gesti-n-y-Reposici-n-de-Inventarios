"""Datos y reposición de un producto."""
from reportes.reporte import Reporte
from modelo.excepciones import ProductoNoEncontradoError


class ReporteIndividual(Reporte):
    def __init__(self, sku):
        self.__sku = sku

    def obtener_datos(self, inventario):
        coincidencias = inventario.buscar_productos(self.__sku, "sku")
        if not coincidencias:
            raise ProductoNoEncontradoError("No existe un producto con ese SKU.")
        producto = coincidencias[0]
        return {
            "sku": producto.sku,
            "nombre": producto.nombre,
            "stock_inicial": producto.stock_inicial,
            "ventas": producto.ventas,
            "mermas": producto.mermas,
            "stock_minimo": producto.stock_minimo,
            "stock_maximo": producto.stock_maximo,
            "stock_actualizado": producto.calcular_stock_actualizado(),
            "requiere_reposicion": producto.requiere_reposicion(),
            "unidades_por_comprar": producto.calcular_unidades_por_comprar(),
        }
