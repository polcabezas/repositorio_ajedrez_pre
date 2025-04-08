"""
Pruebas unitarias exhaustivas para la clase Tablero.

Verifica la correcta implementación de las reglas del ajedrez según FIDE
y las especificaciones del proyecto.
"""

import pytest
import logging
from models.tablero import Tablero
from models.piezas.pieza import Pieza
from models.piezas.rey import Rey
from models.piezas.reina import Reina
from models.piezas.torre import Torre
from models.piezas.alfil import Alfil
from models.piezas.caballo import Caballo
from models.piezas.peon import Peon
from typing import Tuple, Optional, Type

# ============================================================
# Fixtures de Pytest
# ============================================================

@pytest.fixture
def tablero_inicial():
    """
    Proporciona un tablero en su estado inicial estándar.
    """
    return Tablero()

@pytest.fixture
def tablero_vacio():
    """
    Proporciona un tablero vacío sin piezas.
    Util para colocar piezas específicas en tests.
    """
    tablero = Tablero()
    # Vaciar el tablero completamente
    tablero.casillas = [[None for _ in range(8)] for _ in range(8)]
    # Resetear otros estados relevantes si es necesario
    tablero.derechosEnroque = {
        'blanco': {'corto': False, 'largo': False},
        'negro': {'corto': False, 'largo': False}
    }
    tablero.objetivoPeonAlPaso = None
    tablero.historial_movimientos = []
    tablero.piezasCapturadas = []
    tablero.turno_blanco = True
    tablero.contadorRegla50Movimientos = 0
    tablero.contadorPly = 0
    tablero.estado_juego = 'en_curso'
    tablero.numero_movimiento = 1
    tablero.ultimo_movimiento = None
    return tablero

# ============================================================
# Pruebas de Inicialización y Configuración
# ============================================================

def test_inicializacion_dimensiones(tablero_inicial: Tablero):
    """
    Verifica que el tablero se inicializa con 8 filas y 8 columnas.
    """
    assert len(tablero_inicial.casillas) == 8, "El tablero debe tener 8 filas."
    for fila in tablero_inicial.casillas:
        assert len(fila) == 8, "Cada fila debe tener 8 columnas."

def test_inicializacion_piezas_blancas(tablero_inicial: Tablero):
    """
    Verifica la correcta colocación y tipo de las piezas blancas iniciales.
    """
    # Fila 1 (índice 0) - Piezas mayores blancas
    assert isinstance(tablero_inicial.getPieza((0, 0)), Torre) and tablero_inicial.getPieza((0, 0)).color == 'blanco'
    assert isinstance(tablero_inicial.getPieza((0, 1)), Caballo) and tablero_inicial.getPieza((0, 1)).color == 'blanco'
    assert isinstance(tablero_inicial.getPieza((0, 2)), Alfil) and tablero_inicial.getPieza((0, 2)).color == 'blanco'
    assert isinstance(tablero_inicial.getPieza((0, 3)), Reina) and tablero_inicial.getPieza((0, 3)).color == 'blanco'
    assert isinstance(tablero_inicial.getPieza((0, 4)), Rey) and tablero_inicial.getPieza((0, 4)).color == 'blanco'
    assert isinstance(tablero_inicial.getPieza((0, 5)), Alfil) and tablero_inicial.getPieza((0, 5)).color == 'blanco'
    assert isinstance(tablero_inicial.getPieza((0, 6)), Caballo) and tablero_inicial.getPieza((0, 6)).color == 'blanco'
    assert isinstance(tablero_inicial.getPieza((0, 7)), Torre) and tablero_inicial.getPieza((0, 7)).color == 'blanco'

    # Fila 2 (índice 1) - Peones blancos
    for col in range(8):
        assert isinstance(tablero_inicial.getPieza((1, col)), Peon) and tablero_inicial.getPieza((1, col)).color == 'blanco'

def test_inicializacion_piezas_negras(tablero_inicial: Tablero):
    """
    Verifica la correcta colocación y tipo de las piezas negras iniciales.
    """
    # Fila 8 (índice 7) - Piezas mayores negras
    assert isinstance(tablero_inicial.getPieza((7, 0)), Torre) and tablero_inicial.getPieza((7, 0)).color == 'negro'
    assert isinstance(tablero_inicial.getPieza((7, 1)), Caballo) and tablero_inicial.getPieza((7, 1)).color == 'negro'
    assert isinstance(tablero_inicial.getPieza((7, 2)), Alfil) and tablero_inicial.getPieza((7, 2)).color == 'negro'
    assert isinstance(tablero_inicial.getPieza((7, 3)), Reina) and tablero_inicial.getPieza((7, 3)).color == 'negro'
    assert isinstance(tablero_inicial.getPieza((7, 4)), Rey) and tablero_inicial.getPieza((7, 4)).color == 'negro'
    assert isinstance(tablero_inicial.getPieza((7, 5)), Alfil) and tablero_inicial.getPieza((7, 5)).color == 'negro'
    assert isinstance(tablero_inicial.getPieza((7, 6)), Caballo) and tablero_inicial.getPieza((7, 6)).color == 'negro'
    assert isinstance(tablero_inicial.getPieza((7, 7)), Torre) and tablero_inicial.getPieza((7, 7)).color == 'negro'

    # Fila 7 (índice 6) - Peones negros
    for col in range(8):
        assert isinstance(tablero_inicial.getPieza((6, col)), Peon) and tablero_inicial.getPieza((6, col)).color == 'negro'

