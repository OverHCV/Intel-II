"""
Sidebar Configuration Component
Handles all global configuration controls in the sidebar
"""

import streamlit as st
from ui.components.sliders import DiscreteSlider
from ui.utils import (
    get_config,
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

    # Feature type selection
    use_categorical = st.toggle(
        "Include Categorical Features",
        value=get_config("use_categorical") or False,
        help="🔢 OFF: 7 numerical features | 📊 ON: 16 features (7 numerical + 9 categorical)",
        key="categorical_toggle",
    )
    
    # Reload data if settings changed
    needs_reload = (
        use_full != get_config("use_full_dataset") or
        use_categorical != get_config("use_categorical")
    )
    
    if needs_reload:
        update_config("use_full_dataset", use_full)
        update_config("use_categorical", use_categorical)
        with st.spinner("Reloading data..."):
            X, y, feature_names, data_info = load_and_preprocess_data(
                use_full_dataset=use_full,
                use_categorical=use_categorical,
            )
            set_data(X, y, feature_names, data_info)
        st.success(f"✅ Loaded {data_info['feature_mode']} features!")
        st.rerun()

    # Show dataset info
    X, y, feature_names, data_info = get_data()
    st.info(
        f"**{data_info['n_samples']:,}** samples\n"
        f"**{data_info['n_features']}** features ({data_info.get('feature_mode', 'Unknown')})"
    )

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

    # ========== CLASS BALANCING ==========
    st.markdown("### ⚖️ Class Balancing")
    
    st.caption("⚠️ Dataset is imbalanced (88.5% NO / 11.5% YES)")
    
    use_balancing = st.toggle(
        "Enable Class Balancing",
        value=get_config("use_balancing"),
        help="Apply SMOTE or other techniques to balance training data",
        key="balancing_toggle",
    )
    update_config("use_balancing", use_balancing)
    
    if use_balancing:
        balancing_technique = st.selectbox(
            "Technique",
            options=["SMOTE", "RandomOverSampler", "RandomUnderSampler"],
            index=0,
            key="balancing_technique",
            help="SMOTE: Synthetic Minority Over-sampling (Best) | RandomOver: Duplicate minority samples | RandomUnder: Remove majority samples",
        )
        update_config("balancing_technique", balancing_technique)
        
        st.caption(f"✅ Will apply {balancing_technique} to training data only")
    else:
        st.caption("⚠️ Training with imbalanced data (may have poor recall)")
    
    st.divider()
    
    # ========== TEST SET SIZE ==========
    st.markdown("### 🎯 Test Set Size")
    
    test_size = st.slider(
        "Held-out Test Set",
        min_value=10,
        max_value=40,
        value=int((get_config("test_size") or 0.2) * 100),
        step=5,
        key="test_size_slider",
        help="Percentage of data held out for final testing (never balanced, reflects real world)",
        format="%d%%"
    )
    update_config("test_size", test_size / 100)
    
    train_pct = 100 - test_size
    st.caption(f"🔹 Training: {train_pct}% (will be balanced if enabled)")
    st.caption(f"🔹 Testing: {test_size}% (kept imbalanced - real world)")

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

        # Dataset objective (more prominent)
        with st.expander("🎯 Dataset Objective", expanded=True):
            st.markdown("""
            **Bank Marketing - Term Deposit Prediction**
            
            📊 **Goal:** Predict if a client will subscribe to a term deposit  
            📞 **Context:** Direct marketing phone campaigns by a Portuguese bank  
            🎯 **Target:** `y` → "yes" (subscribed) or "no" (declined)
            
            **Why it matters:**  
            - Optimize marketing resources (call the right people)
            - Increase conversion rates (more subscriptions)
            - Reduce costs (avoid calling unlikely prospects)
            
            📁 **Source:** [Bank Marketing Dataset](https://www.kaggle.com/datasets/janiobachmann/bank-marketing-dataset)
            """)
        
        # Feature list with improved descriptions
        with st.expander("📋 Features - What We're Analyzing", expanded=False):
            st.markdown(f"**Using {len(feature_names)} features** ({data_info.get('feature_mode', 'Unknown')})")
            st.divider()
            
            # Enhanced feature descriptions with explanations
            feature_info = {
                "age": ("👤 Age", "Client's age in years", "Older clients might have more savings"),
                "job": ("💼 Job Type", "Occupation category", "admin, technician, blue-collar, etc."),
                "marital": ("💑 Marital Status", "Relationship status", "married, single, divorced"),
                "education": ("🎓 Education", "Highest education level", "primary, secondary, tertiary (university)"),
                "default": ("⚠️ Credit Default", "Has unpaid credit?", "yes/no - affects trust"),
                "balance": ("💰 Bank Balance", "Average yearly balance in euros", "Higher balance = more likely to invest"),
                "housing": ("🏠 Housing Loan", "Has a mortgage?", "yes/no - affects available funds"),
                "loan": ("💳 Personal Loan", "Has personal loan?", "yes/no - affects financial capacity"),
                "contact": ("📞 Contact Type", "How client was reached", "cellular, telephone, unknown"),
                "day": ("📅 Contact Day", "Day of month for last contact", "1-31, timing might matter"),
                "month": ("📆 Contact Month", "Month of last contact", "jan-dec, seasonal patterns"),
                "duration": ("⏱️ Call Duration", "Last call length in seconds", "⚠️ Longer calls = higher interest"),
                "campaign": ("📊 Campaign Contacts", "# of calls this campaign", "Too many calls = annoying"),
                "pdays": ("📉 Days Since Contact", "Days since last campaign contact", "-1 means never contacted before"),
                "previous": ("🔄 Previous Contacts", "# of calls before this campaign", "Prior relationship history"),
                "poutcome": ("📈 Previous Outcome", "Result of last campaign", "success, failure, unknown, other")
            }
            
            # Group by type
            numerical = ["age", "balance", "day", "duration", "campaign", "pdays", "previous"]
            categorical = ["job", "marital", "education", "default", "housing", "loan", "contact", "month", "poutcome"]
            
            # Show numerical features
            if any(f in feature_names for f in numerical):
                st.markdown("**🔢 Numerical Features**")
                for feat in feature_names:
                    if feat in numerical and feat in feature_info:
                        icon_name, desc, note = feature_info[feat]
                        st.markdown(f"**{icon_name}** — {desc}  \n↳ *{note}*")
                st.divider()
            
            # Show categorical features
            if any(f in feature_names for f in categorical):
                st.markdown("**📊 Categorical Features** *(encoded as numbers)*")
                for feat in feature_names:
                    if feat in categorical and feat in feature_info:
                        icon_name, desc, note = feature_info[feat]
                        st.markdown(f"**{icon_name}** — {desc}  \n↳ *{note}*")
