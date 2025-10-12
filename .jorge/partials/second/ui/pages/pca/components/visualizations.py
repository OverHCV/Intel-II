"""
PCA Visualizations Component
Feature Analysis & Data Exploration (moved from SVM)
Plus PCA-specific visualizations
"""

import streamlit as st
from funcs.visual.basic_visuals import (
    plot_correlation_heatmap,
    plot_feature_boxplots,
    plot_feature_distributions,
    plot_interactive_scatter_2d,
    plot_interactive_scatter_3d,
    plot_qq_plots,
)
from ui.pages.pca.components.pca_transformer import render_pca_transformer
from ui.utils.state_manager import get_data


def render_pca_visualizations():
    """
    Render PCA visualization tabs
    Includes Feature Analysis & Data Exploration from original space
    """
    X, y, feature_names, data_info = get_data()

    if X is None:
        st.info("📊 Load data to see visualizations")
        return

    st.subheader("📈 Data Analysis & Exploration")

    # Create tabs
    viz_tabs = st.tabs(
        [
            "🔬 Feature Analysis",
            "🗺️ Data Exploration",
            "📊 PCA Transformation",
        ]
    )

    # Tab 1: Feature Analysis
    with viz_tabs[0]:
        _render_feature_analysis_tab(X, y, feature_names, data_info)

    # Tab 2: Data Exploration
    with viz_tabs[1]:
        _render_data_exploration_tab(X, y, feature_names, data_info)

    # Tab 3: PCA Transformation
    with viz_tabs[2]:
        render_pca_transformer(X, y, feature_names)


def _render_feature_analysis_tab(X, y, feature_names, data_info):
    """Render Feature Analysis tab with comprehensive statistical visualizations"""
    st.markdown("### 📊 Comprehensive Feature Analysis")
    st.markdown(
        "Deep dive into feature distributions, correlations, and statistical properties"
    )

    # Row 1: Correlation Heatmap + Box Plots (side by side)
    st.markdown("#### 🔗 Correlations & Outlier Detection")
    col1, col2 = st.columns([1.3, 1])

    with col1:
        # Correlation heatmap
        fig_corr = plot_correlation_heatmap(
            X, feature_names, "Feature Correlation Matrix"
        )
        st.pyplot(fig_corr)
        st.caption(
            "💡 **Correlation:** Strong values (±0.7+) indicate redundant features. "
            "Red = negative, Blue = positive."
        )

    with col2:
        # Box plots for outlier detection
        fig_box = plot_feature_boxplots(X, feature_names, y, "Outlier Detection")
        st.pyplot(fig_box)
        st.caption(
            "💡 **Box Plots:** Diamonds = outliers. Red diamond = mean. "
            "Box shows quartiles (Q1, median, Q3)."
        )

    st.divider()

    # Row 2: Feature selector and distribution plots
    st.markdown("#### 📈 Distribution Analysis")
    st.markdown("Analyze feature distributions and normality")

    # Feature selector for distributions
    col_select1, col_select2, col_select3, col_select4 = st.columns(4)

    default_indices = [
        0,
        1,
        min(2, len(feature_names) - 1),
        min(3, len(feature_names) - 1),
    ]

    with col_select1:
        feat1 = st.selectbox(
            "Feature 1", feature_names, index=default_indices[0], key="pca_dist_feat1"
        )
    with col_select2:
        feat2 = st.selectbox(
            "Feature 2", feature_names, index=default_indices[1], key="pca_dist_feat2"
        )
    with col_select3:
        feat3 = st.selectbox(
            "Feature 3", feature_names, index=default_indices[2], key="pca_dist_feat3"
        )
    with col_select4:
        feat4 = st.selectbox(
            "Feature 4", feature_names, index=default_indices[3], key="pca_dist_feat4"
        )

    # Get selected indices
    selected_indices = [
        feature_names.index(feat1),
        feature_names.index(feat2),
        feature_names.index(feat3),
        feature_names.index(feat4),
    ]

    # Distribution plots with KDE and normal curve overlay
    fig_dist = plot_feature_distributions(X, feature_names, selected_indices)
    st.pyplot(fig_dist)

    st.caption(
        "💡 **Distribution:** Blue histogram = actual data. "
        "Red line = Kernel Density Estimate (KDE). Green dashed = Normal distribution reference. "
        "μ = mean, σ = standard deviation."
    )

    st.divider()

    # Row 3: Q-Q Plots for normality testing
    st.markdown("#### 🎯 Normality Tests (Q-Q Plots)")
    st.markdown(
        "Test if features follow normal distribution (important for many ML algorithms)"
    )

    fig_qq = plot_qq_plots(X, feature_names, selected_indices)
    st.pyplot(fig_qq)

    st.caption(
        "💡 **Q-Q Plots:** Points on red line = normally distributed. "
        "Green box = passes Shapiro-Wilk test (p>0.05). "
        "Red box = significantly non-normal."
    )