def test_inicializacion_casillas_vacias(tablero_inicial: Tablero):
    """
    Verifica que las casillas intermedias están vacías al inicio.
    """
    for fila in range(2, 6): # Filas de índice 2 a 5
        for col in range(8):
            assert tablero_inicial.getPieza((fila, col)) is None, f"La casilla ({fila}, {col}) debería estar vacía."

def test_inicializacion_estado_juego(tablero_inicial: Tablero):
    """
    Verifica el estado inicial del juego (turno, contadores, derechos enroque, etc.).
    """
    assert tablero_inicial.turno_blanco is True, "El turno inicial debe ser de las blancas."
    assert tablero_inicial.objetivoPeonAlPaso is None, "No debe haber objetivo al paso inicial."
    assert tablero_inicial.piezasCapturadas == [], "La lista de capturadas debe estar vacía."
    assert tablero_inicial.contadorRegla50Movimientos == 0, "El contador de 50 mov. debe ser 0."
    assert tablero_inicial.contadorPly == 0, "El contador de medios movimientos (ply) debe ser 0."
    assert tablero_inicial.numero_movimiento == 1, "El número de movimiento debe ser 1."
    assert tablero_inicial.estado_juego == 'en_curso', "El estado inicial debe ser 'en_curso'."
    assert tablero_inicial.ultimo_movimiento is None, "No debe haber último movimiento registrado."
    # Derechos de enroque
    assert tablero_inicial.derechosEnroque['blanco']['corto'] is True
    assert tablero_inicial.derechosEnroque['blanco']['largo'] is True
    assert tablero_inicial.derechosEnroque['negro']['corto'] is True
    assert tablero_inicial.derechosEnroque['negro']['largo'] is True

# ============================================================
# Pruebas de Consultas Básicas
# ============================================================

@pytest.mark.parametrize("posicion, esperado", [
    ((0, 0), True), ((7, 7), True), ((3, 4), True), # Dentro
    ((-1, 0), False), ((0, -1), False), ((8, 0), False), ((0, 8), False), # Fuera
    ((3.5, 4), False), (("a", 1), False), ((3,), False) # Tipos inválidos
])
def test_esPosicionValida(tablero_inicial: Tablero, posicion: Tuple[int, int], esperado: bool):
    """
    Verifica la validación de posiciones dentro y fuera de los límites.
    """
    assert tablero_inicial.esPosicionValida(posicion) == esperado

def test_getPieza_existente(tablero_inicial: Tablero):
    """
    Verifica obtener una pieza existente en una posición válida.
    """
    pieza = tablero_inicial.getPieza((0, 0))
    assert isinstance(pieza, Torre) and pieza.color == 'blanco'
    pieza = tablero_inicial.getPieza((6, 5))
    assert isinstance(pieza, Peon) and pieza.color == 'negro'

def test_getPieza_vacia(tablero_inicial: Tablero):
    """
    Verifica obtener None de una casilla vacía válida.
    """
    assert tablero_inicial.getPieza((3, 3)) is None

def test_getPieza_invalida(tablero_inicial: Tablero):
    """
    Verifica obtener None de una posición inválida.
    """
    assert tablero_inicial.getPieza((-1, 5)) is None
    assert tablero_inicial.getPieza((4, 8)) is None

def test_esBlanco(tablero_inicial: Tablero):
    """
    Verifica la identificación correcta del color blanco.
    """
    assert tablero_inicial.esBlanco((0, 0)) is True # Torre blanca
    assert tablero_inicial.esBlanco((1, 4)) is True # Peón blanco
    assert tablero_inicial.esBlanco((7, 7)) is False # Torre negra
    assert tablero_inicial.esBlanco((6, 2)) is False # Peón negro
    assert tablero_inicial.esBlanco((4, 4)) is False # Casilla vacía

# ============================================================
# Pruebas de Movimiento Básico (moverPieza)
# ============================================================

def test_moverPieza_simple_ok(tablero_inicial: Tablero):
    """
    Prueba un movimiento simple y legal de un peón blanco.
    Verifica el estado del tablero y el retorno.
    """
    origen = (1, 4) # Peón e2
    destino = (3, 4) # e4
    pieza_movida = tablero_inicial.getPieza(origen)

    resultado = tablero_inicial.moverPieza(origen, destino)

    assert resultado == 'movimiento_ok', "El resultado del movimiento debe ser 'movimiento_ok'."
    assert tablero_inicial.getPieza(origen) is None, "La casilla origen debe quedar vacía."
    assert tablero_inicial.getPieza(destino) is pieza_movida, "La pieza debe estar en la casilla destino."
    assert pieza_movida.posicion == destino, "La posición interna de la pieza debe actualizarse."
    assert tablero_inicial.turno_blanco is False, "El turno debe pasar a las negras."
    assert tablero_inicial.contadorPly == 1, "El contador Ply debe ser 1."
    assert tablero_inicial.numero_movimiento == 1, "El número de movimiento debe seguir siendo 1."
    assert tablero_inicial.contadorRegla50Movimientos == 0, "Contador 50 mov se resetea por peón."
    assert tablero_inicial.ultimo_movimiento == (origen, destino), "Se debe registrar el último movimiento."
    assert tablero_inicial.historial_movimientos[-1] == ('blanco', origen, destino), "El movimiento debe registrarse en el historial."

