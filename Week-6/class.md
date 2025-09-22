# Máquinas de Vectores de Soporte (SVM) y Funciones Kernel

## 1. Mapeo a Espacios de Mayor Dimensión

### Concepto de Mapeo $\phi$
El operador $\phi$ es una **función de mapeo** que transforma datos de un espacio de entrada a un espacio de mayor dimensión (espacio de características). Esto permite que datos que no son linealmente separables en el espacio original se vuelvan linealmente separables en el espacio transformado.

### Ejemplo: Mapeo Polinomial de Grado 2
Para vectores de entrada de 2 dimensiones:
$$
x = [x_1, x_2] \\
y = [y_1, y_2]
$$

El mapeo $\phi$ genera todos los **monomios de grado 2** (combinaciones de productos):
$$
\phi(x) = [x_1^2, x_2^2, \sqrt{2}x_1x_2] \\
\phi(y) = [y_1^2, y_2^2, \sqrt{2}y_1y_2]
$$

> **Nota importante**: El factor $\sqrt{2}$ en el tercer término es crucial para que el kernel funcione correctamente.

## 2. Productos Punto y el Teorema del Binomio

### Producto Punto en el Espacio Original
$$
x^T y = [x_1, x_2] \begin{bmatrix} y_1 \\ y_2 \end{bmatrix} = x_1y_1 + x_2y_2
$$

### Producto Punto en el Espacio Transformado
$$
\phi(x)^T \phi(y) = [x_1^2, x_2^2, \sqrt{2}x_1x_2] \begin{bmatrix} y_1^2 \\ y_2^2 \\ \sqrt{2}y_1y_2 \end{bmatrix}
$$

$$
= x_1^2y_1^2 + x_2^2y_2^2 + 2x_1x_2y_1y_2
$$

### Conexión con el Teorema del Binomio
El resultado anterior es exactamente:
$$
(x_1y_1 + x_2y_2)^2 = (x^T y)^2
$$

Esto demuestra que el producto punto en el espacio transformado es igual al **cuadrado del producto punto** en el espacio original.

## 3. Funciones Kernel: El Truco Computacional

### Definición de Función Kernel
Una **función kernel** $K(x, y)$ es una función que calcula el producto punto en un espacio de mayor dimensión **sin calcular explícitamente el mapeo** $\phi$.

### Ventaja Computacional
- **Camino largo**: Mapear todos los datos → Crear SVM → Clasificar
  - En el dataset Iris: 150 puntos de 4 dimensiones → 150 puntos de ~10 dimensiones
  - Costo computacional: O(n²d) donde d es la dimensión del espacio transformado

- **Camino corto**: Aplicar función kernel directamente
  - Reemplaza productos punto $\phi(x)^T\phi(y)$ por $K(x,y)$
  - Costo computacional: O(n²) independiente de la dimensión del espacio transformado

### Kernel Polinomial de Grado 2
$$
K(x, y) = (x^T y)^2
$$

Esta función kernel es **matemáticamente equivalente** a mapear los datos y calcular el producto punto, pero mucho más eficiente.

## 4. Tipos de Funciones Kernel Más Usadas

### 1. Kernel Polinomial
$$
K(x, y) = (x^T y + c)^d
$$
- **Parámetros**: $c$ (término constante), $d$ (grado del polinomio)
- **Uso**: Captura interacciones polinomiales entre características

### 2. Kernel de Función de Base Radial (RBF/Gaussiano)
$$
K(x, y) = e^{-\frac{||x - y||^2}{2\sigma^2}}
$$
- **Parámetros**: $\sigma$ (ancho del kernel)
- **Uso**: Captura similitudes locales, muy flexible
- **Interpretación**: $\sigma$ controla qué tan "local" es la influencia

### 3. Kernel Sigmoide
$$
K(x, y) = \tanh(\alpha x^T y + c)
$$
- **Parámetros**: $\alpha$ (escala), $c$ (sesgo)
- **Uso**: Similar a redes neuronales de una capa

## 5. Selección de Parámetros

### Parámetro $\sigma$ en RBF
- **$\sigma$ pequeño**: Kernel muy "puntiagudo", sobreajuste
- **$\sigma$ grande**: Kernel muy "suave", subajuste
- **Métodos de selección**:
  - Validación cruzada
  - Grid search
  - Optimización bayesiana

## 6. Espacios de Dimensión Infinita

### Analogía con Series de Taylor
Así como la función exponencial $e^x$ requiere **infinitos términos** en su serie de Taylor:
$$
e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots
$$

Los kernels pueden mapear a espacios de **dimensión infinita**. Por ejemplo:
- El kernel RBF mapea a un espacio de dimensión infinita
- Esto permite capturar patrones muy complejos sin aumentar la complejidad computacional

### Implicaciones
- **Capacidad de modelado**: Puede aproximar cualquier función continua
- **Eficiencia**: No necesitamos calcular explícitamente las infinitas dimensiones
- **Regularización**: Necesaria para evitar sobreajuste

## 7. Kernels Profundos vs. Kernels Tradicionales

### Kernels Tradicionales
- Fijos, diseñados manualmente
- Ejemplos: RBF, polinomial, sigmoide
- Interpretables pero limitados

### Kernels Profundos
- Aprendidos automáticamente
- Pueden adaptarse a la estructura de los datos
- Más flexibles pero menos interpretables
- Conexión con redes neuronales profundas

## Conceptos Clave para Recordar

1. **Mapeo $\phi$**: Transforma datos a espacios de mayor dimensión
2. **Función Kernel**: Calcula productos punto sin mapeo explícito
3. **Ventaja computacional**: O(n²) vs O(n²d)
4. **Teorema del binomio**: Conecta productos punto originales y transformados
5. **Parámetros críticos**: $\sigma$ en RBF, $d$ en polinomial
6. **Dimensión infinita**: Posible con kernels apropiados
7. **Selección de kernel**: Depende del problema y los datos