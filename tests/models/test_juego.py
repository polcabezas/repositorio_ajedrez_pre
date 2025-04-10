import pytest
from collections import defaultdict
from models.juego import Juego
from models.piezas.peon import Peon
from models.piezas.rey import Rey
from models.piezas.torre import Torre
from models.piezas.reina import Reina
from models.piezas.alfil import Alfil
from models.piezas.caballo import Caballo

# Fixture para crear un juego limpio para cada test
@pytest.fixture
def juego_nuevo():
    return Juego()

# ==================================================
# Tests de Movimientos Especiales (Migrados/Adaptados)
# ==================================================

def test_promocion_peon_todos_tipos(juego_nuevo):
    """Verifica la promoción de un peón a todas las piezas posibles (Q, R, B, N)."""
    # --- Promoción Blanca a Reina (Q) ---
    juego_nuevo.tablero.casillas = [[None for _ in range(8)] for _ in range(8)]
    peon_blanco_q = Peon('blanco', (6, 0), juego_nuevo.tablero) # a7
    rey_n_q = Rey('negro', (7, 2), juego_nuevo.tablero)
    rey_b_q = Rey('blanco', (0, 2), juego_nuevo.tablero)
    # Añadir piezas adicionales para evitar tablas por material insuficiente
    peon_extra_b1 = Peon('blanco', (1, 0), juego_nuevo.tablero)
    peon_extra_n1 = Peon('negro', (6, 1), juego_nuevo.tablero)
    juego_nuevo.tablero.setPieza((6, 0), peon_blanco_q)
    juego_nuevo.tablero.setPieza((7, 2), rey_n_q)
    juego_nuevo.tablero.setPieza((0, 2), rey_b_q)
    juego_nuevo.tablero.setPieza((1, 0), peon_extra_b1)
    juego_nuevo.tablero.setPieza((6, 1), peon_extra_n1)
    juego_nuevo.turno_actual = 'blanco'
    
    # DEBUG: Print legal moves for white
    legal_moves_q = juego_nuevo.tablero.obtener_todos_movimientos_legales('blanco')
    print(f"DEBUG: Legal moves for white before a8=Q attempt: {legal_moves_q}")
    assert ((6, 0), (7, 0)) in legal_moves_q, "Promotion move to a8 should be legal"
    
    assert juego_nuevo.realizarMovimiento((6, 0), (7, 0), promocion='Q') == True # a8=Q
    pieza_q = juego_nuevo.tablero.getPieza((7, 0))
    assert isinstance(pieza_q, Reina) and pieza_q.color == 'blanco'
    assert juego_nuevo.turno_actual == 'negro'

    # --- Promoción Negra a Torre (R) ---
    juego_nuevo.tablero.casillas = [[None for _ in range(8)] for _ in range(8)]
    peon_negro_r = Peon('negro', (1, 1), juego_nuevo.tablero) # b2
    rey_b_r = Rey('blanco', (0, 4), juego_nuevo.tablero)
    rey_n_r = Rey('negro', (7, 4), juego_nuevo.tablero)
    # Añadir piezas adicionales para evitar tablas por material insuficiente
    peon_extra_b2 = Peon('blanco', (1, 0), juego_nuevo.tablero)
    peon_extra_n2 = Peon('negro', (6, 1), juego_nuevo.tablero)
    juego_nuevo.tablero.setPieza((1, 1), peon_negro_r)
    juego_nuevo.tablero.setPieza((0, 4), rey_b_r)
    juego_nuevo.tablero.setPieza((7, 4), rey_n_r)
    juego_nuevo.tablero.setPieza((1, 0), peon_extra_b2)
    juego_nuevo.tablero.setPieza((6, 1), peon_extra_n2)
    juego_nuevo.turno_actual = 'negro'
    
    # DEBUG: Print legal moves for black
    legal_moves_r = juego_nuevo.tablero.obtener_todos_movimientos_legales('negro')
    print(f"DEBUG: Legal moves for black before b1=R attempt: {legal_moves_r}")
    assert ((1, 1), (0, 1)) in legal_moves_r, "Promotion move to b1 should be legal"
    
    assert juego_nuevo.realizarMovimiento((1, 1), (0, 1), promocion='R') == True # b1=R
    pieza_r = juego_nuevo.tablero.getPieza((0, 1))
    assert isinstance(pieza_r, Torre) and pieza_r.color == 'negro'
    assert juego_nuevo.turno_actual == 'blanco'

    # --- Promoción Blanca a Alfil (B) ---
    juego_nuevo.tablero.casillas = [[None for _ in range(8)] for _ in range(8)]
    peon_blanco_b = Peon('blanco', (6, 2), juego_nuevo.tablero) # c7
    rey_n_b = Rey('negro', (7, 5), juego_nuevo.tablero)
    rey_b_b = Rey('blanco', (0, 5), juego_nuevo.tablero)
    # Añadir piezas adicionales para evitar tablas por material insuficiente
    peon_extra_b3 = Peon('blanco', (1, 0), juego_nuevo.tablero)
    peon_extra_n3 = Peon('negro', (6, 1), juego_nuevo.tablero)
    juego_nuevo.tablero.setPieza((6, 2), peon_blanco_b)
    juego_nuevo.tablero.setPieza((7, 5), rey_n_b)
    juego_nuevo.tablero.setPieza((0, 5), rey_b_b)
    juego_nuevo.tablero.setPieza((1, 0), peon_extra_b3)
    juego_nuevo.tablero.setPieza((6, 1), peon_extra_n3)
    juego_nuevo.turno_actual = 'blanco'
    
    # DEBUG: Print potential and legal moves for the pawn
    movs_potenciales = peon_blanco_b.obtener_movimientos_potenciales()
    print(f"DEBUG: Potential moves for pawn at c7: {movs_potenciales}")
    movs_legales_peon = peon_blanco_b.obtener_movimientos_legales()
    print(f"DEBUG: Legal moves for pawn at c7: {movs_legales_peon}")
    legal_moves_before_promo = juego_nuevo.tablero.obtener_todos_movimientos_legales('blanco')
    print(f"DEBUG: Legal moves for white before c8=B attempt: {legal_moves_before_promo}")
    assert ((6, 2), (7, 2)) in legal_moves_before_promo, "Promotion move to c8 should be legal"
    
    assert juego_nuevo.realizarMovimiento((6, 2), (7, 2), promocion='B') == True # c8=B
    pieza_b = juego_nuevo.tablero.getPieza((7, 2))
    assert isinstance(pieza_b, Alfil) and pieza_b.color == 'blanco'
    assert juego_nuevo.turno_actual == 'negro'

    # --- Promoción Negra a Caballo (N) ---
    juego_nuevo.tablero.casillas = [[None for _ in range(8)] for _ in range(8)]
    peon_negro_n = Peon('negro', (1, 3), juego_nuevo.tablero) # d2
    rey_b_n = Rey('blanco', (0, 6), juego_nuevo.tablero)
    rey_n_n = Rey('negro', (7, 6), juego_nuevo.tablero)
    # Añadir piezas adicionales para evitar tablas por material insuficiente
    peon_extra_b4 = Peon('blanco', (1, 0), juego_nuevo.tablero)
    peon_extra_n4 = Peon('negro', (6, 1), juego_nuevo.tablero)
    juego_nuevo.tablero.setPieza((1, 3), peon_negro_n)
    juego_nuevo.tablero.setPieza((0, 6), rey_b_n)
    juego_nuevo.tablero.setPieza((7, 6), rey_n_n)
    juego_nuevo.tablero.setPieza((1, 0), peon_extra_b4)
    juego_nuevo.tablero.setPieza((6, 1), peon_extra_n4)
    juego_nuevo.turno_actual = 'negro'
    
    # DEBUG: Print legal moves for black
    legal_moves_n = juego_nuevo.tablero.obtener_todos_movimientos_legales('negro')
    print(f"DEBUG: Legal moves for black before d1=N attempt: {legal_moves_n}")
    assert ((1, 3), (0, 3)) in legal_moves_n, "Promotion move to d1 should be legal"
    
    assert juego_nuevo.realizarMovimiento((1, 3), (0, 3), promocion='N') == True # d1=N
    pieza_n = juego_nuevo.tablero.getPieza((0, 3))
    assert isinstance(pieza_n, Caballo) and pieza_n.color == 'negro'
    assert juego_nuevo.turno_actual == 'blanco'