def test_moverPieza_captura_ok(tablero_inicial: Tablero):
    """
    Prueba una captura simple y legal.
    """
    # Configurar escenario: Caballo blanco en e4, Peón negro en d5
    tablero_inicial.setPieza((3, 4), Caballo('blanco', (3, 4))) # Ne4
    tablero_inicial.setPieza((4, 3), Peon('negro', (4, 3)))    # pd5
    # Limpiar origen del caballo blanco y destino del peón negro (simulación)
    tablero_inicial.setPieza((0, 6), None) # G1
    tablero_inicial.setPieza((6, 3), None) # d7
    tablero_inicial.turno_blanco = True # Turno blanco

    origen = (3, 4)
    destino = (4, 3)
    pieza_movida = tablero_inicial.getPieza(origen)
    pieza_capturada = tablero_inicial.getPieza(destino)

    resultado = tablero_inicial.moverPieza(origen, destino)

    assert resultado == 'movimiento_ok'
    assert tablero_inicial.getPieza(origen) is None
    assert tablero_inicial.getPieza(destino) is pieza_movida
    assert pieza_movida.posicion == destino
    assert pieza_capturada in tablero_inicial.piezasCapturadas, "La pieza capturada debe estar en la lista."
    assert len(tablero_inicial.piezasCapturadas) == 1
    assert tablero_inicial.turno_blanco is False
    assert tablero_inicial.contadorRegla50Movimientos == 0, "Contador 50 mov se resetea por captura."
    assert tablero_inicial.ultimo_movimiento == (origen, destino)
    assert tablero_inicial.historial_movimientos[-1] == ('blanco', origen, destino)

def test_moverPieza_error_origen_vacio(tablero_inicial: Tablero):
    """
    Prueba intentar mover desde una casilla vacía.
    """
    resultado = tablero_inicial.moverPieza((3, 3), (4, 4))
    assert resultado == 'error', "Debe retornar 'error' si el origen está vacío."
    assert tablero_inicial.turno_blanco is True, "El turno no debe cambiar."

def test_moverPieza_error_destino_propio(tablero_inicial: Tablero):
    """
    Prueba intentar capturar una pieza propia.
    """
    resultado = tablero_inicial.moverPieza((0, 0), (1, 0)) # Torre a casilla de peón blanco
    assert resultado == 'error', "Debe retornar 'error' al intentar capturar pieza propia."
    assert isinstance(tablero_inicial.getPieza((1, 0)), Peon), "La pieza destino no debe cambiar."
    assert tablero_inicial.turno_blanco is True, "El turno no debe cambiar."

def test_moverPieza_error_posicion_invalida(tablero_inicial: Tablero):
    """
    Prueba intentar mover a/desde una posición inválida.
    """
    assert tablero_inicial.moverPieza((0, 0), (0, 8)) == 'error' # Destino inválido
    assert tablero_inicial.moverPieza((-1, 0), (2, 2)) == 'error' # Origen inválido
    assert tablero_inicial.turno_blanco is True, "El turno no debe cambiar."

def test_setPieza(tablero_vacio: Tablero):
    """
    Verifica la colocación de piezas con setPieza.
    """
    rey_blanco = Rey('blanco', (4, 4))
    tablero_vacio.setPieza((4, 4), rey_blanco)
    assert tablero_vacio.getPieza((4, 4)) is rey_blanco

    tablero_vacio.setPieza((4, 4), None)
    assert tablero_vacio.getPieza((4, 4)) is None

# ============================================================
# Pruebas de Movimientos Especiales
# ============================================================

# --- En Passant ---

def test_actualizarPeonAlPaso_creacion(tablero_inicial: Tablero):
    """
    Verifica que el objetivo al paso se crea correctamente tras avance doble de peón.
    """
    tablero_inicial.moverPieza((1, 4), (3, 4)) # e2 -> e4
    assert tablero_inicial.objetivoPeonAlPaso == (2, 4), "El objetivo al paso debe ser e3 (2, 4)."
    assert tablero_inicial.turno_blanco is False # Turno negro

def test_actualizarPeonAlPaso_limpieza(tablero_inicial: Tablero):
    """
    Verifica que el objetivo al paso se limpia tras un movimiento que no sea avance doble.
    """
    tablero_inicial.moverPieza((1, 4), (3, 4)) # e4, crea objetivo e3
    assert tablero_inicial.objetivoPeonAlPaso == (2, 4)
    tablero_inicial.moverPieza((6, 0), (5, 0)) # Negro mueve a6
    assert tablero_inicial.objetivoPeonAlPaso is None, "El objetivo al paso debe limpiarse."

def test_moverPieza_enPassant_ok(tablero_inicial: Tablero):
    """
    Prueba una captura al paso válida.
    """
    # Configuración: Peón blanco en e5, Peón negro en d7. Negro mueve d7->d5
    tablero_inicial.setPieza((4, 4), Peon('blanco', (4, 4))) # Peón blanco e5
    tablero_inicial.setPieza((1, 4), None) # Vaciar e2
    tablero_inicial.turno_blanco = False # Turno Negro

    # Negro mueve d7->d5
    tablero_inicial.moverPieza((6, 3), (4, 3)) # Peón negro d5
    assert tablero_inicial.objetivoPeonAlPaso == (5, 3), "Objetivo al paso debe ser d6 (5, 3)."
    assert tablero_inicial.turno_blanco is True # Turno Blanco

    # Blanco captura al paso exd6
    origen_blanco = (4, 4) # e5
    destino_blanco = (5, 3) # d6 (casilla de captura al paso)
    casilla_peon_capturado = (4, 3) # d5 (donde estaba el peón negro)
    pieza_blanca = tablero_inicial.getPieza(origen_blanco)
    pieza_negra_capturada = tablero_inicial.getPieza(casilla_peon_capturado)

    resultado = tablero_inicial.moverPieza(origen_blanco, destino_blanco)

    assert resultado == 'movimiento_ok'
    assert tablero_inicial.getPieza(origen_blanco) is None, "Origen del peón blanco (e5) debe estar vacío."
    assert tablero_inicial.getPieza(destino_blanco) is pieza_blanca, "Peón blanco debe estar en destino (d6)."
    assert pieza_blanca.posicion == destino_blanco, "Posición interna del peón blanco debe ser d6."
    assert tablero_inicial.getPieza(casilla_peon_capturado) is None, "Casilla del peón negro capturado (d5) debe estar vacía."
    assert pieza_negra_capturada in tablero_inicial.piezasCapturadas, "Peón negro debe estar en capturadas."
    assert tablero_inicial.objetivoPeonAlPaso is None, "Objetivo al paso debe limpiarse después de la captura."
    assert tablero_inicial.turno_blanco is False # Turno Negro
    assert tablero_inicial.contadorRegla50Movimientos == 0, "Contador 50 mov se resetea por captura."

