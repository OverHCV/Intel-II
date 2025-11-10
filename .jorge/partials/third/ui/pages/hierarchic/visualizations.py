"""
Visualizations for Hierarchical Clustering results.

Single Responsibility: Render all clustering visualizations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
import logging
from typing import Dict, Any

from states import get_state
from constants.base import get_feature_description

logger = logging.getLogger(__name__)


def render_data_info(results: Dict[str, Any]):
    """
    Render clustering summary information.
    
    Args:
        results: Clustering results dict
    """
    st.info(f"""
    📊 **Clustering Summary**: 
    - Total estudiantes: **{len(results['labels'])}**
    - Número de clusters: **{results['n_clusters']}**
    - Linkage method: **{results['params']['linkage_method']}**
    - Distance metric: **{results['params']['distance_metric']}**
    - Silhouette Score: **{results['silhouette_avg']:.4f}**
    - Fisher J4 (trace(SB)/trace(SW)): **{results['fisher_j4']:.4f}**
    """)
    
    # Explanation of metrics
    with st.expander("📖 Explicación de Métricas"):
        st.markdown("""
        **Silhouette Score** (rango: -1 a 1):
        - Mide qué tan bien están separados los clusters
        - Valores cercanos a 1: clusters bien definidos
        - Valores cercanos a 0: clusters se solapan
        - Valores negativos: muestras mal asignadas
        
        **Fisher J4** = trace(SB) / trace(SW):
        - SB = Between-cluster scatter (varianza entre clusters)
        - SW = Within-cluster scatter (varianza intra-cluster)
        - **Valores más altos = mejor separación**
        - Usado en el notebook de referencia
        """)
    
    st.success("✅ Hierarchical clustering completado exitosamente!")


def render_j4_analysis(j4_results: Dict[str, Any]):
    """
    Render J4 optimal K analysis results.
    
    Args:
        j4_results: J4 analysis results
    """
    if j4_results is None:
        return
    
    st.markdown("### 🎯 Análisis de K Óptimo (Silhouette)")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Plot Silhouette scores vs K
        fig_j4, ax_j4 = plt.subplots(figsize=(10, 5))
        
        k_values = j4_results['k_values']
        silhouette_scores = j4_results['silhouette_scores']
        optimal_k = j4_results['optimal_k']
        
        ax_j4.plot(k_values, silhouette_scores, marker='o', linewidth=2, markersize=8, color='steelblue')
        ax_j4.axvline(x=optimal_k, color='red', linestyle='--', linewidth=2, label=f'K óptimo={optimal_k}')
        ax_j4.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
        ax_j4.set_xlabel("Número de Clusters (K)")
        ax_j4.set_ylabel("Silhouette Score")
        ax_j4.set_title("Silhouette Score vs K")
        ax_j4.grid(True, alpha=0.3)
        ax_j4.legend()
        plt.tight_layout()
        st.pyplot(fig_j4)
        plt.close()
    
    with col2:
        st.markdown("#### 📊 Silhouette Scores")
        j4_df = pd.DataFrame({
            'K': k_values,
            'Silhouette': [f"{score:.4f}" for score in silhouette_scores]
        })
        st.dataframe(j4_df, hide_index=True, use_container_width=True)
        
        st.metric(
            "K Óptimo",
            optimal_k,
            delta=f"Score={j4_results['optimal_score']:.4f}"
        )
    
    st.caption("""
    💡 **Interpretación J4 (Silhouette Score)**:
    - **> 0.7**: Excelente separación entre clusters
    - **0.5-0.7**: Buena estructura de clusters
    - **0.25-0.5**: Estructura débil, clusters se solapan
    - **< 0.25**: Mal clustering, considerar K diferente
    """)


def render_dendrogram(linkage_matrix: np.ndarray, n_clusters: int, truncate_mode: str = 'lastp', p: int = 30):
    """
    Render dendrogram visualization.
    
    Args:
        linkage_matrix: Scipy linkage matrix
        n_clusters: Number of clusters (for color threshold)
        truncate_mode: Truncation mode for large datasets
        p: Number of leaves to show when truncated
    """
    st.markdown("### 🌳 Dendrogram")
    
    fig_dend, ax_dend = plt.subplots(figsize=(12, 6))
    
    # Calculate color threshold (height to cut for n_clusters)
    # Use the merge distance at the (n-k)th merge
    if len(linkage_matrix) >= n_clusters:
        color_threshold_idx = len(linkage_matrix) - n_clusters
        color_threshold = linkage_matrix[color_threshold_idx, 2]
    else:
        color_threshold = None
    
    dendrogram(
        linkage_matrix,
        ax=ax_dend,
        truncate_mode=truncate_mode,
        p=p,
        color_threshold=color_threshold,
        above_threshold_color='gray'
    )
    
    ax_dend.set_xlabel("Sample Index (or Cluster Size)")
    ax_dend.set_ylabel("Distance")
    ax_dend.set_title(f"Hierarchical Clustering Dendrogram (K={n_clusters})")
    ax_dend.axhline(y=color_threshold if color_threshold else 0, color='red', linestyle='--', linewidth=2, label=f'Cut for K={n_clusters}')
    ax_dend.legend()
    plt.tight_layout()
    st.pyplot(fig_dend)
    plt.close()
    
    st.caption(f"""
    📏 **Dendrogram truncado a {p} hojas** por legibilidad.
    - Altura (Y) = distancia entre clusters al momento de fusión
    - Línea roja = corte para obtener {n_clusters} clusters
    - Colores = diferentes clusters finales
    """)


def render_cluster_distribution(cluster_sizes: Dict[int, int]):
    """
    Render cluster size distribution bar chart.
    
    Args:
        cluster_sizes: Dict mapping cluster ID to size
    """
    fig_dist, ax_dist = plt.subplots(figsize=(8, 5))
    
    clusters = list(cluster_sizes.keys())
    sizes = list(cluster_sizes.values())
    
    bars = ax_dist.bar(clusters, sizes, color='steelblue', alpha=0.7, edgecolor='black')
    ax_dist.set_xlabel("Cluster ID")
    ax_dist.set_ylabel("Number of Students")
    ax_dist.set_title("Students per Cluster")
    ax_dist.set_xticks(clusters)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax_dist.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f'{int(height)}',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )
    
    plt.tight_layout()
    st.pyplot(fig_dist)
    plt.close()
    
    # Show distribution table
    dist_df = pd.DataFrame({
        'Cluster': clusters,
        'Size': sizes,
        'Percentage': [f"{(size / sum(sizes)) * 100:.1f}%" for size in sizes]
    })
    st.dataframe(dist_df, hide_index=True, width="stretch")


def render_silhouette_plot(silhouette_vals: np.ndarray, labels: np.ndarray, silhouette_avg: float):
    """
    Render silhouette plot for each cluster.
    
    Args:
        silhouette_vals: Per-sample silhouette coefficients
        labels: Cluster assignments
        silhouette_avg: Average silhouette score
    """
    fig_sil, ax_sil = plt.subplots(figsize=(10, 6))
    
    y_lower = 10
    n_clusters = len(np.unique(labels))
    
    for i in range(n_clusters):
        # Aggregate silhouette scores for samples in cluster i
        cluster_silhouette_vals = silhouette_vals[labels == i]
        cluster_silhouette_vals.sort()
        
        size_cluster_i = cluster_silhouette_vals.shape[0]
        y_upper = y_lower + size_cluster_i
        
        color = plt.cm.nipy_spectral(float(i) / n_clusters)
        ax_sil.fill_betweenx(
            np.arange(y_lower, y_upper),
            0,
            cluster_silhouette_vals,
            facecolor=color,
            edgecolor=color,
            alpha=0.7
        )
        
        # Label cluster
        ax_sil.text(-0.05, y_lower + 0.5 * size_cluster_i, f'C{i}')
        
        y_lower = y_upper + 10
    
    ax_sil.set_xlabel("Silhouette Coefficient")
    ax_sil.set_ylabel("Cluster Label")
    ax_sil.set_title("Silhouette Plot for Each Cluster")
    
    # Add average silhouette line
    ax_sil.axvline(x=silhouette_avg, color='red', linestyle='--', linewidth=2, label=f'Avg={silhouette_avg:.3f}')
    ax_sil.legend()
    ax_sil.set_yticks([])
    ax_sil.set_xlim([-0.1, 1])
    
    plt.tight_layout()
    st.pyplot(fig_sil)
    plt.close()
    
    st.caption("""
    💡 **Interpretación**:
    - Ancho de cada área = tamaño del cluster
    - Valores a la derecha de la línea roja = muestras bien agrupadas
    - Valores a la izquierda = muestras posiblemente mal asignadas
    """)


def render_cluster_profiles(cluster_profiles: Dict[int, Dict], n_features: int = 10):
    """
    Render cluster profiles showing top features per cluster.
    
    Args:
        cluster_profiles: Dict with cluster statistics
        n_features: Number of top features to show
    """
    st.markdown("### 🔍 Cluster Profiles (Top Features)")
    
    # Get feature names from state
    feature_names = get_state("feature_names", None)
    if feature_names is None or len(feature_names) == 0:
        st.warning("⚠️ Feature names not found. Cannot display cluster profiles.")
        return
    
    # Display each cluster profile
    for cluster_id, profile in cluster_profiles.items():
        with st.expander(f"📌 Cluster {cluster_id} ({profile['size']} students)", expanded=(cluster_id == 0)):
            # Ensure means and stds are numpy arrays to avoid pandas indexing warnings
            means = np.asarray(profile['mean'])
            stds = np.asarray(profile['std'])
            
            # Get top N features by absolute mean value (scaled data, so mean shows deviation from 0)
            top_indices = np.argsort(np.abs(means))[-n_features:][::-1]
            
            # Create profile table
            profile_data = []
            for idx in top_indices:
                if idx < len(feature_names):
                    feat_name = feature_names[idx]
                    feat_desc = get_feature_description(feat_name)
                    # Access by integer index (guaranteed safe with numpy array)
                    mean_val = float(means[idx])
                    std_val = float(stds[idx])
                    profile_data.append({
                        'Feature': feat_name,
                        'Description': feat_desc[:50] + "..." if len(feat_desc) > 50 else feat_desc,
                        'Mean': f"{mean_val:.3f}",
                        'Std': f"{std_val:.3f}"
                    })
            
            profile_df = pd.DataFrame(profile_data)
            st.dataframe(profile_df, hide_index=True, width="stretch")
            
            st.caption(f"""
            📊 **Cluster {cluster_id} characteristics**: Top {n_features} features con mayor desviación de la media.
            Mean > 0 = por encima del promedio, Mean < 0 = por debajo del promedio.
            """)


def render_all_results(results: Dict[str, Any]):
    """
    Render all hierarchical clustering results.
    
    Args:
        results: Complete clustering results dict
    """
    # Data info
    render_data_info(results)
    
    # J4 analysis (if performed)
    if results['j4_results'] is not None:
        render_j4_analysis(results['j4_results'])
        st.markdown("---")
    
    # Dendrogram
    render_dendrogram(results['linkage_matrix'], results['n_clusters'])
    st.markdown("---")
    
    # Cluster distribution AND Silhouette plot side by side
    st.markdown("### 📊 Cluster Quality Analysis")
    col_dist, col_sil = st.columns(2)
    
    with col_dist:
        st.markdown("#### Cluster Distribution")
        render_cluster_distribution(results['cluster_sizes'])
    
    with col_sil:
        st.markdown("#### Silhouette Analysis")
        render_silhouette_plot(
            results['silhouette_vals'],
            results['labels'],
            results['silhouette_avg']
        )
    
    st.markdown("---")
    
    # Cluster profiles
    render_cluster_profiles(results['cluster_profiles'])

