# QLearning
from Tools import es_valida, mover_agente, calcular_recompensa, obtener_posiciones, verificar_estado_terminal

def QLearning(mapa, alpha, gamma, epsilon, nS, nA, K, Q, rol):
    '''
    Algoritmo Q-Learning con actualización basada en el valor máximo de Q en el estado siguiente.

    Parámetros:
    - mapa: representación del entorno
    - alpha: tasa de aprendizaje
    - gamma: factor de descuento
    - epsilon: parámetro e-greedy
    - nS, nA: número de estados y acciones
    - K: número de episodios
    - Q: tabla Q unificada
    - rol: rol actual (0 = policía, 1 = ladrón)

    Retorna:
    - Q: tabla Q actualizada
    - retorno_agente: lista con retorno acumulado por episodio
    '''
    retorno_agente = []
    accion_agente = 0
    pos_policia, pos_ladron = obtener_posiciones(mapa)

    for episodio in range(K):
        # Inicializar posiciones
        estado = (pos_policia, pos_ladron)
        retorno_acumulado = 0

        # Seleccionar acción inicial del rol actual
        if rol == 0:
            accion_agente = e_greedy((0, *estado), Q, epsilon, nA, mapa, pos_policia)
        else:
            accion_agente = e_greedy((1, *estado), Q, epsilon, nA, mapa, pos_ladron)

        done = False
        while not done:
            # Iterar sobre todos los estados del otro agente
            if rol == 0:  # Policía
                if es_valida(pos_policia, accion_agente) and pos_policia != pos_ladron:
                    nuevo_pos_agente = mover_agente(pos_policia, accion_agente, mapa)
                else:
                    nuevo_pos_agente = pos_policia
                pos_policia = nuevo_pos_agente
                nuevo_estado = (nuevo_pos_agente, pos_ladron)  # Combinar con estado del ladrón
                # Selección de la nueva acción basada en el valor máximo
                nueva_accion_agente = Q[(0, *nuevo_estado)].index(max(Q[(0, *nuevo_estado)]))
                print(f"nueva_accion_agente: {nueva_accion_agente} {nuevo_estado}")
                recompensa = calcular_recompensa(mapa, nuevo_pos_agente, pos_ladron, 0)
            else:  # Ladrón
                if es_valida(pos_ladron, accion_agente) and pos_policia != pos_ladron:
                    nuevo_pos_agente = mover_agente(pos_ladron, accion_agente, mapa)
                else:
                    nuevo_pos_agente = pos_ladron
                pos_ladron = nuevo_pos_agente
                nuevo_estado = (pos_policia, nuevo_pos_agente)  # Combinar con estado del policía
                # Selección de la nueva acción basada en el valor máximo
                nueva_accion_agente = Q[(1, *nuevo_estado)].index(max(Q[(1, *nuevo_estado)]))
                print(f"nueva_accion_agente: {nueva_accion_agente}")
                recompensa = calcular_recompensa(mapa, nuevo_pos_agente, pos_policia, 1)

            done = verificar_estado_terminal(nuevo_estado[0], nuevo_estado[1], mapa)

            # Actualización Q-Learning
            Q[(rol, *estado)][accion_agente] += alpha * (
                recompensa
                + (gamma * max(Q[(rol, *nuevo_estado)]))
                - Q[(rol, *estado)][accion_agente]
            )

            # Romper bucle si termina el episodio
            if done:
                Q[(rol, *estado)][accion_agente] += alpha * (
                    recompensa - Q[(rol, *estado)][accion_agente]
                )
                retorno_agente.append(retorno_acumulado)

            retorno_acumulado += recompensa
            estado = nuevo_estado
            accion_agente = nueva_accion_agente

            # Reiniciar posiciones para el siguiente episodio
            if pos_ladron == len(mapa) * len(mapa) - 1 and rol == 0:
                pos_ladron = 0
            elif pos_ladron < len(mapa) * len(mapa) - 1 and rol == 0:
                pos_ladron += 1
            elif pos_policia == len(mapa) * len(mapa) - 1 and rol == 1:
                pos_policia = 0
            elif pos_policia < len(mapa) * len(mapa) - 1 and rol == 1:
                pos_policia += 1

    return Q, retorno_agente