# --- Promoción ---

def test_moverPieza_promocion_necesaria_blanco(tablero_vacio: Tablero):
    """
    Verifica que mover un peón blanco a la 8va fila retorna 'promocion_necesaria'.
    """
    peon_blanco = Peon('blanco', (6, 0))
    tablero_vacio.setPieza((6, 0), peon_blanco) # Peón blanco en a7
    tablero_vacio.turno_blanco = True

    resultado = tablero_vacio.moverPieza((6, 0), (7, 0)) # Mueve a a8

    assert resultado == 'promocion_necesaria'
    assert tablero_vacio.getPieza((6, 0)) is None # Origen vacío
    # La pieza en el destino es el peón ANTES de la promoción real
    assert isinstance(tablero_vacio.getPieza((7, 0)), Peon)
    assert tablero_vacio.getPieza((7, 0)) is peon_blanco
    assert peon_blanco.posicion == (7, 0)
    assert tablero_vacio.turno_blanco is False # Turno cambió

def test_moverPieza_promocion_necesaria_negro(tablero_vacio: Tablero):
    """
    Verifica que mover un peón negro a la 1ra fila retorna 'promocion_necesaria'.
    """
    peon_negro = Peon('negro', (1, 7))
    tablero_vacio.setPieza((1, 7), peon_negro) # Peón negro en h2
    tablero_vacio.turno_blanco = False # Turno negro

    resultado = tablero_vacio.moverPieza((1, 7), (0, 7)) # Mueve a h1

    assert resultado == 'promocion_necesaria'
    assert tablero_vacio.getPieza((1, 7)) is None # Origen vacío
    assert isinstance(tablero_vacio.getPieza((0, 7)), Peon)
    assert tablero_vacio.getPieza((0, 7)) is peon_negro
    assert peon_negro.posicion == (0, 7)
    assert tablero_vacio.turno_blanco is True # Turno cambió

# --- Enroque ---

def test_actualizarDerechosEnroque_mov_rey_blanco(tablero_inicial: Tablero):
    """
    Verifica que mover el rey blanco pierde ambos derechos de enroque.
    """
    rey = tablero_inicial.getPieza((0, 4))
    # Asegurarse de que la casilla destino está vacía para la prueba
    tablero_inicial.setPieza((1, 4), None)
    tablero_inicial.moverPieza((0, 4), (1, 4)) # Ke1 -> e2
    assert tablero_inicial.derechosEnroque['blanco']['corto'] is False
    assert tablero_inicial.derechosEnroque['blanco']['largo'] is False
    # Los derechos negros no deben cambiar
    assert tablero_inicial.derechosEnroque['negro']['corto'] is True
    assert tablero_inicial.derechosEnroque['negro']['largo'] is True

def test_actualizarDerechosEnroque_mov_torre_corta_negra(tablero_inicial: Tablero):
    """
    Verifica que mover la torre corta negra pierde el derecho corto negro.
    """
    tablero_inicial.turno_blanco = False # Turno negro
    torre = tablero_inicial.getPieza((7, 7))
    # Asegurarse de que la casilla destino está vacía para la prueba
    tablero_inicial.setPieza((6, 7), None)
    tablero_inicial.moverPieza((7, 7), (6, 7)) # Th8 -> h7
    assert tablero_inicial.derechosEnroque['negro']['corto'] is False
    assert tablero_inicial.derechosEnroque['negro']['largo'] is True # Largo no cambia
    # Los derechos blancos no deben cambiar
    assert tablero_inicial.derechosEnroque['blanco']['corto'] is True
    assert tablero_inicial.derechosEnroque['blanco']['largo'] is True

def test_actualizarDerechosEnroque_mov_torre_larga_blanca(tablero_inicial: Tablero):
    """
    Verifica que mover la torre larga blanca pierde el derecho largo blanco.
    """
    torre = tablero_inicial.getPieza((0, 0))
    # Asegurarse de que la casilla destino está vacía para la prueba
    tablero_inicial.setPieza((0, 1), None)
    tablero_inicial.moverPieza((0, 0), (0, 1)) # Ta1 -> b1
    assert tablero_inicial.derechosEnroque['blanco']['largo'] is False
    assert tablero_inicial.derechosEnroque['blanco']['corto'] is True # Corto no cambia
    assert tablero_inicial.derechosEnroque['negro']['corto'] is True
    assert tablero_inicial.derechosEnroque['negro']['largo'] is True

