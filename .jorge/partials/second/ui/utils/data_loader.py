"""
Data Loading and Preprocessing Utilities
"""

import numpy as np
import pandas as pd
from settings.config import CONF, Keys
from settings.imports import LabelEncoder, StandardScaler


def load_and_preprocess_data(
    use_full_dataset: bool = False, use_categorical: bool = False
):
    """
    Load and preprocess Bank Marketing dataset

    Args:
        use_full_dataset: If True, use bank-full.csv (45K), else bank.csv (4.5K)
        use_categorical: If True, include categorical features with Label encoding

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

    # Select features based on mode
    if use_categorical:
        # Use ALL features (numerical + categorical with encoding)
        numerical_cols = CONF[Keys.NUMERICAL_FEATURES]
        categorical_cols = CONF[Keys.CATEGORICAL_FEATURES]
        
        # Extract numerical features
        X_numerical = df[numerical_cols].values
        
        # Encode categorical features using LabelEncoder
        X_categorical_list = []
        for col in categorical_cols:
            le = LabelEncoder()
            X_categorical_list.append(le.fit_transform(df[col].values).reshape(-1, 1))
        
        X_categorical = np.hstack(X_categorical_list) if X_categorical_list else np.array([]).reshape(len(df), 0)
        
        # Combine numerical and encoded categorical
        X = np.hstack([X_numerical, X_categorical])
        feature_cols = numerical_cols + categorical_cols
    else:
        # Use only numerical features
        feature_cols = CONF[Keys.NUMERICAL_FEATURES]
        X = df[feature_cols].values

    # Extract and encode target
    y_raw = df[CONF[Keys.TARGET_COLUMN]].values
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)

    # Scale all features (numerical + encoded categorical)
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
        "feature_mode": "All (16)" if use_categorical else "Numerical (7)",
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
