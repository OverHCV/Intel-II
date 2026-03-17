"""
Dataset Configuration - Main View Coordinator
Organizes content into tabs and delegates to tab-specific renderers
"""

from content.dataset.tabs import augmentation, distribution, overview, samples
from content.dataset.tooltips import TAB_TOOLTIPS
from state.cache import get_dataset_info, set_dataset_info
from state.workflow import get_dataset_config, has_dataset_config
import streamlit as st
from utils.dataset_utils import scan_dataset


def render():
    """Main render function for Dataset page"""
    st.title("Dataset Configuration", help="Configure your malware image dataset for training.")

    # Initialize dataset cache
    dataset_info = get_dataset_info()
    if not dataset_info:
        with st.spinner("Scanning dataset..."):
            dataset_info = scan_dataset()
            set_dataset_info(dataset_info)

    # Auto-load saved configuration if it exists
    load_saved_configuration()

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📋 Overview & Split",
            "📊 Class Distribution",
            "🖼️ Samples & Preprocessing",
            "🔄 Augmentation",
        ]
    )

    with tab1:
        overview.render(dataset_info)

    with tab2:
        distribution.render(dataset_info)

    with tab3:
        samples.render(dataset_info)

    with tab4:
        augmentation.render(dataset_info)


def load_saved_configuration():
    """Load saved dataset configuration into session state ONCE.

    Only runs on first render to avoid overwriting user changes.
    """
    # Skip if already loaded this session
    if st.session_state.get("_dataset_config_loaded"):
        return

    if not has_dataset_config():
        return

    # Mark as loaded BEFORE loading to prevent re-entry
    st.session_state._dataset_config_loaded = True

    config = get_dataset_config()

    # Load selected classes
    if "selected_families" in config:
        st.session_state.selected_classes = config["selected_families"]

    # Load split configuration
    if "split" in config:
        split_config = config["split"]

        # Check split method
        if split_config.get("method") == "cross_validation":
            st.session_state.use_cross_validation = True
            if "n_folds" in split_config:
                st.session_state.n_folds = split_config["n_folds"]
            if "stratified" in split_config:
                st.session_state.stratified_kfold = split_config["stratified"]
        else:
            st.session_state.use_cross_validation = False
            if "train" in split_config:
                st.session_state.train_split = int(split_config["train"])
            if "val" in split_config and "test" in split_config:
                # Reverse calculate val_of_remaining from stored val percentage
                train_pct = int(split_config.get("train", 70))
                val_pct = split_config.get("val", 15)
                remaining = 100 - train_pct
                if remaining > 0:
                    val_of_remaining = int((val_pct / remaining) * 100)
                    st.session_state.val_split = val_of_remaining
            if "stratified" in split_config:
                st.session_state.stratified_split = split_config["stratified"]

        if "random_seed" in split_config:
            st.session_state.random_seed = split_config["random_seed"]

    # Load augmentation configuration
    if "augmentation" in config:
        aug_config = config["augmentation"]
        if "preset" in aug_config:
            st.session_state.augmentation_preset = aug_config["preset"]

        # Load custom augmentation settings
        if "custom" in aug_config and aug_config["preset"] == "Custom":
            custom = aug_config["custom"]
            # Map saved config keys to session state widget keys
            key_mapping = {
                "horizontal_flip": "aug_h_flip",
                "vertical_flip": "aug_v_flip",
                "rotation": "aug_rotation",
                "rotation_angles": "aug_rotation_angles",
                "brightness": "aug_brightness",
                "brightness_range": "aug_brightness_range",
                "contrast": "aug_contrast",
                "contrast_range": "aug_contrast_range",
                "gaussian_noise": "aug_noise",
            }
            for saved_key, value in custom.items():
                session_key = key_mapping.get(saved_key, f"aug_{saved_key}")
                st.session_state[session_key] = value

    # Load imbalance handling
    if "imbalance_handling" in config:
        imb_config = config["imbalance_handling"]
        if "strategy" in imb_config:
            st.session_state.imbalance_strategy = imb_config["strategy"]

        if "class_weights" in imb_config and imb_config["class_weights"]:
            st.session_state.class_weights = imb_config["class_weights"]

        if "smote_ratio" in imb_config and imb_config["smote_ratio"] is not None:
            st.session_state.smote_ratio = imb_config["smote_ratio"]