def test_promocion_peon_faltante(juego_nuevo):
    """Verifica que el movimiento falle si se requiere promoción y no se especifica."""
    # Configurar tablero para promoción blanca
    juego_nuevo.tablero.casillas = [[None for _ in range(8)] for _ in range(8)]
    peon_blanco = Peon('blanco', (6, 0), juego_nuevo.tablero)
    rey_negro = Rey('negro', (7, 2), juego_nuevo.tablero) 
    rey_blanco = Rey('blanco', (0, 0), juego_nuevo.tablero)
    # Añadir piezas adicionales para evitar tablas por material insuficiente
    peon_extra_b = Peon('blanco', (1, 0), juego_nuevo.tablero)
    peon_extra_n = Peon('negro', (6, 1), juego_nuevo.tablero)
    juego_nuevo.tablero.setPieza((6, 0), peon_blanco)
    juego_nuevo.tablero.setPieza((7, 2), rey_negro)
    juego_nuevo.tablero.setPieza((0, 0), rey_blanco)
    juego_nuevo.tablero.setPieza((1, 0), peon_extra_b)
    juego_nuevo.tablero.setPieza((6, 1), peon_extra_n)
    juego_nuevo.turno_actual = 'blanco'

    # Intentar mover peón sin especificar promoción
    assert juego_nuevo.realizarMovimiento((6, 0), (7, 0)) == False
    # Verificar que la pieza no se movió y sigue siendo peón
    assert isinstance(juego_nuevo.tablero.getPieza((6, 0)), Peon)
    assert juego_nuevo.tablero.getPieza((7, 0)) is None
    assert juego_nuevo.turno_actual == 'blanco' # Turno no cambió

# --- Tests de En Passant ---
def test_peon_al_paso_preparacion(juego_nuevo):
    """Verifica que el objetivo de peón al paso se establece correctamente."""
    assert juego_nuevo.tablero.objetivoPeonAlPaso is None
    # Mover peón blanco dos casillas
    juego_nuevo.realizarMovimiento((1, 4), (3, 4)) # e2-e4
    assert juego_nuevo.tablero.objetivoPeonAlPaso == (2, 4) # Objetivo en e3
    assert juego_nuevo.turno_actual == 'negro'
    
    # Mover peón negro una casilla (no relevante para EP, pero avanza turno)
    juego_nuevo.realizarMovimiento((6, 0), (5, 0)) # a7-a6
    # El objetivo EP debe desaparecer después del siguiente movimiento
    assert juego_nuevo.tablero.objetivoPeonAlPaso is None
    assert juego_nuevo.turno_actual == 'blanco'

