"""
Evaluation module - Performance metrics and quality criteria.

This module provides evaluation functions for both classification (trees)
and clustering algorithms.

WHY: Need objective measures to compare models and validate that our
     student groupings/predictions are meaningful.
"""

from typing import Dict, List, Optional, Any
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import logging

logger = logging.getLogger(__name__)


def calculate_j4_criterion(
    X: np.ndarray,
    labels: np.ndarray
) -> float:
    """
    Calculate J4 criterion for clustering quality evaluation.
    
    WHY: J4 is the standard criterion for hierarchical clustering in this course.
         It measures the ratio of between-cluster to within-cluster scatter.
    
    Formula: J4 = trace(Sw^-1 * Sb)
    where:
        - Sw = within-cluster scatter matrix (dispersion within clusters)
        - Sb = between-cluster scatter matrix (separation between clusters)
    
    Higher J4 = better separated clusters (want high between, low within)
    
    Args:
        X: Feature matrix (n_samples, n_features)
        labels: Cluster assignments (n_samples,)
        
    Returns:
        J4 criterion value
        
    Raises:
        ValueError: If Sw is singular (not invertible)
    """
    n_samples, n_features = X.shape
    unique_labels = np.unique(labels)
    n_clusters = len(unique_labels)
    
    # Step 1: Calculate global mean vector (d x 1)
    global_mean = np.mean(X, axis=0).reshape(n_features, 1)
    
    # Step 2: Initialize scatter matrices (d x d)
    Sw = np.zeros((n_features, n_features))
    Sb = np.zeros((n_features, n_features))
    
    # Step 3: Calculate scatter matrices for each cluster
    for label in unique_labels:
        # Get samples belonging to this cluster
        cluster_mask = (labels == label)
        X_cluster = X[cluster_mask]
        n_cluster = X_cluster.shape[0]
        
        if n_cluster == 0:
            continue
        
        # Cluster mean (d x 1)
        cluster_mean = np.mean(X_cluster, axis=0).reshape(n_features, 1)
        
        # Within-cluster scatter: sum of (x - mu_c)(x - mu_c)^T
        for sample in X_cluster:
            diff = sample.reshape(n_features, 1) - cluster_mean
            Sw += diff @ diff.T
        
        # Between-cluster scatter: n_c * (mu_c - mu)(mu_c - mu)^T
        diff_cluster = cluster_mean - global_mean
        Sb += n_cluster * (diff_cluster @ diff_cluster.T)
    
    # Step 4: Calculate J4 = trace(inv(Sw) @ Sb)
    # Add small regularization to prevent singular matrix
    regularization = 1e-6 * np.eye(n_features)
    Sw_reg = Sw + regularization
    
    try:
        # Compute inverse of within-scatter
        Sw_inv = np.linalg.inv(Sw_reg)
        
        # Compute J4 = trace(Sw^-1 * Sb)
        j4_value = np.trace(Sw_inv @ Sb)
        
        logger.info(
            f"J4 criterion calculated: {j4_value:.4f} "
            f"({n_clusters} clusters, {n_samples} samples)"
        )
        
        return float(j4_value)
        
    except np.linalg.LinAlgError:
        logger.error("Sw matrix is singular, cannot compute J4")
        raise ValueError(
            "Within-cluster scatter matrix is singular. "
            "This can happen with very few samples or degenerate clusters."
        )


