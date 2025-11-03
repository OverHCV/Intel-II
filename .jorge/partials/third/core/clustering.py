"""
Clustering module - Hierarchical and K-means algorithms.

This module implements unsupervised learning algorithms to discover natural
groupings in student data without predefined labels.

WHY: Clustering reveals hidden patterns like "high-performing students with
     low social activity" that classification might miss.
"""

from typing import Dict, List, Tuple, Optional, Any
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist
import logging

logger = logging.getLogger(__name__)


def hierarchical_clustering(
    X: np.ndarray,
    n_clusters: int,
    linkage_method: str = "ward",
    distance_metric: str = "euclidean"
) -> Tuple[np.ndarray, Any]:
    """
    Perform hierarchical clustering on student data.
    
    WHY: Hierarchical clustering shows relationships BETWEEN groups,
         not just final assignment. The dendrogram reveals how students
         naturally group at different similarity levels.
    
    Args:
        X: Feature matrix (n_samples, n_features)
        n_clusters: Number of clusters to form
        linkage_method: "ward", "complete", "average", "single"
        distance_metric: Distance measure (default: euclidean)
        
    Returns:
        Tuple of (cluster_labels, linkage_matrix)
    """
    model = AgglomerativeClustering(
        n_clusters=n_clusters,
        linkage=linkage_method
    )
    
    labels = model.fit_predict(X)
    
    # Compute linkage matrix for dendrogram
    linkage_matrix = linkage(X, method=linkage_method, metric=distance_metric)
    
    logger.info(
        f"Hierarchical clustering: {n_clusters} clusters, "
        f"{linkage_method} linkage"
    )
    
    return labels, linkage_matrix


def kmeans_clustering(
    X: np.ndarray,
    n_clusters: int,
    random_state: Optional[int] = None,
    max_iter: int = 300,
    n_init: int = 10
) -> Tuple[KMeans, np.ndarray]:
    """
    Perform K-means clustering on student data.
    
    WHY: K-means is faster than hierarchical and works well when cluster
         shapes are roughly spherical. Good for large datasets.
    
    Args:
        X: Feature matrix
        n_clusters: Number of clusters
        random_state: Random seed
        max_iter: Maximum iterations
        n_init: Number of initializations (best is kept)
        
    Returns:
        Tuple of (fitted_model, cluster_labels)
    """
    model = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        max_iter=max_iter,
        n_init=n_init
    )
    
    labels = model.fit_predict(X)
    
    logger.info(
        f"K-means: {n_clusters} clusters, "
        f"inertia={model.inertia_:.2f}, "
        f"iterations={model.n_iter_}"
    )
    
    return model, labels


def compare_linkage_methods(
    X: np.ndarray,
    n_clusters: int,
    methods: Optional[List[str]] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Compare different hierarchical linkage methods.
    
    WHY: Different linkage methods produce different cluster structures.
         Ward minimizes variance, Complete avoids chaining, Average is
         balanced. Need to compare to find best fit for student data.
    
    WIP: Add silhouette scores and calinski-harabasz index for each method.
    WHY: Need quantitative comparison, not just visual inspection.
    
    Args:
        X: Feature matrix
        n_clusters: Number of clusters
        methods: List of linkage methods to compare
        
    Returns:
        Dictionary with results for each method
    """
    if methods is None:
        methods = ["ward", "complete", "average", "single"]
    
    results = {}
    
    for method in methods:
        try:
            labels, linkage_mat = hierarchical_clustering(
                X, n_clusters, linkage_method=method
            )
            
            results[method] = {
                "labels": labels,
                "linkage_matrix": linkage_mat,
                "n_clusters": n_clusters,
                "silhouette": "WIP: Calculate silhouette score",
                "calinski_harabasz": "WIP: Calculate CH index",
                "why": f"{method} linkage characteristics and when to use"
            }
        except Exception as e:
            logger.error(f"Error with {method} linkage: {e}")
            results[method] = {"error": str(e)}
    
    return results


def get_cluster_statistics(
    X: np.ndarray,
    labels: np.ndarray,
    feature_names: Optional[List[str]] = None
) -> Dict[int, Dict[str, Any]]:
    """
    Calculate statistics for each cluster.
    
    WHY: Understanding WHAT characterizes each cluster is crucial.
         E.g., "Cluster 1: High studytime, low absences → high performers"
    
    Args:
        X: Feature matrix
        labels: Cluster assignments
        feature_names: Optional feature names
        
    Returns:
        Dictionary mapping cluster_id to statistics
    """
    stats = {}
    n_clusters = len(np.unique(labels))
    
    for cluster_id in range(n_clusters):
        mask = labels == cluster_id
        cluster_data = X[mask]
        
        stats[cluster_id] = {
            "size": int(np.sum(mask)),
            "centroid": cluster_data.mean(axis=0).tolist(),
            "std": cluster_data.std(axis=0).tolist(),
            "min": cluster_data.min(axis=0).tolist(),
            "max": cluster_data.max(axis=0).tolist(),
            "feature_names": feature_names,
            "interpretation": "WIP: Generate natural language description",
            "why": "Each cluster represents a distinct student profile"
        }
    
    logger.info(f"Computed statistics for {n_clusters} clusters")
    return stats


def calculate_inertia_curve(
    X: np.ndarray,
    k_range: Tuple[int, int] = (2, 10),
    random_state: Optional[int] = None
) -> Dict[int, float]:
    """
    Calculate K-means inertia (within-cluster sum of squares) for range of k.
    
    WHY: The "elbow method" - plot inertia vs k to find optimal number
         of clusters. Sharp elbow indicates natural grouping.
    
    Args:
        X: Feature matrix
        k_range: Tuple of (min_k, max_k)
        random_state: Random seed
        
    Returns:
        Dictionary mapping k to inertia
    """
    inertias = {}
    
    for k in range(k_range[0], k_range[1] + 1):
        model = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        model.fit(X)
        inertias[k] = float(model.inertia_)
    
    logger.info(f"Computed inertia for k={k_range[0]} to {k_range[1]}")
    return inertias


# Module metadata
__version__ = "1.0.0"
__algorithms__ = ["Hierarchical", "K-means"]

