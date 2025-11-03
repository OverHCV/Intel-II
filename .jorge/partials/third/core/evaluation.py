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
        - Sw = within-cluster scatter matrix
        - Sb = between-cluster scatter matrix
    
    Higher J4 = better separated clusters
    
    Args:
        X: Feature matrix (n_samples, n_features)
        labels: Cluster assignments (n_samples,)
        
    Returns:
        J4 criterion value
    """
    # WIP: Implement full J4 calculation
    # WHY: This is exam-critical - must match course definition exactly
    
    # Steps needed:
    # 1. Calculate global mean vector
    # 2. Calculate within-cluster scatter matrix Sw
    #    Sw = sum over clusters of: sum over samples in cluster of: (x - cluster_mean)(x - cluster_mean)^T
    # 3. Calculate between-cluster scatter matrix Sb
    #    Sb = sum over clusters of: n_cluster * (cluster_mean - global_mean)(cluster_mean - global_mean)^T
    # 4. Compute J4 = trace(inv(Sw) @ Sb)
    
    n_samples, n_features = X.shape
    unique_labels = np.unique(labels)
    n_clusters = len(unique_labels)
    
    # Global mean
    global_mean = X.mean(axis=0).reshape(-1, 1)
    
    # Initialize scatter matrices
    Sw = np.zeros((n_features, n_features))
    Sb = np.zeros((n_features, n_features))
    
    # WIP: Complete calculation
    # Placeholder to prevent errors
    logger.warning("J4 calculation not fully implemented - returning placeholder")
    return 0.0


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
    average = "binary" if n_classes == 2 else "macro"
    
    results = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, average=average, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, average=average, zero_division=0)),
        "f1_score": float(f1_score(y_true, y_pred, average=average, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        "n_samples": len(y_true),
        "n_classes": n_classes
    }
    
    # Add per-class metrics if multiclass
    if n_classes > 2:
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

