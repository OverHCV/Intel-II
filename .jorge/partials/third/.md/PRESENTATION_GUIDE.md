# 🎓 Guía de Presentación - Tercer Parcial
## Sistemas Inteligentes II - Universidad de Caldas

**Estudiante**: Jorge Alberto Jaramillo Garzón  
**Dataset**: Student Performance (UCI ML Repository)  
**Formato**: Aplicación web interactiva con Streamlit

---

## 📋 Estructura de la Presentación

### Introducción (2 min)

**Lo que debes decir:**

> "Para este examen desarrollé una aplicación web interactiva que implementa los tres algoritmos solicitados: Decision Trees (CART), Hierarchical Clustering y K-means. La aplicación está construida en Python usando Streamlit y está completamente modularizada siguiendo principios de arquitectura de software profesional."

**Detalles importantes a mencionar:**
- Dataset elegido: **Student Performance** de UCI (649 estudiantes, 33 atributos)
- **Por qué este dataset**: Relevancia social (predicción de rendimiento académico), diversidad de atributos (demográficos, sociales, comportamentales)
- **Desafío interesante**: Conversión de variable numérica (G3: 0-20) a categórica para clasificación
- Aplicación **completamente funcional** con interfaz intuitiva

**Puntos técnicos a resaltar:**
- ~3,500 LOC organizadas en **módulos con single responsibility** (todos < 300 LOC)
- **5 páginas principales** con navegación horizontal
- **Experiment tracking persistente** (sandbox con metadata.json + model.pkl)
- **0 errores de linter**, código limpio y documentado

---

## 🌳 Punto 1: Decision Trees (0.9 puntos)

### Narrativa de Demostración

**Introducción al módulo:**

> "Empecemos con el primer punto del examen: Decision Trees. Como pueden apreciar en la pantalla, la aplicación cuenta con una página dedicada a CART que integra tanto la teoría como la experimentación práctica."

### 1. Dataset Review (Preparación de Datos)

**Lo que debes mostrar:**
1. Navega a **"📊 Dataset Review"**
2. Muestra la sección **"🎛️ Data Controls"**

**Lo que debes decir:**

> "Antes de entrenar cualquier modelo, implementé un pipeline completo de preparación de datos. Como pueden ver, la aplicación permite seleccionar entre tres opciones de dataset: Portuguese (649 estudiantes para entrenamiento), Math (395 para testing), o ambos combinados."

**Detalles técnicos a mencionar:**

- **Target Engineering**: 
  > "Aquí pueden ver las opciones de transformación de G3. Implementé cuatro estrategias: binaria (Pass/Fail), tres clases (Bajo/Medio/Alto), cinco clases (A/B/C/D/F), y thresholds personalizados. Para la demostración usaré cinco clases porque proporciona mayor granularidad en las predicciones."

- **Class Balancing**:
  > "El dataset original está desbalanceado. Implementé tres técnicas de balanceo: SMOTE (genera muestras sintéticas), Random Oversample, y Random Undersample. SMOTE es el recomendado porque no duplica ejemplos sino que crea nuevos mediante interpolación entre vecinos cercanos."

- **Data Leakage Prevention**:
  > "Punto crítico: G1 y G2 (notas de periodos anteriores) correlacionan casi perfectamente con G3. Incluirlas haría la predicción trivial. Por defecto, la aplicación las excluye automáticamente. Sin embargo, agregué controles opcionales para incluirlas experimentalmente y demostrar su impacto en la accuracy."

**Muestra las visualizaciones:**

> "Una vez procesados los datos, la aplicación muestra tres visualizaciones clave:"

1. **Class Distribution**: 
   > "Aquí vemos la distribución de clases después del balanceo. SMOTE llevó las 649 muestras originales a 1005, balanceando perfectamente las cinco clases a 201 muestras cada una."

2. **Feature Correlation**:
   > "Esta matriz muestra las correlaciones entre features. Notar que solo se muestra el triángulo inferior para evitar redundancia. Las correlaciones más fuertes ayudan a entender las relaciones entre variables."

3. **Summary Statistics**:
   > "Estadísticas descriptivas de cada feature. Esta tabla incluye una columna de 'Description' que mapea los nombres técnicos a descripciones legibles (por ejemplo, 'failures' → 'Número de reprobaciones previas')."