def test_peon_al_paso_ejecucion(juego_nuevo):
    """Verifica la captura al paso exitosa."""
    # 1. e4
    juego_nuevo.realizarMovimiento((1, 4), (3, 4))
    assert juego_nuevo.tablero.objetivoPeonAlPaso == (2, 4)
    # 2. a6 (movimiento irrelevante negro)
    juego_nuevo.realizarMovimiento((6, 0), (5, 0)) 
    assert juego_nuevo.tablero.objetivoPeonAlPaso is None
    # 3. e5
    juego_nuevo.realizarMovimiento((3, 4), (4, 4))
    # 4. d5 (prepara captura al paso por peón e)
    juego_nuevo.realizarMovimiento((6, 3), (4, 3)) # Peón negro a d5
    assert juego_nuevo.tablero.objetivoPeonAlPaso == (5, 3) # Objetivo en d6 (no relevante ahora)
    
    # 5. Peón blanco en e5 captura peón negro en d5 via en passant en d6
    peon_blanco_captor = juego_nuevo.tablero.getPieza((4, 4))
    assert isinstance(peon_blanco_captor, Peon)
    
    # Verificar que el movimiento EP está en los legales
    movimientos_legales_blanco = juego_nuevo.tablero.obtener_todos_movimientos_legales('blanco')
    # El destino del EP es (5,3) [d6], no (4,3) [d5] donde está el peón
    # CORRECCIÓN: El destino *es* la casilla objetivo EP
    mov_ep_esperado = ((4, 4), (5, 3)) # e5xd6
    assert mov_ep_esperado in movimientos_legales_blanco

    # Realizar la captura al paso
    assert juego_nuevo.realizarMovimiento((4, 4), (5, 3)) == True # e5xd6
    
    # Verificar resultado
    assert juego_nuevo.tablero.getPieza((5, 3)) == peon_blanco_captor # Peón blanco movido a d6
    assert juego_nuevo.tablero.getPieza((4, 4)) is None # Origen vacío
    assert juego_nuevo.tablero.getPieza((4, 3)) is None # Peón negro capturado en d5 vacío
    assert len(juego_nuevo.piezasCapturadas['blanco']) == 1 # Una pieza negra capturada por blancas
    assert isinstance(juego_nuevo.piezasCapturadas['blanco'][0], Peon)
    assert juego_nuevo.turno_actual == 'negro'
    assert juego_nuevo.tablero.objetivoPeonAlPaso is None # EP target se limpia

# --- Tests de Enroque ---
def test_enroque_corto_blanco_ok(juego_nuevo):
    """Verifica el enroque corto blanco legal."""
    # Quitar Alfil y Caballo blancos
    juego_nuevo.tablero.setPieza((0, 5), None) # Alfil f1
    juego_nuevo.tablero.setPieza((0, 6), None) # Caballo g1
    
    movs_legales = juego_nuevo.tablero.obtener_todos_movimientos_legales('blanco')
    enroque_corto_mov = ((0, 4), (0, 6)) # e1g1
    assert enroque_corto_mov in movs_legales
    
    # Realizar enroque
    assert juego_nuevo.realizarMovimiento((0, 4), (0, 6)) == True
    
    # Verificar posiciones finales
    assert isinstance(juego_nuevo.tablero.getPieza((0, 6)), Rey) # Rey en g1
    assert isinstance(juego_nuevo.tablero.getPieza((0, 5)), Torre) # Torre en f1
    assert juego_nuevo.tablero.getPieza((0, 4)) is None # e1 vacío
    assert juego_nuevo.tablero.getPieza((0, 7)) is None # h1 vacío
    assert juego_nuevo.tablero.derechosEnroque['blanco']['corto'] == False
    assert juego_nuevo.tablero.derechosEnroque['blanco']['largo'] == False
    assert juego_nuevo.turno_actual == 'negro'

def test_enroque_largo_negro_ok(juego_nuevo):
    """Verifica el enroque largo negro legal."""
    # Hacer un movimiento blanco primero
    juego_nuevo.realizarMovimiento((1, 0), (2, 0)) # a2-a3
    
    # Quitar Reina, Alfil y Caballo negros
    juego_nuevo.tablero.setPieza((7, 1), None) # Caballo b8
    juego_nuevo.tablero.setPieza((7, 2), None) # Alfil c8
    juego_nuevo.tablero.setPieza((7, 3), None) # Reina d8
    
    movs_legales = juego_nuevo.tablero.obtener_todos_movimientos_legales('negro')
    enroque_largo_mov = ((7, 4), (7, 2)) # e8c8
    assert enroque_largo_mov in movs_legales
    
    # Realizar enroque
    assert juego_nuevo.realizarMovimiento((7, 4), (7, 2)) == True
    
    # Verificar posiciones finales
    assert isinstance(juego_nuevo.tablero.getPieza((7, 2)), Rey) # Rey en c8
    assert isinstance(juego_nuevo.tablero.getPieza((7, 3)), Torre) # Torre en d8
    assert juego_nuevo.tablero.getPieza((7, 4)) is None # e8 vacío
    assert juego_nuevo.tablero.getPieza((7, 0)) is None # a8 vacío
    assert juego_nuevo.tablero.derechosEnroque['negro']['corto'] == False
    assert juego_nuevo.tablero.derechosEnroque['negro']['largo'] == False
    assert juego_nuevo.turno_actual == 'blanco'

def test_enroque_ilegal_rey_movido(juego_nuevo):
    """Verifica que no se puede enrocar si el rey se ha movido."""
    # Quitar piezas intermedias
    juego_nuevo.tablero.setPieza((0, 5), None) 
    juego_nuevo.tablero.setPieza((0, 6), None)
    # *** Añadido: Quitar peón en e2 para permitir Ke1-e2 ***
    juego_nuevo.tablero.setPieza((1, 4), None) # Peón e2
    
    # Mover rey blanco y volver
    assert juego_nuevo.realizarMovimiento((0, 4), (1, 4)) == True # Ke1-e2
    assert juego_nuevo.realizarMovimiento((6, 0), (5, 0)) == True # pa7-a6 (negro)
    assert juego_nuevo.realizarMovimiento((1, 4), (0, 4)) == True # Ke2-e1
    assert juego_nuevo.realizarMovimiento((5, 0), (4, 0)) == True # pa6-a5 (negro)

    # Verificar que el derecho de enroque se perdió
    assert juego_nuevo.tablero.derechosEnroque['blanco']['corto'] == False
    assert juego_nuevo.tablero.derechosEnroque['blanco']['largo'] == False

    # Intentar enrocar (no debería estar en legales)
    movs_legales = juego_nuevo.tablero.obtener_todos_movimientos_legales('blanco')
    enroque_corto_mov = ((0, 4), (0, 6))
    assert enroque_corto_mov not in movs_legales
    assert juego_nuevo.realizarMovimiento((0, 4), (0, 6)) == False # Intento directo falla

