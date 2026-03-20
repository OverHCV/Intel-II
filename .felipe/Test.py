from tabulate import tabulate
from Tools import inicializar_mapa
from SARSA import inicializar_Q, sarsa
import time
from QLearning import QLearning
# Definimos los parámetros de SARSA
#nS = 9  # 3x3 mapa -> 9 posibles estados (uno por cada casilla)

"""
SARSA HIPERPARAMETROS
ns = 5 # 5*5 -> 25 posibles estados
nA = 4   # 4 acciones posibles: arriba, abajo, izquierda, derecha
alpha = 0.4  # Tasa de aprendizaje
gamma = 0.999  # Factor de descuento
epsilon = 0.1  # Parámetro epsilon para el algoritmo e-greedy
K = 4000  # Número de episodios
"""

"""
QLEARNING HIPERPARAMETROS
"""
nS = 25 # 5*5 -> 25 posibles estados
nA = 4   # 4 acciones posibles: arriba, abajo, izquierda, derecha
alpha = 0.6  # Tasa de aprendizaje
gamma = 0.999  # Factor de descuento
epsilon = 0.1  # Parámetro epsilon para el algoritmo e-greedy
K = 4000  # Número de episodios
mapa, policia_pos, ladron_pos = inicializar_mapa(5)

# Inicialización de las tablas Q para ambos agentes
Q = inicializar_Q(nS, nA)
Q_ladron = inicializar_Q(nS, nA)
retorno = []
# Ejecutar SARSA para el policía
#Q_policia,Q_ladron, retorno = sarsa(mapa, alpha, gamma, epsilon, nS, nA, K, Q_policia, Q_ladron)

# Ejecutar SARSA para el ladrón
inicio = time.time()
Q, retorno = sarsa(mapa, alpha, gamma, epsilon, nS, nA, K, Q,0)
Q, retorno = sarsa(mapa, alpha, gamma, epsilon, nS, nA, K, Q,1)
final = time.time()
print(f"Tiempo de ejecución: {final - inicio:.5f} segundos")
#Q, retorno = QLearning(mapa, alpha, gamma, epsilon, nS, nA, K, Q,1)
#print("MApa", mapa, policia_pos, ladron_pos)
table_Q = [(str(key), values) for key, values in Q.items()]

# Imprimir la tabla
print("mapa",mapa)
print("POLICIA\n",tabulate(table_Q, headers=["Key", "Values"], tablefmt="grid"))
print("RETORNOO",retorno)

