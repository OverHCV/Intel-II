"""
UI Controls for Decision Tree page.

Single Responsibility: Render all hyperparameter and validation controls.
"""

import streamlit as st
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def render_controls() -> Dict[str, Any]:
    """
    Render all hyperparameter and validation control widgets.
    
    Uses st.session_state values for initialization to persist across tabs.
    Widget keys are managed by Streamlit automatically.
    
    Returns:
        Dict with user selections: {
            'max_depth': int,
            'min_samples_split': int,
            'criterion': str,
            'test_size': float,
            'cv_folds': int
        }
    """
    st.markdown("### ⚙️ Hyperparameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        max_depth = st.slider(
            "Max Depth",
            min_value=1,
            max_value=20,
            value=st.session_state.get("dt_max_depth", 5),
            key="dt_max_depth",
            help="Controla complejidad del árbol. Menor = reglas simples, mayor = más específico pero riesgo overfitting."
        )
    
    with col2:
        min_samples_split = st.slider(
            "Min Samples Split",
            min_value=2,
            max_value=20,
            value=st.session_state.get("dt_min_samples_split", 10),
            key="dt_min_samples_split",
            help="Mínimo de muestras necesarias para dividir un nodo. Mayor = más conservador, previene divisiones pequeñas."
        )
    
    with col3:
        criterion_options = ["gini", "entropy"]
        current_criterion = st.session_state.get("dt_criterion", "gini")
        criterion_index = criterion_options.index(current_criterion) if current_criterion in criterion_options else 0
        
        criterion = st.selectbox(
            "Split Criterion",
            criterion_options,
            index=criterion_index,
            key="dt_criterion",
            help="Gini = más rápido, Entropy (info gain) = ligeramente más preciso. Resultados similares."
        )
    
    st.markdown("---")
    
    # Validation controls
    st.markdown("### 🎯 Validation Settings")
    
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        test_size_pct = st.slider(
            "Test Size (%)",
            min_value=10,
            max_value=40,
            value=st.session_state.get("dt_test_size_pct", 20),
            step=5,
            key="dt_test_size_pct",
            help="Porcentaje de datos para testing. 20% es estándar (80% train, 20% test)."
        )
    
    with col_v2:
        cv_folds = st.slider(
            "Cross-Validation Folds",
            min_value=2,
            max_value=10,
            value=st.session_state.get("dt_cv_folds", 5),
            key="dt_cv_folds",
            help="Número de folds para CV. 5-10 es estándar. Mayor = más robusto pero más lento."
        )
    
    st.markdown("---")
    
    return {
        'max_depth': max_depth,
        'min_samples_split': min_samples_split,
        'criterion': criterion,
        'test_size': test_size_pct / 100,  # Convert to decimal
        'cv_folds': cv_folds
    }