def test_enroque_ilegal_torre_movida(juego_nuevo):
    """Verifica que no se puede enrocar si la torre relevante se ha movido."""
    # Quitar piezas intermedias
    juego_nuevo.tablero.setPieza((0, 5), None) 
    juego_nuevo.tablero.setPieza((0, 6), None)
    # *** Añadido: Quitar peón en h2 para permitir Th1-h2 ***
    juego_nuevo.tablero.setPieza((1, 7), None) # Peón h2
    
    # Mover torre corta blanca y volver
    assert juego_nuevo.realizarMovimiento((0, 7), (1, 7)) == True # Th1-h2
    assert juego_nuevo.realizarMovimiento((6, 0), (5, 0)) == True # pa7-a6 (negro)
    assert juego_nuevo.realizarMovimiento((1, 7), (0, 7)) == True # Th2-h1
    assert juego_nuevo.realizarMovimiento((5, 0), (4, 0)) == True # pa6-a5 (negro)
    
    # Verificar que el derecho de enroque corto se perdió
    assert juego_nuevo.tablero.derechosEnroque['blanco']['corto'] == False
    assert juego_nuevo.tablero.derechosEnroque['blanco']['largo'] == True # Largo aún posible
    
    # Intentar enrocar corto (no debería estar en legales)
    movs_legales = juego_nuevo.tablero.obtener_todos_movimientos_legales('blanco')
    enroque_corto_mov = ((0, 4), (0, 6))
    assert enroque_corto_mov not in movs_legales
    assert juego_nuevo.realizarMovimiento((0, 4), (0, 6)) == False

def test_enroque_ilegal_camino_bloqueado(juego_nuevo):
    """Verifica que no se puede enrocar si el camino está bloqueado."""
    # Caballo blanco en g1 bloquea enroque corto
    assert juego_nuevo.tablero.getPieza((0, 6)) is not None 
    
    movs_legales = juego_nuevo.tablero.obtener_todos_movimientos_legales('blanco')
    enroque_corto_mov = ((0, 4), (0, 6))
    assert enroque_corto_mov not in movs_legales
    assert juego_nuevo.realizarMovimiento((0, 4), (0, 6)) == False

def test_enroque_ilegal_jaque_actual(juego_nuevo):
    """Verifica que no se puede enrocar si el rey está en jaque."""
    # Poner torre negra amenazando al rey blanco
    juego_nuevo.tablero.setPieza((4, 4), Torre('negro', (4, 4), juego_nuevo.tablero)) # Torre negra en e5
    # Quitar piezas intermedias blancas para enroque corto
    juego_nuevo.tablero.setPieza((0, 5), None) 
    juego_nuevo.tablero.setPieza((0, 6), None)
    # Quitar peón en e2 que bloquea el jaque
    juego_nuevo.tablero.setPieza((1, 4), None)
    
    # Debug: verificar si la torre negra en e5 realmente amenaza al rey blanco en e1
    rey_blanco_pos = (0, 4)  # e1
    torre_negra_pos = (4, 4)  # e5
    torre_negra = juego_nuevo.tablero.getPieza(torre_negra_pos)
    
    print(f"Torre negra en {torre_negra_pos}: {torre_negra}")
    print(f"Rey blanco en {rey_blanco_pos}: {juego_nuevo.tablero.getPieza(rey_blanco_pos)}")
    
    # Verificar si hay alguna pieza bloqueando el camino entre la torre y el rey
    bloqueo = False
    for fila in range(1, 4):  # Comprobar casillas e2, e3, e4
        pieza_intermedia = juego_nuevo.tablero.getPieza((fila, 4))
        if pieza_intermedia:
            bloqueo = True
            print(f"Pieza bloqueando en {(fila, 4)}: {pieza_intermedia}")
    
    print(f"¿Camino bloqueado entre torre y rey?: {bloqueo}")
    print(f"¿Rey en jaque según el método?: {juego_nuevo.estaEnJaque('blanco')}")
    print(f"¿Casilla amenazada directamente?: {juego_nuevo.tablero.esCasillaAmenazada(rey_blanco_pos, 'negro')}")
    
    # Actualizar estado del juego (debería detectar jaque)
    juego_nuevo._actualizarEstadoJuego() # Forzar actualización manual, normalmente se hace tras mover
    print(f"Estado del juego después de actualizar: {juego_nuevo.estado_juego}")
    
    assert juego_nuevo.estado_juego == 'jaque' 
    assert juego_nuevo.estaEnJaque('blanco') == True

    # Intentar enrocar (no debería estar en legales)
    movs_legales = juego_nuevo.tablero.obtener_todos_movimientos_legales('blanco')
    enroque_corto_mov = ((0, 4), (0, 6))
    print(f"Movimientos legales para blanco: {movs_legales}")
    print(f"¿Enroque corto entre movimientos legales?: {enroque_corto_mov in movs_legales}")
    
    assert enroque_corto_mov not in movs_legales
    assert juego_nuevo.realizarMovimiento((0, 4), (0, 6)) == False

