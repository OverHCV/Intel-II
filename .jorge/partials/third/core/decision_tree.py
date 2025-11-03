"""
Decision Tree module - CART algorithm with rule extraction.

This module implements Classification and Regression Trees (CART) for student
performance prediction, with emphasis on extractable rules for interpretability.

WHY: Educational context requires transparent models - teachers need to understand
     WHY a student is predicted to fail/pass, not just the prediction itself.
"""

from typing import Dict, List, Tuple, Optional, Any
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
import logging

logger = logging.getLogger(__name__)


def train_cart(
    X: np.ndarray,
    y: np.ndarray,
    max_depth: Optional[int] = None,
    min_samples_split: int = 2,
    min_samples_leaf: int = 1,
    criterion: str = "gini",
    random_state: Optional[int] = None
) -> DecisionTreeClassifier:
    """
    Train a CART decision tree classifier.
    
    WHY: CART provides interpretable rules and handles both numerical and
         categorical features naturally (after preprocessing).
    
    Args:
        X: Feature matrix (n_samples, n_features)
        y: Target vector (n_samples,)
        max_depth: Maximum tree depth (None = unlimited)
        min_samples_split: Min samples required to split node
        min_samples_leaf: Min samples required at leaf
        criterion: Split quality measure ("gini" or "entropy")
        random_state: Random seed for reproducibility
        
    Returns:
        Trained DecisionTreeClassifier model
    """
    model = DecisionTreeClassifier(
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        criterion=criterion,
        random_state=random_state
    )
    
    model.fit(X, y)
    logger.info(f"CART trained: depth={model.get_depth()}, leaves={model.get_n_leaves()}")
    
    return model


def extract_rules(
    model: DecisionTreeClassifier,
    feature_names: List[str],
    class_names: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Extract human-readable rules from trained decision tree.
    
    WHY: Rules like "IF studytime <= 2 AND failures > 0 THEN predict Fail"
         are actionable insights for educators.
    
    WIP: Full rule extraction with path tracing and support calculation.
         Currently returns basic structure.
    
    Args:
        model: Trained decision tree
        feature_names: List of feature names
        class_names: Optional class labels
        
    Returns:
        List of rule dictionaries with conditions, predictions, support
    """
    # WIP: Implement recursive tree traversal to extract all paths
    # WHY: Need to traverse from root to each leaf to build IF-THEN rules
    
    tree = model.tree_
    rules = []
    
    # Placeholder structure showing what each rule will contain
    rules.append({
        "id": 1,
        "conditions": "WIP: IF-THEN conditions from root to leaf",
        "prediction": "WIP: Class prediction at leaf",
        "support": "WIP: Number of samples following this path",
        "confidence": "WIP: Purity at leaf node",
        "depth": tree.max_depth,
        "why": "Each rule represents a decision path educators can interpret"
    })
    
    logger.info(f"Extracted {len(rules)} rules (WIP: placeholder)")
    return rules


def rank_rules(
    rules: List[Dict[str, Any]],
    criterion: str = "support"
) -> List[Dict[str, Any]]:
    """
    Rank extracted rules by importance.
    
    WHY: Not all rules are equally useful - prioritize high-support,
         high-confidence rules for actionable insights.
    
    Args:
        rules: List of rule dictionaries
        criterion: Ranking criterion ("support", "confidence", "depth")
        
    Returns:
        Sorted list of rules
    """
    # WIP: Implement multi-criteria ranking
    # WHY: Different stakeholders care about different metrics
    #      - Teachers: high support (common patterns)
    #      - Interventions: high confidence (reliable predictions)
    
    logger.info(f"Ranking {len(rules)} rules by {criterion} (WIP)")
    return rules


def cross_validate(
    X: np.ndarray,
    y: np.ndarray,
    model_params: Dict[str, Any],
    cv: int = 5,
    scoring: str = "accuracy"
) -> Dict[str, float]:
    """
    Perform k-fold cross-validation on decision tree.
    
    WHY: Single train/test split can be misleading - CV provides
         more robust performance estimates.
    
    Args:
        X: Feature matrix
        y: Target vector
        model_params: Decision tree hyperparameters
        cv: Number of folds
        scoring: Metric to evaluate
        
    Returns:
        Dictionary with mean, std, and all fold scores
    """
    model = DecisionTreeClassifier(**model_params)
    scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
    
    results = {
        "mean": float(np.mean(scores)),
        "std": float(np.std(scores)),
        "scores": scores.tolist(),
        "cv_folds": cv
    }
    
    logger.info(f"CV {cv}-fold: {results['mean']:.3f} ± {results['std']:.3f}")
    return results


def get_feature_importance(
    model: DecisionTreeClassifier,
    feature_names: List[str],
    top_n: Optional[int] = None
) -> Dict[str, float]:
    """
    Get feature importance from trained tree.
    
    WHY: Identifies which student attributes most influence predictions.
         Guides where to focus intervention efforts.
    
    Args:
        model: Trained decision tree
        feature_names: List of feature names
        top_n: Return only top N features (None = all)
        
    Returns:
        Dictionary mapping feature names to importance scores
    """
    importances = model.feature_importances_
    feature_importance = dict(zip(feature_names, importances))
    
    # Sort by importance
    sorted_features = sorted(
        feature_importance.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    if top_n:
        sorted_features = sorted_features[:top_n]
    
    logger.info(f"Top feature: {sorted_features[0][0]} ({sorted_features[0][1]:.3f})")
    return dict(sorted_features)


# Module metadata
__version__ = "1.0.0"
__algorithms__ = ["CART"]

