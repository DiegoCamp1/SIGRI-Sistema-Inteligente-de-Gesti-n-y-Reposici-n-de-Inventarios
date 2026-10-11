"""Registro y consulta de productos del inventario."""
from modelo.producto import Producto
from modelo.excepciones import SKUDuplicadoError


class Inventario:
    def __init__(self):
        self.__productos = []

    def registrar_producto(self, producto):
        if not isinstance(producto, Producto):
            raise ValueError("Se necesita un objeto Producto.")
        producto.validar_datos()
        for actual in self.__productos:
            if actual.sku == producto.sku:
                raise SKUDuplicadoError("El SKU " + producto.sku + " ya está registrado.")
        self.__productos.append(producto)

    def buscar_productos(self, criterio, tipo):
        if not isinstance(criterio, str) or not criterio.strip():
            raise ValueError("Escribe un criterio de búsqueda.")
        if not isinstance(tipo, str):
            raise ValueError("El tipo de búsqueda debe ser sku o nombre.")
        tipo = tipo.strip().lower()
        if tipo not in ("sku", "nombre"):
            raise ValueError("El tipo de búsqueda debe ser sku o nombre.")
        criterio = criterio.strip().casefold()
        encontrados = []
        for producto in self.__productos:
            if tipo == "sku" and producto.sku.casefold() == criterio:
                encontrados.append(producto)
            elif tipo == "nombre" and criterio in producto.nombre.casefold():
                encontrados.append(producto)
        return encontrados

    def listar_productos(self):
        # Retorna otra lista para que una consulta no borre la lista interna.
        return self.__productos.copy()

    def listar_criticos(self):
        criticos = []
        for producto in self.__productos:
            if producto.requiere_reposicion():
                criticos.append(producto)
        return criticos

    def generar_reporte(self, reporte):
        # Mismo llamado, comportamiento distinto según el objeto recibido.
        return reporte.generar(self)