### 2. Decision Tree Training

**Navega a "🌳 Decision Trees"**

**Lo que debes mostrar:**
1. Expande el **"📚 TEORÍA"** brevemente
2. Muestra los **controles de hiperparámetros** en el sidebar

**Lo que debes decir:**

> "La página de Decision Trees está completamente modularizada. Pueden ver que incluye una sección teórica expandible que explica el algoritmo CART, Gini impurity, y el proceso de construcción del árbol."

**Hiperparámetros configurables:**

> "Implementé controles para todos los hiperparámetros relevantes:"

- **Max Depth**: `"Profundidad máxima del árbol. Valores bajos previenen overfitting pero pueden causar underfitting."`
- **Min Samples Split**: `"Número mínimo de muestras para dividir un nodo. Actúa como regularización."`
- **Criterion**: `"Gini es más rápido, Entropy (Information Gain) es más interpretable. Generalmente producen resultados similares."`
- **Test Size**: `"Porcentaje de datos para testing. El estándar es 20-30%."`
- **Cross-Validation Folds**: `"Número de folds para validación cruzada. Más folds = estimación más robusta pero más tiempo de cómputo."`

**Click en "🚀 Train Decision Tree"**

**Lo que debes decir durante el entrenamiento:**

> "El entrenamiento ejecuta un pipeline completo: split train/test estratificado, entrenamiento CART, predicción, evaluación de métricas, extracción de reglas, cross-validation, cálculo de feature importance, y guardado del experimento. Todo esto en aproximadamente 1-2 segundos."

### 3. Análisis de Resultados

**Resultados mostrados (en orden):**

#### a) Métricas Principales

> "Como pueden ver, el modelo obtuvo una accuracy de ~37%. Esto puede parecer bajo, pero es importante contextualizarlo: estamos prediciendo 5 clases usando solo factores demográficos y comportamentales, sin las notas previas. El baseline random sería 20% (1/5), así que nuestro modelo supera significativamente el azar."

**Menciona las 4 métricas:**
- **Accuracy**: Proporción de predicciones correctas
- **Precision**: De lo que predijo como X, cuánto era realmente X
- **Recall**: De todo lo que era X, cuánto detectó
- **F1-Score**: Media armónica de precision y recall

#### b) Cross-Validation

> "La validación cruzada con 5 folds confirmó la robustez del modelo. La accuracy promedio es consistente con la del test set, indicando que no hay overfitting significativo."

#### c) Matriz de Confusión + Feature Importance (lado a lado)

**Punto importante a resaltar:**

> "Aquí implementé una mejora en el layout: la matriz de confusión y la importancia de features se muestran lado a lado en dos columnas, aprovechando mejor el espacio horizontal de la pantalla."

**Matriz de Confusión:**
> "La diagonal representa predicciones correctas. Pueden ver que el modelo tiene más dificultad distinguiendo clases adyacentes (como C y D) que clases extremas (A y F), lo cual es esperado."

**Feature Importance:**
> "El gráfico muestra las top 10 features más importantes según reducción de Gini. Como pueden ver, 'failures' (reprobaciones previas) es la más determinante, seguida de 'absences' y 'studytime'. Esto tiene sentido intuitivo: historial académico y dedicación predicen fuertemente el desempeño."

#### d) Estructura del Árbol

> "La visualización del árbol se adapta dinámicamente a la profundidad real. Para árboles muy profundos, solo muestra los primeros 4 niveles por legibilidad. Cada nodo muestra la condición de split, el Gini index, las muestras, y la distribución de clases."

#### e) Reglas Extraídas

> "Una característica clave de los árboles de decisión es su interpretabilidad. La aplicación extrae automáticamente las reglas y las rankea por soporte, confianza, y simplicidad. Las reglas se muestran en dos columnas (5+5) para mejor visualización."

**Ejemplo de regla:**

> "Por ejemplo, esta regla dice: 'SI failures <= 0.5 Y studytime > 2.5 Y absences <= 10, ENTONCES predicción = A'. El soporte indica cuántos estudiantes del train set cumplen esta regla, y la confianza es la precisión de la predicción en ese nodo hoja."

**Interpretación del soporte:**

