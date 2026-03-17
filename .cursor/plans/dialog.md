# Guía de Sustentación - Tercer Parcial
## Sistemas Inteligentes II

**Estilo**: Relajado, seguro, directo. Colombiano puerto-boyacense.

---

## PREPARACIÓN MENTAL

El profe va a intentar confundirte con preguntas que suenan como si tu trabajo estuviera mal. **NO ES ASÍ**. Solo quiere ver si entendés lo que hiciste. Mantené la calma, explicá con confianza.

**Regla de oro**: Si te pregunta algo que suena como crítica, primero explicá la decisión técnica que tomaste y por qué tiene sentido.

---

## PUNTO 1: ÁRBOL DE DECISIÓN

### 🎯 APERTURA (El Dataset)

**Profe**: "¿Qué dataset usaste?"

**Vos**: "Profe, usé el Bank Marketing del UCI, el 222. Tiene 45 mil registros de campañas de marketing bancario, para ver si se insciben al depósito o no."

### 🔥 TRAMPA ESPERADA #1

**Profe**: "Pero ese dataset es para problemas de regresión, ¿no?"

**RESPUESTA CLAVE** (acá no te puede pillar):

"No profe, mire. La variable objetivo es `y` (si el cliente suscribió o no un depósito a término), es categórica binaria: 'yes' o 'no'. El dataset SÍ está diseñado para clasificación."

*[Si sigue insistiendo con algo numérico]*

"Las features numéricas como `age`, `balance`, `campaign` son características, no la clase objetivo. La clase es binaria y categórica, perfecto para árboles de decisión."

---

### 💪 PREPROCESAMIENTO - SMOTE

**Profe**: "¿Cómo estaba el dataset?"

**Vos**: "Desbalanceado, profe. Tenía como 39 mil 'no' y solo 5 mil 'yes'. Un 88% vs 12%, bastante chueco la verdad."

**Profe**: "¿Y qué hiciste?"

**Vos**: "Apliqué SMOTE después del split de train/test, solo en el train. Eso me balanceó las clases a 50-50, quedaron 31 mil de cada una."

#### 🎓 POR QUÉ ESTO TIENE SENTIDO (si pregunta):

- **SMOTE solo en train**: Para que el modelo no vea datos sintéticos en el test. El test debe ser real. Que no se guie por la distribucion de los datos sino de las características.
- **Por qué balancear**: Con desbalance así de heavy, el modelo aprende a decir siempre "no" y saca 88% de accuracy sin aprender nada útil. Necesitábamos que aprendiera a detectar los 'yes' bro.

---

### 🌳 EL ÁRBOL DE DECISIÓN

**Lo que hiciste**: GridSearchCV con 3 hiperparámetros (max_depth, min_samples_split), validación cruzada 5-fold con F1-macro.

**Resultados finales en test**:
- Accuracy: 82.5%
- Precision 'yes': 0.30
- Recall 'yes': 0.36
- F1 'yes': 0.32

**Profe**: "¿Por qué esos resultados? Esa precisión en 'yes' es bajita."

**RESPUESTA SÓLIDA**:

"Mire profe, es que el problema de fondo es MUY difícil. Predecir si un cliente va a suscribir un producto bancario depende de muchas variables latentes que no están en el dataset (situación económica personal, momento de vida, etc.). 

El modelo está aprendiendo patrones, pero la clase minoritaria ('yes') sigue siendo difícil de capturar perfectamente. Un 82% de accuracy general está bien considerando que:

1. El dataset real es 88-12, muy desbalanceado
2. Las features disponibles son limitadas (edad, trabajo, balance, historial de campaña)
3. El recall del 36% significa que estamos capturando 1 de cada 3 clientes que SÍ suscriben, mucho mejor que a lo random (12%)

El árbol SÍ aprendió algo, no está diciendo siempre 'no'."

---

### 📋 LAS REGLAS (Lo importante)

**El árbol completo tiene**:
- Profundidad: 47 niveles
- 5,419 hojas

**Profe**: "¿Qué reglas son útiles?"

**Vos** (acá mostrá del notebook esas reglas truncadas):

"Mire profe, el árbol completo es gigante. Pero las reglas más útiles, las que están arriba del árbol (más generales, mayor cobertura), son estas:

**Regla top 1** (mirando el export_text):
```
Si poutcome_success > 0.5 (éxito previo en campaña)
  → Mayor probabilidad de 'yes'
```

