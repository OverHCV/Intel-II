"""
Main App - Streamlit application with horizontal navigation.

Run with: streamlit run app.py
"""

import streamlit as st
from pathlib import Path
import sys
from ui.state_manager import init_state, get_state, set_state, StateKeys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


# Configure page
st.set_page_config(
    page_title="Student Performance Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize state
init_state(StateKeys.CURRENT_PAGE, "Home")

# App Header with gradient
st.markdown("""
<div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
            padding: 1.5rem 2rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
    <h1 style='color: white; margin: 0; font-size: 2rem;'>🎓 Student Performance Analysis</h1>
    <p style='color: #f0f0f0; margin: 0.5rem 0 0 0; font-size: 0.95rem;'>
        Machine Learning for Educational Data • Universidad de Caldas 2025
    </p>
</div>
""", unsafe_allow_html=True)

# Horizontal Navigation Bar
nav_cols = st.columns([1, 1, 1, 1, 1, 1])

nav_options = [
    ("🏠", "Home"),
    ("📊", "Dataset Review"),
    ("🌳", "Decision Trees"),
    ("🔗", "Hierarchical"),
    ("⭕", "K-means"),
    ("📈", "History")
]

current_page = get_state(StateKeys.CURRENT_PAGE, "Home")

for col, (emoji, page_name) in zip(nav_cols, nav_options):
    with col:
        button_type = "primary" if current_page == page_name else "secondary"
        if st.button(
            f"{emoji} {page_name}",
            key=f"nav_{page_name}",
            type=button_type,
            use_container_width=True
        ):
            set_state(StateKeys.CURRENT_PAGE, page_name)
            st.rerun()

st.markdown("---")

# Sidebar - App State (NOT project status)
with st.sidebar:
    st.markdown("### 📊 App State")
    
    # Dataset info
    dataset_loaded = get_state(StateKeys.DATASET_NAME, None)
    if dataset_loaded:
        st.success(f"✅ Dataset: {dataset_loaded}")
        
        # Show preprocessing state
        target_strategy = get_state(StateKeys.TARGET_STRATEGY, "Not set")
        st.info(f"🎯 Target: {target_strategy}")
        
        balance_method = get_state(StateKeys.BALANCE_METHOD, "None")
        st.info(f"⚖️ Balance: {balance_method}")
        
        # Show if data is prepared
        X_ready = get_state(StateKeys.X_PREPARED, None)
        y_ready = get_state(StateKeys.Y_PREPARED, None)
        if X_ready is not None and y_ready is not None:
            st.success(f"✅ Data Ready: {X_ready.shape[0]} samples")
        else:
            st.warning("⏳ Data not prepared")
    else:
        st.warning("⚠️ No dataset loaded")
        st.caption("Go to Dataset Review to load data")
    
    st.markdown("---")
    
    # Model state
    st.markdown("### 🤖 Models")
    dt_trained = get_state(StateKeys.DT_MODEL, None)
    if dt_trained:
        st.success("✅ Decision Tree trained")
    else:
        st.info("⏳ Decision Tree pending")
    
    hc_done = get_state(StateKeys.HC_LABELS, None)
    if hc_done:
        st.success("✅ Hierarchical done")
    else:
        st.info("⏳ Hierarchical pending")
    
    km_done = get_state(StateKeys.KM_LABELS, None)
    if km_done:
        st.success("✅ K-means done")
    else:
        st.info("⏳ K-means pending")

# Route to appropriate page content
if current_page == "Home":
    st.markdown("""
    ## 📚 Tercer Examen Parcial - Sistemas Inteligentes II
    
    ### Universidad de Caldas
    
    Este proyecto utiliza el dataset de rendimiento estudiantil del 
    [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php) 
    para aplicar técnicas de aprendizaje de máquina supervisado y no supervisado.
    
    ---
    """)
    
    # Exam Requirements
    st.markdown("### 📋 Requisitos del Examen")
    
    # Task 1 - Decision Trees
    with st.container():
        col_icon, col_content = st.columns([0.1, 0.9])
        with col_icon:
            st.markdown("### 🌳")
        with col_content:
            st.markdown("""
            **Tarea 1 (0.9 puntos): Árbol de Decisión CART**
            
            Entrenar un modelo CART o C4.5/ID3 para obtener un árbol de decisión y generar 
            reglas explícitas de clasificación. Analizar las reglas obtenidas, identificar 
            las más útiles (por pureza, cobertura y simplicidad), y realizar validación cruzada.
            """)
            st.progress(0.2, text="En desarrollo - Fase 1")
    
    st.markdown("---")
    
    # Task 2 - Hierarchical Clustering
    with st.container():
        col_icon, col_content = st.columns([0.1, 0.9])
        with col_icon:
            st.markdown("### 🔗")
        with col_content:
            st.markdown("""
            **Tarea 2 (0.9 puntos): Clustering Jerárquico**
            
            Usar el algoritmo de clustering jerárquico con los diferentes criterios de 
            enlazamiento (linkage) para agrupar los datos. Usando el criterio J4, analizar 
            los diferentes puntos de corte para el agrupamiento.
            """)
            st.progress(0.15, text="Pendiente - Fase 2")
    
    st.markdown("---")
    
    # Task 3 - K-means
    with st.container():
        col_icon, col_content = st.columns([0.1, 0.9])
        with col_icon:
            st.markdown("### ⭕")
        with col_content:
            st.markdown("""
            **Tarea 3 (0.7 puntos): K-means**
            
            Usando el número óptimo de clusters encontrado en el punto anterior, usar el 
            algoritmo k-means y evaluar nuevamente usando el criterio J4. Comparar con 
            clustering jerárquico.
            """)
            st.progress(0.1, text="Pendiente - Fase 3")
    
    st.markdown("---")
    
    # Task 4 - Presentation
    with st.container():
        col_icon, col_content = st.columns([0.1, 0.9])
        with col_icon:
            st.markdown("### 🎤")
        with col_content:
            st.markdown("""
            **Tarea 4 (2.5 puntos): Sustentación Oral**
            
            Presentación oral en horario de clase con análisis de resultados y conclusiones.
            """)
            st.progress(0.0, text="Pendiente - Final")
    
    st.markdown("---")
    
    # Dataset Info
    st.markdown("### 📊 Dataset: Student Performance")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Portuguese", "649 estudiantes", "Entrenamiento")
    with col2:
        st.metric("Math", "395 estudiantes", "Prueba cruzada")
    with col3:
        st.metric("Features", "33 atributos", "Mixtos")
    
    st.info("""
    **Estrategia**: Entrenar con Portuguese (mayor cantidad de datos), 
    validar con Math (generalización entre materias).
    """)
    
    # Getting Started
    st.markdown("### 🚀 Comenzar")
    
    st.markdown("""
    1. **📊 Dataset Review** → Explorar datos, balancear clases, ingeniar target
    2. **🌳 Decision Trees** → Entrenar CART, extraer reglas, validación cruzada
    3. **🔗 Hierarchical** → Dendrograma, diferentes linkages, análisis J4
    4. **⭕ K-means** → Encontrar k óptimo, comparar con jerárquico
    5. **📈 History** → Comparar experimentos, timeline de mejoras
    """)
    
    # st.success("👆 **Usa la navegación ** para acceder a cada sección.")

elif current_page == "Dataset Review":
    from ui.pages import dataset_review
    dataset_review.render()

elif current_page == "Decision Trees":
    from ui.pages import decision_tree
    decision_tree.render()

elif current_page == "Hierarchical":
    from ui.pages import hierarchical
    hierarchical.render()

elif current_page == "K-means":
    from ui.pages import kmeans
    kmeans.render()

elif current_page == "History":
    from ui.pages import history
    history.render()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.85rem;'>
    <p>Universidad de Caldas • Intelligence II • 2025</p>
    <p style='font-size: 0.75rem;'>Architecture: Data → Core → Versioning → UI | All files < 300 LOC</p>
</div>
""", unsafe_allow_html=True)
