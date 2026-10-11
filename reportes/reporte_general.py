"""Indicadores generales del inventario."""
from reportes.reporte import Reporte


class ReporteGeneral(Reporte):
    def obtener_datos(self, inventario):
        productos = inventario.listar_productos()
        criticos = 0
        ventas = 0
        mermas = 0
        compra = 0
        mayor_merma = 0
        empatados = []
        for producto in productos:
            if producto.requiere_reposicion():
                criticos += 1
            ventas += producto.ventas
            mermas += producto.mermas
            compra += producto.calcular_unidades_por_comprar()
            if producto.mermas > mayor_merma:
                mayor_merma = producto.mermas
                empatados = [{"sku": producto.sku, "nombre": producto.nombre}]
            elif producto.mermas == mayor_merma and mayor_merma > 0:
                empatados.append({"sku": producto.sku, "nombre": producto.nombre})
        total = len(productos)
        porcentaje = 0
        if total > 0:
            porcentaje = 100 * criticos / total
        return {
            "total_productos": total,
            "productos_criticos": criticos,
            "productos_suficientes": total - criticos,
            "total_ventas": ventas,
            "total_mermas": mermas,
            "total_compra": compra,
            "porcentaje_critico": porcentaje,
            "mayor_merma": mayor_merma,
            "productos_mayor_merma": empatados,
        }