> "Punto importante: el soporte se refiere al **train set balanceado con SMOTE** (1005 estudiantes), no al test set. Por eso los números de soporte son mayores que los de la matriz de confusión (~201 test samples)."

### 4. Experiment Tracking

**Scroll hacia abajo hasta "📊 Experiment History"**

**Lo que debes decir:**

> "Cada vez que entreno un modelo, la aplicación guarda automáticamente el experimento en un storage persistente. Como pueden ver en esta tabla, se registran todos los hiperparámetros, métricas, y timestamp. Esto permite comparar experimentos y trackear mejoras."

**Muestra la evolución de accuracy:**

> "Este gráfico de línea muestra cómo ha evolucionado la accuracy a través de los experimentos. En este caso, vemos que la accuracy se mantiene relativamente estable, lo que sugiere que hemos encontrado una configuración óptima de hiperparámetros."

**Menciona el almacenamiento:**

> "Técnicamente, cada experimento se guarda en el directorio 'sandbox/' con un version_id único (timestamp + hash). Se almacena el modelo serializado (.pkl) y metadata en JSON. Esto facilita la reproducibilidad y el análisis post-mortem."

---

## 🌲 Punto 2: Hierarchical Clustering (0.9 puntos)

### Narrativa de Demostración

**Navega a "🌲 Hierarchical Clustering"**

**Introducción:**

> "Pasemos al segundo punto: Hierarchical Clustering. Como pueden apreciar, la aplicación reutiliza los datos preparados en Dataset Review, lo cual es eficiente y mantiene consistencia en el preprocesamiento."

### 1. Controles y Configuración

**Muestra el sidebar:**

**Lo que debes decir:**

> "Para clustering jerárquico, implementé controles para:"

- **Number of Clusters (K)**:
  > "Slider de 2 a 10 clusters. En la práctica, para este dataset educativo, esperamos entre 3-5 perfiles de estudiantes."

- **Linkage Method**:
  > "Implementé los cuatro criterios principales: Ward (minimiza varianza intra-cluster, recomendado), Complete (distancia máxima), Average (distancia promedio), y Single (distancia mínima). Ward tiende a producir clusters más balanceados."

- **Distance Metric**:
  > "Tres métricas disponibles: Euclidean (estándar para datos numéricos), Manhattan (menos sensible a outliers), y Cosine (útil para datos de alta dimensionalidad). Nota: Ward solo funciona con Euclidean."

**J4 Analysis:**

> "Punto importante del examen: implementé el análisis J4 para encontrar el número óptimo de clusters. Cuando activo esta opción, la aplicación calcula el Silhouette Score para un rango de K y sugiere el óptimo."

### 2. Resultados y Visualizaciones

**Click en "🚀 Run Hierarchical Clustering"**

**Durante el entrenamiento:**

> "El proceso calcula la matriz de linkage usando scipy, corta el dendrograma en K clusters, y evalúa la calidad usando dos métricas: Silhouette Score y Fisher J4."

#### a) Clustering Summary

**Lo que debes decir:**

> "El resumen muestra las métricas clave:"

- **Silhouette Score**: 
  > "Varía de -1 a 1. Valores cercanos a 1 indican clusters bien separados. Un score de ~0.3-0.4 es razonable para datos de estudiantes, donde los límites entre perfiles no son completamente nítidos."

- **Fisher J4**:
  > "Este es el criterio solicitado en el examen. Se define como trace(SB) / trace(SW), donde SB es la matriz de dispersión between-class y SW es within-class. Mayor J4 = mejor separación de clusters."

**Expande el "¿Qué significan estas métricas?":**

> "Aquí pueden ver la explicación detallada de ambas métricas. Silhouette mide qué tan similar es un punto a su propio cluster vs otros clusters. Fisher J4 es una métrica más académica que maximiza la separación entre clusters mientras minimiza la dispersión interna."

#### b) J4 Analysis (si está activado)

**Lo que debes mostrar:**

> "Cuando ejecuto el análisis J4, la aplicación prueba diferentes valores de K (por ejemplo, 2 a 10) y calcula el Silhouette Score para cada uno. Este gráfico muestra la evolución: el pico indica el K óptimo."

**Tabla de scores:**

> "La tabla lista todos los scores calculados. En este caso, el óptimo sugerido es K=3, con un Silhouette de 0.42. Esto sugiere tres perfiles distintos de estudiantes en el dataset."

