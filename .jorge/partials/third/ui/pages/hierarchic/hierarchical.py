"""
Hierarchical Clustering Page - Orchestrator.

Single Responsibility: Coordinate theory, controls, training, and visualizations.
"""

import streamlit as st
import logging

from .theory import render_theory_section
from .controls import render_controls
from .trainer import train_hierarchical_clustering
from .visualizations import render_all_results
from states import get_state, StateKeys

logger = logging.getLogger(__name__)


def render():
    """
    Orchestrate the Hierarchical Clustering page.
    
    Flow:
    1. Render theory expander
    2. Check if data is ready
    3. Render clustering controls
    4. Cluster button → train model → display results
    5. Show experiment history (TODO)
    """
    # Theory section
    render_theory_section()
    
    st.markdown("## 🔗 Hierarchical Clustering")
    
    # Check if data is ready
    X_ready = get_state(StateKeys.X_PREPARED, None)
    
    if X_ready is None:
        st.warning("⚠️ No prepared data found!")
        st.info("👈 Go to **Dataset Review** first to prepare your data.")
        return
    
    st.success(f"✅ Data loaded: {X_ready.shape[0]} samples, {X_ready.shape[1]} features")
    
    st.info("""
    ℹ️ **Nota sobre targets en Clustering**: 
    Clustering es **unsupervised** (no usa etiquetas G3). Solo agrupa estudiantes por similitud
    en sus características demográficas/sociales/comportamentales. Las etiquetas G3 se usan
    **después** para interpretar qué tipo de estudiantes están en cada cluster.
    """)
    
    # Render controls and get parameters
    params = render_controls()
    
    # Cluster button
    if st.button("🚀 Run Hierarchical Clustering", type="primary"):
        with st.spinner("🌀 Clustering students..."):
            try:
                # Train clustering and get all results
                results = train_hierarchical_clustering(X_ready, params)
                
                # Display all results
                render_all_results(results)
                
            except Exception as e:
                st.error(f"❌ Error during clustering: {str(e)}")
                logger.error(f"Hierarchical clustering error: {e}", exc_info=True)
                import traceback
                st.code(traceback.format_exc())
    
    st.markdown("---")
    
    # TODO: Experiment history (similar to decision_tree)
    st.markdown("### 📊 Experiment History")
    history = get_state("experiment_history_hc", [])
    if len(history) == 0:
        st.info("No hay experimentos guardados aún. Ejecuta clustering para empezar!")
    else:
        st.success(f"✅ {len(history)} experimento(s) guardado(s) en esta sesión")
        
        # Simple history table
        import pandas as pd
        history_data = []
        for exp in history:
            history_data.append({
                "ID": exp["id"],
                "Timestamp": exp["timestamp"].split("T")[1][:8] if "T" in exp["timestamp"] else exp["timestamp"],
                "K": exp["params"]["n_clusters"],
                "Linkage": exp["params"]["linkage_method"],
                "Distance": exp["params"]["distance_metric"],
                "Silhouette": f"{exp['metrics']['silhouette_avg']:.4f}",
                "Optimal K (J4)": exp["j4_analysis"]["optimal_k"] if exp["j4_analysis"] else "N/A"
            })
        
        df_history = pd.DataFrame(history_data)
        st.dataframe(df_history, width="stretch", height=200)
        
        # Clear history button
        if st.button("🗑️ Limpiar Historial", type="secondary"):
            st.session_state["experiment_history_hc"] = []
            st.rerun()
