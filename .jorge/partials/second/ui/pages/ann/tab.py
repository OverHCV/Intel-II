"""
ANN Page - Artificial Neural Network Interactive Analysis
"""

import streamlit as st
from ui.pages.ann.components import (
    render_best_model_saver,
    render_model_configuration,
    render_visualizations,
)
from ui.pages.ann.docs import render_ann_documentation
from ui.pages.ann.experiments import render_experiment_history
from ui.utils.state_manager import get_data


def ann_page():
    """
    ANN interactive tab content
    Task 2: Test different architectures and activations
    """
    st.title("🧠 Artificial Neural Network (ANN)")
    st.markdown("Explore architectures and activation functions")

    # Check if data is loaded
    X, y, feature_names, data_info = get_data()

    if X is None:
        st.warning("⚠️ Please load data in the sidebar first!")
        return

    # Render theory documentation
    render_ann_documentation()

    st.divider()

    # Two-column layout: controls on left, visualizations on right
    col_controls, col_viz = st.columns([1, 2])

    with col_controls:
        render_model_configuration(X, y, data_info)

    with col_viz:
        render_visualizations(X, y, data_info)

    # Experiment history (full width)
    render_experiment_history(st.session_state.ann)

    # Best model saver (full width)
    render_best_model_saver(X, y, data_info)
