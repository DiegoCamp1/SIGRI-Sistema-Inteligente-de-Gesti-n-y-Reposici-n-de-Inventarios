"""Inicio de la aplicación."""
from modelo.inventario import Inventario


def main():
    from vista.interfaz import InterfazSIGRI
    aplicacion = InterfazSIGRI(Inventario())
    aplicacion.ejecutar()


if __name__ == "__main__":
    main()