def test_enroque_ilegal_paso_por_jaque(juego_nuevo):
    """Verifica que no se puede enrocar si el rey pasa por una casilla amenazada."""
    # Poner torre negra amenazando f1 (casilla de paso para O-O)
    juego_nuevo.tablero.setPieza((4, 5), Torre('negro', (4, 5), juego_nuevo.tablero)) # Torre negra en f5
    # Quitar piezas intermedias blancas para enroque corto
    juego_nuevo.tablero.setPieza((0, 5), None) 
    juego_nuevo.tablero.setPieza((0, 6), None)
    # Quitar peón en f2 que bloquea el ataque a f1
    juego_nuevo.tablero.setPieza((1, 5), None)
    
    # Debug: verificar si la torre negra en f5 realmente amenaza la casilla f1
    casilla_f1 = (0, 5)  # f1
    torre_negra_pos = (4, 5)  # f5
    torre_negra = juego_nuevo.tablero.getPieza(torre_negra_pos)
    
    print(f"Torre negra en {torre_negra_pos}: {torre_negra}")
    
    # Verificar si hay alguna pieza bloqueando el camino entre la torre y f1
    bloqueo = False
    for fila in range(1, 4):  # Comprobar casillas f2, f3, f4
        pieza_intermedia = juego_nuevo.tablero.getPieza((fila, 5))
        if pieza_intermedia:
            bloqueo = True
            print(f"Pieza bloqueando en {(fila, 5)}: {pieza_intermedia}")
    
    print(f"¿Camino bloqueado entre torre y f1?: {bloqueo}")
    print(f"¿Casilla f1 amenazada directamente?: {juego_nuevo.tablero.esCasillaAmenazada(casilla_f1, 'negro')}")

    # Intentar enrocar (no debería estar en legales)
    movs_legales = juego_nuevo.tablero.obtener_todos_movimientos_legales('blanco')
    enroque_corto_mov = ((0, 4), (0, 6))
    print(f"Movimientos legales para blanco: {movs_legales}")
    print(f"¿Enroque corto entre movimientos legales?: {enroque_corto_mov in movs_legales}")
    
    assert enroque_corto_mov not in movs_legales
    assert juego_nuevo.realizarMovimiento((0, 4), (0, 6)) == False


# ==================================================
# Tests de Estado del Juego (Migrados/Adaptados)
# ==================================================

def test_jaque(juego_nuevo):
    """Verifica la detección de jaque."""
    # Poner Dama blanca dando jaque al rey negro
    juego_nuevo.tablero.setPieza((3, 4), Reina('blanco', (3, 4), juego_nuevo.tablero)) # Dama en e4
    # Quitar peones que bloquean el jaque
    juego_nuevo.tablero.setPieza((6, 4), None) # Quitar peón negro en e7
    
    # Debug: verificar si la reina blanca en e4 realmente amenaza al rey negro en e8
    rey_negro_pos = (7, 4)  # e8
    reina_blanca_pos = (3, 4)  # e4
    reina_blanca = juego_nuevo.tablero.getPieza(reina_blanca_pos)
    
    print(f"Reina blanca en {reina_blanca_pos}: {reina_blanca}")
    print(f"Rey negro en {rey_negro_pos}: {juego_nuevo.tablero.getPieza(rey_negro_pos)}")
    
    # Verificar si hay alguna pieza bloqueando el camino entre la reina y el rey
    bloqueo = False
    for fila in range(4, 7):  # Comprobar casillas e5, e6, e7
        pieza_intermedia = juego_nuevo.tablero.getPieza((fila, 4))
        if pieza_intermedia:
            bloqueo = True
            print(f"Pieza bloqueando en {(fila, 4)}: {pieza_intermedia}")
    
    print(f"¿Camino bloqueado entre reina y rey?: {bloqueo}")
    print(f"¿Rey en jaque según el método?: {juego_nuevo.estaEnJaque('negro')}")
    print(f"¿Casilla amenazada directamente?: {juego_nuevo.tablero.esCasillaAmenazada(rey_negro_pos, 'blanco')}")
    
    # Mover un peón blanco para que sea turno de negras
    juego_nuevo.realizarMovimiento((1, 0), (2, 0)) # a2-a3
    
    # Verificar estado
    print(f"Estado del juego después de mover: {juego_nuevo.estado_juego}")
    print(f"¿Rey en jaque después de mover?: {juego_nuevo.estaEnJaque('negro')}")
    
    assert juego_nuevo.estado_juego == 'jaque'
    assert juego_nuevo.estaEnJaque('negro') == True
    assert juego_nuevo.estaEnJaque('blanco') == False

def test_jaque_mate(juego_nuevo):
    """Verifica la detección de jaque mate (Mate del Loco)."""
    # Mate del loco: 1. f3 e5 2. g4 Dh4#
    assert juego_nuevo.realizarMovimiento((1, 5), (2, 5)) == True # 1. f3
    assert juego_nuevo.realizarMovimiento((6, 4), (4, 4)) == True # 1... e5
    assert juego_nuevo.realizarMovimiento((1, 6), (3, 6)) == True # 2. g4
    assert juego_nuevo.realizarMovimiento((7, 3), (3, 7)) == True # 2... Dh4# (Dama negra a h4)
    
    # Verificar estado
    assert juego_nuevo.estado_juego == 'jaque_mate'
    assert juego_nuevo.estaEnJaque('blanco') == True
    assert juego_nuevo.turno_actual == 'blanco' # Turno cambió a blanco, pero no hay movimientos
    # Verificar que no hay movimientos legales para blancas
    assert not juego_nuevo.tablero.obtener_todos_movimientos_legales('blanco')

def test_ahogado(juego_nuevo):
    """Verifica la detección de tablas por ahogado."""
    # Configurar posición de ahogado: Rey negro en a8, Rey blanco en a6, Reina blanca en b6
    juego_nuevo.tablero.casillas = [[None for _ in range(8)] for _ in range(8)] # Limpiar
    rey_negro = Rey('negro', (7, 0), juego_nuevo.tablero) # Ka8
    rey_blanco = Rey('blanco', (5, 0), juego_nuevo.tablero) # Ka6
    reina_blanca = Reina('blanco', (5, 1), juego_nuevo.tablero) # Qb6
    juego_nuevo.tablero.setPieza((7, 0), rey_negro)
    juego_nuevo.tablero.setPieza((5, 0), rey_blanco)
    juego_nuevo.tablero.setPieza((5, 1), reina_blanca)
    juego_nuevo.turno_actual = 'negro' # Turno de negras
    
    # Actualizar estado (forzar, ya que no hubo movimiento previo)
    juego_nuevo._actualizarEstadoJuego()
    
    # Verificar estado
    assert juego_nuevo.estado_juego == 'tablas_ahogado'
    assert juego_nuevo.estaEnJaque('negro') == False
    assert juego_nuevo.turno_actual == 'negro' # Turno no cambia si no hay movimiento
    assert not juego_nuevo.tablero.obtener_todos_movimientos_legales('negro')


