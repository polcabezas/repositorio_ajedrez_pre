"""
Representa el tablero de ajedrez y las posiciones de las piezas.
""" 
from typing import Dict, List, Tuple, Optional
from models.pieza import Pieza
from models.piezas import Torre, Caballo, Alfil, Reina, Rey, Peon

class Tablero:
    """
    Representa el tablero de ajedrez, incluyendo posiciones de piezas, piezas capturadas,
    derechos de enroque y objetivos de captura al paso.
    """
    def __init__(self):
        """
        Inicializa el tablero con casillas vacías y el estado de juego por defecto
        (derechos de enroque, sin objetivo de captura al paso, lista de capturadas vacía),
        y luego coloca las piezas en sus posiciones iniciales.
        """
        # Tablero 8x8 inicializado con None (casillas vacías)
        self.casillas: List[List[Optional[Pieza]]] = [[None for _ in range(8)] for _ in range(8)]

        # Lista para almacenar las piezas capturadas
        self.piezasCapturadas: List[Pieza] = []

        # Seguimiento de los derechos de enroque
        self.derechosEnroque: Dict[str, Dict[str, bool]] = {
            'blanco': {'corto': True, 'largo': True}, # corto = flanco de rey (O-O), largo = flanco de dama (O-O-O)
            'negro': {'corto': True, 'largo': True}
        }

        # Casilla objetivo para captura al paso, formato (fila, columna) o None
        self.objetivoPeonAlPaso: Optional[Tuple[int, int]] = None
    

    def inicializarTablero(self):
        """
        Coloca las piezas en sus posiciones iniciales estándar.
        """

        # Blancas
        self.casillas[0] = [Torre('blanco', 0, 0), Caballo('blanco', 0, 1), Alfil('blanco', 0, 2), Reina('blanco', 0, 3), Rey('blanco', 0, 4), Alfil('blanco', 0, 5), Caballo('blanco', 0, 6), Torre('blanco', 0, 7)]
        self.casillas[1] = [Peon('blanco', 1, 0), Peon('blanco', 1, 1), Peon('blanco', 1, 2), Peon('blanco', 1, 3), Peon('blanco', 1, 4), Peon('blanco', 1, 5), Peon('blanco', 1, 6), Peon('blanco', 1, 7)]

        # Negras
        self.casillas[6] = [Peon('negro', 6, 0), Peon('negro', 6, 1), Peon('negro', 6, 2), Peon('negro', 6, 3), Peon('negro', 6, 4), Peon('negro', 6, 5), Peon('negro', 6, 6), Peon('negro', 6, 7)]
        self.casillas[7] = [Torre('negro', 7, 0), Caballo('negro', 7, 1), Alfil('negro', 7, 2), Reina('negro', 7, 3), Rey('negro', 7, 4), Alfil('negro', 7, 5), Caballo('negro', 7, 6), Torre('negro', 7, 7)]
    

    def getPieza(self, fila: int, columna: int) -> Optional[Pieza]:
        """
        Obtiene la pieza en una posición específica del tablero.

        Args:
            fila: La fila de la pieza.
            columna: La columna de la pieza.

        Returns:
            La pieza en la posición especificada o None si no hay una pieza en esa posición.
        """
        return self.casillas[fila][columna]
    

    def setPieza(self, fila: int, columna: int, pieza: Pieza):
        """
        Establece una pieza en una posición específica del tablero.

        Args:
            fila: La fila de la pieza.
            columna: La columna de la pieza.
            pieza: La pieza a establecer.
        """
        self.casillas[fila][columna] = pieza
    
    
    def moverPieza(self, filaOrigen: int, columnaOrigen: int, filaDestino: int, columnaDestino: int) -> bool:
        """
        Mueve una pieza desde una posición a otra, si es válido.

        Args:
            filaOrigen: La fila de la pieza.
            columnaOrigen: La columna de la pieza.
            filaDestino: La fila de la pieza.
            columnaDestino: La columna de la pieza.

        Returns:
            True si la pieza se mueve correctamente, False en caso contrario.
        """
        pieza = self.getPieza(filaOrigen, columnaOrigen)
        if pieza is None:
            return False
        
        if pieza.color == 'blanco':
            if not self.esPosicionValida(filaDestino, columnaDestino):
                return False
        
        if pieza.color == 'negro':
            if not self.esPosicionValida(filaDestino, columnaDestino):
                return False
        
        # Mover la pieza
        self.casillas[filaDestino][columnaDestino] = pieza # Mover la pieza al destino
        self.casillas[filaOrigen][columnaOrigen] = None # Eliminar la pieza del origen
        
        # Verificar si hay una pieza en el destino
        if self.getPieza(filaDestino, columnaDestino) is not None:
            self.capturarPieza(self.getPieza(filaDestino, columnaDestino))
        
        return True
    

    def capturarPieza(self, pieza: Pieza) -> bool:
        """
        Captura una pieza y la agrega a la lista de capturadas.

        Args:
            pieza: La pieza a capturar.
        
        Returns:
            True si la pieza se captura correctamente, False en caso contrario.
        """
        # Si la pieza no es None, la agrega a la lista de capturadas
        if pieza is not None:
            self.piezasCapturadas.append(pieza)
            return True
     

    def esPosicionValida(self, fila: int, columna: int) -> bool:
        """
        Verifica si una posición es válida en el tablero.
        """
        return 0 <= fila <= 7 and 0 <= columna <= 7
    

    def esCasillaAmenazada(self, fila: int, columna: int, color: Literal['blanco', 'negro']) -> bool:
        """
        Verifica si una posición es amenazada por una pieza del color especificado.

        Args:
            fila: La fila de la posición.
            columna: La columna de la posición.
            color: El color de la pieza.

        Returns:
            True si la posición es amenazada, False en caso contrario.
        """
        # Verificar si hay una pieza del color especificado en la posición
        return False
    




   
                    
