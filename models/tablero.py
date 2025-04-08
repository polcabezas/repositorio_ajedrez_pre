"""
Representa el tablero de ajedrez y las posiciones de las piezas.
""" 
import logging
from typing import Dict, List, Tuple, Optional, Literal
from collections import defaultdict # Importar defaultdict

# Importar piezas
from models.piezas.pieza import Pieza
from models.piezas.torre import Torre
from models.piezas.caballo import Caballo
from models.piezas.alfil import Alfil
from models.piezas.reina import Reina
from models.piezas.rey import Rey
from models.piezas.peon import Peon

# Configure basic logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Tablero:
    """
    Representa el tablero de ajedrez, incluyendo posiciones de piezas, piezas capturadas,
    derechos de enroque y objetivos de captura al paso.
    """
    # ============================================================
    # 1. Inicialización y Configuración del Tablero
    # ============================================================
    
    def __init__(self):
        """
        Inicializa el tablero con casillas vacías y el estado de juego por defecto
        (derechos de enroque, sin objetivo de captura al paso, lista de capturadas vacía),
        y luego coloca las piezas en sus posiciones iniciales.
        """
        # Tablero 8x8 inicializado con None (casillas vacías)
        self.casillas: List[List[Optional[Pieza]]] = [[None for _ in range(8)] for _ in range(8)]

        # Historial de movimientos (color, posOrigen, posDestino) - Puede necesitar enriquecerse para simulación perfecta
        self.historial_movimientos: List[Tuple[Literal['blanco', 'negro'], Tuple[int, int], Tuple[int, int]]] = []

        # Lista para almacenar las piezas capturadas
        self.piezasCapturadas: List[Pieza] = []

        # Seguimiento de los derechos de enroque
        self.derechosEnroque: Dict[str, Dict[str, bool]] = {
            'blanco': {'corto': True, 'largo': True}, # corto = flanco de rey (O-O), largo = flanco de dama (O-O-O)
            'negro': {'corto': True, 'largo': True}
        }

        # Casilla objetivo para captura al paso, formato (fila, columna) o None
        self.objetivoPeonAlPaso: Optional[Tuple[int, int]] = None

        # Turno del jugador
        self.turno_blanco: bool = True # True = turno del blanco, False = turno del negro

        # Contador para la regla de los 50 movimientos (se resetea con captura o mov. de peón)
        self.contadorRegla50Movimientos: int = 0

        # Contador de plies (medio movimiento). Empieza en 0 antes del primer movimiento.
        self.contadorPly: int = 0

        # Estado del juego (en curso, jaque, jaque mate, tablas, etc.)
        self.estado_juego: Literal['en_curso', 'jaque', 'jaque_mate', 'tablas'] = 'en_curso'

        # Número de movimiento completo (1 para el primer movimiento de blancas)
        self.numero_movimiento: int = 1

        # Información del último movimiento realizado (origen, destino)
        self.ultimo_movimiento: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None

        # Historial de posiciones para la regla de triple repetición
        # Clave: string de representación de posición (FEN-like), Valor: contador de ocurrencias
        self.historial_posiciones: Dict[str, int] = defaultdict(int)

        # Inicializar el tablero con piezas
        self.inicializarTablero()

        # Registrar la posición inicial en el historial de repeticiones
        estado_inicial = self.obtenerPosicionActual()
        self.historial_posiciones[estado_inicial] = 1

    def inicializarTablero(self):
        """
        Coloca las piezas en sus posiciones iniciales estándar.
        Utiliza tuplas (fila, columna) para las posiciones al crear las piezas.
        """
        # Blancas - Usando tuplas para las posiciones
        self.casillas[0] = [Torre('blanco', (0, 0)), Caballo('blanco', (0, 1)), Alfil('blanco', (0, 2)), Reina('blanco', (0, 3)), Rey('blanco', (0, 4)), Alfil('blanco', (0, 5)), Caballo('blanco', (0, 6)), Torre('blanco', (0, 7))]
        self.casillas[1] = [Peon('blanco', (1, 0)), Peon('blanco', (1, 1)), Peon('blanco', (1, 2)), Peon('blanco', (1, 3)), Peon('blanco', (1, 4)), Peon('blanco', (1, 5)), Peon('blanco', (1, 6)), Peon('blanco', (1, 7))]

        # Negras - Usando tuplas para las posiciones
        self.casillas[6] = [Peon('negro', (6, 0)), Peon('negro', (6, 1)), Peon('negro', (6, 2)), Peon('negro', (6, 3)), Peon('negro', (6, 4)), Peon('negro', (6, 5)), Peon('negro', (6, 6)), Peon('negro', (6, 7))]
        self.casillas[7] = [Torre('negro', (7, 0)), Caballo('negro', (7, 1)), Alfil('negro', (7, 2)), Reina('negro', (7, 3)), Rey('negro', (7, 4)), Alfil('negro', (7, 5)), Caballo('negro', (7, 6)), Torre('negro', (7, 7))]

    # ============================================================
    # 2. Consulta del Tablero y Validación Básica
    # ============================================================

    def esPosicionValida(self, posicion: Tuple[int, int]) -> bool:
        """
        Verifica si una posición (tupla) es válida dentro de los límites del tablero.
        
        Args:
            posicion: Una tupla (fila, columna) indicando la casilla.
        """
        # Asegurarse de que posicion es realmente una tupla de dos enteros
        if not (isinstance(posicion, tuple) and len(posicion) == 2 and
                isinstance(posicion[0], int) and isinstance(posicion[1], int)):
            return False
        fila, columna = posicion
        return 0 <= fila <= 7 and 0 <= columna <= 7

    def getPieza(self, posicion: Tuple[int, int]) -> Optional[Pieza]:
        """
        Obtiene la pieza en una posición específica del tablero.

        Args:
            posicion: Una tupla (fila, columna) indicando la casilla.

        Returns:
            La pieza en la posición especificada o None si no hay una pieza en esa posición
            o si la posición es inválida.
        """
        if not self.esPosicionValida(posicion):
            return None
        fila, columna = posicion
        return self.casillas[fila][columna]
    
    def esBlanco(self, posicion: Tuple[int, int]) -> bool:
        """
        Verifica si una pieza en una posición dada es blanca.
        
        Args:
            posicion: Una tupla (fila, columna) indicando la casilla.

        Returns:
            True si la pieza es blanca, False en caso contrario o si la casilla está vacía.
        """
        pieza = self.getPieza(posicion)
        return pieza is not None and pieza.color == 'blanco'
    
    # ============================================================
    # 3. Ejecución Central del Movimiento
    # ============================================================

    def moverPieza(self, posOrigen: Tuple[int, int], posDestino: Tuple[int, int]) -> Literal['movimiento_ok', 'promocion_necesaria', 'error']:
        """
        Intenta mover una pieza desde una posición a otra. Realiza las siguientes acciones:
        1. Validaciones básicas (posiciones válidas, pieza en origen, no captura propia).
        2. Gestiona la captura normal o la captura especial 'al paso'.
        3. Mueve la pieza en el tablero (`self.casillas`).
        4. Añade el movimiento al historial.
        5. Actualiza la posición interna de la pieza (`pieza.posicion`).
        6. Llama a los métodos para actualizar el estado del juego (enroque, peón al paso, contadores, etc.).
        7. Detecta si se requiere una promoción de peón.
        8. Cambia el turno.
        9. Actualiza el historial de posiciones DESPUÉS de cambiar el turno
        
        NOTA: 
         - Esta función NO valida la legalidad completa del movimiento 
           (p. ej., no comprueba si el movimiento sigue las reglas de la pieza 
           o si deja al rey en jaque). Esa validación debe ocurrir ANTES de llamar a este método.
         - NO maneja el movimiento de enroque, para eso usar `realizarEnroque`.

        Args:
            posOrigen: Tupla (fila, columna) de la casilla origen.
            posDestino: Tupla (fila, columna) de la casilla destino.

        Returns:
            - 'movimiento_ok': El movimiento se realizó con éxito.
            - 'promocion_necesaria': El movimiento fue un avance de peón a la última fila y requiere promoción.
            - 'error': Hubo un problema con las validaciones básicas (p.ej., origen vacío, destino inválido).
        """
        # 1. Validar posiciones y pieza en origen
        if not self.esPosicionValida(posOrigen) or not self.esPosicionValida(posDestino):
            logger.error(f"Posición origen {posOrigen} o destino {posDestino} inválida.")
            return 'error'
        pieza_movida = self.getPieza(posOrigen)
        if pieza_movida is None:
            logger.error(f"No hay pieza en la posición origen {posOrigen}.")
            return 'error'

        # Determinar si es captura y si es en passant
        pieza_capturada = self.getPieza(posDestino)
        es_captura = False
        es_en_passant = False
        casilla_captura_ep = None # Casilla donde estaba el peón capturado al paso

        # Comprobar si es un movimiento de peón al destino objetivo de 'al paso'
        if isinstance(pieza_movida, Peon) and posDestino == self.objetivoPeonAlPaso:
            es_captura = True
            es_en_passant = True
            # El peón capturado está en la misma columna que el destino,
            # pero en la fila de origen del peón que se mueve
            fila_capturada = posOrigen[0]
            col_capturada = posDestino[1]
            casilla_captura_ep = (fila_capturada, col_capturada)
            pieza_capturada_ep = self.getPieza(casilla_captura_ep)
            if pieza_capturada_ep is None or pieza_capturada_ep.color == pieza_movida.color:
                logger.error(f"Intento de captura al paso inválida en {posDestino} (sin peón o peón propio en {casilla_captura_ep})")
                return 'error'
            self.capturarPieza(pieza_capturada_ep)
            self.setPieza(casilla_captura_ep, None)
            logger.debug(f"Captura al paso realizada. Peón capturado en {casilla_captura_ep}")

        # 2. Gestionar captura normal (si no fue al paso)
        elif pieza_capturada is not None:
            if pieza_capturada.color == pieza_movida.color:
                logger.error(f"Intento de captura de pieza propia en {posDestino}.")
                return 'error'
            self.capturarPieza(pieza_capturada)
            es_captura = True

        # 3. Mover la pieza en el tablero
        self.setPieza(posDestino, pieza_movida)
        self.setPieza(posOrigen, None)

        # 4. Añadir al historial
        # TODO: Considerar añadir información extra al historial para en passant/promoción si es necesario para FEN o PGN.
        color_jugador = pieza_movida.color
        self.historial_movimientos.append((color_jugador, posOrigen, posDestino))

        # 5. Actualizar posición interna de la pieza
        if hasattr(pieza_movida, 'posicion'):
             pieza_movida.posicion = posDestino
        else:
             logger.warning(f"La pieza {type(pieza_movida).__name__} movida a {posDestino} no tiene atributo 'posicion' para actualizar.")

        # 6. Actualizar estado del juego post-movimiento (excepto turno)
        # Se actualizan derechos de enroque *después* de mover la pieza y registrar captura.
        self.actualizarDerechosEnroque(pieza_movida, posOrigen, pieza_capturada, posDestino)
        # El objetivo al paso se actualiza DESPUÉS de los derechos de enroque
        self.actualizarPeonAlPaso(pieza_movida, posOrigen, posDestino)
        self.actualizarContadores(pieza_movida, es_captura)
        self.actualizarUltimoMovimiento(posOrigen, posDestino)
        self.actualizarEstadoJuego() # Llama internamente a esMaterialInsuficiente y esTripleRepeticion

        # 7. Detectar promoción de peón
        es_promocion = False
        if isinstance(pieza_movida, Peon):
            fila_destino = posDestino[0]
            if (pieza_movida.color == 'blanco' and fila_destino == 7) or \
               (pieza_movida.color == 'negro' and fila_destino == 0):
                es_promocion = True
                logger.debug(f"Promoción necesaria en {posDestino}")

        # 8. Cambiar turno
        self.turno_blanco = not self.turno_blanco

        # 9. Actualizar historial de posiciones DESPUÉS de cambiar el turno
        estado_actual = self.obtenerPosicionActual()
        self.historial_posiciones[estado_actual] += 1
        logger.debug(f"Historial posiciones actualizado. Estado: '{estado_actual}', Count: {self.historial_posiciones[estado_actual]}")

        # Retornar estado
        if es_promocion:
            return 'promocion_necesaria'
        else:
            return 'movimiento_ok'

    def capturarPieza(self, pieza: Pieza) -> bool:
        """
        Añade una pieza a la lista de capturadas.
        Es llamada por `moverPieza`.

        Args:
            pieza: La pieza a capturar.
        
        Returns:
            True si la pieza se añade correctamente (no es None), False en caso contrario.
        """
        if pieza is not None:
            self.piezasCapturadas.append(pieza)
            logger.info(f"Pieza capturada: {type(pieza).__name__} {pieza.color}") # Log info
            return True
        return False

    def setPieza(self, posicion: Tuple[int, int], pieza: Optional[Pieza]):
        """
        Establece una pieza (o None) en una posición específica del tablero.
        Es un método auxiliar para `moverPieza` y `inicializarTablero`. No valida la posición.

        Args:
            posicion: Una tupla (fila, columna) indicando la casilla.
            pieza: La pieza a establecer, o None para vaciar la casilla.
        """
        fila, columna = posicion
        self.casillas[fila][columna] = pieza
    
    def realizarEnroque(self, color: Literal['blanco', 'negro'], tipo: Literal['corto', 'largo']) -> bool:
        """
        Realiza el movimiento de enroque (Rey y Torre) asumiendo que ya ha sido validado.
        Actualiza las posiciones en el tablero, el historial y el estado general del juego.

        Args:
            color: El color del jugador que enroca ('blanco' o 'negro').
            tipo: El tipo de enroque ('corto' para flanco de rey, 'largo' para flanco de dama).

        Returns:
            True si el enroque se realizó con éxito (según los parámetros), False si hubo un error inesperado.
        """
        # Determinar filas y columnas según el color y tipo
        fila = 0 if color == 'blanco' else 7
        
        # Posiciones iniciales y finales del Rey
        rey_col_origen = 4
        rey_pos_origen = (fila, rey_col_origen)
        rey_col_destino = 6 if tipo == 'corto' else 2
        rey_pos_destino = (fila, rey_col_destino)
        
        # Posiciones iniciales y finales de la Torre
        torre_col_origen = 7 if tipo == 'corto' else 0
        torre_pos_origen = (fila, torre_col_origen)
        torre_col_destino = 5 if tipo == 'corto' else 3
        torre_pos_destino = (fila, torre_col_destino)
        
        # Obtener las piezas (deberían ser Rey y Torre)
        rey = self.getPieza(rey_pos_origen)
        torre = self.getPieza(torre_pos_origen)
        
        if not isinstance(rey, Rey) or not isinstance(torre, Torre):
            logger.error(f"Piezas incorrectas en {rey_pos_origen} o {torre_pos_origen} para enroque {color} {tipo}.")
            return False
        
        # Mover las piezas en el tablero
        self.setPieza(rey_pos_destino, rey)
        self.setPieza(rey_pos_origen, None)
        self.setPieza(torre_pos_destino, torre)
        self.setPieza(torre_pos_origen, None)
        
        # Actualizar posición interna de las piezas
        if hasattr(rey, 'posicion'): rey.posicion = rey_pos_destino
        if hasattr(torre, 'posicion'): torre.posicion = torre_pos_destino
        
        # Añadir al historial (puede requerir formato especial para PGN/FEN)
        # Por ahora, añadimos un registro simple indicando enroque
        # O podríamos añadir los dos movimientos individuales? Mejor uno conceptual.
        self.historial_movimientos.append((color, rey_pos_origen, rey_pos_destino)) # Registramos el mov del rey como representativo
        
        # Actualizar estado: derechos de enroque se pierden, contadores avanzan, etc.
        # El rey se movió, así que pierde ambos derechos
        self.derechosEnroque[color]['corto'] = False
        self.derechosEnroque[color]['largo'] = False
        # Actualizar Peón al Paso (se limpia porque no fue mov de peón)
        self.objetivoPeonAlPaso = None 
        # Actualizar Contadores (enroque no es captura ni mov de peón)
        self.actualizarContadores(rey, False) # Usamos el rey como pieza movida
        # Actualizar Último Movimiento (registramos el del rey)
        self.actualizarUltimoMovimiento(rey_pos_origen, rey_pos_destino)
        # Actualizar Estado del Juego
        self.actualizarEstadoJuego()
        
        # Cambiar turno
        self.turno_blanco = not self.turno_blanco
        
        # 9. Actualizar historial de posiciones DESPUÉS de cambiar el turno
        estado_actual = self.obtenerPosicionActual()
        self.historial_posiciones[estado_actual] += 1
        logger.debug(f"Historial posiciones actualizado (enroque). Estado: '{estado_actual}', Count: {self.historial_posiciones[estado_actual]}")
        
        logger.info(f"Enroque {color} {tipo} realizado.")
        return True
    
    # ============================================================
    # 4. Evaluación de Amenazas
    # ============================================================

    def esCasillaAmenazada(self, posicion: Tuple[int, int], color_atacante: Literal['blanco', 'negro']) -> bool:
        """
        Verifica si una posición es amenazada por alguna pieza del color especificado.
        Depende de `obtener_movimientos_potenciales` en las clases de Pieza.
        Es crucial para la detección de jaque.

        Args:
            posicion: Tupla (fila, columna) de la casilla a verificar.
            color_atacante: El color de las piezas que podrían estar atacando.
        
        Returns:
            True si la posición es amenazada, False en caso contrario.
        """
        if not self.esPosicionValida(posicion):
            return False

        for fila_idx, fila in enumerate(self.casillas):
            for col_idx, pieza in enumerate(fila):
                if pieza is not None and pieza.color == color_atacante:
                    try:
                        movimientos_potenciales = pieza.obtener_movimientos_potenciales(self)
                        if posicion in movimientos_potenciales:
                            return True
                    except AttributeError:
                         logger.warning(f"La pieza {type(pieza).__name__} no tiene 'obtener_movimientos_potenciales'. Amenaza desde {(fila_idx, col_idx)} no verificada.")
                         continue
     
        return False

    # ============================================================
    # 5. Actualización del Estado del Juego (Post-Movimiento)
    # ============================================================
    
    def getTurnoColor(self) -> Literal['blanco', 'negro']:
        """
        Devuelve el color del jugador cuyo turno es.
        """
        return 'blanco' if self.turno_blanco else 'negro'
    
    def actualizarDerechosEnroque(self, pieza_movida: Pieza, posOrigen: Tuple[int, int], pieza_capturada: Optional[Pieza] = None, posDestino: Optional[Tuple[int, int]] = None):
        """
        Actualiza los derechos de enroque si se mueve el rey o una torre desde su posición inicial,
        o si una torre es capturada en su posición inicial.
        Llamado por `moverPieza`.

        Args:
            pieza_movida: La pieza que se acaba de mover.
            posOrigen: La posición original de la pieza movida.
            pieza_capturada: La pieza capturada en el movimiento (si la hay).
            posDestino: La posición destino del movimiento (usada para detectar captura de torre).
        """
        color_movido = pieza_movida.color

        # Casillas iniciales de las torres
        torre_blanca_larga, torre_blanca_corta = (0, 0), (0, 7)
        torre_negra_larga, torre_negra_corta = (7, 0), (7, 7)

        # 1. Si el REY se mueve, pierde AMBOS derechos de enroque
        if isinstance(pieza_movida, Rey):
            if self.derechosEnroque[color_movido]['corto']:
                self.derechosEnroque[color_movido]['corto'] = False
                logger.debug(f"Enroque corto perdido para {color_movido} (movimiento de rey)")
            if self.derechosEnroque[color_movido]['largo']:
                self.derechosEnroque[color_movido]['largo'] = False
                logger.debug(f"Enroque largo perdido para {color_movido} (movimiento de rey)")
            # No necesitamos hacer más si el rey se movió
            return

        # 2. Si una TORRE se mueve DESDE su casilla inicial, pierde el derecho de ESE LADO
        if isinstance(pieza_movida, Torre):
            if color_movido == 'blanco':
                if posOrigen == torre_blanca_corta and self.derechosEnroque['blanco']['corto']:
                    self.derechosEnroque['blanco']['corto'] = False
                    logger.debug("Enroque corto perdido para blanco (movimiento torre corta)")
                elif posOrigen == torre_blanca_larga and self.derechosEnroque['blanco']['largo']:
                    self.derechosEnroque['blanco']['largo'] = False
                    logger.debug("Enroque largo perdido para blanco (movimiento torre larga)")
            elif color_movido == 'negro':
                if posOrigen == torre_negra_corta and self.derechosEnroque['negro']['corto']:
                    self.derechosEnroque['negro']['corto'] = False
                    logger.debug("Enroque corto perdido para negro (movimiento torre corta)")
                elif posOrigen == torre_negra_larga and self.derechosEnroque['negro']['largo']:
                    self.derechosEnroque['negro']['largo'] = False
                    logger.debug("Enroque largo perdido para negro (movimiento torre larga)")

        # 3. Si una TORRE es CAPTURADA EN su casilla inicial, el OPONENTE pierde el derecho de ESE LADO
        # Nota: Se usa posDestino porque es la casilla donde estaba la torre *antes* de ser capturada.
        if pieza_capturada is not None and isinstance(pieza_capturada, Torre) and posDestino is not None:
            color_capturada = pieza_capturada.color
            if color_capturada == 'blanco':
                if posDestino == torre_blanca_corta and self.derechosEnroque['blanco']['corto']: # Torre blanca corta fue capturada
                    self.derechosEnroque['blanco']['corto'] = False
                    logger.debug("Enroque corto perdido para blanco (torre corta capturada)")
                elif posDestino == torre_blanca_larga and self.derechosEnroque['blanco']['largo']: # Torre blanca larga fue capturada
                    self.derechosEnroque['blanco']['largo'] = False
                    logger.debug("Enroque largo perdido para blanco (torre larga capturada)")
            elif color_capturada == 'negro':
                if posDestino == torre_negra_corta and self.derechosEnroque['negro']['corto']: # Torre negra corta fue capturada
                    self.derechosEnroque['negro']['corto'] = False
                    logger.debug("Enroque corto perdido para negro (torre corta capturada)")
                elif posDestino == torre_negra_larga and self.derechosEnroque['negro']['largo']: # Torre negra larga fue capturada
                    self.derechosEnroque['negro']['largo'] = False
                    logger.debug("Enroque largo perdido para negro (torre larga capturada)")

    def actualizarPeonAlPaso(self, pieza_movida: Pieza, posOrigen: Tuple[int, int], posDestino: Tuple[int, int]):
        """
        Actualiza la casilla objetivo para captura al paso si un peón avanza dos casillas.
        Limpia el objetivo en cualquier otro movimiento. Llamado por `moverPieza`.

        Args:
            pieza_movida: La pieza que se acaba de mover.
            posOrigen: La posición original de la pieza movida.
            posDestino: La posición final de la pieza movida.
        """
        self.objetivoPeonAlPaso = None 

        if isinstance(pieza_movida, Peon) and abs(posOrigen[0] - posDestino[0]) == 2:
            fila_objetivo = (posOrigen[0] + posDestino[0]) // 2
            columna_objetivo = posOrigen[1]
            self.objetivoPeonAlPaso = (fila_objetivo, columna_objetivo)

    def actualizarContadores(self, pieza_movida: Pieza, es_captura: bool):
        """
        Actualiza el contador de ply, el número de movimiento y el contador de la regla de 50 movimientos.
        Llamado por `moverPieza`.

        Args:
            pieza_movida: La pieza que se acaba de mover.
            es_captura: True si el movimiento fue una captura, False en caso contrario.
        """
        self.contadorPly += 1

        # El número de movimiento incrementa después de que las negras muevan
        if not self.turno_blanco: # Si turno_blanco es False, las negras ACABAN de mover
            self.numero_movimiento += 1

        # Resetear contador de 50 movimientos si fue un movimiento de peón o una captura
        if isinstance(pieza_movida, Peon) or es_captura:
            self.contadorRegla50Movimientos = 0
        else:
            self.contadorRegla50Movimientos += 1
            
    def actualizarUltimoMovimiento(self, posOrigen: Tuple[int, int], posDestino: Tuple[int, int]):
        """
        Almacena las coordenadas del último movimiento realizado. Llamado por `moverPieza`.
        """
        self.ultimo_movimiento = (posOrigen, posDestino)

    def actualizarEstadoJuego(self):
        """
        Evalúa el estado actual del juego (en curso, jaque, jaque mate, tablas).
        Llamado por `moverPieza` y `realizarEnroque`.
        Depende de `esCasillaAmenazada` y `esTripleRepeticion`.
        
        NOTA:
         - Verifica jaque y tablas por 50 mov/repetición/material insuficiente (TODO).
         - NO implementa chequeo completo de mate/ahogado, ya que requiere la 
           generación de TODOS los movimientos legales para el jugador actual, 
           lo cual es responsabilidad de una capa superior (Controlador/Validador).
        """
        color_jugador_actual = self.getTurnoColor() # Color del jugador QUE VA A MOVER AHORA
        color_oponente = 'negro' if color_jugador_actual == 'blanco' else 'blanco'
        
        # Encontrar el rey del jugador actual
        rey_pos = None
        for r, fila in enumerate(self.casillas):
            for c, pieza in enumerate(fila):
                if isinstance(pieza, Rey) and pieza.color == color_jugador_actual:
                    rey_pos = (r, c)
                    break
            if rey_pos: break

        if rey_pos is None:
             logger.critical(f"No se encontró el rey {color_jugador_actual}. Estado del juego no actualizado.") # Use critical for severe errors
             return

        # 1. Comprobar condiciones de Tablas (que no dependen de movimientos legales)
        if self.contadorRegla50Movimientos >= 100:
            self.estado_juego = 'tablas'
            logger.info("Tablas por regla de 50 movimientos.")
            return
        if self.esTripleRepeticion():
            self.estado_juego = 'tablas'
            logger.info("Tablas por triple repetición.")
            return
        # TODO: Añadir chequeo de material insuficiente para tablas
        if self.esMaterialInsuficiente():
            self.estado_juego = 'tablas'
            logger.info("Tablas por material insuficiente.")
            return

        # 2. Comprobar Jaque (evaluando si el rey actual está amenazado)
        esta_en_jaque = self.esCasillaAmenazada(rey_pos, color_oponente)
        
        # 3. Determinar estado final (Mate/Ahogado - REQUIERE MOVIMIENTOS LEGALES)
        # La detección completa de Jaque Mate y Ahogado requiere generar TODOS los
        # movimientos legales para el jugador actual. Si no hay movimientos legales,
        # es Jaque Mate si el rey está en jaque, y Ahogado (tablas) si no lo está.
        # Esta generación de movimientos legales suele residir en una clase
        # ValidadorMovimientos o ControladorJuego para mantener la separación de
        # responsabilidades.
        # Ejemplo conceptual:
        # movimientos_legales = GeneradorMovimientos.obtener_todos_movimientos_legales(self, color_jugador_actual)
        # if not movimientos_legales:
        #    if esta_en_jaque:
        #        self.estado_juego = 'jaque_mate'
        #        logger.info(f"Jaque Mate a {color_jugador_actual}.")
        #    else:
        #        self.estado_juego = 'tablas' # Ahogado
        #        logger.info(f"Tablas por ahogado a {color_jugador_actual}.")
        #    return

        # 4. Si hay movimientos legales (o no hemos comprobado aún), actualizar estado básico
        if esta_en_jaque:
            self.estado_juego = 'jaque'
            # logger.debug(f"Rey {color_jugador_actual} está en jaque.") # Puede ser muy verboso
        else:
            self.estado_juego = 'en_curso'

    def esMaterialInsuficiente(self) -> bool:
        """
        Comprueba si hay material insuficiente en el tablero para forzar un jaque mate.
        Cubre los casos más comunes definidos por la FIDE (Artículo 5.2.f / 9.6).

        Returns:
            True si el material es insuficiente para mate, False en caso contrario.
        """
        piezas_blancas = []
        piezas_negras = []
        alfiles_blancos_casilla_clara = 0
        alfiles_blancos_casilla_oscura = 0
        alfiles_negros_casilla_clara = 0
        alfiles_negros_casilla_oscura = 0

        # Contar piezas (excluyendo reyes) y características de alfiles
        for r in range(8):
            for c in range(8):
                pieza = self.casillas[r][c]
                if pieza is not None and not isinstance(pieza, Rey):
                    tipo_pieza = type(pieza)
                    # Si encontramos una Reina o una Torre o un Peón, el material SIEMPRE es suficiente
                    if tipo_pieza == Reina or tipo_pieza == Torre or tipo_pieza == Peon:
                        return False # Mate es posible

                    if pieza.color == 'blanco':
                        piezas_blancas.append(tipo_pieza)
                        if isinstance(pieza, Alfil):
                            # (0,0) es oscura en la config estándar. (r+c)%2==0 es oscura.
                            if (r + c) % 2 == 0:
                                alfiles_blancos_casilla_oscura += 1
                            else:
                                alfiles_blancos_casilla_clara += 1
                        # Guardar si hay caballos (podríamos solo contar)
                        # elif isinstance(pieza, Caballo): pass
                    else: # Negro
                        piezas_negras.append(tipo_pieza)
                        if isinstance(pieza, Alfil):
                            if (r + c) % 2 == 0:
                                alfiles_negros_casilla_oscura += 1
                            else:
                                alfiles_negros_casilla_clara += 1
                        # elif isinstance(pieza, Caballo): pass

        num_piezas_blancas = len(piezas_blancas)
        num_piezas_negras = len(piezas_negras)

        # Caso 1: Rey vs Rey (ambas listas vacías)
        if num_piezas_blancas == 0 and num_piezas_negras == 0:
            logger.debug("Material insuficiente: K vs K")
            return True

        # Caso 2: Rey + Caballo vs Rey
        if (num_piezas_blancas == 1 and piezas_blancas[0] == Caballo and num_piezas_negras == 0) or \
           (num_piezas_negras == 1 and piezas_negras[0] == Caballo and num_piezas_blancas == 0):
            logger.debug("Material insuficiente: K+N vs K")
            return True

        # Caso 3: Rey + Alfil vs Rey
        if (num_piezas_blancas == 1 and piezas_blancas[0] == Alfil and num_piezas_negras == 0) or \
           (num_piezas_negras == 1 and piezas_negras[0] == Alfil and num_piezas_blancas == 0):
            logger.debug("Material insuficiente: K+B vs K")
            return True

        # Caso 4: Rey + Alfil vs Rey + Alfil (ambos alfiles en casillas del mismo color)
        if num_piezas_blancas == 1 and piezas_blancas[0] == Alfil and \
           num_piezas_negras == 1 and piezas_negras[0] == Alfil:
            # Comprobar si ambos están en claras o ambos en oscuras
            ambos_en_claras = alfiles_blancos_casilla_clara == 1 and alfiles_negros_casilla_clara == 1
            ambos_en_oscuras = alfiles_blancos_casilla_oscura == 1 and alfiles_negros_casilla_oscura == 1
            if ambos_en_claras or ambos_en_oscuras:
                 logger.debug("Material insuficiente: K+B vs K+B (mismo color)")
                 return True

        # NOTA: K+N+N vs K NO se considera insuficiente por las reglas FIDE, aunque
        # forzar mate es extremadamente difícil y raro. Esta función correctamente devuelve False.
        # Otros casos más complejos (e.g., finales con peones bloqueados que no pueden avanzar)
        # no se cubren aquí y generalmente se resuelven por la regla de 50 mov o triple repetición.

        return False

    # ==================================================================
    # 6. Representación de Posición y Chequeo de Repetición (Auxiliares)
    # ==================================================================

    def obtenerPosicionActual(self) -> str:
        """
        Obtiene una representación en texto única de la posición actual del tablero,
        derechos de enroque, turno y objetivo de peón al paso.
        Necesario para el chequeo de triple repetición. Utiliza un formato similar a FEN.
        NOTA: Depende de `obtenerNotacionFEN` en las clases de Pieza para la parte de piezas.

        Returns:
            String representando unívocamente el estado relevante para repetición.
        """
        posicion_piezas = []
        for fila in self.casillas:
            fila_str = ""
            for pieza in fila:
                if pieza is None:
                    fila_str += "." # Representa casilla vacía
                else:
                    # Asume que Pieza tiene este método (necesita implementación)
                    try:
                         letra = pieza.obtenerNotacionFEN()
                         fila_str += letra.upper() if pieza.color == 'blanco' else letra.lower()
                    except AttributeError:
                         logger.warning(f"{type(pieza).__name__} no tiene 'obtenerNotacionFEN'. Usando '?'.")
                         fila_str += "?"
            posicion_piezas.append(fila_str)
        piezas_str = "/".join(posicion_piezas) # Separador de filas estilo FEN
        
        # Añadir otros elementos del estado relevantes para la repetición:
        # Turno
        turno_str = "w" if self.turno_blanco else "b"
        # Derechos de enroque
        enroque_str = ""
        if self.derechosEnroque['blanco']['corto']: enroque_str += "K"
        if self.derechosEnroque['blanco']['largo']: enroque_str += "Q"
        if self.derechosEnroque['negro']['corto']: enroque_str += "k"
        if self.derechosEnroque['negro']['largo']: enroque_str += "q"
        enroque_str = enroque_str if enroque_str else "-"
        # Objetivo peón al paso (en notación algebraica e.g., e3)
        al_paso_str = "-"
        if self.objetivoPeonAlPaso:
            fila, col = self.objetivoPeonAlPaso
            # Convertir (fila, col) a notación algebraica (e.g., (2, 4) -> e3)
            # Columna: 0->a, 1->b, ..., 7->h
            # Fila: 0->8, 1->7, ..., 7->1 (Invertido respecto a FEN estándar)
            # Ajustamos a la convención del tablero (0-7), luego convertimos
            # Columna 'a' + col_index, Fila '1' + (7 - fila_index)
            try:
                 col_letra = chr(ord('a') + col)
                 fila_num = str(8 - fila) # FEN usa 1-8, nuestro tablero 0-7
                 # Corrección: FEN numera filas 1-8 desde abajo, nuestras tuplas 0-7 desde arriba.
                 # Fila FEN = 8 - fila_tablero
                 # E.g., peón blanco mueve e2->e4: (1,4)->(3,4). Objetivo al paso = (2,4)
                 # (2,4) -> col='e', fila FEN = 8 - 2 = 6. -> e6 NO! Debe ser e3
                 # Ajuste: fila FEN = fila_tablero + 1?
                 # (1,4)->(3,4) => Objetivo=(2,4) => col='e', fila FEN = 2+1 = 3 => e3. CORRECTO.
                 # Peón negro mueve d7->d5: (6,3)->(4,3). Objetivo al paso = (5,3)
                 # (5,3) -> col='d', fila FEN = 5+1 = 6 => d6. CORRECTO.
                 fila_num_fen = str(fila + 1) # Corregido
                 al_paso_str = col_letra + fila_num_fen
            except Exception as e: # Catch potential errors during conversion
                 al_paso_str = "?" # Error en conversión
                 logger.error(f"Error convirtiendo objetivo al paso {self.objetivoPeonAlPaso} a notación algebraica: {e}")

        # Combinar todo en una cadena única (ignora contadores de 50-mov y ply)
        # Formato: piezas turno enroque al_paso
        return f"{piezas_str} {turno_str} {enroque_str} {al_paso_str}"

    def esTripleRepeticion(self) -> bool:
        """
        Verifica si la posición actual (definida por piezas, turno, derechos enroque,
        y objetivo al paso) se ha repetido tres veces en la partida consultando
        el historial de posiciones mantenido por el tablero.
        Llamado por `actualizarEstadoJuego`.

        Returns:
            True si la posición actual se ha repetido tres (o más) veces, False en caso contrario.
        """
        # Obtener la representación de la posición actual.
        posicion_actual_str = self.obtenerPosicionActual()
        
        # Consultar el conteo en el historial mantenido por el tablero.
        ocurrencias = self.historial_posiciones[posicion_actual_str]
        
        logger.debug(f"Chequeando Repetición: Pos actual str: '{posicion_actual_str}'. Ocurrencias: {ocurrencias}")
        
        # La regla se cumple si la posición ha aparecido 3 o más veces.
        return ocurrencias >= 3

    # --- Fin Métodos ---
   
                    