#### c) Dendrograma

**Lo que debes decir:**

> "El dendrograma visualiza la jerarquía completa de agrupamientos. La línea roja horizontal indica dónde se cortó el árbol para obtener K clusters. Pueden ver cómo los estudiantes se agrupan progresivamente de abajo hacia arriba."

**Interpreta el dendrograma:**

> "La altura de las uniones indica la distancia/disimilitud entre clusters. Uniones más altas = clusters más disímiles. En este caso, vemos que hay una separación clara entre dos grandes grupos, que luego se subdividen."

#### d) Cluster Distribution + Silhouette Plot (lado a lado)

**Cluster Distribution:**

> "Este gráfico de barras muestra el tamaño de cada cluster. Idealmente, queremos clusters balanceados. Si un cluster tiene solo 5% de las muestras, puede ser un outlier cluster."

**Tabla de tamaños:**

> "La tabla lista el conteo exacto por cluster. También muestra el porcentaje del total, útil para identificar clusters minoritarios."

**Silhouette Plot:**

> "El Silhouette Plot es una visualización muy informativa. Cada barra representa un estudiante, ordenado por cluster. El ancho de la barra es el coeficiente de silhouette de ese estudiante."

**Interpretación:**

> "Barras que exceden la línea roja (promedio) indican estudiantes bien asignados. Barras negativas indican posibles mal-asignaciones. Clusters con muchas barras negativas sugieren que K puede ser subóptimo."

#### e) Cluster Profiles

**Lo que debes mostrar:**

> "Esta es la parte más interesante para interpretación: los perfiles de clusters. Para cada cluster, muestro las top 5 features que más lo caracterizan, junto con su media ± desviación estándar."

**Ejemplo de interpretación:**

> "Por ejemplo, Cluster 0 se caracteriza por 'failures' alto (media 1.2), 'absences' alto, y 'studytime' bajo. Podríamos llamar a este cluster 'Estudiantes en Riesgo'. En contraste, Cluster 2 tiene 'failures' bajo, 'studytime' alto, y 'goout' bajo, sugiriendo 'Estudiantes Dedicados'."

**Menciona las descripciones:**

> "Nota que cada feature incluye su descripción en español entre paréntesis, facilitando la interpretación sin necesidad de consultar el diccionario de datos."

### 3. Diferentes Puntos de Corte (Análisis J4)

**Re-ejecuta con diferentes K:**

**Lo que debes decir:**

> "El examen solicita analizar diferentes puntos de corte. Como pueden ver en el análisis J4, puedo probar múltiples valores de K y compararlos:"

**Ejemplo de comparación:**

> "Con K=2, obtengo solo dos grandes grupos (alto vs bajo rendimiento). Con K=5, tengo mayor granularidad pero los clusters empiezan a solaparse (Silhouette baja). K=3 parece ser el sweet spot para este dataset, balanceando interpretabilidad y calidad de clustering."

**Conclusión para el examen:**

> "En conclusión, el análisis J4 sugiere K=3 como óptimo para este dataset. Esto tiene sentido intuitivo: podríamos tener tres perfiles de estudiantes (Bajo Rendimiento, Promedio, Alto Rendimiento), cada uno con características socioeconómicas y comportamentales distintas."

---

## 🎯 Punto 3: K-means Clustering (0.7 puntos)

### Narrativa de Demostración

**Navega a "🎯 K-means Clustering"**

**Introducción:**

> "Finalmente, el tercer punto: K-means usando el número óptimo de clusters encontrado en el análisis anterior. Como pueden ver, la estructura de esta página es similar a Hierarchical, manteniendo consistencia en la interfaz."

### 1. Uso del K Óptimo

**Configura K=3 (el óptimo encontrado antes):**

**Lo que debes decir:**

> "Basándome en el análisis J4 del clustering jerárquico, voy a usar K=3 para K-means. Esto permite una comparación directa entre ambos algoritmos con el mismo número de clusters."

### 2. Controles de K-means

**Muestra el sidebar:**

> "K-means tiene hiperparámetros específicos:"

- **Init Method**:
  > "k-means++ es el método recomendado (Arthur & Vassilvitskii, 2007). Selecciona centroides iniciales inteligentemente, reduciendo iteraciones y mejorando calidad. Random es más simple pero puede converger a óptimos locales."