def test_actualizarDerechosEnroque_captura_torre_corta_blanca(tablero_vacio: Tablero):
    """
    Verifica que capturar la torre corta blanca en h1 hace perder el derecho corto blanco.
    """
    tablero_vacio.setPieza((0, 7), Torre('blanco', (0, 7))) # Rh1
    tablero_vacio.setPieza((1, 6), Reina('negro', (1, 6))) # Qg2
    tablero_vacio.derechosEnroque['blanco']['corto'] = True # Asegurar derecho inicial
    tablero_vacio.turno_blanco = False # Turno negro

    # Negro captura Dxg2xh1
    tablero_vacio.moverPieza((1, 6), (0, 7))

    assert tablero_vacio.derechosEnroque['blanco']['corto'] is False, "El derecho corto blanco debe perderse por captura de torre."

def test_realizarEnroque_corto_blanco_ok(tablero_vacio: Tablero):
    """
    Prueba la ejecución del enroque corto blanco (asumiendo validez).
    """
    # Setup: Rey en e1, Torre en h1, casillas f1, g1 vacías. Derechos OK.
    rey = Rey('blanco', (0, 4))
    torre = Torre('blanco', (0, 7))
    tablero_vacio.setPieza((0, 4), rey)
    tablero_vacio.setPieza((0, 7), torre)
    tablero_vacio.derechosEnroque['blanco']['corto'] = True
    tablero_vacio.derechosEnroque['blanco']['largo'] = True # Dejar el largo también para ver que no se afecta innecesariamente
    tablero_vacio.turno_blanco = True

    resultado = tablero_vacio.realizarEnroque('blanco', 'corto')

    assert resultado is True
    assert tablero_vacio.getPieza((0, 4)) is None, "e1 debe estar vacío."
    assert tablero_vacio.getPieza((0, 7)) is None, "h1 debe estar vacío."
    assert tablero_vacio.getPieza((0, 6)) is rey, "Rey debe estar en g1."
    assert tablero_vacio.getPieza((0, 5)) is torre, "Torre debe estar en f1."
    assert rey.posicion == (0, 6), "Posición interna del Rey debe ser g1."
    assert torre.posicion == (0, 5), "Posición interna de la Torre debe ser f1."
    assert tablero_vacio.derechosEnroque['blanco']['corto'] is False, "Derecho corto blanco perdido."
    assert tablero_vacio.derechosEnroque['blanco']['largo'] is False, "Derecho largo blanco perdido (movimiento de rey)."
    assert tablero_vacio.turno_blanco is False, "Turno debe pasar a negras."
    assert tablero_vacio.contadorRegla50Movimientos == 1, "Contador 50 mov avanza (no peón, no captura)."
    assert tablero_vacio.ultimo_movimiento == ((0, 4), (0, 6)), "Último mov registrado (mov rey)."
    assert tablero_vacio.historial_movimientos[-1] == ('blanco', (0, 4), (0, 6)), "Historial registra mov rey."

def test_realizarEnroque_largo_negro_ok(tablero_vacio: Tablero):
    """
    Prueba la ejecución del enroque largo negro (asumiendo validez).
    """
    # Setup: Rey en e8, Torre en a8, casillas b8, c8, d8 vacías. Derechos OK.
    rey = Rey('negro', (7, 4))
    torre = Torre('negro', (7, 0))
    tablero_vacio.setPieza((7, 4), rey)
    tablero_vacio.setPieza((7, 0), torre)
    tablero_vacio.derechosEnroque['negro']['corto'] = True
    tablero_vacio.derechosEnroque['negro']['largo'] = True
    tablero_vacio.turno_blanco = False # Turno negro

    resultado = tablero_vacio.realizarEnroque('negro', 'largo')

    assert resultado is True
    assert tablero_vacio.getPieza((7, 4)) is None, "e8 debe estar vacío."
    assert tablero_vacio.getPieza((7, 0)) is None, "a8 debe estar vacío."
    assert tablero_vacio.getPieza((7, 2)) is rey, "Rey debe estar en c8."
    assert tablero_vacio.getPieza((7, 3)) is torre, "Torre debe estar en d8."
    assert rey.posicion == (7, 2), "Posición interna del Rey debe ser c8."
    assert torre.posicion == (7, 3), "Posición interna de la Torre debe ser d8."
    assert tablero_vacio.derechosEnroque['negro']['corto'] is False, "Derecho corto negro perdido."
    assert tablero_vacio.derechosEnroque['negro']['largo'] is False, "Derecho largo negro perdido."
    assert tablero_vacio.turno_blanco is True, "Turno debe pasar a blancas."
    assert tablero_vacio.contadorRegla50Movimientos == 1
    assert tablero_vacio.ultimo_movimiento == ((7, 4), (7, 2))
    assert tablero_vacio.historial_movimientos[-1] == ('negro', (7, 4), (7, 2))

def test_realizarEnroque_error_pieza_incorrecta(tablero_vacio: Tablero):
    """
    Prueba que realizarEnroque falla si las piezas no son Rey/Torre.
    """
    tablero_vacio.setPieza((0, 4), Reina('blanco', (0, 4))) # Reina en lugar de Rey
    tablero_vacio.setPieza((0, 7), Torre('blanco', (0, 7)))
    tablero_vacio.derechosEnroque['blanco']['corto'] = True
    tablero_vacio.turno_blanco = True

    resultado = tablero_vacio.realizarEnroque('blanco', 'corto')
    assert resultado is False, "Debe fallar si no hay un Rey en la posición esperada."

