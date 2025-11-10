"""
UI Controls for Hierarchical Clustering page.

Single Responsibility: Render all clustering parameter controls.
"""

import streamlit as st
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def render_controls() -> Dict[str, Any]:
    """
    Render all hierarchical clustering control widgets.
    
    Uses st.session_state values for initialization to persist across tabs.
    Widget keys are managed by Streamlit automatically.
    
    Returns:
        Dict with user selections: {
            'n_clusters': int,
            'linkage_method': str,
            'distance_metric': str,
            'find_optimal_k': bool,
            'k_range_min': int,
            'k_range_max': int
        }
    """
    st.markdown("### ⚙️ Clustering Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        n_clusters = st.slider(
            "Number of Clusters (K)",
            min_value=2,
            max_value=10,
            value=st.session_state.get("hc_n_clusters", 3),
            key="hc_n_clusters",
            help="Número de clusters a formar. Menor = grupos más generales, Mayor = grupos más específicos."
        )
    
    with col2:
        linkage_options = ["ward", "complete", "average", "single"]
        current_linkage = st.session_state.get("hc_linkage_method", "ward")
        linkage_index = linkage_options.index(current_linkage) if current_linkage in linkage_options else 0
        
        linkage_method = st.selectbox(
            "Linkage Method",
            linkage_options,
            index=linkage_index,
            key="hc_linkage_method",
            help="Ward = minimiza varianza (solo euclidean).\nComplete = clusters compactos.\nAverage = balanceado.\nSingle = puede crear cadenas."
        )
    
    with col3:
        # Ward only works with euclidean distance
        if linkage_method == "ward":
            distance_metric = "euclidean"
            st.selectbox(
                "Distance Metric",
                ["euclidean"],
                index=0,
                key="hc_distance_metric_disabled",
                help="⚠️ Ward linkage solo funciona con distancia Euclidean.",
                disabled=True
            )
        else:
            distance_options = ["euclidean", "cityblock", "cosine"]
            current_distance = st.session_state.get("hc_distance_metric", "euclidean")
            distance_index = distance_options.index(current_distance) if current_distance in distance_options else 0
            
            distance_metric = st.selectbox(
                "Distance Metric",
                distance_options,
                index=distance_index,
                key="hc_distance_metric",
                help="Euclidean = distancia recta.\nCityblock (Manhattan) = distancia ciudad.\nCosine = similitud angular."
            )
    
    st.markdown("---")
    
    # Optimal K finding
    st.markdown("### 🎯 Find Optimal K (J4 Analysis)")
    
    col_k1, col_k2, col_k3 = st.columns(3)
    
    with col_k1:
        find_optimal_k = st.checkbox(
            "Run J4 Analysis",
            value=st.session_state.get("hc_find_optimal_k", False),
            key="hc_find_optimal_k",
            help="Ejecuta Silhouette Analysis para encontrar el K óptimo. Puede tardar ~30 seg para K=2-10."
        )
    
    with col_k2:
        k_range_min = st.number_input(
            "K Min",
            min_value=2,
            max_value=9,
            value=st.session_state.get("hc_k_range_min", 2),
            key="hc_k_range_min",
            help="K mínimo a evaluar en J4 analysis.",
            disabled=not find_optimal_k
        )
    
    with col_k3:
        k_range_max = st.number_input(
            "K Max",
            min_value=3,
            max_value=15,
            value=st.session_state.get("hc_k_range_max", 10),
            key="hc_k_range_max",
            help="K máximo a evaluar en J4 analysis.",
            disabled=not find_optimal_k
        )
    
    st.markdown("---")
    
    return {
        'n_clusters': n_clusters,
        'linkage_method': linkage_method,
        'distance_metric': distance_metric,
        'find_optimal_k': find_optimal_k,
        'k_range_min': k_range_min,
        'k_range_max': k_range_max
    }

