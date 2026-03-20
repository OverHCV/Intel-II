# SARSA
import random
from Tools import verificar_estado_terminal, calcular_recompensa_meta, mover_agente, es_valida, obtener_posiciones

def inicializar_Q(nS, nA, meta_idx):
    """
    Inicializa una tabla Q unificada como un diccionario.
    Cada clave es una tupla (pos_pol, pos_meta, rol) y el valor es una lista de tamaño nA.

    Parámetros:
    - nS: número de posiciones posibles (n x n)
    - nA: número de acciones posibles

    Retorna:
    - Q: un diccionario con tuplas (pos_pol, pos_meta, rol) como claves y listas de tamaño nA como valores
    """
    Q = {}

    # Para cada combinación de estados y roles
    for pos_agente in range(nS):  # Todas las posiciones posibles del policía
        Q[(pos_agente, meta_idx)] = [1] * nA  # Valores iniciales de Q

    return Q


def es_posicion_visitada(pos, accion, posiciones_visitadas, mapa):
    """
    Verifica si la nueva posición después de realizar la acción ha sido visitada antes.
    """
    nuevo_pos = mover_agente(pos, accion, mapa)
    return nuevo_pos in posiciones_visitadas


def e_greedy(s, Q, epsilon, nA, mapa, pos_actual, posiciones_visitadas):
    """
    Selecciona una acción usando la política e-greedy con validación de acciones dentro del mapa
    y evitando moverse a posiciones ya visitadas.
    """

    acciones_validas = [a for a in range(nA) if
                        es_valida(pos_actual, a, mapa) and not es_posicion_visitada(pos_actual, a, posiciones_visitadas, mapa)]
    print(f"Acciones válidas: {acciones_validas, nA} --- {s} ..{ pos_actual}")
    print("Q", Q)
    if not acciones_validas:
        print(f"----gg----{random.randint(0, nA - 1)}")
        return random.randint(0, nA - 1)  # Fallback: acción aleatoria

    if random.uniform(0, 1) < epsilon:
        print(f"----ee----{random.choice(acciones_validas)}")
        return random.choice(acciones_validas)  # Exploración
    print(f"----qq----{max(acciones_validas, key=lambda a: Q[s][a])}")
    return max(acciones_validas, key=lambda a: Q[s][a])  # Explotación


def sarsaMeta(mapa, alpha, gamma, epsilon, nS, nA, K, Q):
    '''
    Algoritmo SARSA que evalúa todos los estados del otro agente según el rol actual.

    Parámetros:
    - mapa: representación del entorno
    - alpha: tasa de aprendizaje
    - gamma: factor de descuento
    - epsilon: parámetro e-greedy
    - nS, nA: número de estados y acciones
    - K: número de episodios
    - Q: tabla Q unificada

    Retorna:
    - Q: tabla Q actualizada
    - retorno_agente: lista con retorno acumulado por episodio
    '''
    retorno_agente = []
    accion_agente = 0

    # posiciones_visitadas = set()  # Inicializamos el conjunto de posiciones visitadas

    for episodio in range(K):
        # Inicializar posiciones
        pos_agente, pos_meta = obtener_posiciones(mapa)
        print(f"pos_agente: {pos_agente} pos_meta: {pos_meta}")
        estado = (pos_agente, pos_meta)
        retorno_acumulado = 0
        posiciones_visitadas = set()

        # Selección de acción utilizando e-greedy
        accion_agente = e_greedy(estado, Q, epsilon, nA, mapa, pos_agente, posiciones_visitadas)

        done = False
        while not done:
            # Iterar sobre todos los estados del otro agente
            if es_valida(pos_agente, accion_agente, mapa) and pos_agente != pos_meta:
                nuevo_pos_agente = mover_agente(pos_agente, accion_agente, mapa)
            else:
                nuevo_pos_agente = pos_agente

            # Verificamos si el agente se mueve a una posición no visitada
            if nuevo_pos_agente not in posiciones_visitadas:
                posiciones_visitadas.add(nuevo_pos_agente)

            nuevo_estado = (nuevo_pos_agente, pos_meta)  # Combina con estado del otro agente
            print("nes",nuevo_estado)
            nueva_accion_agente = e_greedy(nuevo_estado, Q, epsilon, nA, mapa, nuevo_pos_agente, posiciones_visitadas)

            # Calcular la recompensa
            recompensa = calcular_recompensa_meta(mapa, nuevo_pos_agente, pos_meta)

            # Verificar si el episodio ha terminado
            done = verificar_estado_terminal(nuevo_estado[0], nuevo_estado[1], mapa)

            print(f"nuevo_estado ACTUAL----------------{nueva_accion_agente}----: {nuevo_estado} --- {recompensa}")

            # Actualización SARSA
            print("**************************************")
            print(f"estado {estado} --- nuevo {nuevo_estado}")
            print(f"Q[(rol, *estado)]: {estado}")
            print(f"Q[(rol, *estado)]: {Q[estado]}")
            print(f"accion {accion_agente}")
            print(f"nueva accion {nueva_accion_agente}")
            print(f"Q[(rol, *nuevo_estado)]: {Q[nuevo_estado]}")
            print(f"Q[(rol, *estado)][accion_agente]: {Q[estado][accion_agente]}")
            print(f"Q[(rol, *nuevo_estado)][nueva_accion_agente]: {Q[nuevo_estado][nueva_accion_agente]}")
            print(f"alpha: {alpha}")
            print(f"gamma: {gamma}")
            print(f"recompensa: {recompensa}")
            print("resultado", alpha * (
                    recompensa
                    + (gamma * Q[nuevo_estado][nueva_accion_agente])
                    - Q[estado][accion_agente]
            ))

            Q[estado][accion_agente] += alpha * (
                    recompensa
                    + (gamma * Q[nuevo_estado][nueva_accion_agente])
                    - Q[estado][accion_agente]
            )

            # Romper bucle si termina el episodio
            if done:
                print("SALE EVALUACION")
                Q[estado][accion_agente] += alpha * (
                        recompensa - Q[estado][accion_agente]
                )
                retorno_agente.append(retorno_acumulado)
                print(f"Actualizacion tabla {Q}")

            retorno_acumulado += recompensa
            estado = nuevo_estado
            pos_agente = nuevo_pos_agente
            accion_agente = nueva_accion_agente

    return Q, retorno_agente



