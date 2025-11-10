"""
Model Training for K-means Clustering page.

Single Responsibility: Execute K-means clustering and generate all results.
"""

import numpy as np
import logging
import datetime
from typing import Dict, Any
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples

from .elbow_analysis import find_optimal_k_elbow
from ui.pages.hierarchic.fisher_j4 import calculate_fisher_j4
from ui.pages.hierarchic.j4_analysis import get_silhouette_samples_per_cluster
from states import get_state, set_state, StateKeys

logger = logging.getLogger(__name__)


def train_kmeans_clustering(X: np.ndarray, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Train K-means clustering model with given parameters.
    
    Args:
        X: Feature matrix (n_samples, n_features)
        params: Dictionary with clustering parameters:
            - n_clusters: int
            - init_method: str ('k-means++' or 'random')
            - n_init: int
            - max_iter: int
            - run_elbow: bool
            - elbow_k_min: int
            - elbow_k_max: int
    
    Returns:
        Dict with clustering results
        
    Raises:
        Exception: If clustering fails
    """
    try:
        # Run Elbow analysis if requested
        elbow_results = None
        if params['run_elbow']:
            logger.info("Running Elbow Method to find optimal K...")
            elbow_results = find_optimal_k_elbow(
                X,
                k_min=params['elbow_k_min'],
                k_max=params['elbow_k_max'],
                init_method=params['init_method'],
                n_init=params['n_init'],
                max_iter=params['max_iter']
            )
            logger.info(f"Elbow suggests optimal K={elbow_results['suggested_k']}")
        
        # Train K-means
        n_clusters = params['n_clusters']
        logger.info(f"Training K-means with K={n_clusters}, init={params['init_method']}...")
        
        kmeans = KMeans(
            n_clusters=n_clusters,
            init=params['init_method'],
            n_init=params['n_init'],
            max_iter=params['max_iter'],
            random_state=42
        )
        
        labels = kmeans.fit_predict(X)
        
        logger.info(f"Clustered {len(X)} samples into {n_clusters} clusters")
        logger.info(f"Converged in {kmeans.n_iter_} iterations")
        logger.info(f"Inertia (WCSS): {kmeans.inertia_:.2f}")
        
        # Calculate Silhouette scores
        silhouette_avg = silhouette_score(X, labels, metric='euclidean')
        silhouette_vals, cluster_silhouette_means = get_silhouette_samples_per_cluster(
            X, labels, 'euclidean'
        )
        
        logger.info(f"Average Silhouette Score: {silhouette_avg:.4f}")
        
        # Calculate Fisher's J4 (trace(SB)/trace(SW))
        fisher_j4, _, _ = calculate_fisher_j4(X, labels)
        logger.info(f"Fisher J4 (trace(SB)/trace(SW)): {fisher_j4:.4f}")
        
        # Calculate cluster sizes
        unique_labels, counts = np.unique(labels, return_counts=True)
        cluster_sizes = {int(label): int(count) for label, count in zip(unique_labels, counts)}
        
        # Profile clusters (feature means and stds)
        cluster_profiles = {}
        for cluster_id in unique_labels:
            cluster_mask = labels == cluster_id
            cluster_data = X[cluster_mask]
            cluster_profiles[int(cluster_id)] = {
                'mean': np.mean(cluster_data, axis=0),
                'std': np.std(cluster_data, axis=0),
                'size': int(np.sum(cluster_mask))
            }
        
        # Save experiment to history
        experiment_id = f"KM_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        experiment_data = {
            "id": experiment_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "params": {
                "n_clusters": n_clusters,
                "init_method": params['init_method'],
                "n_init": params['n_init'],
                "max_iter": params['max_iter']
            },
            "data": {
                "total_samples": len(X),
                "n_features": X.shape[1]
            },
            "metrics": {
                "silhouette_avg": float(silhouette_avg),
                "fisher_j4": float(fisher_j4),
                "inertia": float(kmeans.inertia_),
                "n_iterations": int(kmeans.n_iter_),
                "cluster_sizes": cluster_sizes
            },
            "elbow_analysis": {
                "suggested_k": elbow_results['suggested_k'] if elbow_results else None
            } if elbow_results else None
        }
        
        # Append to experiment history
        history = get_state("experiment_history_km", [])
        history.append(experiment_data)
        set_state("experiment_history_km", history)
        
        logger.info(f"Saved experiment {experiment_id} to history")
        
        # Store results in state
        set_state(StateKeys.KM_LABELS, labels)
        
        return {
            'kmeans_model': kmeans,
            'labels': labels,
            'centroids': kmeans.cluster_centers_,
            'n_clusters': n_clusters,
            'inertia': kmeans.inertia_,
            'n_iterations': kmeans.n_iter_,
            'silhouette_avg': silhouette_avg,
            'fisher_j4': fisher_j4,
            'silhouette_vals': silhouette_vals,
            'cluster_silhouette_means': cluster_silhouette_means,
            'cluster_sizes': cluster_sizes,
            'cluster_profiles': cluster_profiles,
            'elbow_results': elbow_results,
            'experiment_id': experiment_id,
            'params': params
        }
        
    except Exception as e:
        logger.error(f"K-means clustering error: {e}", exc_info=True)
        raise

