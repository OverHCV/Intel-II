import numpy as np
import copy


policia_pos = (0, 0)
ladron_pos = (4, 4)

# Configuración del mapa
def inicializar_mapa(n):
    """
    Crea un mapa de tamaño n*n con huecos aleatorios, un policía y un ladrón.
    """
    mapa = np.zeros((n, n), dtype=int)
    huecos = 4  # Elegir n huecos aleatorios

    # Colocar huecos en posiciones aleatorias
    for _ in range(huecos):
        while True:
            fila = np.random.randint(0, n)
            columna = np.random.randint(0, n)
            if mapa[fila, columna] == 0:  # Verificar que la posición esté vacía
                mapa[fila, columna] = 1
                break

    return mapa, policia_pos, ladron_pos



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


def es_valida(pos, accion, mapa):
        print(pos,accion,"ES VALIDO?")
        nuevo_pos = mover_agente(pos, accion, mapa)
        if nuevo_pos == pos:
            return False
        filas, cols = len(mapa), len(mapa[0])

        i, j = nuevo_pos // mapa.shape[0], nuevo_pos % mapa.shape[0]
        nuevo_pos = (i, j)
        return 0 <= nuevo_pos[0] < filas and 0 <= nuevo_pos[1] < cols


def calcular_recompensa(mapa, agente_idx, otro_idx, rol):
    print(f" RECOM {agente_idx} ---- {otro_idx} --- rol {rol}")
    """
    Calcula la recompensa según las reglas usando índices planos:
    - Policía: +10 por capturar, -10 por hueco, -1 por moverse.
    - Ladrón: -20 por ser capturado, -10 por hueco, +1 por moverse.
    """
    i, j = agente_idx // mapa.shape[0], agente_idx % mapa.shape[0]  # Convertir índice plano a coordenadas
    if mapa[i, j] == 1:  # Si cae en un hueco
        return -10
    elif agente_idx == otro_idx:  # Si captura o es capturado
        if rol == 0:
            return 20
        else:
            return -10
    else:
        if rol == 0:
            return 0
        else:
            return 1

def calcular_recompensa_meta(mapa, agente_idx, otro_idx):
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
    print("HELLOOO")
    n = mapa.shape[0]
    print("NNNN", n, type(n))
    policia_idx = policia_pos[0] * n + policia_pos[1]  # Convertir a índice plano
    ladron_idx = ladron_pos[0] * n + ladron_pos[1]  # Convertir a índice plano


    return policia_idx, ladron_idx


def verificar_estado_terminal(s_policia_idx, s_ladron_idx, mapa):
    """
    Verifica si el episodio ha terminado usando índices planos.
    """
    # Verificar si el policía y el ladrón están en la misma casilla
    if s_policia_idx == s_ladron_idx:
        return True

    # Verificar si el policía o el ladrón caen en un hueco
    i, j = s_policia_idx // mapa.shape[0], s_policia_idx % mapa.shape[0]
    if mapa[i, j] == 1:  # Policía cae en un hueco
        return True

    i, j = s_ladron_idx // mapa.shape[0], s_ladron_idx % mapa.shape[0]

    if mapa[i, j] == 1:  # Ladrón cae en un hueco
        return True

    return False


