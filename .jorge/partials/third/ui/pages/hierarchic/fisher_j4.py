"""
J4 Fisher Criterion for clustering quality evaluation.

Single Responsibility: Calculate Fisher's J4 metric (trace(SB)/trace(SW)).
"""

import numpy as np
import pandas as pd
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


def calculate_fisher_j4(X: np.ndarray, labels: np.ndarray) -> Tuple[float, np.ndarray, np.ndarray]:
    """
    Calculate Fisher's J4 criterion for clustering quality.
    
    J4 = trace(SB) / trace(SW)
    
    Where:
    - SB = Between-cluster scatter matrix (varianza entre clusters)
    - SW = Within-cluster scatter matrix (varianza intra-cluster)
    
    Higher J4 = better cluster separation
    
    Args:
        X: Feature matrix (n_samples, n_features)
        labels: Cluster assignments
    
    Returns:
        Tuple of (J4 score, SB matrix, SW matrix)
    """
    try:
        # Overall mean
        media_total = np.mean(X, axis=0)
        
        # Group by clusters
        df = pd.DataFrame(X)
        df['cluster'] = labels
        grupos = df.groupby('cluster')
        
        # Cluster means
        medias = grupos.mean().values  # Without 'cluster' column
        
        # Cluster covariances
        n_samples = len(X)
        n_features = X.shape[1]
        
        # Initialize scatter matrices
        SB = np.zeros((n_features, n_features))
        SW = np.zeros((n_features, n_features))
        
        for i, (cluster_id, group) in enumerate(grupos):
            # Remove 'cluster' column from group
            cluster_data = group.drop('cluster', axis=1).values
            ni = len(cluster_data)  # Cluster size
            
            # Cluster mean (ensure it's numpy array)
            cluster_mean = np.asarray(medias[i])
            
            # Between-cluster scatter
            mean_diff = (cluster_mean - media_total).reshape(-1, 1)
            SB += (ni / n_samples) * (mean_diff @ mean_diff.T)
            
            # Within-cluster scatter (covariance)
            cluster_cov = np.cov(cluster_data, rowvar=False, ddof=1)
            if cluster_cov.ndim == 0:  # Handle 1D case
                cluster_cov = np.array([[cluster_cov]])
            SW += (ni / n_samples) * cluster_cov
        
        # Calculate J4
        trace_SB = np.trace(SB)
        trace_SW = np.trace(SW)
        
        if trace_SW == 0 or np.isnan(trace_SW):
            logger.warning("SW trace is zero or NaN, returning J4=0")
            return 0.0, SB, SW
        
        J4 = trace_SB / trace_SW
        
        logger.info(f"Fisher J4 = {J4:.4f} (trace(SB)={trace_SB:.4f}, trace(SW)={trace_SW:.4f})")
        
        return float(J4), SB, SW
        
    except Exception as e:
        logger.error(f"Error calculating Fisher J4: {e}")
        return 0.0, np.zeros((X.shape[1], X.shape[1])), np.zeros((X.shape[1], X.shape[1]))


def calculate_fisher_j4_for_k(
    X: np.ndarray,
    k: int,
    linkage_method: str = "ward",
    distance_metric: str = "euclidean"
) -> float:
    """
    Calculate Fisher J4 for a specific K using hierarchical clustering.
    
    Args:
        X: Feature matrix
        k: Number of clusters
        linkage_method: Linkage method
        distance_metric: Distance metric
    
    Returns:
        float: Fisher J4 score
    """
    try:
        from scipy.cluster.hierarchy import linkage, fcluster
        
        # Compute linkage matrix
        if linkage_method == "ward":
            Z = linkage(X, method=linkage_method)
        else:
            Z = linkage(X, method=linkage_method, metric=distance_metric)
        
        # Cut tree to get k clusters
        labels = fcluster(Z, k, criterion='maxclust') - 1  # 0-indexed
        
        # Calculate Fisher J4
        j4, _, _ = calculate_fisher_j4(X, labels)
        return j4
        
    except Exception as e:
        logger.error(f"Error calculating Fisher J4 for k={k}: {e}")
        return 0.0

