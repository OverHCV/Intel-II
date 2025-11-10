"""
K-means Clustering Page.

Single Responsibility: Orchestrate K-means clustering workflow.
"""

import streamlit as st
import logging

from .theory import render_theory_section
from .controls import render_controls
from .trainer import train_kmeans_clustering
from .visualizations import render_all_results
from states import get_state, StateKeys

logger = logging.getLogger(__name__)


def render():
    """
    Main render function for K-means clustering page.
    """
    st.title("⭕ K-means Clustering")
    st.markdown("Fast partitional clustering with Elbow Method for optimal K finding.")
    st.markdown("---")
    
    # Theory section
    render_theory_section()
    
    st.markdown("---")
    
    # Check if data is prepared
    X_ready = get_state(StateKeys.X_PREPARED, None)
    y_ready = get_state(StateKeys.Y_PREPARED, None)
    
    if X_ready is None:
        st.warning("⚠️ No data prepared. Please go to **Dataset Review** page first.")
        st.info("👈 Use the sidebar to navigate to Dataset Review and prepare the data.")
        return
    
    st.success(f"✅ Data ready: {X_ready.shape[0]} samples, {X_ready.shape[1]} features")
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("## ⚙️ K-means Controls")
        params = render_controls()
    
    # Train model when button clicked
    if params['train_button']:
        with st.spinner("🔄 Running K-means clustering..."):
            try:
                results = train_kmeans_clustering(X_ready, params)
                
                # Display all results
                st.markdown("---")
                st.markdown("## 📊 Clustering Results")
                render_all_results(results)
                
            except Exception as e:
                st.error(f"❌ Error during clustering: {e}")
                logger.error(f"K-means clustering error: {e}", exc_info=True)
                import traceback
                with st.expander("🔍 Error Details"):
                    st.code(traceback.format_exc())


