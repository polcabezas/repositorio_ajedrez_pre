"""
Clase base para todas las piezas de ajedrez.
""" 

from typing import Literal # Importar Literal

class Pieza:
    """
    Clase base para todas las piezas de ajedrez.
    """
    def __init__(self, color: Literal['blanco', 'negro'], fila: int, columna: int):
        """
        Inicializa una pieza.

        Args:
            color: El color de la pieza ('blanco' o 'negro').
            fila: La fila inicial de la pieza (0-7).
            columna: La columna inicial de la pieza (0-7).
        """
        self.color= color
        self.fila: int = fila
        self.columna: int = columna
        # Añadiremos más atributos como 'tablero' y 'seHaMovido' después