# ==================================================
# Tests de Deshacer Movimiento (Nuevos)
# ==================================================

def test_deshacer_movimiento_simple(juego_nuevo):
    """Deshace un movimiento simple de peón."""
    estado_inicial_fen = juego_nuevo._generarFenParcial()
    
    # Guardar estado inicial para comparación (copias superficiales ok para tipos inmutables)
    turno_inicial = juego_nuevo.turno_actual
    ply_inicial = juego_nuevo.contadorPly
    num_mov_inicial = juego_nuevo.numero_movimiento
    hist_pos_inicial_count = juego_nuevo.historial_posiciones.get(estado_inicial_fen, 0)

    # Realizar movimiento
    assert juego_nuevo.realizarMovimiento((1, 4), (3, 4)) == True # e4
    estado_despues_mov_fen = juego_nuevo._generarFenParcial()
    hist_pos_despues_mov_count = juego_nuevo.historial_posiciones.get(estado_despues_mov_fen, 0)

    # Deshacer movimiento
    assert juego_nuevo.deshacerUltimoMovimiento() == True
    estado_final_fen = juego_nuevo._generarFenParcial()

    # Verificar estado restaurado
    assert isinstance(juego_nuevo.tablero.getPieza((1, 4)), Peon)
    assert juego_nuevo.tablero.getPieza((3, 4)) is None
    assert juego_nuevo.turno_actual == turno_inicial
    assert juego_nuevo.contadorPly == ply_inicial
    assert juego_nuevo.numero_movimiento == num_mov_inicial
    assert juego_nuevo.tablero.objetivoPeonAlPaso is None # No debería haberse creado y persistido
    assert estado_final_fen == estado_inicial_fen
    assert juego_nuevo.historial_posiciones.get(estado_inicial_fen, 0) == hist_pos_inicial_count # Contador restaurado
    assert juego_nuevo.historial_posiciones.get(estado_despues_mov_fen) is None # FEN intermedio eliminado

def test_deshacer_captura(juego_nuevo):
    """Deshace una captura."""
    # Simplificar: Poner piezas para captura directa
    juego_nuevo.tablero.casillas = [[None for _ in range(8)] for _ in range(8)] # Limpiar
    alfil_blanco = Alfil('blanco', (3, 3), juego_nuevo.tablero) # Bd4
    caballo_negro = Caballo('negro', (4, 4), juego_nuevo.tablero) # Ne5
    rey_b = Rey('blanco', (0,0), juego_nuevo.tablero)
    rey_n = Rey('negro', (7,7), juego_nuevo.tablero)
    juego_nuevo.tablero.setPieza((3, 3), alfil_blanco)
    juego_nuevo.tablero.setPieza((4, 4), caballo_negro)
    juego_nuevo.tablero.setPieza((0, 0), rey_b)
    juego_nuevo.tablero.setPieza((7, 7), rey_n)
    juego_nuevo.turno_actual = 'blanco'
    juego_nuevo.historial_posiciones = defaultdict(int) # Resetear historial FEN
    juego_nuevo._registrarPosicionActual()
    estado_inicial_fen = juego_nuevo._generarFenParcial()

    # Realizar captura
    assert juego_nuevo.realizarMovimiento((3, 3), (4, 4)) == True # BxNe5
    assert len(juego_nuevo.piezasCapturadas['blanco']) == 1
    assert juego_nuevo.piezasCapturadas['blanco'][0] == caballo_negro

    # Deshacer captura
    assert juego_nuevo.deshacerUltimoMovimiento() == True

    # Verificar estado restaurado
    assert juego_nuevo.tablero.getPieza((3, 3)) == alfil_blanco
    assert juego_nuevo.tablero.getPieza((4, 4)) == caballo_negro
    assert len(juego_nuevo.piezasCapturadas['blanco']) == 0
    assert juego_nuevo.turno_actual == 'blanco'
    assert juego_nuevo._generarFenParcial() == estado_inicial_fen

def test_deshacer_enroque(juego_nuevo):
    """Deshace un enroque corto blanco."""
    juego_nuevo.tablero.setPieza((0, 5), None) 
    juego_nuevo.tablero.setPieza((0, 6), None)
    rey_inicial = juego_nuevo.tablero.getPieza((0, 4))
    torre_inicial = juego_nuevo.tablero.getPieza((0, 7))
    derechos_iniciales = juego_nuevo.tablero.derechosEnroque.copy()
    estado_inicial_fen = juego_nuevo._generarFenParcial()
    
    # Realizar enroque
    assert juego_nuevo.realizarMovimiento((0, 4), (0, 6)) == True
    assert juego_nuevo.tablero.derechosEnroque['blanco']['corto'] == False
    
    # Deshacer enroque
    assert juego_nuevo.deshacerUltimoMovimiento() == True
    
    # Verificar estado restaurado
    assert juego_nuevo.tablero.getPieza((0, 4)) == rey_inicial
    assert juego_nuevo.tablero.getPieza((0, 7)) == torre_inicial
    assert juego_nuevo.tablero.getPieza((0, 5)) is None
    assert juego_nuevo.tablero.getPieza((0, 6)) is None
    assert juego_nuevo.tablero.derechosEnroque['blanco']['corto'] == derechos_iniciales['blanco']['corto']
    assert juego_nuevo.tablero.derechosEnroque['blanco']['largo'] == derechos_iniciales['blanco']['largo']
    assert rey_inicial.se_ha_movido == False # Importante
    assert torre_inicial.se_ha_movido == False # Importante
    assert juego_nuevo.turno_actual == 'blanco'
    assert juego_nuevo._generarFenParcial() == estado_inicial_fen

