"""
Visualizations for K-means Clustering results.

Single Responsibility: Render all clustering visualizations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
    📊 **K-means Clustering Summary**: 
    - Total estudiantes: **{len(results['labels'])}**
    - Número de clusters: **{results['n_clusters']}**
    - Initialization: **{results['params']['init_method']}**
    - Iteraciones: **{results['n_iterations']}/{results['params']['max_iter']}**
    - Inertia (WCSS): **{results['inertia']:.2f}**
    - Silhouette Score: **{results['silhouette_avg']:.4f}**
    - Fisher J4 (trace(SB)/trace(SW)): **{results['fisher_j4']:.4f}**
    """)
    
    # Explanation of metrics
    with st.expander("📖 Explicación de Métricas"):
        st.markdown("""
        **Inertia (WCSS)**: Within-Cluster Sum of Squares
        - Suma de distancias al cuadrado de cada punto a su centroide
        - **Menor = mejor** (clusters más compactos)
        - Usado en Elbow Method
        
        **Silhouette Score** (rango: -1 a 1):
        - Mide qué tan bien están separados los clusters
        - Valores cercanos a 1: clusters bien definidos
        - Valores cercanos a 0: clusters se solapan
        
        **Fisher J4** = trace(SB) / trace(SW):
        - SB = Between-cluster scatter (varianza entre clusters)
        - SW = Within-cluster scatter (varianza intra-cluster)
        - **Valores más altos = mejor separación**
        """)
    
    st.success("✅ K-means clustering completado exitosamente!")


def render_elbow_analysis(elbow_results: Dict[str, Any]):
    """
    Render Elbow Method analysis results.
    
    Args:
        elbow_results: Elbow analysis results
    """
    if elbow_results is None:
        return
    
    st.markdown("### 📊 Elbow Method (Optimal K)")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Plot Inertia vs K
        fig_elbow, ax_elbow = plt.subplots(figsize=(10, 5))
        
        k_values = elbow_results['k_values']
        inertias = elbow_results['inertias']
        suggested_k = elbow_results['suggested_k']
        
        ax_elbow.plot(k_values, inertias, marker='o', linewidth=2, markersize=8, color='steelblue')
        ax_elbow.axvline(x=suggested_k, color='red', linestyle='--', linewidth=2, label=f'Sugerido K={suggested_k}')
        ax_elbow.set_xlabel("Número de Clusters (K)")
        ax_elbow.set_ylabel("Inertia (WCSS)")
        ax_elbow.set_title("Elbow Method: Inertia vs K")
        ax_elbow.grid(True, alpha=0.3)
        ax_elbow.legend()
        plt.tight_layout()
        st.pyplot(fig_elbow)
        plt.close()
    
    with col2:
        st.markdown("#### 📊 Inertia Values")
        elbow_df = pd.DataFrame({
            'K': k_values,
            'Inertia': [f"{inertia:.2f}" for inertia in inertias]
        })
        st.dataframe(elbow_df, hide_index=True, width="stretch")
        
        st.metric(
            "K Sugerido",
            suggested_k,
            delta=f"Inertia={inertias[suggested_k - min(k_values)]:.2f}"
        )
    
    st.caption("""
    💡 **Interpretación del Elbow Method**:
    - El "codo" representa el punto donde la reducción de inercia se desacelera
    - Antes del codo: la inercia baja rápido (añadir clusters ayuda mucho)
    - Después del codo: la inercia baja lento (añadir clusters ayuda poco)
    - **Balance**: Complejidad (K alto) vs Calidad de clustering
    """)


