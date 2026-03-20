import numpy as np
import matplotlib.pyplot as plt
import copy


agente_pos = (0, 0)
meta_pos = (4, 4)

def inicializar_mapa(n):
    """
    Genera un laberinto de tamaño n*n utilizando el algoritmo de backtracking recursivo.
    Las celdas con '0' representan caminos, y las celdas con '1' son paredes.
    Además, garantiza que haya un camino entre la posición (0, 0) y (n-1, n-1).
    """
    # Crear una matriz de n*n llena de paredes
    mapa = np.ones((n, n), dtype=int)

    # Función recursiva para generar el laberinto
    def backtrack(x, y):
        # Direcciones posibles de movimiento (arriba, abajo, izquierda, derecha)
        direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(direcciones)  # Aleatoriza el orden de las direcciones

        # Marcar la celda actual como un pasaje
        mapa[x, y] = 0

        # Probar las direcciones
        for dx, dy in direcciones:
            nx, ny = x + dx * 2, y + dy * 2  # Saltar 2 celdas para asegurar que el camino se dibuje
            if 0 <= nx < n and 0 <= ny < n and mapa[nx, ny] == 1:
                # Crear un camino entre la celda actual y la nueva celda
                mapa[x + dx, y + dy] = 0
                backtrack(nx, ny)

    # Iniciar el backtracking desde la celda (1, 1)
    backtrack(0, 0)

    # Asegurarse de que haya un camino desde (0, 0) hasta (n-1, n-1)
    if mapa[n-1, n-1] == 1:
        # Si la meta está bloqueada, aseguramos un camino directo
        mapa[n-2, n-1] = 0
        mapa[n-1, n-2] = 0

    return mapa, agente_pos, meta_pos


def mostrar_estado(mapa, policia_pos, ladron_pos):
    """
    Muestra el estado actual del mapa con el policía y el ladrón.
    """
    n = mapa.shape[0]
    for i in range(n):
        row = ""
        for j in range(n):
            if (i, j) == policia_pos:
                row += " P "  # Policía
            elif (i, j) == ladron_pos:
                row += " L "  # Ladrón
            elif mapa[i, j] == 1:
                row += " X "  # Hueco
            else:
                row += " . "  # Espacio vacío
        print(row)
    print()

def mover_agente(idx, accion, mapa):
    """
    Mueve al agente según la acción seleccionada, donde `idx` es el índice de la casilla actual.
    Las acciones posibles son:
    0: Arriba, 1: Abajo, 2: Izquierda, 3: Derecha.
    """
    n, m = mapa.shape  # n = filas, m = columnas
    movimientos = {
        0: -m,  # Arriba: restar el número de columnas
        1: m,   # Abajo: sumar el número de columnas
        2: -1,  # Izquierda: restar 1
        3: 1    # Derecha: sumar 1
    }

    # Calcular la nueva posición
    nuevo_idx = idx + movimientos[accion]
    fila_actual, col_actual = idx // m, idx % m  # Posición actual (fila, columna)
    nueva_fila, nueva_col = nuevo_idx // m, nuevo_idx % m  # Nueva posición (fila, columna)
    # Restricciones para evitar salir del mapa
    if accion == 2 and col_actual == 0:  # Izquierda en la primera columna
        return idx  # Movimiento inválido
    if accion == 3 and col_actual == m - 1:  # Derecha en la última columna
        return idx  # Movimiento inválido
    if accion == 0 and fila_actual == 0:  # Arriba en la primera fila
        return idx  # Movimiento inválido
    if accion == 1 and fila_actual == n - 1:  # Abajo en la última fila
        return idx  # Movimiento inválido

    # Verificar si el índice está fuera de los límites (por seguridad)
    if nuevo_idx < 0 or nuevo_idx >= n * m:
        print("Movimiento fuera de los límites del mapa", idx)
        return idx
    print("Movimiento válido", nuevo_idx)
    return nuevo_idx  # Movimiento válido


def es_valida(pos, accion):
        print(pos,accion,"ES VALIDO?")
        nuevo_pos = mover_agente(pos, accion, mapa)
        if nuevo_pos == pos:
            return False
        filas, cols = len(mapa), len(mapa[0])

        i, j = nuevo_pos // mapa.shape[0], nuevo_pos % mapa.shape[0]
        nuevo_pos = (i, j)
        return 0 <= nuevo_pos[0] < filas and 0 <= nuevo_pos[1] < cols


def calcular_recompensa(mapa, agente_idx, otro_idx):
    print(f" RECOM {agente_idx} ---- {otro_idx}")
    """
    Calcula la recompensa según las reglas usando índices planos:
    - Policía: +10 por capturar, -10 por hueco, -1 por moverse.
    - Ladrón: -20 por ser capturado, -10 por hueco, +1 por moverse.
    """
    i, j = agente_idx // mapa.shape[0], agente_idx % mapa.shape[0]  # Convertir índice plano a coordenadas
    if mapa[i, j] == 1:  # Si cae en un hueco
        return -10
    if agente_idx == otro_idx:  # Si llega a la meta
        return 20
    else:
        return 1

# Función para obtener las posiciones del policía y del ladrón
def obtener_posiciones(mapa):
    n = mapa.shape[0]
    agente_idx = agente_pos[0] * n + agente_pos[1]  # Convertir a índice plano
    meta_idx = meta_pos[0] * n + meta_pos[1]  # Convertir a índice plano


    return agente_idx, meta_idx


def verificar_estado_terminal(s_agente_idx, s_meta_idx, mapa):
    """
    Verifica si el episodio ha terminado usando índices planos.
    """
    # Verificar si el policía y el ladrón están en la misma casilla
    if s_agente_idx == s_meta_idx:
        return True

    # Verificar si el policía o el ladrón caen en un hueco
    i, j = s_agente_idx // mapa.shape[0], s_agente_idx % mapa.shape[0]
    if mapa[i, j] == 1:  # Policía cae en un hueco
        return True

    return False


