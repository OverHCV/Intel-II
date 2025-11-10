"""
Data Transformer - Core preprocessing functions.

Responsibilities:
- Engineer target variable (G3 → categorical)
- Remove data leakage features (G1, G2)
- Split features from target
- Get class distribution

NO algorithms, NO UI code, NO file I/O.
"""

import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Literal, Optional
import logging

logger = logging.getLogger(__name__)

TargetStrategy = Literal["binary", "three_class", "five_class", "custom"]


def remove_leakage_features(
    df: pd.DataFrame,
    features_to_remove: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Remove features that cause data leakage.
    
    CRITICAL: Removes G1, G2 (predict G3 trivially) and dataset_source (metadata, not a feature).
    
    Args:
        df: Input dataframe
        features_to_remove: List of column names to remove (defaults to G1, G2, dataset_source)
        
    Returns:
        DataFrame with features removed
    """
    if features_to_remove is None:
        features_to_remove = ["G1", "G2", "dataset_source"]
    
    existing_features = [f for f in features_to_remove if f in df.columns]
    
    if not existing_features:
        logger.warning(f"No leakage features found to remove: {features_to_remove}")
        return df
    
    df_clean = df.drop(columns=existing_features)
    logger.info(f"Removed leakage features: {existing_features}")
    
    return df_clean


def engineer_target(
    df: pd.DataFrame,
    strategy: TargetStrategy = "binary",
    custom_thresholds: Optional[List[float]] = None
) -> pd.Series:
    """
    Transform G3 (0-20) to categorical target variable.
    
    Strategies:
    - binary: Pass/Fail (threshold=10)
    - three_class: Low/Medium/High (thresholds=[10, 14])
    - five_class: A/B/C/D/F (thresholds=[16, 14, 12, 10])
    - custom: User-defined thresholds
    
    Args:
        df: DataFrame with G3 column
        strategy: Which transformation strategy to use
        custom_thresholds: List of thresholds for custom strategy (ascending order)
        
    Returns:
        Series with categorical labels
        
    Raises:
        ValueError: If G3 column missing or invalid strategy
    """
    if "G3" not in df.columns:
        raise ValueError("G3 column not found in dataframe")
    
    g3_values = df["G3"].copy()
    
    if strategy == "binary":
        # Pass (>=10) / Fail (<10)
        target = pd.cut(
            g3_values,
            bins=[-np.inf, 10, np.inf],
            labels=["Fail", "Pass"],
            right=False
        )
        logger.info(f"Engineered binary target: {target.value_counts().to_dict()}")
    
    elif strategy == "three_class":
        # Low (<10), Medium (10-14), High (>=14)
        target = pd.cut(
            g3_values,
            bins=[-np.inf, 10, 14, np.inf],
            labels=["Low", "Medium", "High"],
            right=False
        )
        logger.info(f"Engineered three-class target: {target.value_counts().to_dict()}")
    
    elif strategy == "five_class":
        # A (16-20), B (14-15), C (12-13), D (10-11), F (0-9)
        target = pd.cut(
            g3_values,
            bins=[-np.inf, 10, 12, 14, 16, np.inf],
            labels=["F", "D", "C", "B", "A"],
            right=False
        )
        logger.info(f"Engineered five-class target: {target.value_counts().to_dict()}")
    
    elif strategy == "custom":
        if custom_thresholds is None or len(custom_thresholds) == 0:
            raise ValueError("custom_thresholds required for custom strategy")
        
        # Sort thresholds
        thresholds = sorted(custom_thresholds)
        bins = [-np.inf] + thresholds + [np.inf]
        labels = [f"Class_{i}" for i in range(len(bins) - 1)]
        
        target = pd.cut(g3_values, bins=bins, labels=labels, right=False)
        logger.info(f"Engineered custom target: {target.value_counts().to_dict()}")
    
    else:
        raise ValueError(
            f"Invalid strategy: {strategy}. Must be 'binary', 'three_class', 'five_class', or 'custom'"
        )
    
    return target


def split_features_target(
    df: pd.DataFrame,
    target_col: str = "target"
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Split dataframe into features (X) and target (y).
    
    CRITICAL: Removes dataset_source (metadata) and G3 (if still present) to prevent leakage.
    
    Args:
        df: DataFrame with features and target
        target_col: Name of target column
        
    Returns:
        Tuple of (X, y)
        
    Raises:
        ValueError: If target column not found
    """
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataframe")
    
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Remove metadata and leakage columns if present
    cols_to_drop = []
    if "dataset_source" in X.columns:
        cols_to_drop.append("dataset_source")
    if "G3" in X.columns:
        cols_to_drop.append("G3")
    
    if cols_to_drop:
        X = X.drop(columns=cols_to_drop)
        logger.info(f"Dropped metadata/leakage columns from X: {cols_to_drop}")
    
    logger.info(f"Split into X: {X.shape} and y: {y.shape}")
    
    return X, y


def get_class_distribution(y: pd.Series) -> Dict:
    """
    Get class distribution statistics.
    
    Args:
        y: Target series
        
    Returns:
        Dictionary with distribution info
    """
    counts = y.value_counts().to_dict()
    proportions = y.value_counts(normalize=True).to_dict()
    
    distribution = {
        "counts": counts,
        "proportions": {k: float(f"{v:.3f}") for k, v in proportions.items()},
        "n_classes": len(counts),
        "n_samples": len(y),
        "majority_class": y.value_counts().index[0],
        "minority_class": y.value_counts().index[-1],
        "imbalance_ratio": float(f"{y.value_counts().max() / y.value_counts().min():.2f}")
    }
    
    logger.info(
        f"Class distribution: {distribution['n_classes']} classes, "
        f"imbalance ratio: {distribution['imbalance_ratio']}"
    )
    
    return distribution


def prepare_for_training(
    df: pd.DataFrame,
    target_strategy: TargetStrategy = "binary",
    remove_g1_g2: bool = True,
    encode_method: str = "label",
    scale_method: str = "standard",
    custom_thresholds: Optional[List[float]] = None
) -> Tuple[pd.DataFrame, pd.Series, Dict]:
    """
    Complete preprocessing pipeline.
    
    Args:
        df: Raw dataframe
        target_strategy: How to engineer target
        remove_g1_g2: Whether to remove G1, G2
        encode_method: How to encode categorical
        scale_method: How to scale numerical
        custom_thresholds: For custom target strategy
        
    Returns:
        Tuple of (X, y, metadata)
    """
    from .preprocessor import encode_categorical, scale_numerical
    
    metadata = {
        "original_shape": df.shape,
        "target_strategy": target_strategy,
        "removed_leakage": remove_g1_g2,
        "encoding": encode_method,
        "scaling": scale_method
    }
    
    # 1. Engineer target
    target = engineer_target(df, target_strategy, custom_thresholds)
    df_with_target = df.copy()
    df_with_target["target"] = target
    
    # 2. Remove leakage features
    if remove_g1_g2:
        df_with_target = remove_leakage_features(df_with_target)
    
    # Remove G3 (already in target)
    if "G3" in df_with_target.columns:
        df_with_target = df_with_target.drop(columns=["G3"])
    
    # 3. Split X and y
    X, y = split_features_target(df_with_target, "target")
    
    # 4. Encode categorical
    X_encoded, encoders = encode_categorical(X, method=encode_method)
    metadata["encoders"] = encoders
    
    # 5. Scale numerical
    X_scaled, scaler = scale_numerical(X_encoded, method=scale_method)
    metadata["scaler"] = scaler
    
    # 6. Get distribution
    metadata["class_distribution"] = get_class_distribution(y)
    metadata["final_shape"] = X_scaled.shape
    
    logger.info(
        f"Preprocessing complete: {df.shape} → {X_scaled.shape}, "
        f"{len(y.unique())} classes"
    )
    
    return X_scaled, y, metadata