def evaluate_classification(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    class_names: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Comprehensive classification evaluation.
    
    WHY: Accuracy alone is misleading with imbalanced classes.
         Need precision, recall, F1 to understand model behavior.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        class_names: Optional class names
        
    Returns:
        Dictionary with all classification metrics
    """
    n_classes = len(np.unique(y_true))
    
    # CRITICAL: Use 'weighted' for all cases (binary and multiclass)
    # 'weighted' accounts for class imbalance by weighting metrics by support
    # Don't use 'binary' with string labels (causes pos_label error)
    average = "weighted"
    
    results = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, average=average, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, average=average, zero_division=0)),
        "f1_score": float(f1_score(y_true, y_pred, average=average, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        "n_samples": len(y_true),
        "n_classes": n_classes
    }
    
    # Add per-class metrics for all cases
    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    results["per_class"] = report
    
    logger.info(
        f"Classification: Acc={results['accuracy']:.3f}, "
        f"F1={results['f1_score']:.3f}"
    )
    
    return results


def evaluate_clustering(
    X: np.ndarray,
    labels: np.ndarray
) -> Dict[str, float]:
    """
    Comprehensive clustering evaluation.
    
    WHY: Unsupervised learning has no "true" labels, but we can measure
         cluster quality through cohesion and separation.
    
    Args:
        X: Feature matrix
        labels: Cluster assignments
        
    Returns:
        Dictionary with clustering quality metrics
    """
    from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
    
    results = {
        "j4_criterion": calculate_j4_criterion(X, labels),
        "silhouette_score": float(silhouette_score(X, labels)),
        "calinski_harabasz": float(calinski_harabasz_score(X, labels)),
        "davies_bouldin": float(davies_bouldin_score(X, labels)),
        "n_clusters": len(np.unique(labels)),
        "interpretation": {
            "j4": "Higher is better (ratio of between/within scatter)",
            "silhouette": "[-1, 1], higher is better (1 = perfect)",
            "calinski": "Higher is better (ratio of dispersion)",
            "davies_bouldin": "Lower is better (avg similarity between clusters)"
        }
    }
    
    logger.info(
        f"Clustering: J4={results['j4_criterion']:.3f}, "
        f"Silhouette={results['silhouette_score']:.3f}"
    )
    
    return results


def compare_models(
    results_list: List[Dict[str, Any]],
    metric: str = "accuracy"
) -> Dict[str, Any]:
    """
    Compare multiple model results.
    
    WHY: Need to determine which hyperparameters/algorithms work best
         for our specific student dataset.
    
    Args:
        results_list: List of evaluation result dictionaries
        metric: Metric to use for comparison
        
    Returns:
        Comparison summary with best model
    """
    if not results_list:
        return {"error": "No results to compare"}
    
    # Extract metric values
    values = [r.get(metric, 0) for r in results_list]
    best_idx = np.argmax(values)
    
    comparison = {
        "best_model_index": int(best_idx),
        "best_score": float(values[best_idx]),
        "all_scores": values,
        "mean": float(np.mean(values)),
        "std": float(np.std(values)),
        "metric_used": metric
    }
    
    logger.info(f"Best model: #{best_idx} with {metric}={values[best_idx]:.3f}")
    return comparison


def calculate_model_confidence(
    y_pred_proba: np.ndarray,
    threshold: float = 0.7
) -> Dict[str, Any]:
    """
    Analyze prediction confidence distribution.
    
    WHY: Low confidence predictions indicate uncertain cases where
         human review might be needed.
    
    Args:
        y_pred_proba: Prediction probabilities (n_samples, n_classes)
        threshold: Confidence threshold
        
    Returns:
        Confidence analysis
    """
    max_probs = np.max(y_pred_proba, axis=1)
    
    analysis = {
        "mean_confidence": float(np.mean(max_probs)),
        "std_confidence": float(np.std(max_probs)),
        "high_confidence_pct": float(np.mean(max_probs >= threshold) * 100),
        "low_confidence_pct": float(np.mean(max_probs < threshold) * 100),
        "min_confidence": float(np.min(max_probs)),
        "max_confidence": float(np.max(max_probs)),
        "interpretation": (
            f"{float(np.mean(max_probs < threshold) * 100):.1f}% of predictions "
            f"have confidence below {threshold} - consider manual review"
        )
    }
    
    return analysis


# Module metadata
__version__ = "1.0.0"
__metrics__ = ["J4", "accuracy", "precision", "recall", "f1", "silhouette"]

