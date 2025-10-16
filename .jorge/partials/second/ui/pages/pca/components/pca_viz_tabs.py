"""
PCA Visualization Tabs
Renders the three visualization tabs for PCA results
"""

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


def render_pca_viz_tabs():
    """
    Render PCA visualization tabs (Explained Variance, Loadings, Scree Plot)
    """
    n_components = st.session_state.pca["n_components_used"]
    explained_var = st.session_state.pca["explained_variance_ratio"]
    cumulative_var = st.session_state.pca["cumulative_variance"]

    # Summary metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Components",
            n_components,
            f"-{len(st.session_state.pca['feature_names']) - n_components} features",
        )

    with col2:
        st.metric(
            "Variance Retained",
            f"{cumulative_var[-1] * 100:.1f}%",
            f"{(1 - cumulative_var[-1]) * 100:.1f}% lost",
        )

    with col3:
        reduction = (
            1 - n_components / len(st.session_state.pca["feature_names"])
        ) * 100
        st.metric("Dimensionality Reduction", f"{reduction:.1f}%", "fewer features")

    st.divider()

    # Visualizations in tabs
    viz_tabs = st.tabs(
        ["📊 Explained Variance", "🔍 Component Loadings", "🎯 Scree Plot"]
    )

    with viz_tabs[0]:
        render_explained_variance(explained_var, cumulative_var)

    with viz_tabs[1]:
        render_component_loadings()

    with viz_tabs[2]:
        render_scree_plot(explained_var)


def render_explained_variance(explained_var, cumulative_var):
    """Render explained variance visualization"""
    st.markdown("#### Variance Explained by Each Component")

    fig, ax = plt.subplots(figsize=(10, 5))

    x = np.arange(1, len(explained_var) + 1)

    # Bar plot for individual variance
    ax.bar(x, explained_var * 100, alpha=0.6, color="steelblue", label="Individual")

    # Line plot for cumulative variance
    ax2 = ax.twinx()
    ax2.plot(
        x, cumulative_var * 100, "ro-", linewidth=2, markersize=8, label="Cumulative"
    )
    ax2.axhline(
        y=95, color="g", linestyle="--", linewidth=1, alpha=0.7, label="95% threshold"
    )

    # Labels and styling
    ax.set_xlabel("Principal Component", fontsize=12)
    ax.set_ylabel("Variance Explained (%)", fontsize=12)
    ax2.set_ylabel("Cumulative Variance (%)", fontsize=12)
    ax.set_title(
        "Variance Explained by Principal Components", fontsize=14, fontweight="bold"
    )
    ax.set_xticks(x)
    ax.grid(axis="y", alpha=0.3)
    ax.set_ylim([0, max(explained_var * 100) * 1.1])
    ax2.set_ylim([0, 105])

    # Legends
    ax.legend(loc="upper left")
    ax2.legend(loc="upper right")

    plt.tight_layout()
    st.pyplot(fig)

    # Interpretation
    st.markdown("**📖 How to read this:**")
    st.markdown(
        f"""
    - **Blue bars**: Variance explained by each PC individually
    - **Red line**: Cumulative variance (sum of all PCs up to that point)
    - **Green dashed**: 95% threshold (common target)
    
    **Your results**:
    - PC1 explains **{explained_var[0] * 100:.1f}%** of variance (most important!)
    - First {np.argmax(cumulative_var >= 0.95) + 1 if any(cumulative_var >= 0.95) else len(cumulative_var)} PCs capture **95%** of variance
    - Total retained: **{cumulative_var[-1] * 100:.1f}%**
    """
    )


def render_component_loadings():
    """Render component loadings heatmap"""
    st.markdown("#### Component Loadings (Feature Contributions)")

    components = st.session_state.pca["components"]
    feature_names = st.session_state.pca["feature_names"]
    n_components = st.session_state.pca["n_components_used"]

    # Create loadings matrix (components × features)
    # Loadings = eigenvector * sqrt(eigenvalue)
    explained_var = st.session_state.pca["explained_variance_ratio"]
    loadings = components * np.sqrt(explained_var[:, np.newaxis])

    fig, ax = plt.subplots(figsize=(12, min(n_components * 0.6, 8)))

    # Heatmap
    im = ax.imshow(loadings, cmap="RdBu_r", aspect="auto", vmin=-1, vmax=1)

    # Labels
    ax.set_xticks(np.arange(len(feature_names)))
    ax.set_yticks(np.arange(n_components))
    ax.set_xticklabels(feature_names, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels([f"PC{i + 1}" for i in range(n_components)], fontsize=10)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Loading (correlation)", rotation=270, labelpad=20)

    # Add values to cells
    for i in range(n_components):
        for j in range(len(feature_names)):
            text = ax.text(
                j,
                i,
                f"{loadings[i, j]:.2f}",
                ha="center",
                va="center",
                color="white" if abs(loadings[i, j]) > 0.5 else "black",
                fontsize=7,
            )

    ax.set_title("Component Loadings Heatmap", fontsize=14, fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig)

    # Interpretation
    st.markdown("**📖 How to read this:**")
    st.markdown(
        """
    - **Red (positive)**: Feature increases with this PC
    - **Blue (negative)**: Feature decreases with this PC
    - **White (near 0)**: Feature not related to this PC
    - **Strong loadings (±0.7+)**: Feature heavily contributes to this PC
    
    **Find patterns**: Which features load heavily on PC1? What do they have in common?
    """
    )

    # Top contributors per PC
    st.markdown("**🔝 Top Contributors per Component:**")
    for i in range(min(3, n_components)):  # Show first 3 PCs
        top_indices = np.argsort(np.abs(loadings[i]))[-3:][::-1]
        top_features = [feature_names[idx] for idx in top_indices]
        top_values = [loadings[i, idx] for idx in top_indices]

        st.markdown(
            f"**PC{i + 1}**: {', '.join([f'{feat} ({val:+.2f})' for feat, val in zip(top_features, top_values)])}"
        )


def render_scree_plot(explained_var):
    """Render scree plot for elbow method"""
    st.markdown("#### Scree Plot (Elbow Method)")

    fig, ax = plt.subplots(figsize=(10, 5))

    x = np.arange(1, len(explained_var) + 1)
    ax.plot(x, explained_var * 100, "bo-", linewidth=2, markersize=10)

    # Add markers
    for i, val in enumerate(explained_var * 100):
        ax.text(i + 1, val + 0.5, f"{val:.1f}%", ha="center", fontsize=9)

    ax.set_xlabel("Principal Component", fontsize=12)
    ax.set_ylabel("Variance Explained (%)", fontsize=12)
    ax.set_title("Scree Plot - Find the Elbow!", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)

    # Interpretation
    st.markdown("**📖 How to find the elbow:**")
    st.markdown(
        """
    1. Look for the point where the line **flattens sharply**
    2. That's the "elbow" - components after this are less important
    3. Keep components **before the elbow**
    
    **Example**:
    - If the line drops steeply from PC1-PC3, then flattens after PC3
    - **Elbow = PC3** → Keep 3 components
    """
    )

    # Auto-detect elbow (simple heuristic)
    if len(explained_var) >= 3:
        # Find largest drop
        drops = np.diff(explained_var * 100)
        elbow_idx = np.argmax(np.abs(drops)) + 1

        st.info(
            f"🤖 **Auto-detected elbow**: Around PC{elbow_idx} (largest drop: {-drops[elbow_idx - 1]:.1f}%)"
        )


