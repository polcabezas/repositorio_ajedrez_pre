"""
Define la pieza Reina y su lógica específica.
"""

from .pieza import Pieza  # Importación relativa desde el mismo directorio
from typing import Literal, Tuple

class Reina(Pieza):
    """
    Representa la pieza de ajedrez Reina.
    """
    def __init__(self, color: Literal['blanco', 'negro'], posicion: Tuple[int, int]):
        """
        Inicializa una Reina.

        Args:
            color: El color de la pieza ('blanco' o 'negro').
            posicion: Una tupla (fila, columna) indicando la posición inicial.
        """
        super().__init__(color, posicion)
        # Aquí se podría añadir lógica específica de la Reina si fuera necesario 