"""
States Package - Centralized state management.

This is a SINGLETON pattern. All state is managed through st.session_state,
and this module provides a clean, typed interface.

Usage:
    from states import get_state, set_state, StateKeys, init_all_state
    
    # In app.py (once, at start):
    init_all_state()
    
    # In any page:
    X = get_state(StateKeys.X_PREPARED)
    set_state(StateKeys.DT_MODEL, model)
"""

from .state_manager import (
    init_state,
    get_state,
    set_state,
    reset_state,
    state_exists,
    get_or_compute,
    StateKeys
)

from .dataset_state import init_dataset_state
from .experiments_state import init_experiments_state


def init_all_state():
    """
    Initialize all application state.
    
    Call this ONCE at app startup (in app.py) to ensure consistent state.
    """
    init_dataset_state()
    init_experiments_state()


__all__ = [
    'init_state',
    'get_state',
    'set_state',
    'reset_state',
    'state_exists',
    'get_or_compute',
    'StateKeys',
    'init_all_state',
    'init_dataset_state',
    'init_experiments_state'
]