def test_deshacer_promocion(juego_nuevo):
    """Deshace una promoción de peón."""
    juego_nuevo.tablero.casillas = [[None for _ in range(8)] for _ in range(8)] 
    peon_blanco = Peon('blanco', (6, 0), juego_nuevo.tablero)
    rey_n = Rey('negro', (7, 7), juego_nuevo.tablero)
    rey_b = Rey('blanco', (0,0), juego_nuevo.tablero)
    juego_nuevo.tablero.setPieza((6, 0), peon_blanco)
    juego_nuevo.tablero.setPieza((7, 7), rey_n)
    juego_nuevo.tablero.setPieza((0, 0), rey_b)
    juego_nuevo.turno_actual = 'blanco'
    juego_nuevo.historial_posiciones = defaultdict(int)
    juego_nuevo._registrarPosicionActual()
    estado_inicial_fen = juego_nuevo._generarFenParcial()

    # Realizar promoción a Reina
    assert juego_nuevo.realizarMovimiento((6, 0), (7, 0), promocion='Q') == True
    assert isinstance(juego_nuevo.tablero.getPieza((7, 0)), Reina)
    
    # Deshacer promoción
    assert juego_nuevo.deshacerUltimoMovimiento() == True
    
    # Verificar estado restaurado
    pieza_restaurada = juego_nuevo.tablero.getPieza((6, 0))
    assert isinstance(pieza_restaurada, Peon)
    assert pieza_restaurada.color == 'blanco'
    assert pieza_restaurada.posicion == (6, 0)
    assert juego_nuevo.tablero.getPieza((7, 0)) is None
    assert juego_nuevo.turno_actual == 'blanco'
    assert juego_nuevo._generarFenParcial() == estado_inicial_fen

def test_deshacer_en_passant(juego_nuevo):
    """Deshace una captura de peón al paso."""
    # 1. e4
    juego_nuevo.realizarMovimiento((1, 4), (3, 4))
    # 2. a6 (irrelevante)
    juego_nuevo.realizarMovimiento((6, 0), (5, 0))
    # 3. e5
    juego_nuevo.realizarMovimiento((3, 4), (4, 4))
    # 4. d5 (Crea objetivo EP en d6 (5,3))
    peon_negro_d7 = juego_nuevo.tablero.getPieza((6, 3))
    juego_nuevo.realizarMovimiento((6, 3), (4, 3))
    assert juego_nuevo.tablero.objetivoPeonAlPaso == (5, 3)
    objetivo_ep_antes_captura = juego_nuevo.tablero.objetivoPeonAlPaso
    turno_antes_captura = juego_nuevo.turno_actual
    capturadas_antes_count = len(juego_nuevo.piezasCapturadas['blanco'])
    fen_antes_captura = juego_nuevo._generarFenParcial()
    peon_blanco_captor = juego_nuevo.tablero.getPieza((4, 4))

    # 5. exd6 (Captura al paso)
    assert juego_nuevo.realizarMovimiento((4, 4), (5, 3)) == True
    assert juego_nuevo.tablero.getPieza((5, 3)) == peon_blanco_captor
    assert juego_nuevo.tablero.getPieza((4, 3)) is None # Peon negro capturado
    assert len(juego_nuevo.piezasCapturadas['blanco']) == capturadas_antes_count + 1
    assert juego_nuevo.tablero.objetivoPeonAlPaso is None

    # Deshacer captura al paso
    assert juego_nuevo.deshacerUltimoMovimiento() == True

    # Verificar estado restaurado
    assert juego_nuevo.tablero.getPieza((4, 4)) == peon_blanco_captor
    assert juego_nuevo.tablero.getPieza((5, 3)) is None
    pieza_negra_restaurada = juego_nuevo.tablero.getPieza((4, 3))
    assert isinstance(pieza_negra_restaurada, Peon) # Peón negro vuelve a d5
    assert pieza_negra_restaurada.color == 'negro'
    assert len(juego_nuevo.piezasCapturadas['blanco']) == capturadas_antes_count
    assert juego_nuevo.turno_actual == turno_antes_captura
    assert juego_nuevo.tablero.objetivoPeonAlPaso == objetivo_ep_antes_captura # Objetivo EP restaurado
    assert juego_nuevo._generarFenParcial() == fen_antes_captura

def test_deshacer_promocion_con_captura(juego_nuevo):
    """Deshace una promoción de peón que ocurrió con una captura."""
    juego_nuevo.tablero.casillas = [[None for _ in range(8)] for _ in range(8)]
    peon_blanco = Peon('blanco', (6, 6), juego_nuevo.tablero) # Peón blanco en g7
    torre_negra = Torre('negro', (7, 7), juego_nuevo.tablero) # Torre negra en h8
    rey_n = Rey('negro', (5, 5), juego_nuevo.tablero)
    rey_b = Rey('blanco', (0, 0), juego_nuevo.tablero)
    juego_nuevo.tablero.setPieza((6, 6), peon_blanco)
    juego_nuevo.tablero.setPieza((7, 7), torre_negra)
    juego_nuevo.tablero.setPieza((5, 5), rey_n)
    juego_nuevo.tablero.setPieza((0, 0), rey_b)
    juego_nuevo.turno_actual = 'blanco'
    juego_nuevo.historial_posiciones = defaultdict(int)
    juego_nuevo._registrarPosicionActual()
    estado_inicial_fen = juego_nuevo._generarFenParcial()
    capturadas_antes_count = len(juego_nuevo.piezasCapturadas['blanco'])

    # Realizar captura y promoción a Reina: gxh8=Q
    assert juego_nuevo.realizarMovimiento((6, 6), (7, 7), promocion='Q') == True
    pieza_promocionada = juego_nuevo.tablero.getPieza((7, 7))
    assert isinstance(pieza_promocionada, Reina)
    assert pieza_promocionada.color == 'blanco'
    assert len(juego_nuevo.piezasCapturadas['blanco']) == capturadas_antes_count + 1
    assert isinstance(juego_nuevo.piezasCapturadas['blanco'][0], Torre)

    # Deshacer promoción con captura
    assert juego_nuevo.deshacerUltimoMovimiento() == True

    # Verificar estado restaurado
    pieza_restaurada_peon = juego_nuevo.tablero.getPieza((6, 6))
    assert isinstance(pieza_restaurada_peon, Peon)
    assert pieza_restaurada_peon.color == 'blanco'
    assert pieza_restaurada_peon.posicion == (6, 6)
    pieza_restaurada_torre = juego_nuevo.tablero.getPieza((7, 7))
    assert isinstance(pieza_restaurada_torre, Torre)
    assert pieza_restaurada_torre.color == 'negro'
    assert len(juego_nuevo.piezasCapturadas['blanco']) == capturadas_antes_count
    assert juego_nuevo.turno_actual == 'blanco'
    assert juego_nuevo._generarFenParcial() == estado_inicial_fen

