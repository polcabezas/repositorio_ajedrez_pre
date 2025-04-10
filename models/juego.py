"""
Gestiona el estado general del juego (turno, jaque, jaque mate, tablas),
el historial de movimientos y la orquestación de la partida.
""" 
import logging
from typing import Dict, List, Tuple, Optional, Literal
from collections import defaultdict

# Importar Clases del Modelo
from models.tablero import Tablero
from models.piezas.pieza import Pieza
from models.piezas.peon import Peon  # Import Peon for instanceof checks
from models.piezas.rey import Rey    # Import Rey for instanceof checks
from models.piezas.reina import Reina
from models.piezas.torre import Torre
from models.piezas.alfil import Alfil
from models.piezas.caballo import Caballo
# from models.jugador import Jugador # Descomentar cuando se cree Jugador
# from models.move_info import MoveInfo # Descomentar si se crea MoveInfo
# from models.configuracion import ConfiguracionJuego # Descomentar si se crea ConfiguracionJuego
# from models.temporizador import Temporizador # Descomentar si se crea Temporizador


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Juego:
    """
    Clase principal del modelo que orquesta la partida de ajedrez.
    Contiene el tablero, gestiona los jugadores, el turno, el estado del juego,
    el historial de movimientos y las condiciones de finalización.
    """

    def __init__(self): # config: Optional['ConfiguracionJuego'] = None): # Añadir config cuando exista
        """
        Inicializa una nueva partida de ajedrez.

        Args:
            config: Opcional. Objeto con la configuración de la partida 
                    (tipos de jugador, tiempo, etc.).
        """
        logger.info("Inicializando nueva partida de ajedrez...")
        
        self.tablero = Tablero()
        # self.config = config if config else ConfiguracionJuego() # Usar config cuando exista
        
        # Atributos de estado del juego (anteriormente en Tablero)
        self.turno_actual: Literal['blanco', 'negro'] = 'blanco'
        self.estado_juego: Literal['inicio', 'en_curso', 'jaque', 'jaque_mate', 'tablas_ahogado', 'tablas_repeticion', 'tablas_50_mov', 'tablas_material'] = 'inicio'
        self.contadorRegla50Movimientos: int = 0
        self.contadorPly: int = 0 # Medio movimiento
        self.numero_movimiento: int = 1 # Movimiento completo

        # Historial y piezas capturadas
        # self.historial_movimientos: List['MoveInfo'] = [] # Usar MoveInfo cuando exista
        self.historial_movimientos: List[Dict] = [] # Placeholder con dict
        self.piezasCapturadas: Dict[Literal['blanco', 'negro'], List[Pieza]] = {'blanco': [], 'negro': []}
        
        # Historial para regla de triple repetición (clave: FEN parcial, valor: contador)
        self.historial_posiciones: Dict[str, int] = defaultdict(int)
        
        # Registrar la posición inicial
        self._registrarPosicionActual()

        # Componentes adicionales (placeholders)
        # self.jugadores: List['Jugador'] = self._configurar_jugadores(self.config)
        # self.jugadorActual: 'Jugador' = self.jugadores[0] if self.jugadores else None
        # self.temporizador: Optional['Temporizador'] = self._configurar_temporizador(self.config)
        
        self.estado_juego = 'en_curso' # Cambiar estado después de inicializar todo
        logger.info("Partida inicializada. Turno de Blancas.")

    # ------------------------------------------------------------
    # Métodos Principales de Interacción
    # ------------------------------------------------------------

    def realizarMovimiento(self, posOrigen: Tuple[int, int], posDestino: Tuple[int, int], promocion: Optional[str] = None) -> bool:
        """
        Intenta realizar un movimiento solicitado.
        1. Valida si el movimiento es legal para la pieza y el estado actual.
        2. Llama a tablero.moverPieza() o tablero.realizarEnroque().
        3. Actualiza el historial, estado del juego, contadores.
        4. Cambia el turno.
        5. Maneja la promoción de peones.

        Args:
            posOrigen: Coordenadas (fila, col) de origen.
            posDestino: Coordenadas (fila, col) de destino.
            promocion: Símbolo de la pieza a la que promociona un peón ('Q', 'R', 'B', 'N'), si aplica.

        Returns:
            True si el movimiento se realizó con éxito, False en caso contrario.
        """
        logger.info(f"Intento de movimiento: {posOrigen} -> {posDestino} (Promoción: {promocion})")
        
        pieza_a_mover = self.tablero.getPieza(posOrigen)

        # Validación básica inicial
        if pieza_a_mover is None:
            logger.warning("Movimiento inválido: No hay pieza en origen.")
            return False
        if pieza_a_mover.color != self.turno_actual:
            logger.warning(f"Movimiento inválido: No es el turno de {pieza_a_mover.color}.")
            return False
        if self.estado_juego not in ['en_curso', 'jaque']:
             logger.warning(f"Movimiento inválido: La partida ha terminado ({self.estado_juego}).")
             return False

        # Validar si el movimiento está en la lista de movimientos legales
        movimientos_legales = self.tablero.obtener_todos_movimientos_legales(self.turno_actual)
        es_movimiento_legal = (posOrigen, posDestino) in movimientos_legales

        # --- Ejecución del Movimiento ---
        pieza_capturada: Optional[Pieza] = None
        status_tablero: str = 'error'
        info_extra = {} # Para guardar detalles como enroque, al paso
        es_enroque = isinstance(pieza_a_mover, Rey) and abs(posOrigen[1] - posDestino[1]) == 2

        # Comprobar si el movimiento intentado es legal ANTES de proceder
        if not es_movimiento_legal:
            # A pesar de que no esté en la lista, podría ser un enroque que el usuario intentó
            # pero las condiciones fallaron (ej. rey movido). `obtener_todos_movimientos_legales` 
            # ya filtra esto. Si no está en la lista, es ilegal.
            logger.warning(f"Movimiento ilegal (no encontrado en la lista de legales): {posOrigen}->{posDestino}")
            return False

        # Ejecutar el movimiento
        if es_enroque: # Caso especial para enroque
            tipo_enroque = 'corto' if posDestino[1] == 6 else 'largo'
            color = self.turno_actual
            self.tablero.realizarEnroque(color, tipo_enroque)
            info_extra['enroque'] = tipo_enroque
            status_tablero = 'movimiento_ok'
            logger.info(f"Enroque {tipo_enroque} {color} completado en {posDestino}.")
        else: # Movimiento normal
            status_tablero, pieza_capturada = self.tablero.moverPieza(posOrigen, posDestino)
            
            if pieza_capturada:
                info_extra['captura'] = True
                self.piezasCapturadas[self.turno_actual].append(pieza_capturada)
                logger.info(f"Pieza capturada: {type(pieza_capturada).__name__} {pieza_capturada.color}")

            # Manejo de Promoción (Revised Logic)
            if status_tablero == 'promocion_necesaria':
                if not promocion or promocion.upper() not in ['Q', 'R', 'B', 'N']:
                    # Promotion needed, but invalid/missing input provided
                    logger.error("Movimiento requiere promoción, pero no se especificó pieza válida ('Q', 'R', 'B', 'N').")
                    # Implementar rollback: mover la pieza de vuelta a su posición original
                    peon_a_restaurar = self.tablero.getPieza(posDestino)
                    if peon_a_restaurar:
                        # Mover peón de vuelta a origen
                        self.tablero.setPieza(posOrigen, peon_a_restaurar)
                        peon_a_restaurar.posicion = posOrigen
                        # Restaurar estado 'se_ha_movido' si acaba de mover por primera vez
                        if hasattr(peon_a_restaurar, 'se_ha_movido') and not pieza_a_mover.se_ha_movido:
                            peon_a_restaurar.se_ha_movido = False
                        # Limpiar casilla destino
                        self.tablero.setPieza(posDestino, None)
                        # Si hubo captura, restaurarla también
                        if pieza_capturada:
                            # Devolver pieza capturada a su posición original
                            self.tablero.setPieza(posDestino, pieza_capturada)
                            pieza_capturada.posicion = posDestino
                            # Quitar de la lista de piezas capturadas
                            if pieza_capturada in self.piezasCapturadas[self.turno_actual]:
                                self.piezasCapturadas[self.turno_actual].remove(pieza_capturada)
                    return False
                else:
                    # Promotion needed AND valid piece provided
                    pieza_promocionada: Optional[Pieza] = None
                    tipo_pieza_prom = promocion.upper()
                    color_promocion = self.turno_actual
                    logger.debug(f"Realizando promoción a {tipo_pieza_prom} en {posDestino}")

                    # Crear la nueva pieza
                    if tipo_pieza_prom == 'Q':
                        pieza_promocionada = Reina(color_promocion, posDestino, self.tablero)
                    elif tipo_pieza_prom == 'R':
                        pieza_promocionada = Torre(color_promocion, posDestino, self.tablero)
                    elif tipo_pieza_prom == 'B':
                        pieza_promocionada = Alfil(color_promocion, posDestino, self.tablero)
                    elif tipo_pieza_prom == 'N':
                        pieza_promocionada = Caballo(color_promocion, posDestino, self.tablero)

                    if pieza_promocionada:
                        self.tablero.setPieza(posDestino, pieza_promocionada)
                        info_extra['promocion'] = tipo_pieza_prom
                        if hasattr(pieza_promocionada, 'se_ha_movido'):
                            pieza_promocionada.se_ha_movido = True
                    else:
                        logger.error(f"Error creando la pieza de promoción {tipo_pieza_prom}")
                        # Rollback similar al caso anterior
                        peon_a_restaurar = self.tablero.getPieza(posDestino)
                        if peon_a_restaurar:
                            self.tablero.setPieza(posOrigen, peon_a_restaurar)
                            peon_a_restaurar.posicion = posOrigen
                            self.tablero.setPieza(posDestino, None)
                        return False # Failed to create the piece instance
                    # --- Promotion successfully handled, continue below ---

            # Actualizar derechos de enroque y peón al paso (lo hace Juego ahora)
            # Esta llamada debe ocurrir DESPUÉS de la promoción, por si la pieza promocionada es una Torre
            # aunque en la práctica, la promoción ocurre en filas finales donde las torres iniciales ya perdieron derechos.
            self.tablero.actualizarDerechosEnroque(pieza_a_mover, posOrigen, pieza_capturada, posDestino) # Usa pieza_a_mover (el peón original)
            self.tablero.actualizarPeonAlPaso(pieza_a_mover, posOrigen, posDestino)


        # --- Actualizar Estado del Juego ---
        # Se pasa la pieza original (Peón) a _actualizarContadores, no la promocionada,
        # porque el contador de 50 movimientos se resetea por el *movimiento de peón*.
        self._actualizarContadores(pieza_a_mover, bool(pieza_capturada)) 
        # Se registra el movimiento con la pieza original (Peón) y la info de promoción
        self._registrarMovimiento(pieza_a_mover, posOrigen, posDestino, pieza_capturada, info_extra)
        self._registrarPosicionActual() # Para triple repetición
        self._actualizarEstadoJuego() # Comprobar jaque/mate/tablas
        
        # Cambiar turno
        self.cambiarTurno()
        
        logger.info(f"Movimiento {posOrigen}->{posDestino} realizado. Turno de {self.turno_actual}. Estado: {self.estado_juego}")
        return True

    def deshacerUltimoMovimiento(self) -> bool:
        """
        Deshace el último movimiento realizado, restaurando el estado anterior del tablero,
        turno, contadores, derechos de enroque, etc.
        
        Returns:
            True si se pudo deshacer, False si no hay movimientos en el historial.
        """
        if not self.historial_movimientos:
            logger.warning("No hay movimientos para deshacer.")
            return False
            
        logger.info("Deshaciendo último movimiento...")
        
        # 1. Obtener y eliminar último movimiento del historial
        ultimo_movimiento = self.historial_movimientos.pop()
        
        # 2. Extraer información del movimiento
        origen = ultimo_movimiento['origen']
        destino = ultimo_movimiento['destino']
        pieza_nombre = ultimo_movimiento['pieza'] # Nombre de la clase
        pieza_color = ultimo_movimiento['color']
        captura_nombre = ultimo_movimiento.get('pieza_capturada')
        captura_color = ultimo_movimiento.get('color_capturada')
        promocion_a = ultimo_movimiento.get('promocion')
        tipo_enroque = ultimo_movimiento.get('enroque')
        estado_anterior = ultimo_movimiento['estado_anterior']

        # 3. Decrementar contador de posición actual (ANTES de cambiar el tablero)
        fen_actual = self._generarFenParcial()
        if fen_actual in self.historial_posiciones:
             self.historial_posiciones[fen_actual] -= 1
             if self.historial_posiciones[fen_actual] <= 0:
                 del self.historial_posiciones[fen_actual] # Limpiar si llega a 0 o menos
             logger.debug(f"Decrementado contador para FEN '{fen_actual}', nuevo valor: {self.historial_posiciones.get(fen_actual, 0)}")
        else:
             logger.warning(f"Intento de decrementar FEN no registrado: '{fen_actual}'")
             
        # 4. Cambiar turno ANTES de restaurar el tablero (afecta a qué pieza restaurar de capturadas)
        color_que_movio = self.turno_actual # Quien movía ANTES de deshacer
        self.cambiarTurno() # Ahora el turno es del que hizo el movimiento que estamos deshaciendo
        color_actual_despues_cambio = self.turno_actual 
        assert color_actual_despues_cambio == pieza_color # Verificar que el turno restaurado coincide con la pieza movida

        # 5. Restaurar estado del tablero
        pieza_restaurada_captura: Optional[Pieza] = None
        
        # 5.a Restaurar pieza capturada (si hubo)
        if captura_nombre:
            # Recuperar la ÚLTIMA pieza capturada del color correspondiente
            try:
                pieza_restaurada_captura = self.piezasCapturadas[color_actual_despues_cambio].pop()
                # Verificar que coincida (opcional pero bueno para debug)
                if not isinstance(pieza_restaurada_captura, self._obtenerClasePieza(captura_nombre)) or \
                   pieza_restaurada_captura.color != captura_color:
                    logger.error(f"Discrepancia al deshacer captura: Esperaba {captura_nombre} {captura_color}, obtuve {type(pieza_restaurada_captura).__name__} {pieza_restaurada_captura.color}")
                    # Intentar continuar, pero el estado puede ser inconsistente
            except (IndexError, KeyError):
                 logger.error(f"Error al deshacer: No se encontró pieza capturada {captura_nombre} {captura_color} en el historial de capturas.")
                 # No podemos restaurar, el estado será inconsistente. ¿Detener? Por ahora continuamos.
                 pieza_restaurada_captura = None # Asegurarse de que es None

        # 5.b Determinar si fue captura al paso
        objetivo_ep_anterior = estado_anterior.get('objetivo_ep')
        es_en_passant = (pieza_nombre == 'Peon' and 
                         destino == objetivo_ep_anterior and 
                         captura_nombre == 'Peon')

        # 5.c Restaurar tablero según tipo de movimiento
        if tipo_enroque: # Deshacer Enroque
            fila = 0 if color_actual_despues_cambio == 'blanco' else 7
            rey_col_origen_enroque = 4
            torre_col_origen_enroque = 7 if tipo_enroque == 'corto' else 0
            rey_pos_origen = (fila, rey_col_origen_enroque)
            torre_pos_origen = (fila, torre_col_origen_enroque)
            
            # Obtener piezas de sus posiciones DESPUÉS del enroque
            rey_pos_destino_enroque = (fila, 6 if tipo_enroque == 'corto' else 2)
            torre_pos_destino_enroque = (fila, 5 if tipo_enroque == 'corto' else 3)
            rey = self.tablero.getPieza(rey_pos_destino_enroque)
            torre = self.tablero.getPieza(torre_pos_destino_enroque)

            if isinstance(rey, Rey) and isinstance(torre, Torre):
                # Mover de vuelta
                self.tablero.setPieza(rey_pos_origen, rey)
                self.tablero.setPieza(torre_pos_origen, torre)
                self.tablero.setPieza(rey_pos_destino_enroque, None)
                self.tablero.setPieza(torre_pos_destino_enroque, None)
                # Actualizar posición interna
                rey.posicion = rey_pos_origen
                torre.posicion = torre_pos_origen
                # Restaurar estado 'se_ha_movido' (es crucial para futuros enroques)
                rey.se_ha_movido = False # El enroque solo es posible si no se habían movido
                torre.se_ha_movido = False
                logger.debug(f"Enroque {tipo_enroque} deshecho.")
            else:
                 logger.error(f"Error deshaciendo enroque {tipo_enroque}: No se encontraron Rey/Torre en posiciones esperadas.")
        
        else: # Deshacer movimiento normal, captura, EP o promoción
            # Obtener la pieza que se movió (puede ser la original o la promocionada)
            pieza_movida = self.tablero.getPieza(destino) 
            if pieza_movida is None:
                 logger.error(f"Error deshaciendo movimiento: No hay pieza en destino {destino}")
                 # No se puede continuar con la restauración del tablero de forma fiable
                 # TODO: ¿Qué hacer? Quizás restaurar estado y devolver False?
                 return False # Abortar deshacer por inconsistencia

            # 5.c.i Manejar Reversión de Promoción
            if promocion_a:
                # La pieza en 'destino' es la promocionada. Reemplazarla por un Peón.
                pieza_movida = Peon(color_actual_despues_cambio, destino, self.tablero)
                # No necesita restaurar se_ha_movido porque creamos un peón nuevo
                logger.debug(f"Promoción a {promocion_a} revertida a Peón.")
                # Si hubo captura DURANTE la promoción, pieza_restaurada_captura ya está lista
            
            # 5.c.ii Mover pieza de vuelta a origen
            self.tablero.setPieza(origen, pieza_movida)
            pieza_movida.posicion = origen
            # Restaurar el estado 'se_ha_movido' de ANTES del movimiento
            pieza_movida.se_ha_movido = estado_anterior.get('pieza_se_ha_movido', pieza_movida.se_ha_movido) # Usar valor actual como fallback improbable

            # 5.c.iii Colocar pieza capturada (si la hubo y se recuperó)
            if pieza_restaurada_captura:
                if es_en_passant:
                    # La casilla donde estaba el peón capturado al paso
                    fila_captura_ep = origen[0] 
                    col_captura_ep = destino[1]
                    casilla_captura_ep = (fila_captura_ep, col_captura_ep)
                    self.tablero.setPieza(casilla_captura_ep, pieza_restaurada_captura)
                    pieza_restaurada_captura.posicion = casilla_captura_ep
                    # Limpiar casilla destino (donde aterrizó el peón que capturó EP)
                    self.tablero.setPieza(destino, None) 
                    logger.debug(f"Captura EP deshecha. {type(pieza_restaurada_captura).__name__} restaurada en {casilla_captura_ep}")
                else:
                    # Captura normal o captura durante promoción: la pieza va al destino
                    self.tablero.setPieza(destino, pieza_restaurada_captura)
                    pieza_restaurada_captura.posicion = destino
                    logger.debug(f"Captura normal deshecha. {type(pieza_restaurada_captura).__name__} restaurada en {destino}")
            else:
                 # Si no hubo captura (o no se pudo restaurar), asegurarse que destino está vacío
                 # (a menos que fuera EP, que ya lo limpió)
                 if not es_en_passant:
                     self.tablero.setPieza(destino, None)

        # 6. Restaurar estado del Juego y Tablero
        self.tablero.derechosEnroque = estado_anterior['derechos_enroque']
        self.tablero.objetivoPeonAlPaso = estado_anterior['objetivo_ep']
        self.contadorRegla50Movimientos = estado_anterior['contador_50']
        
        # Restaurar contadores de movimiento
        self.contadorPly -= 1
        # El número de movimiento solo decrementa si las negras deshicieron su movimiento
        # (es decir, si ANTES de cambiar el turno, el turno era de blancas)
        if color_que_movio == 'blanco': 
             self.numero_movimiento -= 1
             # Asegurarse que no sea menor que 1
             if self.numero_movimiento < 1: self.numero_movimiento = 1

        # 7. Actualizar estado del juego (jaque/mate/etc.) basado en la posición restaurada
        self._actualizarEstadoJuego() 

        logger.info(f"Movimiento deshecho. Turno de {self.turno_actual}. Estado: {self.estado_juego}")
        return True

    # ------------------------------------------------------------
    # Métodos Auxiliares Internos
    # ------------------------------------------------------------

    def cambiarTurno(self):
        """ Cambia el turno al jugador opuesto. """
        self.turno_actual = 'negro' if self.turno_actual == 'blanco' else 'blanco'
        # Si hubiera temporizador: self.temporizador.cambiarJugador(self.turno_actual)
        logger.debug(f"Turno cambiado a {self.turno_actual}")

    def _actualizarContadores(self, pieza_movida: Pieza, es_captura: bool):
        """
        Actualiza los contadores de ply, número de movimiento y regla de 50 movimientos.
        """
        self.contadorPly += 1

        # El número de movimiento incrementa DESPUÉS de que las negras muevan (antes de que blancas muevan de nuevo)
        if self.turno_actual == 'blanco': # Si ahora es turno de blancas, negras acaban de mover
            self.numero_movimiento += 1

        # Resetear contador de 50 movimientos si fue un movimiento de peón o una captura
        if isinstance(pieza_movida, Peon) or es_captura:
            self.contadorRegla50Movimientos = 0
            logger.debug("Contador 50 mov reseteado.")
        else:
            self.contadorRegla50Movimientos += 1 # Se cuenta por medio movimiento (ply)
            logger.debug(f"Contador 50 mov incrementado a {self.contadorRegla50Movimientos}")
            
    def _registrarMovimiento(self, pieza: Pieza, origen: Tuple[int, int], destino: Tuple[int, int], pieza_capturada: Optional[Pieza], info: Dict):
        """
        Registra la información del movimiento en el historial.
        TODO: Usar una clase MoveInfo más completa.
        """
        movimiento_info = {
            'pieza': type(pieza).__name__,
            'color': pieza.color,
            'origen': origen,
            'destino': destino,
            'pieza_capturada': type(pieza_capturada).__name__ if pieza_capturada else None,
            'color_capturada': pieza_capturada.color if pieza_capturada else None,
            'ply': self.contadorPly,
            'numero_movimiento': self.numero_movimiento,
            # Añadir estado ANTES del movimiento para deshacer
            'estado_anterior': { 
                'derechos_enroque': self.tablero.derechosEnroque.copy(), # Copia profunda necesaria? defaultdict podría requerirla
                'objetivo_ep': self.tablero.objetivoPeonAlPaso,
                'contador_50': self.contadorRegla50Movimientos - (1 if not isinstance(pieza, Peon) and not pieza_capturada else 0), # Revertir incremento si aplica
                'pieza_se_ha_movido': pieza.se_ha_movido # Guardar estado ANTES de que moverPieza/enroque lo ponga a True
            }
        }
        movimiento_info.update(info) # Añadir 'enroque', 'promocion', 'captura', etc.
        self.historial_movimientos.append(movimiento_info)
        logger.debug(f"Movimiento registrado: {movimiento_info}")

    def _registrarPosicionActual(self):
         """ Genera el FEN parcial y lo registra en el historial de posiciones. """
         posicion_fen = self._generarFenParcial() # Usar helper
         self.historial_posiciones[posicion_fen] += 1
         logger.debug(f"Posición registrada: '{posicion_fen}', Count: {self.historial_posiciones[posicion_fen]}")

    def _actualizarEstadoJuego(self):
        """
        Evalúa el estado actual del juego después de un movimiento.
        Comprueba jaque, mate, ahogado y condiciones de tablas.
        """
        color_jugador_actual = self.turno_actual # Color del jugador QUE VA A MOVER
        color_oponente = 'negro' if color_jugador_actual == 'blanco' else 'blanco'

        # 1. Comprobar condiciones de Tablas automáticas
        if self.contadorRegla50Movimientos >= 100: # 50 movimientos completos = 100 plies
            self.estado_juego = 'tablas_50_mov'
            logger.info("Tablas por regla de 50 movimientos.")
            return
        if self._esTripleRepeticion():
            self.estado_juego = 'tablas_repeticion'
            logger.info("Tablas por triple repetición.")
            return
        if self.tablero.esMaterialInsuficiente():
            self.estado_juego = 'tablas_material'
            logger.info("Tablas por material insuficiente.")
            return

        # 2. Comprobar Jaque al rey del jugador actual Y del oponente
        rey_pos_actual = self._encontrarRey(color_jugador_actual)
        rey_pos_oponente = self._encontrarRey(color_oponente)
        
        if rey_pos_actual is None or rey_pos_oponente is None:
             logger.critical(f"No se encontró alguno de los reyes. Estado del juego no puede ser evaluado.")
             # Quizás marcar un estado de error?
             return

        # Verificar si algún rey está en jaque
        esta_en_jaque_actual = self.tablero.esCasillaAmenazada(rey_pos_actual, color_oponente)
        esta_en_jaque_oponente = self.tablero.esCasillaAmenazada(rey_pos_oponente, color_jugador_actual)

        # 3. Comprobar Mate o Ahogado (si no hay movimientos legales)
        movimientos_legales = self.tablero.obtener_todos_movimientos_legales(color_jugador_actual)

        if not movimientos_legales:
            if esta_en_jaque_actual:
                self.estado_juego = 'jaque_mate'
                logger.info(f"Jaque Mate a {color_jugador_actual}.")
            else:
                self.estado_juego = 'tablas_ahogado' # Ahogado
                logger.info(f"Tablas por ahogado a {color_jugador_actual}.")
            return # El juego termina

        # 4. Si hay movimientos legales
        if esta_en_jaque_actual or esta_en_jaque_oponente:
            self.estado_juego = 'jaque'
            if esta_en_jaque_actual:
                logger.info(f"Jaque a {color_jugador_actual}.")
            else:
                logger.info(f"Jaque a {color_oponente}.")
        else:
            self.estado_juego = 'en_curso'
            logger.debug(f"Juego en curso. Turno de {color_jugador_actual}.")
            
    def _encontrarRey(self, color: Literal['blanco', 'negro']) -> Optional[Tuple[int, int]]:
         """ Encuentra la posición del rey de un color dado. """
         for r, fila in enumerate(self.tablero.casillas):
             for c, pieza in enumerate(fila):
                 if isinstance(pieza, Rey) and pieza.color == color:
                     return (r, c)
         return None # No debería ocurrir en una partida normal

    def _esTripleRepeticion(self) -> bool:
        """ Comprueba si la posición actual se ha repetido 3 veces. """
        # Reconstruir FEN parcial actual para la búsqueda
        fen_piezas = self.tablero.obtenerRepresentacionPiezas()
        fen_turno = 'w' if self.turno_actual == 'blanco' else 'b'
        enroque_str = ""
        if self.tablero.derechosEnroque['blanco']['corto']: enroque_str += "K"
        if self.tablero.derechosEnroque['blanco']['largo']: enroque_str += "Q"
        if self.tablero.derechosEnroque['negro']['corto']: enroque_str += "k"
        if self.tablero.derechosEnroque['negro']['largo']: enroque_str += "q"
        fen_enroque = enroque_str if enroque_str else "-"
        fen_ep = "-"
        if self.tablero.objetivoPeonAlPaso:
             try:
                 fila, col = self.tablero.objetivoPeonAlPaso
                 col_letra = chr(ord('a') + col)
                 fila_num_fen = str(fila + 1)
                 fen_ep = col_letra + fila_num_fen
             except:
                 fen_ep = "?"
        
        posicion_fen_actual = f"{fen_piezas} {fen_turno} {fen_enroque} {fen_ep}"
        ocurrencias = self.historial_posiciones.get(posicion_fen_actual, 0)
        logger.debug(f"Chequeo Repetición: Pos='{posicion_fen_actual}', Ocurrencias={ocurrencias}")
        return ocurrencias >= 3

    # ------------------------------------------------------------
    # Métodos de Consulta de Estado (Ejemplos)
    # ------------------------------------------------------------

    def getTurnoColor(self) -> Literal['blanco', 'negro']:
        """ Devuelve el color del jugador cuyo turno es. """
        return self.turno_actual
        
    def estaEnJaque(self, color: Literal['blanco', 'negro']) -> bool:
        """ Comprueba si el rey del color especificado está actualmente en jaque. """
        # Método directo: siempre verificar si la casilla del rey está amenazada
        rey_pos = self._encontrarRey(color)
        if not rey_pos: 
            return False # No hay rey?
        color_oponente = 'negro' if color == 'blanco' else 'blanco'
        return self.tablero.esCasillaAmenazada(rey_pos, color_oponente)

    # TODO: Implementar el resto de métodos de consulta y generación (FEN, PGN, etc.)
    # def estaEnJaqueMate(self, color: Literal['blanco', 'negro']) -> bool: ...
    # def estaAhogado(self, color: Literal['blanco', 'negro']) -> bool: ...
    # def estaEnTablas(self) -> bool: ...
    # def getFEN(self) -> str: ...
    # def getPGN(self) -> str: ...
    
    # --- Métodos Auxiliares Internos ---
    
    # Helper para obtener la clase de pieza desde su nombre
    def _obtenerClasePieza(self, nombre_clase: str) -> Optional[type]:
        clases = {'Peon': Peon, 'Torre': Torre, 'Caballo': Caballo, 'Alfil': Alfil, 'Reina': Reina, 'Rey': Rey}
        return clases.get(nombre_clase)

    # Helper para generar FEN parcial para historial de posiciones
    def _generarFenParcial(self) -> str:
        """ Genera el FEN parcial (piezas, turno, enroque, EP) para el estado actual. """
        fen_piezas = self.tablero.obtenerRepresentacionPiezas()
        fen_turno = 'w' if self.turno_actual == 'blanco' else 'b'
        enroque_str = ""
        if self.tablero.derechosEnroque.get('blanco', {}).get('corto', False): enroque_str += "K"
        if self.tablero.derechosEnroque.get('blanco', {}).get('largo', False): enroque_str += "Q"
        if self.tablero.derechosEnroque.get('negro', {}).get('corto', False): enroque_str += "k"
        if self.tablero.derechosEnroque.get('negro', {}).get('largo', False): enroque_str += "q"
        fen_enroque = enroque_str if enroque_str else "-"
        fen_ep = "-"
        if self.tablero.objetivoPeonAlPaso:
             try:
                 fila, col = self.tablero.objetivoPeonAlPaso
                 # FEN usa notación algebraica para EP target square
                 col_letra = chr(ord('a') + col) 
                 # FEN usa rank 1-8, nuestro índice 0-7. Fila para EP es donde el peón ATERRIZARÍA.
                 fila_num_fen = str(3) if self.turno_actual == 'blanco' else str(6) # Peón negro movió -> target fila 3; Peón blanco movió -> target fila 6
                 fen_ep = col_letra + fila_num_fen
             except Exception as e:
                 logger.error(f"Error generando FEN EP para {self.tablero.objetivoPeonAlPaso}: {e}")
                 fen_ep = "?" # Error
        
        return f"{fen_piezas} {fen_turno} {fen_enroque} {fen_ep}"
        
# --- Fin de la clase Juego --- 