# ============================================================
# Pruebas de Evaluación de Amenazas y Estado del Juego
# ============================================================

# Mock simple de obtener_movimientos_potenciales para piezas
# Necesario porque esCasillaAmenazada depende de ello y las clases Pieza no están completas
def mock_obtener_movimientos_potenciales(self, tablero):
    # Simulación muy básica: devolver la casilla adyacente para el test
    if isinstance(self, Reina) and self.posicion == (3, 3): return [(4, 4)]
    if isinstance(self, Caballo) and self.posicion == (2, 1): return [(4, 2)]
    # Añadir más mocks según sea necesario para otros tests
    return []

@pytest.fixture(autouse=True)
def patch_pieza_movimientos(monkeypatch):
    """
    Parchea temporalmente obtener_movimientos_potenciales en las clases de Pieza
    para los tests de esCasillaAmenazada.
    """
    monkeypatch.setattr(Pieza, "obtener_movimientos_potenciales", mock_obtener_movimientos_potenciales, raising=False)
    # Asegurar que las subclases también lo usen si no lo sobreescriben
    monkeypatch.setattr(Reina, "obtener_movimientos_potenciales", mock_obtener_movimientos_potenciales, raising=False)
    monkeypatch.setattr(Caballo, "obtener_movimientos_potenciales", mock_obtener_movimientos_potenciales, raising=False)
    # Añadir más parches si se usan otras piezas en los tests de amenaza

def test_esCasillaAmenazada_positiva(tablero_vacio: Tablero):
    """
    Verifica que una casilla es identificada como amenazada.
    """
    reina_negra = Reina('negro', (3, 3))
    tablero_vacio.setPieza((3, 3), reina_negra) # Reina negra en d4
    # El mock hace que d4 amenace e5=(4,4)
    assert tablero_vacio.esCasillaAmenazada((4, 4), 'negro') is True

def test_esCasillaAmenazada_negativa_color(tablero_vacio: Tablero):
    """
    Verifica que una casilla no es amenazada por el color incorrecto.
    """
    reina_negra = Reina('negro', (3, 3))
    tablero_vacio.setPieza((3, 3), reina_negra)
    assert tablero_vacio.esCasillaAmenazada((4, 4), 'blanco') is False # Amenaza negra, no blanca

def test_esCasillaAmenazada_negativa_no_amenaza(tablero_vacio: Tablero):
    """
    Verifica que una casilla no es amenazada si ninguna pieza la ataca.
    """
    reina_negra = Reina('negro', (3, 3))
    tablero_vacio.setPieza((3, 3), reina_negra)
    assert tablero_vacio.esCasillaAmenazada((5, 5), 'negro') is False # d4 no amenaza f6 en el mock

def test_esCasillaAmenazada_posicion_invalida(tablero_vacio: Tablero):
    """
    Verifica que una posición inválida nunca está amenazada.
    """
    assert tablero_vacio.esCasillaAmenazada((-1, 0), 'blanco') is False

def test_actualizarEstadoJuego_jaque(tablero_vacio: Tablero):
    """
    Verifica que el estado cambia a 'jaque' si el rey actual está amenazado.
    """
    rey_blanco = Rey('blanco', (4, 4)) # Rey blanco en e5
    reina_negra = Reina('negro', (3, 3)) # Reina negra en d4 (amenaza e5 segun mock)
    tablero_vacio.setPieza((4, 4), rey_blanco)
    tablero_vacio.setPieza((3, 3), reina_negra)
    tablero_vacio.turno_blanco = True # Turno blanco (rey amenazado)

    tablero_vacio.actualizarEstadoJuego() # Debe detectar la amenaza al rey blanco
    assert tablero_vacio.estado_juego == 'jaque'

def test_actualizarEstadoJuego_en_curso(tablero_vacio: Tablero):
    """
    Verifica que el estado permanece 'en_curso' si no hay jaque ni tablas.
    """
    rey_blanco = Rey('blanco', (5, 5)) # Rey blanco en f6
    reina_negra = Reina('negro', (3, 3)) # Reina negra en d4 (NO amenaza f6 segun mock)
    tablero_vacio.setPieza((5, 5), rey_blanco)
    tablero_vacio.setPieza((3, 3), reina_negra)
    tablero_vacio.turno_blanco = True

    tablero_vacio.actualizarEstadoJuego()
    assert tablero_vacio.estado_juego == 'en_curso'

def test_actualizarEstadoJuego_tablas_50_mov(tablero_vacio: Tablero):
    """
    Verifica que el estado cambia a 'tablas' por la regla de 50 movimientos.
    """
    rey_b = Rey('blanco', (0, 0))
    rey_n = Rey('negro', (7, 7))
    tablero_vacio.setPieza((0, 0), rey_b)
    tablero_vacio.setPieza((7, 7), rey_n)
    tablero_vacio.contadorRegla50Movimientos = 99 # A punto de cumplir la regla
    tablero_vacio.turno_blanco = True

    # Mover rey blanco (no captura, no peón)
    resultado = tablero_vacio.moverPieza((0, 0), (0, 1)) # Ka1 -> b1
    assert resultado == 'movimiento_ok'
    # moverPieza llama a actualizarContadores (incrementa a 100)
    # y luego a actualizarEstadoJuego
    assert tablero_vacio.contadorRegla50Movimientos == 100
    assert tablero_vacio.estado_juego == 'tablas'

# ============================================================
# Pruebas de Condiciones de Tablas
# ============================================================

# --- Material Insuficiente ---

