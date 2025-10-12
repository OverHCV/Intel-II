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
    """Render Data Exploration tab with multiple predefined 2D and 3D plots"""
    st.markdown("### 🗺️ Interactive Data Exploration")
    st.markdown(
        "Explore feature relationships with predefined comparisons"
    )

    # Get class names from data_info
    if data_info and "classes" in data_info:
        class_names = data_info["classes"]
    else:
        class_names = None

    n_features = len(feature_names)

    # ========== ROW 1: THREE 2D SCATTER PLOTS ==========
    st.markdown("#### 📊 2D Feature Comparisons")
    
    # Inline selectors (label and input on same row)
    col_sel1, col_sel2, col_sel3 = st.columns(3)
    
    with col_sel1:
        col_label1, col_input1 = st.columns([1, 2])
        with col_label1:
            st.markdown("**Plot 1:**")
        with col_input1:
            x1 = st.selectbox("X", feature_names, index=0, key="pca_2d_1_x", label_visibility="collapsed")
            y1 = st.selectbox("Y", feature_names, index=min(1, n_features-1), key="pca_2d_1_y", label_visibility="collapsed")
    
    with col_sel2:
        col_label2, col_input2 = st.columns([1, 2])
        with col_label2:
            st.markdown("**Plot 2:**")
        with col_input2:
            x2 = st.selectbox("X", feature_names, index=min(1, n_features-1), key="pca_2d_2_x", label_visibility="collapsed")
            y2 = st.selectbox("Y", feature_names, index=min(2, n_features-1), key="pca_2d_2_y", label_visibility="collapsed")
    
    with col_sel3:
        col_label3, col_input3 = st.columns([1, 2])
        with col_label3:
            st.markdown("**Plot 3:**")
        with col_input3:
            x3 = st.selectbox("X", feature_names, index=0, key="pca_2d_3_x", label_visibility="collapsed")
            y3 = st.selectbox("Y", feature_names, index=min(2, n_features-1), key="pca_2d_3_y", label_visibility="collapsed")

    # Render 2D plots
    col_2d1, col_2d2, col_2d3 = st.columns(3)
    
    with col_2d1:
        fig_2d1 = plot_interactive_scatter_2d(
            X, y, feature_names, 
            feature_names.index(x1), feature_names.index(y1), 
            class_names, f"{x1} vs {y1}"
        )
        st.pyplot(fig_2d1)
    
    with col_2d2:
        fig_2d2 = plot_interactive_scatter_2d(
            X, y, feature_names, 
            feature_names.index(x2), feature_names.index(y2), 
            class_names, f"{x2} vs {y2}"
        )
        st.pyplot(fig_2d2)
    
    with col_2d3:
        fig_2d3 = plot_interactive_scatter_2d(
            X, y, feature_names, 
            feature_names.index(x3), feature_names.index(y3), 
            class_names, f"{x3} vs {y3}"
        )
        st.pyplot(fig_2d3)

    st.caption("💡 **2D Views:** Compare different feature pairs to find separable patterns")

    st.divider()

    # ========== ROW 2: THREE 3D SCATTER PLOTS ==========
    st.markdown("#### 🎲 3D Feature Comparisons")
    
    # Inline selectors for 3D plots
    col_sel3d1, col_sel3d2, col_sel3d3 = st.columns(3)
    
    with col_sel3d1:
        col_label3d1, col_input3d1 = st.columns([1, 2])
        with col_label3d1:
            st.markdown("**3D Plot 1:**")
        with col_input3d1:
            x3d1 = st.selectbox("X", feature_names, index=0, key="pca_3d_1_x", label_visibility="collapsed")
            y3d1 = st.selectbox("Y", feature_names, index=min(1, n_features-1), key="pca_3d_1_y", label_visibility="collapsed")
            z3d1 = st.selectbox("Z", feature_names, index=min(2, n_features-1), key="pca_3d_1_z", label_visibility="collapsed")
    
    with col_sel3d2:
        col_label3d2, col_input3d2 = st.columns([1, 2])
        with col_label3d2:
            st.markdown("**3D Plot 2:**")
        with col_input3d2:
            x3d2 = st.selectbox("X", feature_names, index=min(1, n_features-1), key="pca_3d_2_x", label_visibility="collapsed")
            y3d2 = st.selectbox("Y", feature_names, index=min(2, n_features-1), key="pca_3d_2_y", label_visibility="collapsed")
            z3d2 = st.selectbox("Z", feature_names, index=min(3, n_features-1), key="pca_3d_2_z", label_visibility="collapsed")
    
    with col_sel3d3:
        col_label3d3, col_input3d3 = st.columns([1, 2])
        with col_label3d3:
            st.markdown("**3D Plot 3:**")
        with col_input3d3:
            x3d3 = st.selectbox("X", feature_names, index=0, key="pca_3d_3_x", label_visibility="collapsed")
            y3d3 = st.selectbox("Y", feature_names, index=min(2, n_features-1), key="pca_3d_3_y", label_visibility="collapsed")
            z3d3 = st.selectbox("Z", feature_names, index=min(3, n_features-1), key="pca_3d_3_z", label_visibility="collapsed")

    # Render 3D plots
    col_3d1, col_3d2, col_3d3 = st.columns(3)
    
    with col_3d1:
        fig_3d1 = plot_interactive_scatter_3d(
            X, y, feature_names,
            feature_names.index(x3d1), feature_names.index(y3d1), feature_names.index(z3d1),
            class_names, f"{x3d1}-{y3d1}-{z3d1}"
        )
        if fig_3d1 is not None:
            st.plotly_chart(fig_3d1, use_container_width=True)
        else:
            st.warning("⚠️ Plotly not available")
    
    with col_3d2:
        fig_3d2 = plot_interactive_scatter_3d(
            X, y, feature_names,
            feature_names.index(x3d2), feature_names.index(y3d2), feature_names.index(z3d2),
            class_names, f"{x3d2}-{y3d2}-{z3d2}"
        )
        if fig_3d2 is not None:
            st.plotly_chart(fig_3d2, use_container_width=True)
        else:
            st.warning("⚠️ Plotly not available")
    
    with col_3d3:
        fig_3d3 = plot_interactive_scatter_3d(
            X, y, feature_names,
            feature_names.index(x3d3), feature_names.index(y3d3), feature_names.index(z3d3),
            class_names, f"{x3d3}-{y3d3}-{z3d3}"
        )
        if fig_3d3 is not None:
            st.plotly_chart(fig_3d3, use_container_width=True)
        else:
            st.warning("⚠️ Plotly not available")

    st.caption("💡 **3D Views:** Drag to rotate, scroll to zoom, double-click to reset. Explore 3-feature relationships.")


