"""
Clase base para todas las piezas de ajedrez.
""" 

from typing import Literal, Tuple, List

class Pieza:
    """
    Clase base para todas las piezas de ajedrez.
    """
    def __init__(self, color: Literal['blanco', 'negro'], posicion: Tuple[int, int]):
        """
        Inicializa una pieza.

        Args:
            color: El color de la pieza ('blanco' o 'negro').
            posicion: Una tupla (fila, columna) indicando la posición inicial.
        """
        self.color: Literal['blanco', 'negro'] = color
        self.posicion: Tuple[int, int] = posicion



