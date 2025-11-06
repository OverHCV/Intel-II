"""
Experiments State - Initialize experiment tracking state.

This module manages state for:
- Trained models (DT, Hierarchical, K-means)
- Experiment history
- Model artifacts (rules, labels, metrics)
"""

import logging
from .state_manager import init_state, StateKeys

logger = logging.getLogger(__name__)


def init_experiments_state():
    """
    Initialize experiment tracking state keys.
    
    Called once at app startup to ensure consistent defaults.
    """
    # Decision Tree
    init_state(StateKeys.DT_MODEL, None)
    init_state(StateKeys.DT_RULES, None)
    
    # Hierarchical Clustering
    init_state(StateKeys.HC_LABELS, None)
    init_state("hierarchical_linkage", None)
    init_state("hierarchical_j4_score", None)
    
    # K-means
    init_state(StateKeys.KM_LABELS, None)
    init_state("kmeans_model", None)
    init_state("kmeans_inertia", None)
    
    # Experiment history (shared across algorithms)
    init_state(StateKeys.EXPERIMENT_HISTORY, [])
    init_state("experiment_history", [])  # Legacy key for DT page
    
    # UI flags
    init_state("_training_now", False)
    
    logger.debug("Experiments state initialized")

