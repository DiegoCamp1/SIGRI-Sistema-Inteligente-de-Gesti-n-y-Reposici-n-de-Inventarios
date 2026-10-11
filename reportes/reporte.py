"""Flujo común para generar reportes."""
from abc import ABC, abstractmethod


class Reporte(ABC):
    def generar(self, inventario):
        datos = self.obtener_datos(inventario)
        return self.formatear(datos)

    @abstractmethod
    def obtener_datos(self, inventario):
        pass

    def formatear(self, datos):
        # Copia estructurada: conserva números y no introduce widgets.
        return dict(datos)
