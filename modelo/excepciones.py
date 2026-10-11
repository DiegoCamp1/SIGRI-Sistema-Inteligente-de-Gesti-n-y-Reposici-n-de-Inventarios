"""Excepciones para duplicados y productos inexistentes."""


class SKUDuplicadoError(ValueError):
    pass


class ProductoNoEncontradoError(ValueError):
    pass