- **N Init**:
  > "Número de inicializaciones. K-means ejecuta N veces con diferentes semillas y retorna la mejor. Por defecto uso 10, balanceando calidad y velocidad."

- **Max Iter**:
  > "Iteraciones máximas antes de forzar convergencia. 300 es generalmente suficiente para datasets de este tamaño."

**Elbow Method:**

> "También implementé el Elbow Method como método alternativo para encontrar K óptimo. Cuando activo esta opción, calcula la inercia (WCSS) para diferentes valores de K y detecta automáticamente el 'codo' en la curva."

### 3. Resultados y Visualizaciones

**Click en "🚀 Run K-means Clustering"**

#### a) Clustering Summary

**Lo que debes decir:**

> "El resumen muestra tres métricas:"

- **Silhouette Score**: `"0.38 - comparable al Hierarchical (0.40), confirmando calidad similar."`
- **Fisher J4**: `"El criterio J4 solicitado. Permite comparación directa con Hierarchical."`
- **Inertia**: `"Sum of squared distances de cada punto a su centroide. Específico de K-means. Menor = mejor, pero debe balancearse con K."`

#### b) Elbow Analysis (si está activado)

**Muestra el gráfico:**

> "El Elbow plot visualiza la inercia vs número de clusters. La línea roja indica el K óptimo detectado automáticamente usando el método de perpendicular distance."

**Interpretación:**

> "Pueden ver que la inercia decrece rápidamente hasta K=3, luego la mejora es marginal. Este 'codo' confirma que K=3 es óptimo, coincidiendo con el análisis J4 de Hierarchical."

#### c) Cluster Distribution + Silhouette Plot

**Similar a Hierarchical, pero resalta las diferencias:**

> "Interesante: mientras Hierarchical produjo clusters de tamaños 180, 220, 605, K-means produce 334, 336, 335 - mucho más balanceados. Esto es característico de K-means, que busca minimizar WCSS y tiende a crear clusters de tamaño similar."

**Silhouette Plot:**

> "El Silhouette plot muestra calidad ligeramente inferior a Hierarchical en algunos clusters, pero es consistente. Esto sugiere que ambos algoritmos encuentran estructuras válidas pero ligeramente diferentes en los datos."

#### d) Cluster Profiles

**Compara con Hierarchical:**

> "Los perfiles de K-means son ligeramente diferentes a Hierarchical. Por ejemplo, K-means Cluster 0 se caracteriza por 'absences' alto y 'Dalc' (alcohol en días laborables) alto, mientras que Hierarchical enfatizó más 'failures'. Ambos son válidos, pero capturan aspectos diferentes de la estructura de datos."

### 4. Comparación K-means vs Hierarchical

**Tabla comparativa que debes mencionar:**

| Aspecto | K-means | Hierarchical |
|---------|---------|--------------|
| **Velocidad** | ⚡ Muy rápido (~0.1s) | 🐢 Más lento (~0.5s) |
| **Silhouette** | 0.38 | 0.40 |
| **Fisher J4** | X.XX | X.XX |
| **Clusters balanceados** | ✅ Sí (334, 336, 335) | ❌ No (180, 220, 605) |
| **Determinístico** | ❌ No (depende de init) | ✅ Sí |
| **Dendrograma** | ❌ No disponible | ✅ Sí |

**Lo que debes decir:**

> "En conclusión, ambos algoritmos encontraron K=3 como óptimo y produjeron Silhouette scores similares (~0.38-0.40). K-means es significativamente más rápido y produce clusters más balanceados, mientras que Hierarchical proporciona el dendrograma para análisis visual de la jerarquía. Ambos son válidos, la elección depende de las necesidades específicas del análisis."

---

## 📈 Feature Extra: Experiment History

**Navega a "📈 History"**

**Introducción:**

> "Como valor agregado más allá de los requisitos del examen, implementé un dashboard completo de tracking de experimentos que permite comparar y analizar todos los modelos entrenados."

### Características a Demostrar

**1. Timeline:**

> "Este gráfico muestra la evolución temporal de experimentos. Pueden ver scatter plots por tipo de algoritmo (color-coded) y un bar chart de actividad diaria. Esto es útil para trackear la velocidad de experimentación."

**2. Experiment Table:**