@pytest.mark.parametrize("piezas_blancas, piezas_negras, esperado", [
    # Casos de material insuficiente (True)
    ([], [], True),                                  # K vs K
    ([(Caballo, (0, 1))], [], True),                 # K+N vs K
    ([(Alfil, (0, 2))], [], True),                   # K+B vs K
    ([], [(Caballo, (7, 1))], True),                 # K vs K+N
    ([], [(Alfil, (7, 2))], True),                   # K vs K+B
    ([(Alfil, (0, 2))], [(Alfil, (7, 5))], True),    # K+B vs K+B (mismo color, c1 y f8 son oscuras)
    ([(Alfil, (0, 1))], [(Alfil, (7, 6))], True),    # K+B vs K+B (mismo color, b1 y g8 son claras)

    # Casos de material suficiente (False)
    ([(Reina, (0, 3))], [], False),                  # K+Q vs K
    ([(Torre, (0, 0))], [], False),                  # K+R vs K
    ([(Peon, (1, 0))], [], False),                   # K+P vs K
    ([(Alfil, (0, 2)), (Caballo, (0, 1))], [], False), # K+B+N vs K
    ([(Alfil, (0, 1))], [(Alfil, (7, 5))], False),   # K+B vs K+B (diferente color, b1 clara, f8 oscura)
    ([(Caballo, (0,1)), (Caballo, (0,6))], [], False) # K+N+N vs K (FIDE considera suficiente)
])
def test_esMaterialInsuficiente(tablero_vacio: Tablero, piezas_blancas: list[tuple[Type[Pieza], tuple[int, int]]], piezas_negras: list[tuple[Type[Pieza], tuple[int, int]]], esperado: bool):
    """
    Verifica la detección de material insuficiente para varios escenarios.
    """
    # Colocar reyes
    tablero_vacio.setPieza((4, 4), Rey('blanco', (4, 4))) # Ke5
    tablero_vacio.setPieza((4, 0), Rey('negro', (4, 0))) # Ka5

    # Colocar piezas de prueba
    for tipo_pieza, pos in piezas_blancas:
        tablero_vacio.setPieza(pos, tipo_pieza('blanco', pos))
    for tipo_pieza, pos in piezas_negras:
        tablero_vacio.setPieza(pos, tipo_pieza('negro', pos))

    assert tablero_vacio.esMaterialInsuficiente() == esperado

# --- Triple Repetición ---
# ADVERTENCIA: La implementación actual es defectuosa (usa simulación).
# Estas pruebas son básicas y pueden fallar o dar falsos positivos/negativos
# debido a las limitaciones en el manejo de enroque/promoción en la simulación.

# Mock simple para obtenerNotacionFEN (necesario para obtenerPosicionActual)
def mock_obtenerNotacionFEN(self):
    if isinstance(self, Peon): return 'P'
    if isinstance(self, Torre): return 'R'
    if isinstance(self, Caballo): return 'N'
    if isinstance(self, Alfil): return 'B'
    if isinstance(self, Reina): return 'Q'
    if isinstance(self, Rey): return 'K'
    return '?'

@pytest.fixture(autouse=True)
def patch_pieza_fen(monkeypatch):
    """Parchea obtenerNotacionFEN en Pieza para los tests."""
    monkeypatch.setattr(Pieza, "obtenerNotacionFEN", mock_obtenerNotacionFEN, raising=False)

# @pytest.mark.skip(reason="La implementación de esTripleRepeticion usa simulación y es inherentemente frágil.")
def test_esTripleRepeticion_simple(tablero_vacio: Tablero):
    """
    Prueba básica de triple repetición con movimientos simples de rey.
    """
    # Setup: Reyes solos, tablero_vacio starts with history reset
    rey_b = Rey('blanco', (0, 0))
    rey_n = Rey('negro', (7, 7))
    tablero_vacio.setPieza((0, 0), rey_b)
    tablero_vacio.setPieza((7, 7), rey_n)
    tablero_vacio.turno_blanco = True
    # Reset history for this specific test scenario, as __init__ on tablero_vacio might have run differently
    tablero_vacio.historial_posiciones.clear()
    pos_inicial_str = tablero_vacio.obtenerPosicionActual()
    tablero_vacio.historial_posiciones[pos_inicial_str] = 1 # Add the actual starting position for the test

    # Get a logger for this test
    test_logger = logging.getLogger('TestTripleRepeticion')
    test_logger.setLevel(logging.DEBUG) # Ensure debug messages are processed

    # Sequence: Kb1(W), Kh7(B), Ka1(W), Kh8(B), Kb1(W), Kh7(B), Ka1(W), Kh8(B)
    # Target state (S0 = initial): Ka1, Kh8, turn W
    # S0 count should be 1 initially.
    # After move 4 (Kh8), S0 occurs again, count becomes 2.
    # After move 8 (Kh8), S0 occurs again, count becomes 3.

    # Mov 1: Kb1 (W) -> Turn B
    tablero_vacio.moverPieza((0, 0), (0, 1)) # S1
    assert not tablero_vacio.esTripleRepeticion(), "Repetition check after move 1 failed"
    # Mov 2: Kh7 (B) -> Turn W
    tablero_vacio.moverPieza((7, 7), (7, 6)) # S2
    assert not tablero_vacio.esTripleRepeticion(), "Repetition check after move 2 failed"
    # Mov 3: Ka1 (W) -> Turn B
    tablero_vacio.moverPieza((0, 1), (0, 0)) # S3
    assert not tablero_vacio.esTripleRepeticion(), "Repetition check after move 3 failed"
    # Mov 4: Kh8 (B) -> Turn W
    tablero_vacio.moverPieza((7, 6), (7, 7)) # S0 (Count = 2)
    assert not tablero_vacio.esTripleRepeticion(), "Repetition check after move 4 failed"
    # Mov 5: Kb1 (W) -> Turn B
    tablero_vacio.moverPieza((0, 0), (0, 1)) # S1 (Count = 2)
    assert not tablero_vacio.esTripleRepeticion(), "Repetition check after move 5 failed"
    # Mov 6: Kh7 (B) -> Turn W
    tablero_vacio.moverPieza((7, 7), (7, 6)) # S2 (Count = 2)
    assert not tablero_vacio.esTripleRepeticion(), "Repetition check after move 6 failed"
    # Mov 7: Ka1 (W) -> Turn B
    tablero_vacio.moverPieza((0, 1), (0, 0)) # S3 (Count = 2)
    assert not tablero_vacio.esTripleRepeticion(), "Repetition check after move 7 failed"
    # Mov 8: Kh8 (B) -> Turn W
    tablero_vacio.moverPieza((7, 6), (7, 7)) # S0 (Count = 3)
    # Now the initial state (S0) should have occurred 3 times.

    # Debug logs just before the final check
    test_logger.debug(f"\nDEBUG: Estado inicial guardado: {pos_inicial_str}")
    estado_final_str = tablero_vacio.obtenerPosicionActual()
    test_logger.debug(f"DEBUG: Estado antes de la aserción final: {estado_final_str}")
    # Log count for initial and final strings specifically
    test_logger.debug(f"DEBUG: Count for initial string '{pos_inicial_str}': {tablero_vacio.historial_posiciones.get(pos_inicial_str, 0)}")
    test_logger.debug(f"DEBUG: Count for final string '{estado_final_str}': {tablero_vacio.historial_posiciones.get(estado_final_str, 0)}")
    test_logger.debug(f"DEBUG: Historial de posiciones completo final: {tablero_vacio.historial_posiciones}")

    # The call to esTripleRepeticion should now return True
    assert tablero_vacio.esTripleRepeticion() is True, "Debería detectar la tercera repetición después del 8º movimiento."


