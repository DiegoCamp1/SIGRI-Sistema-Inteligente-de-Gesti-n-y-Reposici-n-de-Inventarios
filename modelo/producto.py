"""Validación y cálculos de un producto."""


class Producto:
    def __init__(self, sku, nombre, stock_inicial, ventas, mermas,
                 stock_minimo, stock_maximo):
        if not isinstance(sku, str) or not isinstance(nombre, str):
            raise ValueError("El SKU y el nombre deben ser texto.")
        self.__sku = sku.strip().upper()
        self.__nombre = nombre.strip()
        self.__stock_inicial = stock_inicial
        self.__ventas = ventas
        self.__mermas = mermas
        self.__stock_minimo = stock_minimo
        self.__stock_maximo = stock_maximo
        self.validar_datos()

    def validar_datos(self):
        if not self.__sku or not self.__nombre:
            raise ValueError("Completa el SKU y el nombre del producto.")
        cantidades = [
            ("Stock inicial", self.__stock_inicial),
            ("Ventas", self.__ventas),
            ("Mermas", self.__mermas),
            ("Stock mínimo", self.__stock_minimo),
            ("Stock máximo", self.__stock_maximo),
        ]
        for campo, valor in cantidades:
            # bool hereda de int; no representa una cantidad válida aquí.
            if type(valor) is not int or valor < 0:
                raise ValueError(campo + " debe ser un entero no negativo.")
        if self.__stock_maximo <= self.__stock_minimo:
            raise ValueError("El stock máximo debe ser mayor que el mínimo.")
        if self.__ventas + self.__mermas > self.__stock_inicial:
            raise ValueError("Ventas más mermas no pueden superar el stock inicial.")

    # Propiedades de consulta: los datos no se modifican desde la interfaz.
    @property
    def sku(self):
        return self.__sku

    @property
    def nombre(self):
        return self.__nombre

    @property
    def stock_inicial(self):
        return self.__stock_inicial

    @property
    def ventas(self):
        return self.__ventas

    @property
    def mermas(self):
        return self.__mermas

    @property
    def stock_minimo(self):
        return self.__stock_minimo

    @property
    def stock_maximo(self):
        return self.__stock_maximo

    def calcular_stock_actualizado(self):
        return self.__stock_inicial - self.__ventas - self.__mermas

    def requiere_reposicion(self):
        return self.calcular_stock_actualizado() <= self.__stock_minimo

    def calcular_unidades_por_comprar(self):
        if self.requiere_reposicion():
            return self.__stock_maximo - self.calcular_stock_actualizado()
        return 0
