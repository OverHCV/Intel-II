"""
Model Training for Decision Tree page.

Single Responsibility: Train CART model and generate all results.
"""

import numpy as np
import logging
import datetime
from typing import Dict, Any, Tuple, Optional, List
from sklearn.model_selection import train_test_split

from core.decision_tree import train_cart, extract_rules, rank_rules, cross_validate, get_feature_importance
from core.evaluation import evaluate_classification
from states import get_state, set_state, StateKeys

logger = logging.getLogger(__name__)


def get_feature_names(X_ready: np.ndarray) -> List[str]:
    """
    Get or reconstruct feature names from session state.
    
    Args:
        X_ready: Feature matrix (used to validate length)
    
    Returns:
        List of feature names
    """
    feature_names = get_state("feature_names", None)
    
    if feature_names is None or len(feature_names) != X_ready.shape[1]:
        # Fallback: try to reconstruct from raw data
        raw_df = get_state(StateKeys.RAW_DATA, None)
        if raw_df is not None:
            all_cols = list(raw_df.columns)
            exclude_list = ['G3', 'dataset_source']
            
            # Infer which G features are included based on shape
            if X_ready.shape[1] == 30:
                exclude_list.extend(['G1', 'G2'])
            elif X_ready.shape[1] == 31:
                pass  # One of G1/G2 included
            # else 32 features = both included
            
            feature_names = [col for col in all_cols if col not in exclude_list]
            
            # Final validation
            if len(feature_names) != X_ready.shape[1]:
                logger.warning(f"Feature name mismatch: {len(feature_names)} names vs {X_ready.shape[1]} features. Using generic names.")
                feature_names = [f"feature_{i}" for i in range(X_ready.shape[1])]
        else:
            logger.warning("No raw data or feature_names found. Using generic names.")
            feature_names = [f"feature_{i}" for i in range(X_ready.shape[1])]
    
    logger.info(f"Using feature names: {len(feature_names)} features")
    return feature_names


def get_class_names(y: np.ndarray) -> List[str]:
    """
    Get human-readable class names based on number of unique classes.
    
    Args:
        y: Target vector
    
    Returns:
        List of class names
    """
    unique_classes = np.unique(y)
    n_classes = len(unique_classes)
    
    if n_classes == 2:
        return ["Reprueba", "Aprueba"]
    elif n_classes == 3:
        return ["Bajo", "Medio", "Alto"]
    elif n_classes == 5:
        return ["F", "D", "C", "B", "A"]
    else:
        return [f"Clase {i}" for i in unique_classes]


def train_model(X: np.ndarray, y: np.ndarray, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Train CART model and generate all results.
    
    Pipeline:
    1. Get feature names
    2. Split train/test
    3. Train CART model
    4. Make predictions
    5. Evaluate metrics
    6. Extract and rank rules
    7. Cross-validate
    8. Get feature importance
    9. Save experiment to history
    
    Args:
        X: Feature matrix (prepared data)
        y: Target vector (prepared labels)
        params: Dict with hyperparameters and validation settings
    
    Returns:
        Dict with all results: {
            'model': trained model,
            'X_train': training features,
            'X_test': test features,
            'y_train': training labels,
            'y_test': test labels,
            'y_pred': predictions,
            'metrics': evaluation metrics,
            'class_names': class labels,
            'feature_names': feature names,
            'rules': extracted rules,
            'cv_results': cross-validation results,
            'feature_importance': feature importance dict,
            'experiment_id': saved experiment ID
        }
    
    Raises:
        Exception: If training fails
    """
    try:
        # Get feature and class names
        feature_names = get_feature_names(X)
        class_names = get_class_names(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=params['test_size'], 
            random_state=42, 
            stratify=y
        )
        
        # Train model
        model = train_cart(
            X_train, y_train,
            max_depth=params['max_depth'],
            min_samples_split=params['min_samples_split'],
            criterion=params['criterion'],
            random_state=42
        )
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Evaluate
        metrics = evaluate_classification(y_test, y_pred)
        
        # Extract rules
        rules = extract_rules(model, feature_names, class_names=class_names)
        ranked_rules = rank_rules(rules, criterion="combined")
        
        # Cross-validation
        cv_results = cross_validate(
            X, y,
            model_params={
                "max_depth": params['max_depth'],
                "min_samples_split": params['min_samples_split'],
                "criterion": params['criterion'],
                "random_state": 42
            },
            cv=params['cv_folds']
        )
        
        # Feature importance
        feature_importance = get_feature_importance(model, feature_names, top_n=10)
        
        # Store model and rules in state
        set_state(StateKeys.DT_MODEL, model)
        set_state(StateKeys.DT_RULES, ranked_rules)
        
        # Save experiment to history
        experiment_id = f"DT_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        experiment_data = {
            "id": experiment_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "algorithm": "Decision Tree (CART)",
            "params": {
                "max_depth": params['max_depth'],
                "min_samples_split": params['min_samples_split'],
                "criterion": params['criterion'],
                "test_size": params['test_size'],
                "cv_folds": params['cv_folds']
            },
            "data": {
                "total_samples": len(X),
                "n_features": X.shape[1],
                "n_classes": len(np.unique(y)),
                "train_samples": len(X_train),
                "test_samples": len(X_test)
            },
            "metrics": {
                "accuracy": metrics['accuracy'],
                "precision": metrics['precision'],
                "recall": metrics['recall'],
                "f1_score": metrics['f1_score'],
                "cv_mean": cv_results['mean'],
                "cv_std": cv_results['std']
            },
            "tree_info": {
                "depth": model.get_depth(),
                "n_leaves": model.get_n_leaves(),
                "n_rules": len(rules)
            }
        }
        
        # Append to experiment history
        history = get_state("experiment_history", [])
        history.append(experiment_data)
        set_state("experiment_history", history)
        
        logger.info(f"Saved experiment {experiment_id} to history")
        
        return {
            'model': model,
            'X_train': X_train,
            'X_test': X_test,
            'y_train': y_train,
            'y_test': y_test,
            'y_pred': y_pred,
            'metrics': metrics,
            'class_names': class_names,
            'feature_names': feature_names,
            'rules': ranked_rules,
            'cv_results': cv_results,
            'feature_importance': feature_importance,
            'experiment_id': experiment_id,
            'n_classes': len(np.unique(y))
        }
        
    except Exception as e:
        logger.error(f"Decision tree training error: {e}", exc_info=True)
        raise

