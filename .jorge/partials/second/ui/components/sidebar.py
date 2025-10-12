"""
Sidebar Configuration Component
Handles all global configuration controls in the sidebar
"""

import streamlit as st
from ui.components.sliders import DiscreteSlider
from ui.utils import (
    get_config,
    get_dataset_info,
    load_and_preprocess_data,
    update_config,
)
from ui.utils.state_manager import get_data, set_data


def sidebar_render():
    """
    Render all configuration controls in the sidebar
    - Dataset selection (small/full)
    - CV strategy (train/test vs k-fold)
    - Data summary
    """

    st.divider()

    # ========== DATASET SELECTION ==========
    st.markdown("### 📊 Dataset")

    use_full = st.toggle(
        "Use Full Dataset",
        value=get_config("use_full_dataset"),
        help="Small: 4.5K samples | Full: 45K samples",
        key="dataset_toggle",
    )

    # Reload data if dataset type changed
    if use_full != get_config("use_full_dataset"):
        update_config("use_full_dataset", use_full)
        with st.spinner("Reloading..."):
            X, y, feature_names, data_info = load_and_preprocess_data(
                use_full_dataset=use_full,
                use_categorical=get_config("use_categorical"),
            )
            set_data(X, y, feature_names, data_info)
        st.success(f"✅ {'Full' if use_full else 'Small'} loaded!")
        st.rerun()

    # Show dataset info
    info = get_dataset_info(use_full)
    st.info(f"**{info['n_samples']:,}** samples\n**{info['n_features']}** features")

    st.divider()

    # ========== CV STRATEGY ==========
    st.markdown("### 🔄 Validation")

    cv_strategy = st.radio(
        "Method",
        options=["train_test", "kfold"],
        format_func=lambda x: "Train/Test (Fast)"
        if x == "train_test"
        else "K-Fold (Robust)",
        index=0 if get_config("cv_strategy") == "train_test" else 1,
        key="cv_strategy_radio",
    )
    update_config("cv_strategy", cv_strategy)

    if cv_strategy == "kfold":
        n_folds = DiscreteSlider(
            label="Folds",
            min_value=2,
            max_value=10,
            default_value=get_config("n_folds"),
            key="n_folds_slider",
            help_text="More = robust but slower",
        )
        update_config("n_folds", n_folds)

        estimated_time = n_folds * 2
        st.caption(f"⏱️ ~{estimated_time}s per model")
    else:
        st.caption("⚡ 80/20 split")

    st.divider()

    # ========== DATA SUMMARY ==========
    X, y, feature_names, data_info = get_data()

    if X is not None:
        st.markdown("### 📈 Data Summary")

        # Metrics in 2 rows
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Samples", f"{data_info['n_samples']:,}")
        with col2:
            st.metric("Features", data_info["n_features"])

        # Class distribution
        class_0_count = data_info["class_distribution"][data_info["classes"][0]]
        class_1_count = data_info["class_distribution"][data_info["classes"][1]]

        col1, col2 = st.columns(2)
        with col1:
            st.metric(data_info["classes"][0], f"{class_0_count:,}")
        with col2:
            st.metric(data_info["classes"][1], f"{class_1_count:,}")

        # Balance info
        st.caption(
            f"⚖️ {class_0_count / data_info['n_samples']:.1%} / "
            f"{class_1_count / data_info['n_samples']:.1%}"
        )

        # Feature list in expander
        with st.expander("📋 Features"):
            for i, feat in enumerate(feature_names, 1):
                st.caption(f"{i}. {feat}")