def _render_data_exploration_tab(X, y, feature_names, data_info):
    """Render Data Exploration tab with both 2D and 3D scatter plots side by side"""
    st.markdown("### 🗺️ Interactive Data Exploration")
    st.markdown(
        "Explore feature relationships with side-by-side 2D and 3D visualizations"
    )

    # Get class names from data_info
    if data_info and "classes" in data_info:
        class_names = data_info["classes"]
    else:
        class_names = None

    # Two-column layout: 2D on left, 3D on right
    col_2d, col_3d = st.columns(2)

    # ========== 2D SCATTER PLOT ==========
    with col_2d:
        st.markdown("#### 📊 2D Scatter Plot")

        # 2D Selectors (stacked vertically)
        x_feature_2d = st.selectbox(
            "X-Axis", feature_names, index=0, key="pca_scatter_2d_x"
        )
        y_feature_2d = st.selectbox(
            "Y-Axis",
            feature_names,
            index=min(1, len(feature_names) - 1),
            key="pca_scatter_2d_y",
        )

        # Get indices
        x_idx_2d = feature_names.index(x_feature_2d)
        y_idx_2d = feature_names.index(y_feature_2d)

        # Plot 2D
        fig_2d = plot_interactive_scatter_2d(
            X, y, feature_names, x_idx_2d, y_idx_2d, class_names, "2D Feature Space"
        )
        st.pyplot(fig_2d)
        st.caption("💡 **2D View:** Analyze relationships between two features")

    # ========== 3D SCATTER PLOT ==========
    with col_3d:
        st.markdown("#### 🎲 3D Scatter Plot")

        # 3D Selectors (stacked vertically)
        x_feature_3d = st.selectbox(
            "X-Axis", feature_names, index=0, key="pca_scatter_3d_x"
        )
        y_feature_3d = st.selectbox(
            "Y-Axis",
            feature_names,
            index=min(1, len(feature_names) - 1),
            key="pca_scatter_3d_y",
        )
        z_feature_3d = st.selectbox(
            "Z-Axis",
            feature_names,
            index=min(2, len(feature_names) - 1),
            key="pca_scatter_3d_z",
        )

        # Get indices
        x_idx_3d = feature_names.index(x_feature_3d)
        y_idx_3d = feature_names.index(y_feature_3d)
        z_idx_3d = feature_names.index(z_feature_3d)

        # Try plotly 3D first, fallback to matplotlib 2D
        fig_3d = plot_interactive_scatter_3d(
            X,
            y,
            feature_names,
            x_idx_3d,
            y_idx_3d,
            z_idx_3d,
            class_names,
            "3D Feature Space",
        )

        if fig_3d is not None:
            st.plotly_chart(fig_3d, width="stretch")
            st.caption(
                "💡 **3D View:** Drag to rotate, scroll to zoom, double-click to reset"
            )
        else:
            st.warning("⚠️ Plotly not available. Showing 2D fallback.")
            fig_2d_fallback = plot_interactive_scatter_2d(
                X, y, feature_names, x_idx_3d, y_idx_3d, class_names, "2D Fallback"
            )
            st.pyplot(fig_2d_fallback)
            st.caption("💡 Install plotly for interactive 3D: `pip install plotly`")