# ==================================================
# Tests de Fin de Juego (Draws)
# ==================================================

def test_juego_termina_tablas_50_movimientos(juego_nuevo):
    """Verifica que el juego termina en tablas por la regla de 50 movimientos."""
    # Configurar K vs K
    juego_nuevo.tablero.casillas = [[None for _ in range(8)] for _ in range(8)]
    rey_b = Rey('blanco', (0, 0), juego_nuevo.tablero) # Ka1
    rey_n = Rey('negro', (7, 7), juego_nuevo.tablero) # Kh8
    juego_nuevo.tablero.setPieza((0, 0), rey_b)
    juego_nuevo.tablero.setPieza((7, 7), rey_n)
    juego_nuevo.turno_actual = 'blanco'
    juego_nuevo.contadorRegla50Movimientos = 99 # A un semi-movimiento del límite

    # Mover rey blanco (movimiento 100 sin captura/peón)
    assert juego_nuevo.realizarMovimiento((0, 0), (0, 1)) == True # Kb1

    # Verificar que el estado del juego es tablas
    # El estado se actualiza después de que el movimiento se completa y el turno cambia
    assert juego_nuevo.contadorRegla50Movimientos == 100
    # La comprobación de estado final ocurre *antes* de cambiar el turno en _actualizarEstadoJuego
    # El estado final debería haberse detectado para el jugador cuyo turno acaba de terminar (blanco)
    # Pero el estado del JUEGO se establece independientemente del turno.
    assert juego_nuevo.estado_juego == 'tablas_50_movimientos' # O el string exacto usado

def test_juego_termina_tablas_triple_repeticion(juego_nuevo):
    """Verifica que el juego termina en tablas por triple repetición."""
    # Configuración: Reyes solos
    juego_nuevo.tablero.casillas = [[None for _ in range(8)] for _ in range(8)]
    rey_b = Rey('blanco', (0, 0), juego_nuevo.tablero) # Ka1
    rey_n = Rey('negro', (7, 7), juego_nuevo.tablero) # Kh8
    juego_nuevo.tablero.setPieza((0, 0), rey_b)
    juego_nuevo.tablero.setPieza((7, 7), rey_n)
    juego_nuevo.turno_actual = 'blanco'
    juego_nuevo.historial_posiciones.clear()
    juego_nuevo._registrarPosicionActual() # Registrar estado inicial

    # Secuencia para repetir estado inicial (Ka1, Kh8, turno blanco) 3 veces
    # Mov 1: Kb1 (W) -> Turn B
    juego_nuevo.realizarMovimiento((0, 0), (0, 1))
    # Mov 2: Kh7 (B) -> Turn W
    juego_nuevo.realizarMovimiento((7, 7), (7, 6))
    # Mov 3: Ka1 (W) -> Turn B (Estado inicial repetido 1 vez por blancas)
    juego_nuevo.realizarMovimiento((0, 1), (0, 0))
    # Mov 4: Kh8 (B) -> Turn W (Estado inicial POSICIÓN repetida 2 veces, turno W)
    juego_nuevo.realizarMovimiento((7, 6), (7, 7))
    # Mov 5: Kb1 (W) -> Turn B
    juego_nuevo.realizarMovimiento((0, 0), (0, 1))
    # Mov 6: Kh7 (B) -> Turn W
    juego_nuevo.realizarMovimiento((7, 7), (7, 6))
    # Mov 7: Ka1 (W) -> Turn B (Estado inicial repetido 2 vez por blancas)
    juego_nuevo.realizarMovimiento((0, 1), (0, 0))
    # Mov 8: Kh8 (B) -> Turn W (Estado inicial POSICIÓN repetida 3 veces, turno W)
    assert juego_nuevo.realizarMovimiento((7, 6), (7, 7)) == True

    # Verificar estado del juego después del movimiento que causa la 3ª repetición
    assert juego_nuevo.estado_juego == 'tablas_triple_repeticion' # O el string exacto

def test_juego_termina_tablas_material_insuficiente(juego_nuevo):
    """Verifica que el juego termina en tablas por material insuficiente."""
    # Configurar K+N vs K
    juego_nuevo.tablero.casillas = [[None for _ in range(8)] for _ in range(8)]
    rey_b = Rey('blanco', (0, 0), juego_nuevo.tablero)
    caballo_b = Caballo('blanco', (0, 1), juego_nuevo.tablero)
    rey_n = Rey('negro', (7, 7), juego_nuevo.tablero)
    juego_nuevo.tablero.setPieza((0, 0), rey_b)
    juego_nuevo.tablero.setPieza((0, 1), caballo_b)
    juego_nuevo.tablero.setPieza((7, 7), rey_n)
    juego_nuevo.turno_actual = 'negro' # Turno negro

    # Realizar cualquier movimiento legal (p.ej., mover rey negro)
    # El estado debería actualizarse *después* del movimiento
    assert juego_nuevo.realizarMovimiento((7, 7), (7, 6)) == True # Kh7

    # Verificar estado del juego
    assert juego_nuevo.estado_juego == 'tablas_material_insuficiente' # O el string exacto


# Puedes añadir más tests para deshacer EP, deshacer promoción con captura, etc.
# También tests para tablas por 50 movimientos y triple repetición.
