"""
Visualizations for Dataset Review page.

Single Responsibility: Render all data visualizations (plots, tables, metrics).
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
from typing import Tuple

from states import get_state, StateKeys
from constants.base import get_feature_description

logger = logging.getLogger(__name__)


def render_visualizations(X: np.ndarray, y: np.ndarray, balance_method: str):
    """
    Render all data visualizations.
    
    Args:
        X: Feature matrix (prepared data)
        y: Target vector (prepared labels)
        balance_method: Balancing method used (for display)
    """
    st.subheader("📈 Data Visualization")
    
    tabs = st.tabs(["Class Distribution", "Feature Correlation", "Summary Stats"])
    
    with tabs[0]:
        _render_class_distribution(y, balance_method)
    
    with tabs[1]:
        _render_correlation_heatmap(X)
    
    with tabs[2]:
        _render_summary_stats(X)


def _render_class_distribution(y: np.ndarray, balance_method: str):
    """
    Render class distribution bar chart.
    
    Args:
        y: Target vector
        balance_method: Balancing method name
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    unique, counts = np.unique(y, return_counts=True)
    colors = plt.cm.Set3(np.linspace(0, 1, len(unique)))
    ax.bar([f"Class {u}" for u in unique], counts, color=colors)
    ax.set_ylabel("Number of Students")
    ax.set_title(f"Class Distribution (After {balance_method})")
    ax.set_ylim(0, max(counts) * 1.2)
    
    # Add count labels
    for i, v in enumerate(counts):
        ax.text(i, v + max(counts)*0.02, str(v), ha='center', fontweight='bold')
    
    st.pyplot(fig)
    plt.close()
    
    imbalance_ratio = max(counts) / min(counts) if len(counts) > 1 else 1.0
    st.caption(f"💡 Ratio de desbalance: {imbalance_ratio:.2f}. Si >2.0 una clase domina → sesgo del modelo")


def _render_correlation_heatmap(X: np.ndarray):
    """
    Render feature correlation heatmap (lower triangle only).
    
    Args:
        X: Feature matrix
    """
    st.markdown("#### 🔥 Feature Correlation Matrix")
    
    # Compute correlation
    corr_matrix = pd.DataFrame(X).corr()
    
    # Mask upper triangle and diagonal
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    corr_masked = corr_matrix.mask(mask)
    
    # Plot heatmap
    fig_corr, ax_corr = plt.subplots(figsize=(12, 10))
    im = ax_corr.imshow(corr_masked, cmap='coolwarm', vmin=-1, vmax=1, aspect='auto')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax_corr)
    cbar.set_label("Correlation Coefficient", rotation=270, labelpad=20)
    
    # Set ticks (show every Nth feature to avoid clutter)
    n_features = corr_matrix.shape[0]
    tick_positions = list(range(0, n_features, max(1, n_features // 10)))
    ax_corr.set_xticks(tick_positions)
    ax_corr.set_yticks(tick_positions)
    ax_corr.set_xticklabels([f"F{i}" for i in tick_positions], rotation=45)
    ax_corr.set_yticklabels([f"F{i}" for i in tick_positions])
    
    ax_corr.set_title("Feature Correlation Heatmap (Lower Triangle)", fontsize=14, pad=20)
    plt.tight_layout()
    st.pyplot(fig_corr)
    plt.close()
    
    st.caption("💡 Solo triángulo inferior (sin duplicados ni diagonal). Rojo = correlación positiva, Azul = negativa. Alta correlación (>0.9) = características redundantes.")
    
    # Show top correlations
    _render_top_correlations(corr_matrix)


def _render_top_correlations(corr_matrix: pd.DataFrame):
    """
    Render top 5 correlated feature pairs.
    
    Args:
        corr_matrix: Correlation matrix
    """
    n_features = corr_matrix.shape[0]
    corr_pairs = []
    
    for i in range(n_features):
        for j in range(i+1, n_features):
            corr_pairs.append((i, j, abs(corr_matrix.iloc[i, j])))
    
    corr_pairs.sort(key=lambda x: x[2], reverse=True)
    
    if corr_pairs:
        st.markdown("**Top 5 Correlated Feature Pairs:**")
        
        # Get actual feature names from raw data
        raw_df = get_state(StateKeys.RAW_DATA, None)
        if raw_df is not None:
            feature_names = list(raw_df.columns)
            for i, j, corr in corr_pairs[:5]:
                feat_i = feature_names[i] if i < len(feature_names) else f"F{i}"
                feat_j = feature_names[j] if j < len(feature_names) else f"F{j}"
                desc_i = get_feature_description(feat_i)
                desc_j = get_feature_description(feat_j)
                st.markdown(f"**{feat_i}** ⋈ **{feat_j}**: {corr:.3f}")
                st.caption(f"   {desc_i} ↔ {desc_j}")
        else:
            for i, j, corr in corr_pairs[:5]:
                st.markdown(f"Feature {i} ⋈ Feature {j}: {corr:.3f}")


def _render_summary_stats(X: np.ndarray):
    """
    Render summary statistics table with feature descriptions.
    
    Args:
        X: Feature matrix
    """
    st.markdown("#### 📊 Feature Statistics")
    
    # Get actual feature names
    raw_df = get_state(StateKeys.RAW_DATA, None)
    df_stats = pd.DataFrame(X)
    summary = df_stats.describe().T
    
    if raw_df is not None:
        feature_names = list(raw_df.columns)
        # Remove G1, G2, G3, dataset_source if present
        feature_names = [f for f in feature_names if f not in ['G1', 'G2', 'G3', 'dataset_source']]
        
        # Reset index to make it a column
        summary = summary.reset_index()
        
        # Map numeric indices to actual feature names (if lengths match)
        if len(feature_names) == len(summary):
            summary.insert(0, 'Feature', feature_names)
            summary.insert(1, 'Description', summary['Feature'].apply(get_feature_description))
            # Select only relevant columns
            summary = summary[['Feature', 'Description', 'mean', 'std', 'min', 'max']]
            summary.columns = ['Feature', 'Descripción', 'Media', 'Desv. Est.', 'Mín', 'Máx']
        else:
            # Fallback if mismatch
            summary.insert(0, 'Feature', [f"Feature_{i}" for i in range(len(summary))])
            summary = summary[['Feature', 'mean', 'std', 'min', 'max']]
            summary.columns = ['Feature', 'Media', 'Desv. Est.', 'Mín', 'Máx']
    else:
        summary = summary.reset_index()
        summary.insert(0, 'Feature', [f"Feature_{i}" for i in range(len(summary))])
        summary = summary[['Feature', 'mean', 'std', 'min', 'max']]
        summary.columns = ['Feature', 'Media', 'Desv. Est.', 'Mín', 'Máx']
    
    st.dataframe(summary, use_container_width=True, height=400)
    st.caption("💡 Estadísticas descriptivas de cada característica. Comprender las características es clave para interpretar decisiones del modelo.")

