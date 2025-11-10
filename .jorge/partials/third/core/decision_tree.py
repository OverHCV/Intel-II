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
    
    Implements recursive tree traversal to extract all root-to-leaf paths.
    Each path becomes an IF-THEN rule with support and confidence metrics.
    
    Args:
        model: Trained decision tree
        feature_names: List of feature names
        class_names: Optional class labels (default: class_0, class_1, ...)
        
    Returns:
        List of rule dictionaries with conditions, predictions, support
    """
    tree = model.tree_
    rules = []
    
    if class_names is None:
        class_names = [f"class_{i}" for i in range(tree.n_classes[0])]
    
    def recurse(node, path_conditions, path_samples):
        """
        Recursive tree traversal to extract all paths.
        
        WHY: Each root-to-leaf path is a complete decision rule.
        """
        # If leaf node, create rule
        if tree.feature[node] == -2:  # Leaf node indicator
            # Get class distribution at this leaf
            class_samples = tree.value[node][0]
            total_samples = np.sum(class_samples)
            predicted_class_idx = np.argmax(class_samples)
            predicted_class = class_names[predicted_class_idx]
            confidence = class_samples[predicted_class_idx] / total_samples
            
            # Build human-readable condition string
            if len(path_conditions) == 0:
                condition_str = "ALWAYS (root only)"
            else:
                condition_str = " AND ".join(path_conditions)
            
            rule = {
                "id": len(rules) + 1,
                "conditions": condition_str,
                "prediction": predicted_class,
                "predicted_class_idx": int(predicted_class_idx),
                "support": int(total_samples),
                "support_pct": float(total_samples / tree.n_node_samples[0] * 100),
                "confidence": float(confidence),
                "purity": float(confidence),  # Same as confidence
                "depth": len(path_conditions),
                "class_distribution": {
                    class_names[i]: int(class_samples[i])
                    for i in range(len(class_names))
                },
                "simplicity_score": 1.0 / (len(path_conditions) + 1)  # Shorter = simpler
            }
            rules.append(rule)
            return
        
        # Internal node - recurse left and right
        feature_idx = tree.feature[node]
        threshold = tree.threshold[node]
        feature_name = feature_names[feature_idx]
        
        # Left child (<=)
        left_condition = f"{feature_name} <= {threshold:.3f}"
        left_path = path_conditions + [left_condition]
        recurse(tree.children_left[node], left_path, path_samples)
        
        # Right child (>)
        right_condition = f"{feature_name} > {threshold:.3f}"
        right_path = path_conditions + [right_condition]
        recurse(tree.children_right[node], right_path, path_samples)
    
    # Start recursion from root
    recurse(0, [], tree.n_node_samples[0])
    
    logger.info(f"Extracted {len(rules)} rules from decision tree")
    return rules


def rank_rules(
    rules: List[Dict[str, Any]],
    criterion: str = "support"
) -> List[Dict[str, Any]]:
    """
    Rank extracted rules by importance.
    
    WHY: Not all rules are equally useful - prioritize high-support,
         high-confidence rules for actionable insights.
    
    Supports multiple ranking criteria:
    - support: Number of samples (common patterns)
    - confidence: Prediction certainty (reliable rules)
    - purity: Class homogeneity at leaf
    - simplicity: Shorter rules (easier to interpret)
    - combined: Weighted combination
    
    Args:
        rules: List of rule dictionaries
        criterion: Ranking criterion
        
    Returns:
        Sorted list of rules (highest first)
    """
    if not rules:
        logger.warning("No rules to rank")
        return []
    
    # Define sorting keys
    if criterion == "support":
        sort_key = lambda r: r.get("support", 0)
    elif criterion == "confidence":
        sort_key = lambda r: r.get("confidence", 0)
    elif criterion == "purity":
        sort_key = lambda r: r.get("purity", 0)
    elif criterion == "simplicity":
        sort_key = lambda r: r.get("simplicity_score", 0)
    elif criterion == "combined":
        # Combined score: support * confidence * simplicity
        # WHY: Balances all three factors - want common, reliable, simple rules
        sort_key = lambda r: (
            r.get("support", 0) *
            r.get("confidence", 0) *
            r.get("simplicity_score", 0)
        )
    else:
        logger.warning(f"Unknown criterion '{criterion}', using support")
        sort_key = lambda r: r.get("support", 0)
    
    ranked_rules = sorted(rules, key=sort_key, reverse=True)
    
    logger.info(f"Ranked {len(ranked_rules)} rules by {criterion}")
    logger.info(f"Top rule: support={ranked_rules[0].get('support')}, "
                f"confidence={ranked_rules[0].get('confidence'):.3f}")
    
    return ranked_rules


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

