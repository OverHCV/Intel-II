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

# Sidebar info (collapsed by default)
with st.sidebar:
    st.markdown("### 📁 Active Dataset")
    dataset_name = get_state(StateKeys.DATASET_NAME, "None loaded")
    st.info(dataset_name)
    
    st.markdown("### 🎯 Development Progress")
    st.progress(0.2, text="Phase 1: BFS Complete")
    
    st.markdown("### ℹ️ About")
    st.markdown("""
    **Architecture**: 4-Layer  
    **Approach**: BFS (Skeleton-first)  
    **Status**: Navigable prototype
    """)

# Route to appropriate page content
if current_page == "Home":
    st.markdown("""
    ## 🏠 Welcome to Student Performance Analysis
    
    This application provides comprehensive ML analysis of student data using
    **classification** (Decision Trees) and **clustering** (Hierarchical, K-means).
    """)
    
    with st.expander("📚 THEORY: Why This Project Matters", expanded=False):
        st.markdown("""
        ### Educational Context
        
        **WHY ML in Education?**
        - Early identification of at-risk students
        - Personalized intervention strategies
        - Understanding factors that influence success
        - Data-driven educational policy
        
        ### Datasets
        
        - **Portuguese Dataset**: 649 students → **TRAINING SET** (more samples)
        - **Math Dataset**: 395 students → **TEST SET** (cross-domain validation)
        - **Features**: 33 attributes (demographic, social, school-related)
        - **Target**: G3 score (0-20) → categorical transformation
        
        ### Approach
        
        1. Train on Portuguese (larger dataset)
        2. Test on Math (different subject - tests generalization)
        3. Reflect: Do patterns transfer across subjects?
        """)
    
    st.markdown("### 🎯 Project Objectives")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Classification (Decision Trees)
        - **Build**: CART algorithm for pass/fail prediction
        - **Extract**: Human-readable IF-THEN rules
        - **Analyze**: Feature importance and rule ranking
        - **Validate**: Cross-validation for robustness
        
        **WHY**: Teachers need interpretable models, not black boxes.
        """)
    
    with col2:
        st.markdown("""
        #### Clustering (Hierarchical & K-means)
        - **Discover**: Natural student groupings
        - **Compare**: Different linkage methods
        - **Optimize**: Find optimal number of clusters (J4 criterion)
        - **Profile**: Generate cluster descriptions
        
        **WHY**: Reveals hidden patterns classification might miss.
        """)
    
    st.markdown("### 🚀 Getting Started")
    st.info("👆 Use the **horizontal navigation tabs above** to explore different analysis sections.")
    
    # Quick stats
    st.markdown("### 📊 Architecture Overview")
    metric_cols = st.columns(4)
    with metric_cols[0]:
        st.metric("Core Modules", "4", "ML algorithms")
    with metric_cols[1]:
        st.metric("Versioning", "3", "Experiment tracking")
    with metric_cols[2]:
        st.metric("UI Pages", "6", "Fully navigable")
    with metric_cols[3]:
        st.metric("Development", "BFS", "Skeleton-first")

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
