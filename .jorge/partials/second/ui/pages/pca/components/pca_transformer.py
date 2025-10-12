"""
PCA Transformer Component
Handles PCA transformation with n_components selection
"""

import numpy as np
import streamlit as st
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from ui.pages.pca.components.pca_viz_tabs import render_pca_viz_tabs


def render_pca_transformer(X, y, feature_names):
    """
    Render PCA transformation controls and visualizations

    Args:
        X: Feature matrix
        y: Target labels
        feature_names: List of feature names
    """
    st.markdown("### 📊 PCA Transformation")

    # Initialize PCA state if needed
    if "pca_applied" not in st.session_state.pca:
        st.session_state.pca["pca_applied"] = False

    # Controls column
    col_controls, col_info = st.columns([1, 2])

    with col_controls:
        _render_controls(X, feature_names)

    with col_info:
        if st.session_state.pca["pca_applied"]:
            render_pca_viz_tabs()
        else:
            st.info("👈 Configure and apply PCA to see results")


def _render_controls(X, feature_names):
    """Render PCA configuration controls"""
    st.markdown("**Configure PCA**")

    n_features = X.shape[1]

    # Selection method
    selection_method = st.radio(
        "Selection method:",
        ["Variance Threshold", "Fixed Number", "Scree Plot (Visual)"],
        key="pca_selection_method",
        help="How to choose number of components",
    )

    if selection_method == "Variance Threshold":
        variance_threshold = st.slider(
            "Variance to retain:",
            min_value=0.80,
            max_value=0.99,
            value=0.95,
            step=0.01,
            key="pca_variance_threshold",
            help="Keep enough PCs to retain this % of total variance",
        )
        st.caption(
            f"💡 Will auto-select n_components to retain {variance_threshold * 100:.0f}% variance"
        )
        n_components = variance_threshold  # PCA accepts float for variance threshold

    elif selection_method == "Fixed Number":
        n_components = st.slider(
            "Number of components:",
            min_value=2,
            max_value=min(n_features, 15),
            value=min(5, n_features),
            step=1,
            key="pca_n_components",
            help="Fixed number of principal components",
        )
        st.caption(f"💡 Will keep exactly {n_components} components")

    else:  # Scree Plot
        st.info("Apply PCA first to see scree plot, then adjust")
        n_components = st.slider(
            "Number of components:",
            min_value=2,
            max_value=min(n_features, 15),
            value=min(5, n_features),
            step=1,
            key="pca_n_components_scree",
        )

    st.divider()

    # Apply button
    if st.button("🔄 Apply PCA Transformation", type="primary", width="stretch"):
        _apply_pca(X, feature_names, n_components)


def _apply_pca(X, feature_names, n_components):
    """Apply PCA transformation to data"""
    with st.spinner("Applying PCA transformation..."):
        # Standardize data (critical for PCA!)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Apply PCA
        pca = PCA(n_components=n_components)
        X_pca = pca.fit_transform(X_scaled)

        # Store results
        st.session_state.pca["pca_model"] = pca
        st.session_state.pca["scaler"] = scaler
        st.session_state.pca["X_pca"] = X_pca
        st.session_state.pca["X_scaled"] = X_scaled
        st.session_state.pca["n_components_used"] = pca.n_components_
        st.session_state.pca["explained_variance_ratio"] = pca.explained_variance_ratio_
        st.session_state.pca["cumulative_variance"] = np.cumsum(
            pca.explained_variance_ratio_
        )
        st.session_state.pca["components"] = pca.components_
        st.session_state.pca["feature_names"] = feature_names
        st.session_state.pca["pca_applied"] = True

        st.success(
            f"✅ PCA applied! Reduced {len(feature_names)} → {pca.n_components_} dimensions"
        )
        st.rerun()