# ============================================================
# Pruebas de Representación (obtenerPosicionActual)
# ============================================================

def test_obtenerPosicionActual_inicial(tablero_inicial: Tablero):
    """
    Verifica la representación de la posición inicial.
    """
    # Construcción manual de la representación esperada (simplificada con '.' y letras)
    fila_negras = "rnbqkbnr"
    peones_negras = "pppppppp"
    vacias = "........"
    peones_blancas = "PPPPPPPP"
    fila_blancas = "RNBQKBNR"
    piezas_esperadas = "/".join([
        fila_blancas, peones_blancas, vacias, vacias, vacias, vacias, peones_negras, fila_negras
    ])
    turno_esperado = "w"
    enroque_esperado = "KQkq"
    alpaso_esperado = "-"

    esperado_str = f"{piezas_esperadas} {turno_esperado} {enroque_esperado} {alpaso_esperado}"
    # Nota: La implementación actual usa '.' para vacíos, pero el cálculo FEN usa números.
    # Adaptaremos la prueba a la salida *actual* de la función.
    # Reemplazar números FEN con puntos para coincidir:
    fila_negras = "rnbqkbnr" # ok
    peones_negras = "pppppppp" # ok
    vacias = "........" # ok
    peones_blancas = "PPPPPPPP" # ok
    fila_blancas = "RNBQKBNR" # ok
    piezas_esperadas_actual = "/".join([
        fila_blancas, peones_blancas, vacias, vacias, vacias, vacias, peones_negras, fila_negras
    ])
    esperado_str_actual = f"{piezas_esperadas_actual} {turno_esperado} {enroque_esperado} {alpaso_esperado}"


    assert tablero_inicial.obtenerPosicionActual() == esperado_str_actual

def test_obtenerPosicionActual_post_movimiento(tablero_inicial: Tablero):
    """
    Verifica la representación tras un movimiento (e4).
    """
    tablero_inicial.moverPieza((1, 4), (3, 4)) # e4

    fila_negras = "rnbqkbnr"
    peones_negras = "pppppppp"
    vacias = "........"
    fila3 = "....P..." # Peón blanco en e4
    fila2_modif = "PPPP.PPP" # Peón e2 movido
    fila_blancas = "RNBQKBNR"
    piezas_esperadas = "/".join([
        fila_blancas, fila2_modif, vacias, fila3, vacias, vacias, peones_negras, fila_negras
    ])
    turno_esperado = "b" # Turno negro
    enroque_esperado = "KQkq" # No cambia
    alpaso_esperado = "e3" # Objetivo al paso creado (fila 2, col 4 -> e3)

    esperado_str = f"{piezas_esperadas} {turno_esperado} {enroque_esperado} {alpaso_esperado}"
    assert tablero_inicial.obtenerPosicionActual() == esperado_str

def test_obtenerPosicionActual_sin_enroque(tablero_inicial: Tablero):
    """
    Verifica la representación cuando se pierden derechos de enroque.
    """
    tablero_inicial.derechosEnroque['blanco']['corto'] = False
    tablero_inicial.derechosEnroque['negro']['largo'] = False
    enroque_esperado = "Qk" # Solo quedan Largo Blanco y Corto Negro

    pos_str = tablero_inicial.obtenerPosicionActual()
    partes = pos_str.split(' ')
    assert len(partes) == 4
    assert partes[2] == enroque_esperado # Verificar parte del enroque

