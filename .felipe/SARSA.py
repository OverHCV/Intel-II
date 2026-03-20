#SARSA
import random
from Tools import es_valida, mover_agente, calcular_recompensa, obtener_posiciones, verificar_estado_terminal

def inicializar_Q(nS, nA):
    """
    Inicializa una tabla Q unificada como un diccionario.
    Cada clave es una tupla (pos_pol, pos_ladron, rol) y el valor es una lista de tamaño nA.

    Parámetros:
    - nS: número de posiciones posibles (n x n)
    - nA: número de acciones posibles

    Retorna:
    - Q: un diccionario con tuplas (pos_pol, pos_ladron, rol) como claves y listas de tamaño nA como valores
    """
    Q = {}

    # Para cada combinación de estados y roles
    for rol in [0, 1]:  # 0 = policía, 1 = ladrón
      for pos_pol in range(nS):  # Todas las posiciones posibles del policía
          for pos_ladron in range(nS):  # Todas las posiciones posibles del ladrón
              Q[(rol, pos_pol, pos_ladron)] = [1] * nA  # Valores iniciales de Q

    return Q



def e_greedy(s, Q, epsilon, nA, mapa, pos_actual):
    """
    Selecciona una acción usando la política e-greedy con validación de acciones dentro del mapa.
    """


    acciones_validas = [a for a in range(nA) if es_valida(pos_actual, a, mapa)]
    print(f"Acciones_validas: {acciones_validas, nA} --- {s,pos_actual}")
    if not acciones_validas:
        print(f"----gg----{random.randint(0, nA - 1)}")
        return random.randint(0, nA - 1)  # Fallback: acción aleatoria

    if random.uniform(0, 1) < epsilon:
        print(f"----ee----{random.choice(acciones_validas)}")
        return random.choice(acciones_validas)  # Exploración
    print(f"----qq----{max(acciones_validas, key=lambda a: Q[s][a])}")
    return max(acciones_validas, key=lambda a: Q[s][a])  # Explotación



def sarsa(mapa, alpha, gamma, epsilon, nS, nA, K, Q, rol):
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
    - rol: rol actual (0 = policía, 1 = ladrón)

    Retorna:
    - Q: tabla Q actualizada
    - retorno_agente: lista con retorno acumulado por episodio
    '''
    retorno_agente = []
    accion_agente = 0
    pos_policia, pos_ladron = obtener_posiciones(mapa)
    print("afuera")
    for episodio in range(K):
      print("ADentro")
      # Inicializar posiciones

      print(f"pos_policia ----: {pos_policia} pos_ladron: {pos_ladron}")
      estado = (pos_policia, pos_ladron)
      retorno_acumulado = 0



      # Seleccionar acción inicial del rol actual

      if rol == 0:
          print("POLICIA")
          accion_agente = e_greedy((0, *estado), Q, epsilon, nA, mapa, pos_policia)
      else:
          print("LADRON")
          accion_agente = e_greedy((1, *estado), Q, epsilon, nA, mapa, pos_ladron)

      done = False
      while not done:

          # Iterar sobre todos los estados del otro agente
          if rol == 0:  # Policía
              if es_valida(pos_policia, accion_agente, mapa) and pos_policia != pos_ladron:
                  nuevo_pos_agente = mover_agente(pos_policia, accion_agente, mapa)
              else:
                  nuevo_pos_agente = pos_policia
              pos_policia = nuevo_pos_agente
              nuevo_estado = (nuevo_pos_agente, pos_ladron)  # Combinar con estado del ladrón
              nueva_accion_agente = e_greedy((0, *nuevo_estado), Q, epsilon, nA, mapa, nuevo_pos_agente)
              recompensa = calcular_recompensa(mapa, nuevo_pos_agente, pos_ladron, 0)
              #print(f"nuevo_estado ACTUAL----------------{nueva_accion_agente}----: {nuevo_estado} --- {recompensa}")
          else:  # Ladrón
              print(f"WH LADRON", accion_agente, estado,es_valida(pos_ladron, accion_agente, mapa))
              if es_valida(pos_ladron, accion_agente, mapa) and pos_policia != pos_ladron:
                nuevo_pos_agente = mover_agente(pos_ladron, accion_agente, mapa)
              else:
                nuevo_pos_agente = pos_ladron
              pos_ladron = nuevo_pos_agente
              nuevo_estado = (pos_policia, nuevo_pos_agente)  # Combinar con estado del policía
              nueva_accion_agente = e_greedy((1, *nuevo_estado), Q, epsilon, nA, mapa, nuevo_pos_agente)
              recompensa = calcular_recompensa(mapa, nuevo_pos_agente, pos_policia, 1)
          done = verificar_estado_terminal(nuevo_estado[0], nuevo_estado[1], mapa)

          print(f"nuevo_estado ACTUAL----------------{nueva_accion_agente}----: {nuevo_estado} --- {recompensa}")
          # Calcular recompensa
          print("DONE", done)
          # Actualización SARSA
          print("**************************************")
          print(f"estado {estado} --- nuevo {nuevo_estado}")
          print(f"Q[(rol, *estado)]: {(rol, *estado)}")
          print(f"Q[(rol, *estado)]: {Q[(rol, *estado)]}")
          print(f"accion {accion_agente}")
          print(f"nueva accion {nueva_accion_agente}")
          print(f"Q[(rol, *nuevo_estado)]: {Q[(rol, *nuevo_estado)]}")
          print(f"Q[(rol, *estado)][accion_agente]: {Q[(rol, *estado)][accion_agente]}")
          print(f"Q[(rol, *nuevo_estado)][nueva_accion_agente]: {Q[(rol, *nuevo_estado)][nueva_accion_agente]}")
          print(f"alpha: {alpha}")
          print(f"gamma: {gamma}")
          print(f"recompensa: {recompensa}")
          print("resultado", alpha * (
              recompensa
              + (gamma * Q[(rol, *nuevo_estado)][nueva_accion_agente])
              - Q[(rol, *estado)][accion_agente]
          ))

          Q[(rol, *estado)][accion_agente] += alpha * (
            recompensa
            + (gamma * Q[(rol, *nuevo_estado)][nueva_accion_agente])
            - Q[(rol, *estado)][accion_agente]
          )
          # Romper bucle si termina el episodio
          if done:
              print("SALE EVALUACION")
              Q[(rol, *estado)][accion_agente] += alpha * (
                recompensa - Q[(rol, *estado)][accion_agente]
            )
              retorno_agente.append(retorno_acumulado)
              print(f"Actualizacion tabla {Q}")
          retorno_acumulado += recompensa

              # Verificar estado terminal
          estado = nuevo_estado
          accion_agente = nueva_accion_agente

          if pos_ladron == len(mapa) * len(mapa) - 1 and rol == 0:
              pos_ladron = 0
          elif pos_ladron < len(mapa) * len(mapa) - 1 and rol == 0:
              pos_ladron = pos_ladron + 1
          elif pos_policia == len(mapa) * len(mapa) - 1 and rol == 1:
              pos_policia = 0
          elif pos_policia < len(mapa) *  len(mapa) - 1 and rol == 1:
              pos_policia = pos_policia + 1
          # Actualizar estado y acción
    return Q, retorno_agente