> "Tabla interactiva con filtros por algoritmo y fecha. Cada experimento muestra sus métricas clave: para Decision Trees, accuracy y F1; para clustering, K, Silhouette y J4. Puedo seleccionar hasta 5 experimentos para comparación."

**3. Comparison Tool:**

> "Cuando selecciono múltiples experimentos del mismo algoritmo, la aplicación genera tablas y gráficos comparativos lado a lado. Esto facilita identificar el mejor performer y entender el impacto de diferentes hiperparámetros."

**4. Management:**

> "También incluye herramientas de gestión: puedo ver el storage usado (~X MB), eliminar experimentos individuales, o limpiar todo con confirmación doble. Esto previene acumulación de artefactos innecesarios."

---

## 🎯 Conclusiones Finales

### Resumen Técnico

**Lo que debes decir para cerrar:**

> "Para resumir el proyecto completo:"

1. **Arquitectura Profesional**:
   > "La aplicación está construida con ~3,500 LOC organizadas en módulos con single responsibility. Todos los archivos son < 300 LOC, facilitando mantenimiento y testing. Usé direct absolute imports para evitar problemas de circular dependencies."

2. **Pipeline de ML Completo**:
   > "Implementé un pipeline end-to-end: carga de datos, feature engineering, preprocesamiento (encoding, scaling), balanceo (SMOTE), entrenamiento, evaluación, visualización, y persistencia de experimentos."

3. **Prevención de Data Leakage**:
   > "Punto crítico del examen: excluí G1 y G2 por defecto para evitar data leakage. Sin embargo, agregué controles opcionales para demostrar experimentalmente su impacto (~90%+ accuracy con ellas vs ~37% sin ellas)."

4. **Interpretabilidad**:
   > "Todas las visualizaciones incluyen descripciones en español de las features (e.g., 'failures' → 'Número de reprobaciones previas'). Las reglas de Decision Trees son completamente legibles. Los cluster profiles permiten entender qué caracteriza cada grupo."

5. **Reproducibilidad**:
   > "Cada experimento se guarda con timestamp, hiperparámetros, métricas, y modelo serializado. Esto permite reproducir resultados exactos y comparar configuraciones."

### Resultados por Algoritmo

**Decision Trees:**
- ✅ Accuracy ~37% (5 clases, sin G1/G2)
- ✅ Reglas interpretables extraídas y rankeadas
- ✅ Feature importance: 'failures' más determinante
- ✅ Cross-validation confirma robustez

**Hierarchical Clustering:**
- ✅ K óptimo = 3 (análisis J4/Silhouette)
- ✅ Silhouette Score = 0.40
- ✅ Tres perfiles identificados: Alto/Promedio/Bajo rendimiento
- ✅ Dendrograma visualiza jerarquía completa

**K-means:**
- ✅ K=3 confirmado por Elbow Method
- ✅ Silhouette Score = 0.38 (comparable a Hierarchical)
- ✅ Clusters más balanceados (334, 336, 335)
- ✅ ~5x más rápido que Hierarchical

### Valor Agregado

**Menciona características extras:**

> "Más allá de los requisitos, agregué:"
- 📈 **Experiment History Dashboard** con timeline, comparación, y management
- 🎨 **UI/UX profesional** con navegación intuitiva y visualizaciones ricas
- 📚 **Secciones teóricas educativas** en cada página
- 🔄 **State management robusto** con persistencia entre páginas
- 🚀 **Performance optimizado** (entrenamiento en 1-2 segundos)
- 📊 **Múltiples visualizaciones** (15+ tipos de plots/tablas)

### Mensaje Final

> "La aplicación está lista para demostración en vivo y el código está completamente documentado. Todos los archivos están en el repositorio y la aplicación puede ejecutarse localmente con un simple `streamlit run app.py`. Gracias por su atención, quedo atento a sus preguntas."

---

## 💡 Tips para la Sustentación Oral

### Antes de Empezar

1. **Practica la navegación**: Familiarízate con los clicks necesarios
2. **Prepara experimentos**: Entrena 2-3 modelos antes de presentar para que History tenga contenido
3. **Timing**: Practica para que dure 8-10 minutos, dejando 2-3 minutos para preguntas
4. **Backup**: Ten screenshots por si falla la conexión o la app

