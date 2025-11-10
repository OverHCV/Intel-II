"""
J4 Analysis for finding optimal K in Hierarchical Clustering.

Single Responsibility: Calculate silhouette scores for different K values.
"""

import numpy as np
import logging
from typing import Dict, List, Tuple
from sklearn.metrics import silhouette_score, silhouette_samples
from scipy.cluster.hierarchy import linkage, fcluster

logger = logging.getLogger(__name__)


def calculate_j4_for_k(
    X: np.ndarray, 
    k: int, 
    linkage_method: str = "ward",
    distance_metric: str = "euclidean"
) -> float:
    """
    Calculate J4 (average silhouette score) for a specific K.
    
    Args:
        X: Feature matrix (n_samples, n_features)
        k: Number of clusters
        linkage_method: Linkage method for hierarchical clustering
        distance_metric: Distance metric
    
    Returns:
        float: Silhouette score (J4 metric)
    """
    try:
        # Compute linkage matrix
        if linkage_method == "ward":
            # Ward only works with euclidean
            Z = linkage(X, method=linkage_method)
        else:
            Z = linkage(X, method=linkage_method, metric=distance_metric)
        
        # Cut tree to get k clusters
        labels = fcluster(Z, k, criterion='maxclust')
        
        # Calculate silhouette score
        if len(np.unique(labels)) < 2:
            return -1.0  # Invalid clustering
        
        score = silhouette_score(X, labels, metric=distance_metric)
        return float(score)
        
    except Exception as e:
        logger.error(f"Error calculating J4 for k={k}: {e}")
        return -1.0


def find_optimal_k(
    X: np.ndarray,
    k_min: int = 2,
    k_max: int = 10,
    linkage_method: str = "ward",
    distance_metric: str = "euclidean"
) -> Dict[str, any]:
    """
    Find optimal K using J4 (silhouette) analysis.
    
    Runs clustering for K in [k_min, k_max] and computes silhouette score.
    
    Args:
        X: Feature matrix
        k_min: Minimum K to test
        k_max: Maximum K to test
        linkage_method: Linkage method
        distance_metric: Distance metric
    
    Returns:
        Dict with results: {
            'k_values': list of K tested,
            'j4_scores': list of silhouette scores,
            'optimal_k': best K value,
            'optimal_j4': best silhouette score
        }
    """
    logger.info(f"Running J4 analysis for K={k_min} to {k_max}...")
    
    k_values = list(range(k_min, k_max + 1))
    j4_scores = []
    
    for k in k_values:
        score = calculate_j4_for_k(X, k, linkage_method, distance_metric)
        j4_scores.append(score)
        logger.info(f"K={k}: J4={score:.4f}")
    
    # Find optimal K (highest silhouette score)
    optimal_idx = np.argmax(j4_scores)
    optimal_k = k_values[optimal_idx]
    optimal_j4 = j4_scores[optimal_idx]
    
    logger.info(f"✅ Optimal K: {optimal_k} (J4={optimal_j4:.4f})")
    
    return {
        'k_values': k_values,
        'j4_scores': j4_scores,
        'optimal_k': optimal_k,
        'optimal_j4': optimal_j4
    }


def get_silhouette_samples_per_cluster(
    X: np.ndarray,
    labels: np.ndarray,
    distance_metric: str = "euclidean"
) -> Tuple[np.ndarray, Dict[int, float]]:
    """
    Calculate silhouette coefficient for each sample.
    
    Args:
        X: Feature matrix
        labels: Cluster labels
        distance_metric: Distance metric
    
    Returns:
        Tuple of (silhouette_values, cluster_silhouette_means)
    """
    silhouette_vals = silhouette_samples(X, labels, metric=distance_metric)
    
    # Calculate mean silhouette per cluster
    cluster_means = {}
    for cluster_id in np.unique(labels):
        cluster_mask = labels == cluster_id
        cluster_means[cluster_id] = float(np.mean(silhouette_vals[cluster_mask]))
    
    return silhouette_vals, cluster_means

