"""
Visualizations Component
Handles all visualization tabs for SVM analysis
"""

import streamlit as st
from funcs.visualizers import (
    plot_confusion_matrix,
    plot_correlation_heatmap,
    plot_interactive_scatter_2d,
    plot_interactive_scatter_3d,
    plot_metrics_bars,
)
from ui.utils.state_manager import get_data


def render_visualizations():
    """
    Render visualization tabs (Model Performance, Feature Analysis, Data Exploration)
    """
    if not st.session_state.svm["is_trained"]:
        st.info("🦜 Configure parameters and click **Train SVM** to see results 👉")
        return

    st.subheader("📈 Visualizations")

    # Create tabs for organized visualizations
    viz_tabs = st.tabs(
        ["📊 Model Performance", "🔬 Feature Analysis", "🗺️ Data Exploration"]
    )

    # Tab 1: Model Performance
    with viz_tabs[0]:
        _render_model_performance_tab()

    # Tab 2: Feature Analysis
    with viz_tabs[1]:
        _render_feature_analysis_tab()

    # Tab 3: Data Exploration
    with viz_tabs[2]:
        _render_data_exploration_tab()


def _render_model_performance_tab():
    """Render Model Performance tab with confusion matrix and metrics"""
    st.markdown("### Confusion Matrix & Metrics")

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


def _render_feature_analysis_tab():
    """Render Feature Analysis tab with correlation heatmap"""
    st.markdown("### Feature Correlation Analysis")
    st.markdown("Understand relationships and dependencies between features")

    X, y, feature_names, data_info = get_data()

    # Plot correlation heatmap
    fig_corr = plot_correlation_heatmap(X, feature_names, "Feature Correlation Matrix")
    st.pyplot(fig_corr)

    st.caption(
        "💡 **Interpretation:** Strong correlations (±0.7+) may indicate redundant features. "
        "Red = negative correlation, Blue = positive correlation."
    )


def _render_data_exploration_tab():
    """Render Data Exploration tab with interactive scatter plots"""
    st.markdown("### Interactive Data Exploration")
    st.markdown("Explore relationships between features visually")

    X, y, feature_names, data_info = get_data()

    # Axis selectors
    col_x, col_y, col_z = st.columns(3)

    with col_x:
        x_feature = st.selectbox(
            "X Axis", options=feature_names, index=0, key="svm_scatter_x"
        )

    with col_y:
        y_feature = st.selectbox(
            "Y Axis",
            options=feature_names,
            index=min(1, len(feature_names) - 1),
            key="svm_scatter_y",
        )

    with col_z:
        enable_3d = st.checkbox("Enable 3D", value=False, key="svm_scatter_3d")

    # Get indices
    x_idx = feature_names.index(x_feature)
    y_idx = feature_names.index(y_feature)

    # Get class names from data_info
    if data_info and "classes" in data_info:
        class_names = data_info["classes"]
    else:
        class_names = None

    if enable_3d:
        # 3D scatter plot
        z_feature = st.selectbox(
            "Z Axis",
            options=feature_names,
            index=min(2, len(feature_names) - 1),
            key="svm_scatter_z",
        )
        z_idx = feature_names.index(z_feature)

        # Try plotly 3D first, fallback to matplotlib 2D
        fig_3d = plot_interactive_scatter_3d(
            X, y, feature_names, x_idx, y_idx, z_idx, class_names
        )

        if fig_3d is not None:
            st.plotly_chart(fig_3d, use_container_width=True)
            st.caption(
                "💡 **Tip:** Drag to rotate, scroll to zoom, double-click to reset"
            )
        else:
            st.warning("⚠️ Plotly not available. Showing 2D plot instead.")
            fig_2d = plot_interactive_scatter_2d(
                X, y, feature_names, x_idx, y_idx, class_names
            )
            st.pyplot(fig_2d)
    else:
        # 2D scatter plot
        fig_2d = plot_interactive_scatter_2d(
            X, y, feature_names, x_idx, y_idx, class_names
        )
        st.pyplot(fig_2d)
        st.caption("💡 **Tip:** Enable 3D to explore three features simultaneously")