def render_cluster_distribution(labels: np.ndarray, cluster_sizes: Dict[int, int]):
    """
    Render cluster size distribution bar chart.
    
    Args:
        labels: Cluster assignments
        cluster_sizes: Dict with cluster sizes
    """
    fig_dist, ax_dist = plt.subplots(figsize=(10, 5))
    
    clusters = list(cluster_sizes.keys())
    sizes = list(cluster_sizes.values())
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(clusters)))
    bars = ax_dist.bar(clusters, sizes, color=colors, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax_dist.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax_dist.set_xlabel("Cluster ID")
    ax_dist.set_ylabel("Number of Students")
    ax_dist.set_title("Cluster Size Distribution")
    ax_dist.grid(True, axis='y', alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig_dist)
    plt.close()
    
    # Balance analysis
    max_size = max(sizes)
    min_size = min(sizes)
    balance_ratio = max_size / min_size if min_size > 0 else float('inf')
    
    if balance_ratio <= 1.5:
        st.success(f"✅ Clusters bien balanceados (ratio {balance_ratio:.2f})")
    elif balance_ratio <= 3.0:
        st.warning(f"⚠️ Desbalance moderado (ratio {balance_ratio:.2f})")
    else:
        st.error(f"❌ Clusters muy desbalanceados (ratio {balance_ratio:.2f})")


def render_silhouette_plot(silhouette_vals: np.ndarray, labels: np.ndarray, 
                           silhouette_avg: float, cluster_silhouette_means: Dict[int, float]):
    """
    Render silhouette plot for cluster quality visualization.
    
    Args:
        silhouette_vals: Silhouette coefficient for each sample
        labels: Cluster assignments
        silhouette_avg: Average silhouette score
        cluster_silhouette_means: Mean silhouette per cluster
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
        
        color = plt.cm.Set3(float(i) / n_clusters)
        ax_sil.fill_betweenx(
            np.arange(y_lower, y_upper),
            0,
            cluster_silhouette_vals,
            facecolor=color,
            edgecolor=color,
            alpha=0.7
        )
        
        # Label the silhouette plots with their cluster numbers at the middle
        ax_sil.text(-0.05, y_lower + 0.5 * size_cluster_i, f"Cluster {i}")
        
        y_lower = y_upper + 10
    
    ax_sil.set_xlabel("Silhouette Coefficient")
    ax_sil.set_ylabel("Cluster ID")
    ax_sil.set_title(f"Silhouette Plot (avg={silhouette_avg:.3f})")
    
    # Vertical line for average silhouette score
    ax_sil.axvline(x=silhouette_avg, color="red", linestyle="--", linewidth=2, label=f"Avg: {silhouette_avg:.3f}")
    ax_sil.legend()
    ax_sil.set_yticks([])
    ax_sil.set_xlim([-0.2, 1])
    
    plt.tight_layout()
    st.pyplot(fig_sil)
    plt.close()
    
    st.caption("""
    💡 **Interpretación del Silhouette Plot**:
    - Línea roja = Silhouette Score promedio
    - Valores a la derecha de la línea roja = muestras bien agrupadas
    - Valores a la izquierda = muestras posiblemente mal asignadas
    - Grosor de cada cluster = número de muestras
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
            💡 **Mean**: Valor promedio de la feature en este cluster (datos escalados).
            **Std**: Desviación estándar (variabilidad dentro del cluster).
            """)


def render_all_results(results: Dict[str, Any]):
    """
    Render all K-means clustering results.
    
    Args:
        results: Complete clustering results dict
    """
    # Data info
    render_data_info(results)
    
    # Elbow analysis (if performed)
    if results['elbow_results'] is not None:
        render_elbow_analysis(results['elbow_results'])
        st.markdown("---")
    
    # Cluster distribution AND Silhouette plot side by side
    st.markdown("### 📊 Cluster Quality Analysis")
    col_dist, col_sil = st.columns(2)
    
    with col_dist:
        st.markdown("#### 📊 Cluster Distribution")
        render_cluster_distribution(results['labels'], results['cluster_sizes'])
    
    with col_sil:
        st.markdown("#### 📈 Silhouette Plot")
        render_silhouette_plot(
            results['silhouette_vals'],
            results['labels'],
            results['silhouette_avg'],
            results['cluster_silhouette_means']
        )
    
    st.markdown("---")
    
    # Cluster profiles
    render_cluster_profiles(results['cluster_profiles'])

