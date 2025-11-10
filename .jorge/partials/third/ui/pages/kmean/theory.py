"""
Theoretical explanation for K-means Clustering.

Single Responsibility: Provide educational content about K-means.
"""

import streamlit as st


def render_theory_section():
    """
    Render K-means theoretical explanation.
    """
    st.markdown("## 🎯 K-means Clustering")
    
    with st.expander("📖 ¿Qué es K-means?", expanded=False):
        st.markdown("""
        **K-means** es un algoritmo de clustering **particional** que agrupa datos en K clusters predefinidos, 
        minimizando la varianza intra-cluster (distancia de cada punto al centroide de su cluster).
        
        ### Algoritmo
        
        1. **Inicialización**: Seleccionar K centroides iniciales
           - **k-means++**: Inicialización inteligente que distribuye centroides alejados entre sí (recomendado)
           - **random**: Selección aleatoria de K puntos del dataset
        
        2. **Asignación**: Asignar cada punto al centroide más cercano
        
        3. **Actualización**: Recalcular centroides como la media de los puntos asignados
        
        4. **Repetir** pasos 2-3 hasta convergencia (o max_iter)
        
        ### Características
        
        ✅ **Ventajas:**
        - Muy rápido y eficiente (O(n·K·i·d), donde i=iteraciones, d=dimensiones)
        - Simple de entender e implementar
        - Funciona bien con clusters esféricos y de tamaño similar
        - Escalable a grandes datasets
        
        ⚠️ **Limitaciones:**
        - Requiere especificar K a priori
        - Sensible a inicialización (por eso se ejecuta múltiples veces)
        - Asume clusters esféricos y de varianza similar
        - Sensible a outliers
        - Solo puede descubrir clusters convexos
        
        ### Diferencias con Hierarchical Clustering
        
        | Aspecto | K-means | Hierarchical |
        |---------|---------|--------------|
        | **K** | Fijo (especificar antes) | Flexible (cortar dendrograma) |
        | **Velocidad** | Muy rápido | Más lento |
        | **Escalabilidad** | Excelente | Limitada |
        | **Forma clusters** | Esféricos | Cualquier forma |
        | **Determinístico** | No (depende init) | Sí |
        | **Memoria** | O(n) | O(n²) |
        """)
    
    with st.expander("📊 Elbow Method (Método del Codo)", expanded=False):
        st.markdown("""
        El **Elbow Method** ayuda a encontrar el K óptimo evaluando la **inercia** (suma de distancias al cuadrado 
        de cada punto a su centroide) para diferentes valores de K.
        
        ### Inercia (Within-Cluster Sum of Squares - WCSS)
        
        $$
        \\text{Inercia} = \\sum_{i=1}^{K} \\sum_{x \\in C_i} \\|x - \\mu_i\\|^2
        $$
        
        Donde:
        - $K$ = número de clusters
        - $C_i$ = cluster i
        - $\\mu_i$ = centroide del cluster i
        - $x$ = punto de datos
        
        ### Interpretación
        
        - Graficamos **Inercia vs K**
        - La inercia **siempre decrece** al aumentar K
        - Buscamos el **"codo"** = punto donde la reducción de inercia se desacelera
        - **Codo** = balance entre complejidad (K alto) y calidad de clustering
        
        💡 **Ejemplo**: Si la inercia baja mucho de K=2 a K=3, pero poco de K=3 a K=4, 
        entonces K=3 es probablemente óptimo.
        """)
    
    with st.expander("📏 Métricas de Evaluación", expanded=False):
        st.markdown("""
        ### 1. Silhouette Score (-1 a 1)
        
        Mide qué tan bien está asignado cada punto a su cluster comparado con otros clusters.
        
        $$
        s(i) = \\frac{b(i) - a(i)}{\\max(a(i), b(i))}
        $$
        
        - $a(i)$ = distancia promedio intra-cluster
        - $b(i)$ = distancia promedio al cluster más cercano
        
        **Interpretación:**
        - **> 0.7**: Excelente separación
        - **0.5-0.7**: Buena estructura
        - **0.25-0.5**: Estructura débil
        - **< 0.25**: Sin estructura clara
        
        ### 2. Fisher J4 (trace(SB)/trace(SW))
        
        Métrica académica que mide la **separación entre clusters** vs **cohesión intra-cluster**.
        
        - **SB** (Between-cluster scatter): Varianza ENTRE clusters
        - **SW** (Within-cluster scatter): Varianza DENTRO de clusters
        - **J4 alto** = clusters bien separados y compactos
        
        ### 3. Inercia (WCSS)
        
        Suma de distancias al cuadrado de puntos a sus centroides. 
        
        - **Menor inercia** = clusters más compactos
        - Usada en Elbow Method
        """)
    
    with st.expander("🎲 Inicialización: k-means++ vs Random", expanded=False):
        st.markdown("""
        ### k-means++ (Recomendado)
        
        Algoritmo inteligente propuesto por Arthur & Vassilvitskii (2007):
        
        1. Seleccionar primer centroide aleatoriamente
        2. Para cada centroide siguiente:
           - Calcular distancia de cada punto al centroide más cercano
           - Seleccionar siguiente centroide con probabilidad proporcional a distancia²
        3. Repetir hasta tener K centroides
        
        **Ventajas:**
        - Centroides iniciales bien distribuidos
        - Converge más rápido
        - Mejor calidad final
        - Menos sensible a outliers
        
        ### Random
        
        Selección aleatoria uniforme de K puntos del dataset.
        
        **Desventajas:**
        - Puede seleccionar centroides muy cercanos
        - Mayor variabilidad en resultados
        - Requiere más ejecuciones (n_init)
        
        💡 **Tip**: K-means se ejecuta `n_init` veces con diferentes inicializaciones 
        y se retorna el mejor resultado (menor inercia).
        """)