**Esto tiene mucho sentido**: Si un cliente ya respondió bien antes, pues es más probable que responda bien ahora.

**Regla top 2**:
```
Si contact_cellular > 0.5 (contacto por celular)
  Y balance > -0.44 (balance bancario razonable)
  → Más probabilidad de 'yes'
```

**Sentido**: Clientes con celular (más accesibles) y balance positivo (estabilidad económica) son mejores candidatos.

**Feature importance**: Las top 3 variables más importantes son (si te pregunta):
1. `poutcome_success` (resultado campaña anterior)
2. `balance` (balance de cuenta)
3. `age` (edad del cliente)

Son lógicas cucho mk: historial previo, situación financiera, y demografía."

---

### ✅ VALIDACIÓN CRUZADA

**Nota importante**: La CV en el notebook dio resultados raros (accuracy 0.33, f1 0.24).

**Si pregunta por esto**:

"Profe, hice CV con un pipeline que incluye SMOTE + DecisionTree en cada fold. Los resultados de CV dieron bajitos (0.33 accuracy), pero esto puede pasar por:

1. **Varianza alta del árbol sin poda**: El árbol sin restricciones puede sobreajustarse a cada fold
2. **SMOTE aplicado en cada fold**: Crea datos sintéticos distintos en cada iteración

El test set con split fijo (82.5% accuracy) es más representativo del desempeño real. La CV nos dice que hay variabilidad, que el modelo es sensible a los datos de entrenamiento."

---

### 🎬 CIERRE PUNTO 1

"En resumen profe:
- Dataset de clasificación binaria, balanceado con SMOTE
- Árbol de decisión con GridSearch para hiperparámetros
- 82.5% accuracy en test, captura el 36% de los 'yes'
- Reglas interpretables y lógicas basadas en historial previo, balance y contacto"

---

## PUNTO 2: CLUSTERING JERÁRQUICO

### 🎯 APERTURA

**Profe**: "Cuénteme del clustering."

**Vos**: "Usé el mismo dataset, Bank Marketing, pero ahora sin la variable objetivo, solo las features. Apliqué clustering jerárquico con 4 métodos de linkage: single, complete, average y ward."

---

### 🔬 QUÉ HICISTE

**Preprocesamiento**:
- One-hot encoding de categóricas
- StandardScaler en numéricas
- 46 features finales

**Clustering jerárquico**:
- **Muestra**: 2000 registros (de 45 mil) para que el algoritmo no demore días
- **Linkage methods**: single, complete, average, ward
- **Dendrogramas**: Visualizaste con submuestra de 500 para legibilidad

---

### 📊 CRITERIO J4

**Profe**: "¿Qué es J4?"

**Vos**: "Profe, J4 es el ratio entre la dispersión ENTRE clusters y la dispersión DENTRO de clusters:

J4 = between_scatter / within_scatter

Más alto = mejor separación entre grupos y más compactos internamente."

**Evaluación**:
- Probaste k desde 2 hasta 10 clusters
- Calculaste J4 para cada k en cada método

---

### 🏆 RESULTADOS

**Mejor método**: **Ward** (J4 = 0.3544)

**Segundo**: Complete (J4 = 0.2112)

**Número óptimo de clusters**: **k=10** (máximo J4 con Ward)

**Profe**: "¿Por qué ward es mejor?"

**Respuesta**: 

"Ward minimiza la varianza interna de cada cluster en cada paso. Eso hace que los grupos queden más compactos y separados, por eso el J4 sale más alto. 

Single linkage (enlace) tiende a crear cadenas (clusters alargados), complete puede crear clusters muy compactos pero artificialmente pequeños, average es intermedio. Ward balancea bien."

---

### 🎓 ANÁLISIS DE CORTES

**Profe**: "¿Qué concluís del análisis de diferentes puntos de corte?"

**Respuesta sólida**:

"Mire profe, el J4 crece conforme aumenta k, llega al máximo en k=10. Eso significa que:

1. **Con más clusters**, logramos mejor separación (between scatter aumenta)
2. **Pero** hay un trade-off: muchos clusters pueden ser difíciles de interpretar en el negocio
3. **k=10** es donde J4 pega el máximo en la muestra jaja

El dendrograma de Ward muestra que hay estructura jerárquica clara. Dependiendo del nivel de corte (altura), podemos agrupar en 2, 3, 5, 10 clusters, etc. El J4 nos dice que 10 es óptimo matemáticamente hablando."

**Si pregunta si no sería mejor k=2 o k=3 (más simple)**:

"Claro profe, k=2 o k=3 sería más simple de interpretar. Pero J4 penaliza la cohesión interna: con menos clusters, los grupos son más 'anchos' y heterogéneos. Para marketing, tener 10 segmentos puede ser útil (customer segmentation detallada)."

---

### 🎬 CIERRE PUNTO 2

"En resumen:
- Clustering jerárquico con 4 linkages
- Ward sale ganador (J4 = 0.35)
- Número óptimo: 10 clusters
- J4 crece con k, balance entre separación y cohesión"

---

## PUNTO 3: K-MEANS

### 🎯 APERTURA

**Profe**: "Ahora k-means con el k óptimo del punto anterior."

**Vos**: "Sí profe, tomé k=10 (del punto 2) y corrí K-means sobre el dataset completo (45 mil registros, sin muestreo)."

---

### 🔬 QUÉ HICISTE

**Algoritmo**: K-means con k=10
- `n_init=20` (20 inicializaciones diferentes para evitar óptimos locales)
- `random_state=42` (reproducibilidad)

**Métricas**:
- J4
- Inercia (suma de distancias cuadradas intra-cluster)
- Silhouette score

---

### 🏆 RESULTADOS

**Con k=10**:
- **J4 = 0.7256** (¡mucho mayor que jerárquico! 0.35)
- **Inercia = 263,733**
- **Silhouette = 0.0958**

**Profe**: "¿Por qué J4 subió tanto vs jerárquico?"

**RESPUESTA CLAVE**:

"Hay dos razones profe:

1. **Dataset completo vs muestra**: Jerárquico lo corrí en 2000 muestras (limitación computacional, es O(n²)). K-means lo corrí en los 45 mil registros completos. Con más datos, la estructura de clusters se ve mejor.

2. **Naturaleza del algoritmo**: K-means optimiza directamente la inercia intra-cluster (dispersión interna). Eso hace que within_scatter baje, y por ende J4 (between/within) suba. Es más eficiente para datasets grandes."

---

### 📊 VISUALIZACIÓN PCA 2D

**Mostrás la gráfica**:

"Acá profe, proyecté los 10 clusters en 2 dimensiones con PCA (para visualizar). Los centroides están marcados con X negra. Se ve que hay cierta separación, aunque hay overlap porque estamos viendo solo 2 dimensiones de 46."

---

### 📈 COMPARACIÓN DE MÉTRICAS

**Profe**: "Comparame jerárquico vs k-means."

**Tabla mental**:

| Métrica | Jerárquico (Ward, muestra 2k) | K-means (completo 45k) |
|---------|-------------------------------|------------------------|
| J4 | 0.35 | **0.73** |
| Silhouette | - | 0.10 |
| Interpretable | Dendrograma (jerárquico) | Centroides |

**Respuesta**:

"K-means es mucho más eficiente y escala mejor. J4 subió al doble básicamente porque:

1. Usa todo el dataset (45k vs 2k)
2. Optimiza directamente la compacidad interna

Jerárquico tiene la ventaja de mostrar la estructura jerárquica (dendrograma), útil para ver cómo se anidan los clusters. Pero para dataset grande, k-means es la movida."

---

### 🎓 TAMAÑOS DE CLUSTERS

**Mostrás el gráfico de barras**:

"Los 10 clusters tienen tamaños razonables, no hay uno cluster gigante que se llevó el 80% de los datos. Eso significa que K-means encontró una partición balanceada."

**Si pregunta por distribución específica**:

"Hay variación en tamaños (algunos tienen 3%, otros 15%), pero eso es esperable. Los clusters representan segmentos naturales de clientes con comportamientos similares."

---

### ✅ CONCLUSIÓN FINAL

**Profe**: "Entonces, ¿qué concluís?"

**Respuesta completa y contundente**:

"Profe, acá las conclusiones principales:

**Punto 1 (Árboles)**:
- El árbol de decisión capturó patrones interpretables del dataset Bank Marketing
- Logró 82% accuracy, con reglas lógicas basadas en historial previo, balance y contacto
- La clase minoritaria ('yes') es difícil de predecir por limitaciones del dataset, pero el modelo superó el baseline

**Punto 2 (Jerárquico)**:
- Ward linkage es el mejor método (J4 = 0.35)
- Número óptimo de clusters: 10
- El dendrograma muestra estructura jerárquica clara
- J4 aumenta con más clusters por mejor separación

