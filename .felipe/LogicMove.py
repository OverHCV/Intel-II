import serial
import time
from Tools import verificar_estado_terminal
from tabulate import tabulate
from SARSA_META import sarsaMeta, inicializar_Q

# Configuración del puerto serial
PORT = "COM4"  # Cambia esto según el puerto asignado al Bluetooth
BAUD_RATE = 115200  # Velocidad de comunicación

# Crear la conexión serial
try:
    bt_connection = serial.Serial(PORT, BAUD_RATE, timeout=1)
    print(f"Conectado al puerto {PORT}")
    time.sleep(2)  # Esperar a que el módulo Bluetooth esté listo
except Exception as e:
    print(f"Error al conectar con el puerto {PORT}: {e}")
    exit()


# Función para enviar un comando
def send_command(command):
    if bt_connection.is_open:
        bt_connection.write(command.encode("utf-8"))  # Enviar el comando como bytes
        print(f"Comando enviado: {command}")
        time.sleep(0.1)  # Pausa breve para evitar congestión
    else:
        print("La conexión serial no está abierta")


# Función para leer datos del Arduino
def read_from_arduino():
    if bt_connection.is_open and bt_connection.in_waiting > 0:
        data = bt_connection.readline().decode("utf-8").strip()
        return data
    return None


# Función para obtener la dirección basada en la tabla q y el estado actual
def obtener_direccion_mas_alta(estado, mapa, posicion_actual, Q):
    """
    Obtiene la dirección asociada con la acción de mayor valor para un estado dado en la tabla Q.
    También valida si el movimiento es posible según el mapa.

    Estado: (x, y, z), donde:
        - x: rol actual (0 = policía, 1 = ladrón)
        - y: índice de la casilla del policía
        - z: índice de la casilla del ladrón
    Mapa: Matriz que representa el entorno (0 = vacío, 1 = hueco, etc.).
    Posición actual: (fila, columna) del agente en el mapa.
    """
    # Obtener las políticas asociadas al estado
    politicas = Q.get(estado)
    print(f"Políticas para el estado {estado}: {politicas}")
    if not politicas:
        print(f"Estado no encontrado en la tabla Q: {estado}")
        return None  # Si no hay políticas para este estado, devolver None

    movimientos = {
        0: (-1, 0),  # Arriba
        1: (1, 0),  # Abajo
        2: (0, -1),  # Izquierda
        3: (0, 1),  # Derecha
    }

    fila_actual, columna_actual, angulo_actual = posicion_actual
    direcciones_ordenadas = sorted(
        enumerate(politicas), key=lambda x: x[1], reverse=True
    )  # Ordenar políticas por valor de mayor a menor

    for direccion_idx, _ in direcciones_ordenadas:
        movimiento = movimientos[direccion_idx]
        nueva_fila = fila_actual + movimiento[0]
        nueva_columna = columna_actual + movimiento[1]
        print(
            "Marlon ",
            direccion_idx,
            nueva_columna,
            nueva_fila,
            movimiento,
            fila_actual,
            columna_actual,
        )
        # Verificar si el movimiento es válido (dentro del mapa y no a un hueco)
        if 0 <= nueva_fila < mapa.shape[0] and 0 <= nueva_columna < mapa.shape[1]:
            if (
                mapa[nueva_fila, nueva_columna] == 0
            ):  # Supongamos que 0 es una casilla válida
                if direccion_idx == 0:
                    return "w"  # Arriba
                elif direccion_idx == 1:
                    return "s"  # Abajo
                elif direccion_idx == 2:
                    return "a"  # Izquierda
                elif direccion_idx == 3:
                    return "d"  # Derecha

    print("No se encontró una dirección válida basada en las políticas")
    return None


# Función para avanzar utilizando la política obtenida
# Función para calcular la diferencia mínima entre dos ángulos
def diferencia_angulo(angulo1, angulo2):
    """
    Calcula la diferencia mínima entre dos ángulos (en grados) considerando la periodicidad de 360°.
    """
    diferencia = abs(angulo1 - angulo2) % 360
    return min(diferencia, 360 - diferencia)


