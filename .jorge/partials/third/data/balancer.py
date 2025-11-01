"""
Data Balancer - Class balancing strategies.

Responsibilities:
- Apply SMOTE (Synthetic Minority Over-sampling Technique)
- Apply random oversampling
- Apply random undersampling
- Get class distribution metrics

NO algorithms (just calls to libraries), NO UI code, NO file I/O.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Literal, Optional
from collections import Counter
import logging

logger = logging.getLogger(__name__)

BalancingMethod = Literal["smote", "random_over", "random_under", "none"]


def apply_smote(
    X: pd.DataFrame,
    y: pd.Series,
    sampling_strategy: str = "auto",
    k_neighbors: int = 5,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Apply SMOTE to balance classes.
    
    Args:
        X: Feature dataframe
        y: Target series
        sampling_strategy: 'auto', 'minority', 'not majority', or ratio dict
        k_neighbors: Number of nearest neighbors for SMOTE
        random_state: Random seed for reproducibility
        
    Returns:
        Tuple of (X_resampled, y_resampled)
        
    Raises:
        ImportError: If imblearn not installed
        ValueError: If not enough samples for SMOTE
    """
    try:
        from imblearn.over_sampling import SMOTE
    except ImportError:
        raise ImportError(
            "imbalanced-learn not installed. Install with: pip install imbalanced-learn"
        )
    
    original_dist = Counter(y)
    logger.info(f"Original distribution: {dict(original_dist)}")
    
    try:
        smote = SMOTE(
            sampling_strategy=sampling_strategy,
            k_neighbors=k_neighbors,
            random_state=random_state
        )
        
        X_resampled, y_resampled = smote.fit_resample(X, y)
        
        new_dist = Counter(y_resampled)
        logger.info(f"After SMOTE: {dict(new_dist)}")
        logger.info(
            f"SMOTE complete: {len(y)} → {len(y_resampled)} samples "
            f"(+{len(y_resampled) - len(y)} synthetic)"
        )
        
        return pd.DataFrame(X_resampled, columns=X.columns), pd.Series(y_resampled)
    
    except ValueError as e:
        logger.error(f"SMOTE failed: {e}")
        logger.warning("Returning original data without balancing")
        return X, y


