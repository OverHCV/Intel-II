"""
Visualizations Component
Side-by-side confusion matrix + metrics bar chart
"""

import streamlit as st
from funcs.visualizers import plot_confusion_matrix, plot_metrics_bars


def render_visualizations(X, y, data_info):
    """
    Render visualizations panel with side-by-side layout
    
    Args:
        X: Feature matrix
        y: Target labels
        data_info: Dataset information dictionary
    """
    st.subheader("📈 Visualizations")

    if st.session_state.ann["is_trained"]:
        # Get data
        y_true = st.session_state.ann["y_true"]
        y_pred = st.session_state.ann["y_pred"]
        metrics = st.session_state.ann["metrics"]

        # Get class names
        if data_info:
            labels = data_info["classes"]
        else:
            labels = ["Class 0", "Class 1"]

        # Side-by-side layout
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Confusion Matrix**")
            fig_cm = plot_confusion_matrix(y_true, y_pred, labels=labels)
            st.pyplot(fig_cm)

        with col2:
            st.markdown("**Performance Metrics**")
            # Filter only 0-1 metrics for bar chart
            plot_metrics = {k: v for k, v in metrics.items() if 0 <= v <= 1}

            if plot_metrics:
                fig_metrics = plot_metrics_bars(plot_metrics)
                st.pyplot(fig_metrics)
            else:
                st.info("K-Fold CV metrics (not 0-1 range)")

        st.caption(
            f"⏱️ Training time: {st.session_state.ann['training_time']:.2f}s"
        )

    else:
        st.info("🦜 Configure parameters and click **Train ANN** to see results 👈")

