"""
Model Training for Hierarchical Clustering page.

Single Responsibility: Execute clustering and generate all results.
"""

import numpy as np
import logging
import datetime
from typing import Dict, Any
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.metrics import silhouette_score

from .j4_analysis import find_optimal_k, get_silhouette_samples_per_cluster
from .fisher_j4 import calculate_fisher_j4
from states import get_state, set_state, StateKeys
from versioning.experiment_store import save_experiment

logger = logging.getLogger(__name__)


def train_hierarchical_clustering(
    X: np.ndarray,
    params: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Train hierarchical clustering model and generate all results.
    
    Pipeline:
    1. Run J4 analysis if requested (find optimal K)
    2. Compute linkage matrix
    3. Cut tree to get cluster labels
    4. Calculate silhouette scores
    5. Profile clusters (feature means per cluster)
    6. Save experiment to history
    
    Args:
        X: Feature matrix (prepared data)
        params: Dict with clustering parameters
    
    Returns:
        Dict with all results: {
            'linkage_matrix': scipy linkage matrix,
            'labels': cluster assignments,
            'n_clusters': number of clusters,
            'silhouette_avg': average silhouette score,
            'silhouette_vals': per-sample silhouette scores,
            'cluster_silhouette_means': dict of mean silhouette per cluster,
            'cluster_sizes': dict of cluster sizes,
            'cluster_profiles': dict of feature means per cluster,
            'j4_results': J4 analysis results (if requested),
            'experiment_id': saved experiment ID
        }
    
    Raises:
        Exception: If clustering fails
    """
    try:
        # Run J4 analysis if requested
        j4_results = None
        if params['find_optimal_k']:
            logger.info("Running J4 analysis to find optimal K...")
            j4_results = find_optimal_k(
                X,
                k_min=params['k_range_min'],
                k_max=params['k_range_max'],
                linkage_method=params['linkage_method'],
                distance_metric=params['distance_metric']
            )
            logger.info(f"J4 suggests optimal K={j4_results['optimal_k']}")
        
        # Compute linkage matrix
        logger.info(f"Computing linkage matrix with {params['linkage_method']} method...")
        if params['linkage_method'] == "ward":
            # Ward only works with euclidean
            Z = linkage(X, method=params['linkage_method'])
        else:
            Z = linkage(X, method=params['linkage_method'], metric=params['distance_metric'])
        
        # Cut tree to get cluster labels
        n_clusters = params['n_clusters']
        labels = fcluster(Z, n_clusters, criterion='maxclust')
        
        # Convert to 0-indexed (fcluster returns 1-indexed)
        labels = labels - 1
        
        logger.info(f"Clustered {len(X)} samples into {n_clusters} clusters")
        
        # Calculate Silhouette scores
        silhouette_avg = silhouette_score(X, labels, metric=params['distance_metric'])
        silhouette_vals, cluster_silhouette_means = get_silhouette_samples_per_cluster(
            X, labels, params['distance_metric']
        )
        
        logger.info(f"Average Silhouette Score: {silhouette_avg:.4f}")
        
        # Calculate Fisher's J4 (trace(SB)/trace(SW))
        fisher_j4, _, _ = calculate_fisher_j4(X, labels)  # _ = unused SB, SW matrices
        logger.info(f"Fisher J4 (trace(SB)/trace(SW)): {fisher_j4:.4f}")
        
        # Calculate cluster sizes
        unique_labels, counts = np.unique(labels, return_counts=True)
        cluster_sizes = {int(label): int(count) for label, count in zip(unique_labels, counts)}
        
        # Profile clusters (feature means)
        cluster_profiles = {}
        for cluster_id in unique_labels:
            cluster_mask = labels == cluster_id
            cluster_data = X[cluster_mask]
            cluster_profiles[int(cluster_id)] = {
                'mean': np.mean(cluster_data, axis=0),
                'std': np.std(cluster_data, axis=0),
                'size': int(np.sum(cluster_mask))
            }
        
        # Save experiment to persistent storage
        experiment_data_for_store = {
            "parameters": {
                "n_clusters": n_clusters,
                "linkage_method": params['linkage_method'],
                "distance_metric": params['distance_metric']
            },
            "metrics": {
                "silhouette_avg": float(silhouette_avg),
                "fisher_j4": float(fisher_j4),
                "n_clusters": n_clusters
            },
            "dataset_info": {
                "total_samples": len(X),
                "n_features": X.shape[1]
            }
        }
        
        experiment_id = save_experiment(
            experiment_data_for_store,
            algorithm_type="hierarchical"
        )
        
        logger.info(f"Saved experiment {experiment_id} to persistent storage")
        
        # Store results in state
        set_state(StateKeys.HC_LABELS, labels)
        
        return {
            'linkage_matrix': Z,
            'labels': labels,
            'n_clusters': n_clusters,
            'silhouette_avg': silhouette_avg,
            'fisher_j4': fisher_j4,
            'silhouette_vals': silhouette_vals,
            'cluster_silhouette_means': cluster_silhouette_means,
            'cluster_sizes': cluster_sizes,
            'cluster_profiles': cluster_profiles,
            'j4_results': j4_results,
            'experiment_id': experiment_id,
            'params': params
        }
        
    except Exception as e:
        logger.error(f"Hierarchical clustering error: {e}", exc_info=True)
        raise

