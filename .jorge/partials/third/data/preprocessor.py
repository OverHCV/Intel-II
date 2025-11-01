"""
Data Preprocessor - Encoding and scaling functions.

Responsibilities:
- Encode categorical variables (label encoding, one-hot)
- Scale numerical features (standard, minmax)

NO algorithms, NO UI code, NO file I/O.
"""

import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Literal, Optional
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
import logging

logger = logging.getLogger(__name__)

EncodingMethod = Literal["label", "onehot"]
ScalingMethod = Literal["standard", "minmax", "none"]


def encode_categorical(
    df: pd.DataFrame,
    method: EncodingMethod = "label",
    columns: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, Dict]:
    """
    Encode categorical variables.
    
    Args:
        df: DataFrame with categorical columns
        method: Encoding method ('label' or 'onehot')
        columns: List of columns to encode (defaults to all object/category columns)
        
    Returns:
        Tuple of (encoded_df, encoders_dict)
    """
    df_encoded = df.copy()
    encoders = {}
    
    if columns is None:
        columns = df.select_dtypes(include=["object", "category"]).columns.tolist()
        # Exclude dataset_source if present
        columns = [c for c in columns if c != "dataset_source"]
    
    if method == "label":
        for col in columns:
            if col not in df.columns:
                logger.warning(f"Column {col} not found, skipping")
                continue
            
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
            
            logger.debug(f"Label encoded {col}: {len(le.classes_)} classes")
        
        logger.info(f"Label encoded {len(columns)} columns")
    
    elif method == "onehot":
        df_encoded = pd.get_dummies(
            df_encoded,
            columns=columns,
            prefix=columns,
            drop_first=True  # Avoid dummy variable trap
        )
        encoders["method"] = "onehot"
        encoders["columns"] = columns
        
        logger.info(
            f"One-hot encoded {len(columns)} columns, "
            f"resulting in {len(df_encoded.columns)} total columns"
        )
    
    else:
        raise ValueError(f"Invalid method: {method}. Must be 'label' or 'onehot'")
    
    return df_encoded, encoders


def scale_numerical(
    df: pd.DataFrame,
    method: ScalingMethod = "standard",
    columns: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, Optional[object]]:
    """
    Scale numerical features.
    
    Args:
        df: DataFrame with numerical columns
        method: Scaling method ('standard', 'minmax', or 'none')
        columns: List of columns to scale (defaults to all numeric columns)
        
    Returns:
        Tuple of (scaled_df, scaler_object)
    """
    if method == "none":
        logger.info("No scaling applied")
        return df.copy(), None
    
    df_scaled = df.copy()
    
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if method == "standard":
        scaler = StandardScaler()
        df_scaled[columns] = scaler.fit_transform(df[columns])
        logger.info(f"Standard scaled {len(columns)} columns")
    
    elif method == "minmax":
        scaler = MinMaxScaler()
        df_scaled[columns] = scaler.fit_transform(df[columns])
        logger.info(f"MinMax scaled {len(columns)} columns")
    
    else:
        raise ValueError(f"Invalid method: {method}. Must be 'standard', 'minmax', or 'none'")
    
    return df_scaled, scaler


