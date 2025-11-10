"""
UI Controls for K-means Clustering page.

Single Responsibility: Render and manage all user input widgets.
"""

import streamlit as st


def render_controls():
    """
    Render K-means clustering control panel.
    
    Returns:
        dict: Dictionary with clustering parameters
    """
    st.markdown("### ⚙️ Clustering Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        n_clusters = st.slider(
            "Number of Clusters (K)",
            min_value=2,
            max_value=15,
            value=st.session_state.get("km_n_clusters", 5),
            key="km_n_clusters",
            help="Número de clusters a formar. Usa Elbow Method para encontrar el K óptimo."
        )
    
    with col2:
        init_method = st.selectbox(
            "Initialization Method",
            options=["k-means++", "random"],
            index=0 if st.session_state.get("km_init_method", "k-means++") == "k-means++" else 1,
            key="km_init_method",
            help="k-means++: Inicialización inteligente (recomendado).\nrandom: Selección aleatoria de centroides."
        )
    
    col3, col4 = st.columns(2)
    
    with col3:
        n_init = st.number_input(
            "Number of Initializations (n_init)",
            min_value=1,
            max_value=50,
            value=st.session_state.get("km_n_init", 10),
            key="km_n_init",
            help="Número de veces que se ejecuta el algoritmo con diferentes centroides iniciales. Se retorna el mejor resultado."
        )
    
    with col4:
        max_iter = st.number_input(
            "Max Iterations",
            min_value=50,
            max_value=1000,
            value=st.session_state.get("km_max_iter", 300),
            key="km_max_iter",
            help="Número máximo de iteraciones del algoritmo K-means."
        )
    
    st.markdown("---")
    
    # Elbow Method analysis
    st.markdown("### 📊 Elbow Method (Optimal K Finder)")
    
    col_e1, col_e2, col_e3 = st.columns(3)
    
    with col_e1:
        run_elbow = st.checkbox(
            "Run Elbow Analysis",
            value=st.session_state.get("km_run_elbow", False),
            key="km_run_elbow",
            help="Ejecuta Elbow Method para encontrar el K óptimo evaluando la inercia para diferentes K. Puede tardar ~30-60 seg."
        )
    
    with col_e2:
        elbow_k_min = st.number_input(
            "K Min",
            min_value=2,
            max_value=9,
            value=st.session_state.get("km_elbow_k_min", 2),
            key="km_elbow_k_min",
            help="K mínimo a evaluar en Elbow analysis.",
            disabled=not run_elbow
        )
    
    with col_e3:
        elbow_k_max = st.number_input(
            "K Max",
            min_value=3,
            max_value=20,
            value=st.session_state.get("km_elbow_k_max", 10),
            key="km_elbow_k_max",
            help="K máximo a evaluar en Elbow analysis.",
            disabled=not run_elbow
        )
    
    st.markdown("---")
    
    # Train button
    train_button = st.button(
        "🚀 Run K-means Clustering",
        type="primary",
        use_container_width=True,
        help="Ejecuta K-means con los parámetros configurados."
    )
    
    return {
        'n_clusters': n_clusters,
        'init_method': init_method,
        'n_init': n_init,
        'max_iter': max_iter,
        'run_elbow': run_elbow,
        'elbow_k_min': elbow_k_min,
        'elbow_k_max': elbow_k_max,
        'train_button': train_button
    }

