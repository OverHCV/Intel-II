"""
Configuration Page - Dataset and global settings
"""

import streamlit as st
from settings.config import CONF, Keys
from ui.components import DiscreteSlider, MetricsGrid, TwoColumnLayout
from ui.utils import (
    get_config,
    get_dataset_info,
    load_and_preprocess_data,
    update_config,
)
from ui.utils.state_manager import set_data


def config_page():
    """
    Configuration tab content
    - Dataset selection (small/full)
    - CV strategy (train/test vs k-fold)
    - Feature selection (numerical only for now)
    - Data preview
    """
    st.title("⚙️ Configuration & Setup")
    st.markdown("Configure global settings for the analysis")

    st.divider()

    # Dataset Selection
    st.subheader("📊 Dataset Selection")

    col1, col2 = st.columns(2)

    with col1:
        use_full = st.toggle(
            "Use Full Dataset",
            value=get_config("use_full_dataset"),
            help="Toggle between small (4.5K) and full (45K) dataset",
            key="dataset_toggle",
        )

        # Reload data if dataset type changed
        if use_full != get_config("use_full_dataset"):
            update_config("use_full_dataset", use_full)
            with st.spinner("Reloading dataset..."):
                X, y, feature_names, data_info = load_and_preprocess_data(
                    use_full_dataset=use_full,
                    use_categorical=get_config("use_categorical"),
                )
                set_data(X, y, feature_names, data_info)
            st.success(f"✅ {'Full' if use_full else 'Small'} dataset loaded!")
            st.rerun()

        # Show dataset info
        info = get_dataset_info(use_full)
        st.info(
            f"**{info['n_samples']:,}** samples × **{info['n_features']}** features"
        )

    with col2:
        use_cat = st.toggle(
            "Include Categorical Features",
            value=get_config("use_categorical"),
            help="Include categorical features (OneHot encoded) - Feature not yet implemented",
            key="categorical_toggle",
            disabled=True,
        )
        update_config("use_categorical", use_cat)

        st.caption("ℹ️ Only numerical features currently available")

    st.divider()

    # CV Strategy
    st.subheader("🔄 Cross-Validation Strategy")

    cv_strategy = st.radio(
        "Evaluation Method",
        options=["train_test", "kfold"],
        format_func=lambda x: "Train/Test Split (Fast)"
        if x == "train_test"
        else "K-Fold CV (Robust)",
        index=0 if get_config("cv_strategy") == "train_test" else 1,
        key="cv_strategy_radio",
        horizontal=True,
    )
    update_config("cv_strategy", cv_strategy)

    if cv_strategy == "kfold":
        n_folds = DiscreteSlider(
            label="Number of Folds",
            min_value=2,
            max_value=10,
            default_value=get_config("n_folds"),
            key="n_folds_slider",
            help_text="More folds = more robust but slower",
        )
        update_config("n_folds", n_folds)

        estimated_time = n_folds * 2  # Rough estimate
        st.caption(f"⏱️ Estimated training time: ~{estimated_time}s per model")
    else:
        st.caption("⚡ Fast evaluation using 80/20 train/test split")

    st.divider()

    # Show loaded data info (auto-loaded on init)
    from ui.utils.state_manager import get_data

    X, y, feature_names, data_info = get_data()

    if X is not None:
        st.divider()
        st.subheader("📈 Loaded Data Summary")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Samples", f"{data_info['n_samples']:,}")

        with col2:
            st.metric("Features", data_info["n_features"])

        with col3:
            class_0_count = data_info["class_distribution"][data_info["classes"][0]]
            st.metric(f"Class: {data_info['classes'][0]}", f"{class_0_count:,}")

        with col4:
            class_1_count = data_info["class_distribution"][data_info["classes"][1]]
            st.metric(f"Class: {data_info['classes'][1]}", f"{class_1_count:,}")

        # Feature list
        with st.expander("📋 Feature List"):
            st.write(feature_names)

        # Class balance
        st.caption(
            f"⚖️ Class balance: {class_0_count / data_info['n_samples']:.1%} / {class_1_count / data_info['n_samples']:.1%}"
        )