# Modificar avanzar_y_corregir
def avanzar_y_corregir(estado_actual, posicion_real, detected_shapes, Q, mapa):
    """
    Avanza y corrige el movimiento del robot según el estado actual y la política en la tabla Q.
    """
    # Obtener la política basada en el estado actual
    politica = obtener_direccion_mas_alta(estado_actual, mapa, posicion_real, Q)
    if not politica:
        print("No se encontró una política válida para el estado actual")
        return  # Devolver el estado y posición actual si no hay política

    print(f"Política seleccionada para el estado {estado_actual}: {politica}")

    # Movimiento asociado a cada política
    movimientos = {
        "w": (-1, 0, 90),  # Arriba
        "s": (1, 0, 270),  # Abajo
        "a": (0, -1, 180),  # Izquierda
        "d": (0, 1, 0),  # Derecha
    }

    movimiento = movimientos[politica]
    angulo_esperado = movimiento[2]

    # Verificar si el ángulo actual coincide con el esperado
    x_real, y_real, angulo_real = posicion_real
    tolerancia = 10  # Tolerancia en grados
    diferencia = diferencia_angulo(angulo_real, angulo_esperado)

    print("Valores ->", tolerancia, angulo_real, angulo_esperado, diferencia)
    if diferencia <= tolerancia:
        # Avanzar si el ángulo es correcto
        send_command("w")
        print("ENVIO W")
        time.sleep(0.5)  # Esperar al movimiento del robot
        return
    else:
        # Corregir el ángulo
        if (angulo_real - angulo_esperado) % 360 < 180:
            send_command("d")  # Girar a la derecha
            print("ENVIO D")
            return
        else:
            send_command("a")  # Girar a la izquierda
            print("ENVIO A")
            return


# Función para obtener la posición actual del robot
def obtener_posicion_actual(detected_shapes, cell_index):
    for shape in detected_shapes:
        if shape["cell_index"] == cell_index:
            return shape["x"], shape["y"], shape["angle"]
    # Devuelve una posición por defecto (0, 0, 0.0) si no se encuentra
    return 0, 0, 0.0


# Recorrer el mapa evitando huecos y siguiendo las políticas
def recorrer_mapa(mapa, detected_shapes, Q, estado_actual):
    recorrido = []
    # Suponemos que el estado inicial es (rol, índice policía, índice ladrón)
    for shape in detected_shapes:
        if shape["shape"] == "0":  # Procesar sólo las formas de tipo "circle"
            print("IN 3", estado_actual, shape)
            indice_agente = shape["cell_index"]
            posicion_real = (shape["row"], shape["col"], shape["angle"])

            print(f"Estado actual: {estado_actual}, Posición real: {posicion_real}")

            # Avanzar y corregir en función de la política
            avanzar_y_corregir(estado_actual, posicion_real, detected_shapes, Q, mapa)
            estado_actual = (indice_agente, estado_actual[1])
            print("ESTADO SIGUIENTE", estado_actual, posicion_real)
            # Leer respuesta del Arduino
            response = read_from_arduino()
            if response:
                print(f"Arduino dice: {response}")
                time.sleep(0.9)
                return estado_actual

    return estado_actual


def tablaQ(maze):
    n = 5
    nS = 25  # 5*5 -> 25 posibles estados
    nA = 4  # 4 acciones posibles: arriba, abajo, izquierda, derecha
    alpha = 0.6  # Tasa de aprendizaje
    gamma = 0.5  # Factor de descuento
    epsilon = 0.1  # Parámetro epsilon para el algoritmo e-greedy
    K = 4000  # Número de episodios
    agente_pos = (0, 0)
    meta_pos = (n - 1, n - 1)
    meta_indice = meta_pos[0] * n + meta_pos[1]
    # Inicialización de las tablas Q para el agente
    Q = inicializar_Q(nS, nA, meta_indice)
    retorno = []

    Q, retorno = sarsaMeta(maze, alpha, gamma, epsilon, nS, nA, K, Q)
    # Q, retorno = QLearning(mapa, alpha, gamma, epsilon, nS, nA, K, Q,1)
    print("Mapa", maze, agente_pos, meta_pos)
    time.sleep(0.5)
    table_Q = [(str(key), values) for key, values in Q.items()]

    print(tabulate(table_Q, headers=["Key", "Values"], tablefmt="grid"))
    print("RETORNOO", retorno)
    return Q
