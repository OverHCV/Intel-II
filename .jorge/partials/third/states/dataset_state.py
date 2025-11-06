"""
Dataset State - Initialize dataset-related state.

This module manages state for:
- Raw data (DataFrame before preprocessing)
- Prepared data (X, y after preprocessing)
- Dataset metadata (name, strategy, balance method)
"""

import logging
from .state_manager import init_state, StateKeys

logger = logging.getLogger(__name__)


def init_dataset_state():
    """
    Initialize dataset-related state keys.
    
    Called once at app startup to ensure consistent defaults.
    """
    # Dataset selection
    init_state(StateKeys.DATASET_NAME, None)
    
    # Raw and processed data
    init_state(StateKeys.RAW_DATA, None)
    init_state(StateKeys.X_PREPARED, None)
    init_state(StateKeys.Y_PREPARED, None)
    
    # Data configuration
    init_state(StateKeys.TARGET_STRATEGY, None)
    init_state(StateKeys.BALANCE_METHOD, None)
    
    # UI flags
    init_state("data_loaded", False)
    init_state("data_preparation_timestamp", None)
    
    logger.debug("Dataset state initialized")

