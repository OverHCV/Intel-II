"""
SVM Page - Support Vector Machine Interactive Analysis
Modular architecture with separated concerns
"""

import streamlit as st
from ui.pages.svm.components import (
    render_best_model_saver,
    render_model_configuration,
    render_visualizations,
)
from ui.pages.svm.docs import render_svm_documentation
from ui.pages.svm.experiments import render_experiment_history
from ui.utils.state_manager import get_data


def svm_page():
    """
    SVM interactive tab content
    Task 1: Test different kernels and parameters
    """
    st.title("🔍 Support Vector Machine (SVM)")
    st.markdown("Explore different kernels and hyperparameters for classification")

    # Check if data is loaded
    X, y, feature_names, data_info = get_data()

    if X is None:
        st.warning("⚠️ Please load data in the **Config** tab first!")
        return

    # Documentation Section
    render_svm_documentation()

    st.divider()

    # Model Configuration Section
    # Only show when no model trained, or always available in compact form
    render_model_configuration()

    # Visualizations Section
    st.divider()
    render_visualizations()

    # Experiment History Section
    render_experiment_history(st.session_state.svm)

    # Save Best Model Section
    render_best_model_saver()
