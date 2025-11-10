"""
Elbow Method analysis for finding optimal K in K-means.

Single Responsibility: Calculate inertia for different K values.
"""

import numpy as np
import logging
from typing import Dict, List
from sklearn.cluster import KMeans

logger = logging.getLogger(__name__)


def calculate_inertia_for_k(
    X: np.ndarray,
    k: int,
    init_method: str = "k-means++",
    n_init: int = 10,
    max_iter: int = 300,
    random_state: int = 42
) -> float:
    """
    Calculate inertia (WCSS) for a specific K.
    
    Args:
        X: Feature matrix (n_samples, n_features)
        k: Number of clusters
        init_method: Initialization method ('k-means++' or 'random')
        n_init: Number of time the k-means algorithm will be run
        max_iter: Maximum number of iterations
        random_state: Random seed for reproducibility
    
    Returns:
        float: Inertia (within-cluster sum of squares)
    """
    try:
        kmeans = KMeans(
            n_clusters=k,
            init=init_method,
            n_init=n_init,
            max_iter=max_iter,
            random_state=random_state
        )
        kmeans.fit(X)
        return float(kmeans.inertia_)
        
    except Exception as e:
        logger.error(f"Error calculating inertia for k={k}: {e}")
        return -1.0


def find_optimal_k_elbow(
    X: np.ndarray,
    k_min: int = 2,
    k_max: int = 10,
    init_method: str = "k-means++",
    n_init: int = 10,
    max_iter: int = 300
) -> Dict[str, any]:
    """
    Find optimal K using Elbow Method.
    
    Runs K-means for K in [k_min, k_max] and computes inertia.
    The "elbow" in the inertia plot suggests the optimal K.
    
    Args:
        X: Feature matrix
        k_min: Minimum K to test
        k_max: Maximum K to test
        init_method: Initialization method
        n_init: Number of initializations
        max_iter: Max iterations
    
    Returns:
        Dict with results: {
            'k_values': list of K tested,
            'inertias': list of inertias,
            'suggested_k': suggested optimal K (using elbow detection)
        }
    """
    logger.info(f"Running Elbow Method for K={k_min} to {k_max}...")
    
    k_values = list(range(k_min, k_max + 1))
    inertias = []
    
    for k in k_values:
        inertia = calculate_inertia_for_k(X, k, init_method, n_init, max_iter)
        inertias.append(inertia)
        logger.info(f"K={k}: Inertia={inertia:.2f}")
    
    # Simple elbow detection: find K where the rate of decrease slows down
    # Using "knee" detection: maximum distance from line connecting first and last points
    suggested_k = detect_elbow_knee(k_values, inertias)
    
    logger.info(f"✅ Suggested K (Elbow): {suggested_k}")
    
    return {
        'k_values': k_values,
        'inertias': inertias,
        'suggested_k': suggested_k
    }


def detect_elbow_knee(k_values: List[int], inertias: List[float]) -> int:
    """
    Detect elbow using perpendicular distance method.
    
    Finds the point with maximum perpendicular distance to the line 
    connecting the first and last points.
    
    Args:
        k_values: List of K values
        inertias: List of corresponding inertias
    
    Returns:
        int: Suggested optimal K
    """
    if len(k_values) < 3:
        return k_values[0]
    
    # Normalize to [0, 1] range for fair comparison
    k_norm = np.array([(k - min(k_values)) / (max(k_values) - min(k_values)) for k in k_values])
    inertia_norm = np.array([(i - min(inertias)) / (max(inertias) - min(inertias)) for i in inertias])
    
    # Line from first to last point
    p1 = np.array([k_norm[0], inertia_norm[0]])
    p2 = np.array([k_norm[-1], inertia_norm[-1]])
    
    # Calculate perpendicular distance for each point
    distances = []
    for i in range(len(k_norm)):
        point = np.array([k_norm[i], inertia_norm[i]])
        # Distance from point to line p1-p2
        distance = np.abs(np.cross(p2 - p1, p1 - point)) / np.linalg.norm(p2 - p1)
        distances.append(distance)
    
    # Return K with maximum distance (the "elbow")
    elbow_idx = np.argmax(distances)
    return k_values[elbow_idx]

