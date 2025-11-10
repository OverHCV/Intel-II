"""
Experiments State - Initialize experiment tracking state.

This module manages state for:
- Trained models (DT, Hierarchical, K-means)
- Experiment history
- Model artifacts (rules, labels, metrics)
- UI widget values (hyperparameters, for persistence)
"""

import logging
from .state_manager import init_state, StateKeys

logger = logging.getLogger(__name__)


def init_experiments_state():
    """
    Initialize experiment tracking state keys.
    
    Called once at app startup to ensure consistent defaults.
    Includes UI widget defaults for persistence.
    """
    # Decision Tree
    init_state(StateKeys.DT_MODEL, None)
    init_state(StateKeys.DT_RULES, None)
    
    # DT UI widget values (for persistence)
    init_state("dt_max_depth", 5)
    init_state("dt_min_samples_split", 2)
    init_state("dt_criterion", "gini")
    init_state("dt_test_size_pct", 20)  # Percentage (will divide by 100)
    init_state("dt_cv_folds", 5)
    
    # Hierarchical Clustering
    init_state(StateKeys.HC_LABELS, None)
    init_state("hierarchical_linkage", None)
    init_state("hierarchical_j4_score", None)
    
    # HC UI widget values
    init_state("hc_linkage_method", "ward")
    init_state("hc_n_clusters", 5)
    init_state("hc_find_optimal", False)
    
    # K-means
    init_state(StateKeys.KM_LABELS, None)
    init_state("kmeans_model", None)
    init_state("kmeans_inertia", None)
    
    # KM UI widget values
    init_state("km_n_clusters", 5)
    init_state("km_max_iter", 300)
    
    # Experiment history (shared across algorithms)
    init_state(StateKeys.EXPERIMENT_HISTORY, [])
    init_state("experiment_history", [])  # Legacy key for DT page
    
    # UI flags
    init_state("_training_now", False)
    
    logger.debug("Experiments state initialized with UI widget defaults")