def apply_random_oversample(
    X: pd.DataFrame,
    y: pd.Series,
    sampling_strategy: str = "auto",
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Apply random oversampling to balance classes.
    
    Args:
        X: Feature dataframe
        y: Target series
        sampling_strategy: 'auto', 'minority', 'not majority', or ratio dict
        random_state: Random seed for reproducibility
        
    Returns:
        Tuple of (X_resampled, y_resampled)
    """
    try:
        from imblearn.over_sampling import RandomOverSampler
    except ImportError:
        raise ImportError(
            "imbalanced-learn not installed. Install with: pip install imbalanced-learn"
        )
    
    original_dist = Counter(y)
    logger.info(f"Original distribution: {dict(original_dist)}")
    
    ros = RandomOverSampler(sampling_strategy=sampling_strategy, random_state=random_state)
    X_resampled, y_resampled = ros.fit_resample(X, y)
    
    new_dist = Counter(y_resampled)
    logger.info(f"After random oversampling: {dict(new_dist)}")
    logger.info(
        f"Random oversample complete: {len(y)} → {len(y_resampled)} samples "
        f"(+{len(y_resampled) - len(y)} duplicates)"
    )
    
    return pd.DataFrame(X_resampled, columns=X.columns), pd.Series(y_resampled)


def apply_random_undersample(
    X: pd.DataFrame,
    y: pd.Series,
    sampling_strategy: str = "auto",
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Apply random undersampling to balance classes.
    
    Args:
        X: Feature dataframe
        y: Target series
        sampling_strategy: 'auto', 'majority', 'not minority', or ratio dict
        random_state: Random seed for reproducibility
        
    Returns:
        Tuple of (X_resampled, y_resampled)
    """
    try:
        from imblearn.under_sampling import RandomUnderSampler
    except ImportError:
        raise ImportError(
            "imbalanced-learn not installed. Install with: pip install imbalanced-learn"
        )
    
    original_dist = Counter(y)
    logger.info(f"Original distribution: {dict(original_dist)}")
    
    rus = RandomUnderSampler(sampling_strategy=sampling_strategy, random_state=random_state)
    X_resampled, y_resampled = rus.fit_resample(X, y)
    
    new_dist = Counter(y_resampled)
    logger.info(f"After random undersampling: {dict(new_dist)}")
    logger.info(
        f"Random undersample complete: {len(y)} → {len(y_resampled)} samples "
        f"(-{len(y) - len(y_resampled)} removed)"
    )
    
    return pd.DataFrame(X_resampled, columns=X.columns), pd.Series(y_resampled)


def balance_classes(
    X: pd.DataFrame,
    y: pd.Series,
    method: BalancingMethod = "smote",
    **method_params
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Balance classes using specified method.
    
    Args:
        X: Feature dataframe
        y: Target series
        method: Balancing method ('smote', 'random_over', 'random_under', 'none')
        **method_params: Additional parameters for the method
        
    Returns:
        Tuple of (X_balanced, y_balanced)
    """
    if method == "none":
        logger.info("No balancing applied")
        return X, y
    
    elif method == "smote":
        return apply_smote(X, y, **method_params)
    
    elif method == "random_over":
        return apply_random_oversample(X, y, **method_params)
    
    elif method == "random_under":
        return apply_random_undersample(X, y, **method_params)
    
    else:
        raise ValueError(
            f"Invalid method: {method}. "
            f"Must be 'smote', 'random_over', 'random_under', or 'none'"
        )


def get_imbalance_metrics(y: pd.Series) -> dict:
    """
    Calculate imbalance metrics for target variable.
    
    Args:
        y: Target series
        
    Returns:
        Dictionary with imbalance metrics
    """
    counts = Counter(y)
    total = len(y)
    
    if len(counts) == 0:
        raise ValueError("Empty target series")
    
    sorted_counts = sorted(counts.values(), reverse=True)
    majority_count = sorted_counts[0]
    minority_count = sorted_counts[-1]
    
    metrics = {
        "n_samples": total,
        "n_classes": len(counts),
        "class_counts": dict(counts),
        "class_proportions": {k: v / total for k, v in counts.items()},
        "majority_count": majority_count,
        "minority_count": minority_count,
        "imbalance_ratio": majority_count / minority_count if minority_count > 0 else float('inf'),
        "is_balanced": majority_count == minority_count
    }
    
    # Calculate imbalance severity
    if metrics["imbalance_ratio"] < 1.5:
        severity = "low"
    elif metrics["imbalance_ratio"] < 3:
        severity = "moderate"
    elif metrics["imbalance_ratio"] < 10:
        severity = "high"
    else:
        severity = "severe"
    
    metrics["imbalance_severity"] = severity
    
    logger.info(
        f"Imbalance metrics: {metrics['n_classes']} classes, "
        f"ratio: {metrics['imbalance_ratio']:.2f} ({severity})"
    )
    
    return metrics


def recommend_balancing_method(y: pd.Series) -> str:
    """
    Recommend a balancing method based on data characteristics.
    
    Args:
        y: Target series
        
    Returns:
        Recommended method name
    """
    metrics = get_imbalance_metrics(y)
    
    # Decision logic
    if metrics["is_balanced"]:
        recommendation = "none"
        reason = "Classes are already balanced"
    
    elif metrics["minority_count"] < 6:
        recommendation = "random_over"
        reason = "Too few minority samples for SMOTE (needs at least 6)"
    
    elif metrics["imbalance_ratio"] > 10:
        recommendation = "smote"
        reason = "Severe imbalance, SMOTE generates diverse synthetic samples"
    
    elif metrics["majority_count"] > 1000:
        recommendation = "random_under"
        reason = "Large dataset, undersampling will speed up training"
    
    else:
        recommendation = "smote"
        reason = "Moderate imbalance, SMOTE is generally effective"
    
    logger.info(f"Recommended method: {recommendation} ({reason})")
    
    return recommendation


def compare_distributions(
    y_before: pd.Series,
    y_after: pd.Series
) -> dict:
    """
    Compare class distributions before and after balancing.
    
    Args:
        y_before: Original target series
        y_after: Balanced target series
        
    Returns:
        Dictionary with comparison metrics
    """
    before_counts = Counter(y_before)
    after_counts = Counter(y_after)
    
    comparison = {
        "before": {
            "n_samples": len(y_before),
            "class_counts": dict(before_counts),
            "imbalance_ratio": max(before_counts.values()) / min(before_counts.values())
        },
        "after": {
            "n_samples": len(y_after),
            "class_counts": dict(after_counts),
            "imbalance_ratio": max(after_counts.values()) / min(after_counts.values())
        },
        "change": {
            "n_samples_added": len(y_after) - len(y_before),
            "ratio_improvement": (
                max(before_counts.values()) / min(before_counts.values()) -
                max(after_counts.values()) / min(after_counts.values())
            )
        }
    }
    
    logger.info(
        f"Distribution comparison: "
        f"{comparison['before']['n_samples']} → {comparison['after']['n_samples']} samples, "
        f"ratio improved by {comparison['change']['ratio_improvement']:.2f}"
    )
    
    return comparison


