"""
UI Controls for Dataset Review page.

Single Responsibility: Render all user input controls (selectboxes, sliders, checkboxes).
Returns user selections as a dictionary.
"""

import streamlit as st
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def render_controls() -> Dict[str, Any]:
    """
    Render all data control widgets and return user selections.
    
    CRITICAL: Uses st.session_state values for initialization to persist across tabs.
    Widget keys (e.g., "dataset_selection") are managed by Streamlit automatically.
    
    Returns:
        Dict with user selections: {
            'dataset': str,
            'target_strategy': str,
            'balance_method': str,
            'k_neighbors': int,
            'include_g1': bool,
            'include_g2': bool,
            'custom_thresh': str (optional)
        }
    """
    st.subheader("🎛️ Data Controls")
    
    # Dataset selection
    # Read current value from session_state (persists across tabs)
    current_dataset = st.session_state.get("dataset_selection", "Portuguese (Training - 649 students)")
    
    dataset = st.selectbox(
        "Select Dataset",
        ["Portuguese (Training - 649 students)",
         "Math (Test - 395 students)",
         "Both (Combined - 1044 students)"],
        index=["Portuguese (Training - 649 students)",
               "Math (Test - 395 students)",
               "Both (Combined - 1044 students)"].index(current_dataset) if current_dataset in [
            "Portuguese (Training - 649 students)",
            "Math (Test - 395 students)",
            "Both (Combined - 1044 students)"
        ] else 0,
        key="dataset_selection",
        help="Portuguese tiene más muestras (649) → mejor para entrenamiento. Math (395) prueba si los patrones generalizan entre materias."
    )
    
    st.markdown("---")
    
    # Target engineering
    st.subheader("🎯 Target Engineering")
    current_target = st.session_state.get("target_strategy", "Five-class (A/B/C/D/F)")
    
    target_strategy = st.selectbox(
        "G3 Transformation",
        ["Five-class (A/B/C/D/F)",
         "Binary (Pass/Fail at 10)",
         "Three-class (Low/Med/High)",
         "Custom thresholds"],
        index=["Five-class (A/B/C/D/F)",
               "Binary (Pass/Fail at 10)",
               "Three-class (Low/Med/High)",
               "Custom thresholds"].index(current_target) if current_target in [
            "Five-class (A/B/C/D/F)",
            "Binary (Pass/Fail at 10)",
            "Three-class (Low/Med/High)",
            "Custom thresholds"
        ] else 0,
        key="target_strategy",
        help="Binary (Pass/Fail) es simple y accionable. Multi-clase permite intervenciones más finas (e.g., estudiantes 'Medios' necesitan diferente apoyo que 'Bajos')."
    )
    
    custom_thresh = None
    if target_strategy == "Custom thresholds":
        custom_thresh = st.text_input(
            "Thresholds (comma-separated)",
            value=st.session_state.get("custom_thresholds", "10,14"),
            key="custom_thresholds",
            help="E.g., '10,14' creates 3 classes: [0-10), [10-14), [14-20]"
        )
    
    st.markdown("---")
    
    # Class balancing
    st.subheader("⚖️ Class Balancing")
    current_balance = st.session_state.get("balance_method", "SMOTE")
    
    balance_method = st.selectbox(
        "Balancing Method",
        ["SMOTE", "Random Oversample", "Random Undersample", "None"],
        index=["SMOTE", "Random Oversample", "Random Undersample", "None"].index(current_balance) if current_balance in [
            "SMOTE", "Random Oversample", "Random Undersample", "None"
        ] else 0,
        key="balance_method",
        help="SMOTE (default) crea ejemplos sintéticos (mejor para datos desbalanceados). None si ya está balanceado. Random Oversample duplica. Random Undersample pierde datos.",
    )
    
    k_neighbors = 5  # Default
    if balance_method == "SMOTE":
        k_neighbors = st.slider(
            "K-neighbors", 
            1, 10, 
            value=st.session_state.get("k_neighbors", 5),
            key="k_neighbors",
            help="SMOTE crea muestras sintéticas interpolando entre k vecinos más cercanos. Mayor k = más diversidad pero riesgo de incluir clase incorrecta."
        )
    
    st.markdown("---")
    
    # G1/G2 Inclusion (Optional features)
    st.subheader("📝 Notas Previas")
    
    col_g1, col_g2, col_feat = st.columns([1, 1, 1])
    
    with col_g1:
        include_g1 = st.checkbox(
            "Include G1", 
            value=st.session_state.get("include_g1", False),
            key="include_g1",
            help="Primera nota del periodo"
        )
    
    with col_g2:
        include_g2 = st.checkbox(
            "Include G2", 
            value=st.session_state.get("include_g2", False),
            key="include_g2",
            help="Segunda nota del periodo"
        )
    
    with col_feat:
        n_features = 30 + int(include_g1) + int(include_g2)
        st.metric("Features", n_features)
    
    st.markdown("---")
    
    # Return all selections
    return {
        'dataset': dataset,
        'target_strategy': target_strategy,
        'balance_method': balance_method,
        'k_neighbors': k_neighbors,
        'include_g1': include_g1,
        'include_g2': include_g2,
        'custom_thresh': custom_thresh
    }

