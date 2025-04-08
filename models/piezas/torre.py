"""
Define la pieza Torre y su lógica específica.
"""

from .pieza import Pieza  # Importación relativa desde el mismo directorio
from typing import Literal, Tuple

class Torre(Pieza):
    """
    Representa la pieza de ajedrez Torre.
    """
    def __init__(self, color: Literal['blanco', 'negro'], posicion: Tuple[int, int]):
        """
        Inicializa una Torre.

        Args:
            color: El color de la pieza ('blanco' o 'negro').
            posicion: Una tupla (fila, columna) indicando la posición inicial.
        """
        super().__init__(color, posicion)
        # Aquí se podría añadir lógica específica de la Torre si fuera necesario
