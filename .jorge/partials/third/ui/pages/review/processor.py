"""
Data Processing for Dataset Review page.

Single Responsibility: Load, transform, and prepare data based on user selections.
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, Tuple, Any

from data.loader import load_dataset
from data.transformer import engineer_target, remove_leakage_features, split_features_target
from data.preprocessor import encode_categorical, scale_numerical
from data.balancer import balance_classes
from states import set_state, StateKeys

logger = logging.getLogger(__name__)


def process_data(user_selections: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    """
    Process data based on user selections.
    
    Pipeline:
    1. Load dataset
    2. Engineer target
    3. Remove leakage features (conditional on G1/G2 toggles)
    4. Split X and y
    5. Encode categorical
    6. Scale numerical
    7. Apply balancing
    8. Store in session state
    
    Args:
        user_selections: Dict from controls.render_controls()
    
    Returns:
        Tuple of (X_final, y_final, df_raw)
    
    Raises:
        Exception: If any processing step fails
    """
    # Extract user selections
    dataset_choice = user_selections['dataset'].split(" ")[0].lower()  # "portuguese" or "math"
    target_type = user_selections['target_strategy'].split(" ")[0].lower()  # "binary", "five-class", etc.
    balance_method = user_selections['balance_method']
    k_neighbors = user_selections['k_neighbors']
    include_g1 = user_selections['include_g1']
    include_g2 = user_selections['include_g2']
    
    # 1. Load dataset
    logger.info(f"Loading dataset: {dataset_choice}")
    df_raw = load_dataset(dataset_choice)
    
    # 2. Engineer target
    target_map = {
        "binary": "binary",
        "three-class": "three_class",
        "five-class": "five_class"
    }
    target_strategy = target_map.get(target_type, "binary")
    logger.info(f"Engineering target: {target_strategy}")
    y = engineer_target(df_raw, target_strategy)
    
    # 3. Remove leakage features (conditional on toggles)
    features_to_remove = []
    if not include_g1:
        features_to_remove.append("G1")
    if not include_g2:
        features_to_remove.append("G2")
    
    if features_to_remove:
        df_clean = remove_leakage_features(df_raw, features_to_remove=features_to_remove)
        logger.info(f"Removed leakage features: {features_to_remove}")
    else:
        # Keep G1/G2, but remove dataset_source
        df_clean = remove_leakage_features(df_raw, features_to_remove=["dataset_source"])
        logger.info("Keeping G1/G2 (data leakage mode)")
    
    # 4. Split X and y
    X, _ = split_features_target(df_clean.assign(target=y), "target")
    logger.info(f"Split into X: {X.shape}")
    
    # 5. Encode categorical
    X_encoded, encoders = encode_categorical(X, method="label")
    logger.info(f"Encoded categorical features: {X_encoded.shape}")
    
    # 6. Scale numerical
    X_scaled, scalers = scale_numerical(X_encoded, method="standard")
    logger.info(f"Scaled numerical features: {X_scaled.shape}")
    
    # 7. Apply balancing
    balance_map = {
        "SMOTE": "smote",
        "None": "none",
        "Random Oversample": "random_over",
        "Random Undersample": "random_under"
    }
    balance_strategy = balance_map[balance_method]
    
    logger.info(f"Applying balancing: {balance_strategy}")
    X_final, y_final = balance_classes(
        X_scaled, y,
        method=balance_strategy,
        random_state=42,
        k_neighbors=k_neighbors if balance_strategy == "smote" else 5
    )
    
    logger.info(f"Final shapes: X={X_final.shape}, y={len(y_final)}")
    
    # 8. Store in session state (ONLY metadata keys, NOT widget keys!)
    set_state(StateKeys.RAW_DATA, df_raw)
    set_state(StateKeys.X_PREPARED, X_final)
    set_state(StateKeys.Y_PREPARED, y_final)
    
    # Store metadata (derived from widget values)
    set_state(StateKeys.DATASET_NAME, dataset_choice)
    set_state(StateKeys.TARGET_STRATEGY, target_strategy)
    set_state(StateKeys.BALANCE_METHOD, balance_strategy)
    
    # Store feature names for later use (CRITICAL for Decision Trees)
    feature_names_list = [col for col in df_raw.columns 
                          if col not in ['G3', 'dataset_source'] + features_to_remove]
    set_state("feature_names", feature_names_list)
    
    # Mark data as loaded
    set_state("data_loaded", True)
    
    logger.info("✅ Data processing complete and stored in session state")
    
    return X_final, y_final, df_raw

