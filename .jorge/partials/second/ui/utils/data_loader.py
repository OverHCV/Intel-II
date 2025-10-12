"""
Data Loading and Preprocessing Utilities
"""

import numpy as np
import pandas as pd
from settings.config import CONF, Keys
from settings.feats import BankFeatures, BankTarget
from settings.imports import LabelEncoder, StandardScaler


def load_and_preprocess_data(
    use_full_dataset: bool = False, use_categorical: bool = False
):
    """
    Load and preprocess Bank Marketing dataset

    Args:
        use_full_dataset: If True, use bank-full.csv (45K), else bank.csv (4.5K)
        use_categorical: If True, include categorical features with OneHot encoding

    Returns:
        tuple: (X_scaled, y, feature_names, dataset_info)
    """
    # Load dataset
    dataset_path = (
        CONF[Keys.DATASET_PATH_FULL]
        if use_full_dataset
        else CONF[Keys.DATASET_PATH_SMALL]
    )

    df = pd.read_csv(
        dataset_path,
        delimiter=CONF[Keys.DATASET_DELIMITER],
        encoding=CONF[Keys.DATASET_ENCODING],
    )

    # Select features
    if use_categorical:
        # Use all features (numerical + categorical)
        # For now, just use numerical to keep it simple
        # TODO: Implement OneHot encoding for categorical
        feature_cols = CONF[Keys.NUMERICAL_FEATURES]
    else:
        # Use only numerical features
        feature_cols = CONF[Keys.NUMERICAL_FEATURES]

    # Extract features and target
    X = df[feature_cols].values
    y_raw = df[CONF[Keys.TARGET_COLUMN]].values

    # Encode target labels (yes/no → 1/0)
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Dataset info
    dataset_info = {
        "n_samples": X.shape[0],
        "n_features": X.shape[1],
        "feature_names": feature_cols,
        "target_name": CONF[Keys.TARGET_COLUMN],
        "classes": label_encoder.classes_.tolist(),
        "class_distribution": {
            label_encoder.classes_[0]: int((y == 0).sum()),
            label_encoder.classes_[1]: int((y == 1).sum()),
        },
        "dataset_type": "Full" if use_full_dataset else "Small",
    }

    return X_scaled, y, feature_cols, dataset_info


def get_dataset_info(use_full_dataset: bool = False):
    """
    Get dataset info without loading full data

    Args:
        use_full_dataset: Which dataset to check

    Returns:
        dict: Dataset information
    """
    dataset_path = (
        CONF[Keys.DATASET_PATH_FULL]
        if use_full_dataset
        else CONF[Keys.DATASET_PATH_SMALL]
    )

    df = pd.read_csv(
        dataset_path,
        delimiter=CONF[Keys.DATASET_DELIMITER],
        encoding=CONF[Keys.DATASET_ENCODING],
    )

    return {
        "path": dataset_path,
        "n_samples": len(df),
        "n_features": len(df.columns) - 1,  # -1 for target
        "target_distribution": df[CONF[Keys.TARGET_COLUMN]].value_counts().to_dict(),
    }
