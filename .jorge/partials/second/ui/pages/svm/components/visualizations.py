"""
Visualizations Component
Handles SVM model performance visualizations
(Feature Analysis & Data Exploration moved to PCA tab)
"""

import streamlit as st
from funcs.visual.basic_visuals import (
    plot_confusion_matrix,
    plot_metrics_bars,
)
from ui.utils.state_manager import get_data


def render_visualizations():
    """
    Render SVM model performance visualizations
    Note: Feature Analysis & Data Exploration tabs moved to PCA section
    """
    if not st.session_state.svm["is_trained"]:
        st.info("🦜 Configure parameters and click **Train SVM** to see results 👉")
        return

    st.subheader("📊 Model Performance")
    _render_model_performance()


def _render_model_performance():
    """Render Model Performance with confusion matrix and metrics"""
    X, y, feature_names, data_info = get_data()
    y_true = st.session_state.svm["y_true"]
    y_pred = st.session_state.svm["y_pred"]

    if data_info:
        labels = data_info["classes"]
    else:
        labels = ["Class 0", "Class 1"]

    # Show graphs side by side with better proportions
    col_cm, col_metrics = st.columns([1.2, 1])

    with col_cm:
        # Confusion Matrix
        fig_cm = plot_confusion_matrix(y_true, y_pred, labels=labels)
        st.pyplot(fig_cm)

    with col_metrics:
        # Metrics bar chart
        metrics = st.session_state.svm["metrics"]
        # Only plot metrics that are between 0 and 1
        plot_metrics = {k: v for k, v in metrics.items() if 0 <= v <= 1}

        if plot_metrics:
            fig_metrics = plot_metrics_bars(plot_metrics)
            st.pyplot(fig_metrics)

    st.caption(f"⏱️ Training time: {st.session_state.svm['training_time']:.2f}s")
    st.caption("💡 For feature analysis and data exploration, see the **PCA** tab →")