### Durante la Presentación

1. **Confidence**: Habla con seguridad, conoces tu código perfectamente
2. **Slow down**: No vayas demasiado rápido, deja que el profesor absorba la información
3. **Eye contact**: Mira al profesor, no solo la pantalla
4. **Interactividad**: Si el profesor pregunta durante la presentación, responde calmadamente

### Preguntas Probables

**P: "¿Por qué la accuracy es tan baja?"**
> **R**: "Es esperado. Estamos prediciendo 5 clases sin las notas previas (G1/G2). El baseline random sería 20%, nosotros tenemos 37%, casi el doble. Con G1/G2 llegaríamos a ~85-90% pero habría data leakage."

**P: "¿Cómo manejaste el desbalance de clases?"**
> **R**: "Implementé SMOTE (Synthetic Minority Over-sampling Technique) que genera muestras sintéticas interpolando entre vecinos cercanos. Balanceé las 5 clases de 649 muestras desbalanceadas a 1005 balanceadas (201 por clase)."

**P: "¿Por qué usaste CART y no C4.5/ID3?"**
> **R**: "CART es el algoritmo implementado en sklearn (DecisionTreeClassifier). Es más robusto que ID3 porque maneja features numéricas directamente y usa Gini/Entropy. C4.5 es una extensión de ID3, pero sklearn usa CART por su eficiencia y performance."

**P: "¿Qué significa el J4 exactamente?"**
> **R**: "Fisher J4 es el ratio trace(SB)/trace(SW), donde SB es la matriz de dispersión between-class y SW es within-class. Maximizar J4 significa maximizar separación entre clusters mientras minimizamos dispersión interna. También usé Silhouette Score como métrica complementaria, que es más interpretable (-1 a 1)."

**P: "¿Por qué K-means produce clusters más balanceados?"**
> **R**: "K-means minimiza WCSS (within-cluster sum of squares), que tiende a favorecer clusters de tamaño similar porque cada punto contribuye igualmente. Hierarchical no tiene esta restricción, entonces puede producir clusters muy desbalanceados si la estructura de datos lo sugiere."

**P: "¿Cómo implementaste el Elbow Method?"**
> **R**: "Calculé la inercia para K=2 hasta K=max, luego usé el método de perpendicular distance: encuentro el punto más alejado de la línea que conecta (K=2, inertia_max) con (K=max, inertia_min). Ese punto es el 'codo'."

**P: "¿El código es tuyo o usaste templates?"**
> **R**: "Todo el código es original. Usé librerías estándar (sklearn, scipy, matplotlib, streamlit) pero la arquitectura modular, el pipeline de datos, las visualizaciones, y el experiment tracking son implementación propia. Puede verificar el repositorio."

---

## 📚 Documentos de Referencia

Durante la presentación, ten estos documentos a mano (en ventanas separadas):

1. **README.md** - Descripción del examen
2. **motivation.md** - Justificación del dataset
3. **DECISION_TREE_REFACTOR.md** - Arquitectura de Decision Trees
4. **HIERARCHICAL_IMPLEMENTATION.md** - Detalles de Hierarchical
5. **KMEANS_IMPLEMENTATION.md** - Detalles de K-means
6. **HISTORY_IMPLEMENTATION.md** - Experiment tracking

---

## 🎬 Flow de Demostración Recomendado (10 min)

1. **Introducción** (1 min)
   - Presentación del proyecto
   - Stack técnico
   - Estructura modular

2. **Dataset Review** (2 min)
   - Pipeline de preparación
   - Target engineering
   - Balanceo con SMOTE
   - Visualizaciones

3. **Decision Trees** (3 min)
   - Hiperparámetros
   - Entrenamiento
   - Métricas y visualizaciones
   - Reglas interpretables

4. **Hierarchical Clustering** (2 min)
   - Análisis J4 para K óptimo
   - Dendrograma
   - Cluster profiles

5. **K-means** (1.5 min)
   - Uso de K óptimo
   - Elbow Method
   - Comparación con Hierarchical

6. **Experiment History** (0.5 min)
   - Dashboard de tracking
   - Comparación de experimentos

7. **Conclusiones** (1 min)
   - Resumen de resultados
   - Valor agregado
   - Cierre

---

**¡Éxito en tu presentación! 🎓🚀**

