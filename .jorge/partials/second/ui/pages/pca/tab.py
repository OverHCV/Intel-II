"""
PCA Page - Principal Component Analysis & Comparison
"""

import streamlit as st
from ui.pages.pca.components import (
    render_model_comparison,
    render_overall_analysis,
    render_pca_visualizations,
)
from ui.pages.pca.docs import render_pca_documentation
from ui.utils.state_manager import get_data


def pca_page():
    """
    PCA interactive tab content
    Task 3: Apply PCA and compare with original models
    """
    st.title("📈 PCA Analysis & Comparison")
    st.markdown("Apply dimensionality reduction and compare performance")

    # Check if data is loaded
    X, y, feature_names, data_info = get_data()

    if X is None:
        st.warning("⚠️ Please load data in the sidebar first!")
        return

    # Documentation Section
    render_pca_documentation()

    st.divider()

    # Visualizations (Feature Analysis, Data Exploration & PCA Transformation)
    render_pca_visualizations()

    st.divider()

    # Model Comparison (SVM and ANN with PCA)
    render_model_comparison()

    st.divider()

    # Overall Analysis & Conclusions
    render_overall_analysis()
