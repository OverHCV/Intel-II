"""
Session State Management
"""

import streamlit as st
from settings.config import CONF, Keys


def init_session_state():
    """
    Initialize Streamlit session state with default values
    Auto-loads small dataset on first run
    """
    # Config settings
    if "config" not in st.session_state:
        st.session_state.config = {
            "use_full_dataset": False,  # Start with small dataset
            "use_categorical": False,  # Start with numerical only
            "cv_strategy": "kfold",  # Default to K-Fold CV (more robust)
            "n_folds": CONF[Keys.CV_FOLDS],  # Default from config
            "random_state": CONF[Keys.RANDOM_STATE],
        }

    # Data cache - auto-load small dataset on first run
    if "data" not in st.session_state:
        from ui.utils.data_loader import load_and_preprocess_data

        X, y, feature_names, data_info = load_and_preprocess_data(
            use_full_dataset=False, use_categorical=False
        )
        st.session_state.data = {
            "X": X,
            "y": y,
            "feature_names": feature_names,
            "info": data_info,
        }

    # SVM results
    if "svm" not in st.session_state:
        # Load persisted experiment history
        from funcs.persistence import load_experiments_from_file

        st.session_state.svm = {
            "model": None,
            "params": {},
            "metrics": {},
            "is_trained": False,
            "best_model": None,
            "best_metrics": {},
            "best_params": {},
            "experiment_history": load_experiments_from_file("svm"),  # Load from disk
        }

    # ANN results
    if "ann" not in st.session_state:
        st.session_state.ann = {
            "model": None,
            "params": {},
            "metrics": {},
            "is_trained": False,
            "best_model": None,
            "best_metrics": {},
        }

    # PCA results
    if "pca" not in st.session_state:
        st.session_state.pca = {
            "pca_object": None,
            "n_components": 10,
            "X_pca": None,
            "svm_pca_metrics": {},
            "ann_pca_metrics": {},
        }


def get_config(key: str = None):
    """
    Get configuration value from session state

    Args:
        key: Config key (if None, returns full config dict)

    Returns:
        Config value or full config dict
    """
    if key is None:
        return st.session_state.config
    return st.session_state.config.get(key)


def update_config(key: str, value):
    """
    Update configuration in session state

    Args:
        key: Config key
        value: New value
    """
    st.session_state.config[key] = value


def get_data():
    """
    Get loaded data from session state

    Returns:
        tuple: (X, y, feature_names, info) or (None, None, None, None) if not loaded
    """
    data = st.session_state.data
    return data["X"], data["y"], data["feature_names"], data["info"]


def set_data(X, y, feature_names, info):
    """
    Store loaded data in session state

    Args:
        X: Feature matrix
        y: Target vector
        feature_names: List of feature names
        info: Dataset info dict
    """
    st.session_state.data["X"] = X
    st.session_state.data["y"] = y
    st.session_state.data["feature_names"] = feature_names
    st.session_state.data["info"] = info