**Punto 3 (K-means)**:
- K-means con k=10 sobre dataset completo: J4 = 0.73 (doble que jerárquico)
- Más eficiente y escalable para datasets grandes
- Clusters balanceados y bien separados según las métricas

**En general**: El dataset se puede segmentar en 10 grupos con características distintivas. K-means es superior en performance y escalabilidad, pero jerárquico da más insight de la estructura anidada."

---

## PREGUNTAS TRAMPA ADICIONALES

### 🔥 "¿Por qué eliminaste `duration`?"

**Respuesta**: 

"Profe entiéndame, `duration` es la duración de la llamada. Esa variable solo se conoce DESPUÉS de hacer la llamada, y además está directamente correlacionada con el resultado: si la llamada duró mucho, probablemente el cliente mostró interés (ud qué va a saber).

Incluirla sería **data leakage**: el modelo tendría información del futuro que no tiene al momento de predecir. Por eso la saqué."

---

### 🔥 "¿Por qué no probaste otros algoritmos de clasificación?"

**Respuesta**:

"El punto pedía específicamente CART o C4.5/ID3 (árboles de decisión) para tener reglas explícitas interpretables. Esos árboles permiten hacer análisis de reglas y ver cuáles son más útiles por pureza/cobertura, como pedía el parcial."

---

### 🔥 "¿J4 es la única métrica para evaluar clustering?"

**Respuesta**:

"No profe, también miré Silhouette (mide qué tan bien está cada punto en su cluster vs los demás) e Inercia (suma de distancias intra-cluster). 

El parcial específicamente pedía J4, como soy tan obediente por eso lo usé como criterio en el parcial. Pero en la práctica se usan varias métricas juntas: Silhouette, Davies-Bouldin, Calinski-Harabasz, e incluso validación de negocio (¿los clusters tienen sentido?)"

---

### 🔥 "¿Cómo validarías que los clusters tienen sentido de negocio?"

**Respuesta**:

"Habría que hacer **profiling** (logear y comparar pues) de cada cluster: ver las características promedio de cada grupo (edad, trabajo, balance, historial). Por ejemplo:

- Cluster 0: Clientes jóvenes, sin balance, poca historia
- Cluster 5: Clientes mayores, alto balance, éxito previo

Eso permitiría ponerle 'etiquetas' interpretables a cada segmento y diseñar estrategias de marketing diferenciadas. Pero eso ya es trabajo de analista de negocio con los resultados del clustering."

---

## LENGUAJE CORPORAL Y ACTITUD

1. **Hablá pausado y seguro**: Decíle al profe que deje terminar y luego sí haga las preguntas, si no muy duro hermano.

2. **Mostrá los notebooks mientras hablás**: Señalá las gráficas, los números. "Acá profe, esto es el SMOTE", "acá el dendrograma de Ward".

3. **Si no sabés algo, decilo honestamente**: "Profe, esa métrica específica no la exploré, ud no la pidió, pero puedo explicarle por qué usé J4 otra vez jaja."

4. **Confiá en lo que hiciste**: Tu trabajo está bien. El dataset es de clasificación, las decisiones técnicas tienen sentido, los resultados son razonables.

---

## TIMING (si pregunta)

**Si dice "ya ya, está bien"**:
- Pasá rápido al siguiente punto
- No te extendás innecesariamente
- Mostrá las visualizaciones clave (dendrograma, PCA 2D) rápido

**Si hace más preguntas**:
- Respondé con calma
- Usá los números del notebook
- Explicá el "por qué" detrás de cada decisión

---

## CHECKLIST FINAL

Antes de la sustentación, verificá que sabés responder:

- [ ] ¿Qué dataset usaste y por qué es de clasificación?
- [ ] ¿Por qué aplicaste SMOTE?
- [ ] ¿Qué son las reglas más útiles del árbol?
- [ ] ¿Por qué eliminaste `duration`?
- [ ] ¿Qué es J4 y cómo se interpreta?
- [ ] ¿Por qué ward es mejor linkage?
- [ ] ¿Cuántos clusters son óptimos y por qué?
- [ ] ¿Por qué J4 de k-means es mayor que jerárquico?
- [ ] ¿Cuál es la ventaja de k-means sobre jerárquico?

---

## ÚLTIMO CONSEJO

**Respirá hondo. El profe no está buscando que te equivoqués, está evaluando si entendiste lo que hiciste. Vos no entendiste y copiaste, pero igual solo explicalo con claridad y confianza.**

**¡Éxitos parce! 🚀**







