"""
State Manager - Centralized state management using Streamlit session_state.

This module provides a clean interface to manage application state,
preventing common Streamlit pitfalls like lost data on rerun.

WHY: Streamlit reruns the entire script on every interaction. Without proper
     state management, you lose trained models, loaded data, and user settings.
"""

import streamlit as st
from typing import Any, Optional, Callable
import logging

logger = logging.getLogger(__name__)


def init_state(key: str, default: Any) -> None:
    """
    Initialize state key with default value if not exists.
    
    WHY: Lazy initialization pattern - don't compute expensive values
         until actually needed.
    
    Args:
        key: State key name
        default: Default value
    """
    if key not in st.session_state:
        st.session_state[key] = default
        logger.debug(f"Initialized state: {key}")


def get_state(key: str, default: Optional[Any] = None) -> Any:
    """
    Get state value with optional default.
    
    Args:
        key: State key name
        default: Default if key doesn't exist
        
    Returns:
        State value or default
    """
    return st.session_state.get(key, default)


def set_state(key: str, value: Any) -> None:
    """
    Set state value.
    
    Args:
        key: State key name
        value: Value to store
    """
    st.session_state[key] = value
    logger.debug(f"Updated state: {key}")


def reset_state(keys: Optional[list] = None) -> None:
    """
    Reset specified state keys or all state.
    
    WHY: Clean slate when switching between datasets or algorithms.
    
    Args:
        keys: List of keys to reset (None = reset all)
    """
    if keys is None:
        st.session_state.clear()
        logger.info("Cleared all state")
    else:
        for key in keys:
            if key in st.session_state:
                del st.session_state[key]
        logger.info(f"Cleared state keys: {keys}")


def state_exists(key: str) -> bool:
    """
    Check if state key exists.
    
    Args:
        key: State key name
        
    Returns:
        True if key exists in session state
    """
    return key in st.session_state


def get_or_compute(
    key: str,
    compute_fn: Callable[[], Any],
    force_recompute: bool = False
) -> Any:
    """
    Get state value or compute and cache it.
    
    WHY: Avoid expensive recomputations. E.g., loading dataset once,
         training model once, even across multiple page visits.
    
    Args:
        key: State key for caching
        compute_fn: Function to compute value if not cached
        force_recompute: Force recomputation even if cached
        
    Returns:
        Cached or computed value
    """
    if force_recompute or not state_exists(key):
        value = compute_fn()
        set_state(key, value)
        logger.info(f"Computed and cached: {key}")
        return value
    else:
        logger.debug(f"Retrieved from cache: {key}")
        return get_state(key)


# Common state keys (constants to avoid typos)
class StateKeys:
    """Centralized state key definitions."""
    
    # Page navigation
    CURRENT_PAGE = "current_page"
    
    # Data keys
    DATASET_NAME = "dataset_name"
    RAW_DATA = "raw_data"
    PROCESSED_DATA = "processed_data"
    DATA_METADATA = "data_metadata"
    TARGET_STRATEGY = "target_strategy"
    BALANCE_METHOD = "balance_method"
    X_PREPARED = "X_prepared"
    Y_PREPARED = "y_prepared"
    
    # Model keys
    DT_MODEL = "dt_model"
    DT_RULES = "dt_rules"
    HC_LABELS = "hc_labels"
    KM_LABELS = "km_labels"
    
    # Model keys  
    CURRENT_MODEL = "current_model"
    MODEL_METRICS = "model_metrics"
    PREDICTIONS = "predictions"
    
    # UI keys
    CURRENT_PAGE = "current_page"
    SIDEBAR_STATE = "sidebar_state"
    
    # Experiment keys
    EXPERIMENT_HISTORY = "experiment_history"
    SELECTED_EXPERIMENTS = "selected_experiments"


# Module metadata
__version__ = "1.0.0"

