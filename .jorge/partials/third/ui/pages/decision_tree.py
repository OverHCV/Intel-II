"""Decision Tree Page - CART classification with rule extraction."""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import logging

logger = logging.getLogger(__name__)


def render():
    """Render Decision Tree page with WORKING implementation."""
    
    # THEORY FIRST
    with st.expander("📚 THEORY: Decision Trees & Rule Extraction", expanded=False):
        st.markdown("""
        ### What are Decision Trees?
        
        **CART (Classification and Regression Trees)**: Creates a tree structure
        where each internal node tests a feature, each branch represents the test
        outcome, and each leaf assigns a class label.
        
        ### Why Decision Trees for Education?
        
        - **Interpretable**: Can be converted to IF-THEN rules
        - **No assumptions**: Works with any data distribution
        - **Non-linear**: Captures complex student patterns
        - **Feature importance**: Shows which factors matter most
        
        ### Rule Extraction
        
        Each path from root to leaf = one decision rule:
        ```
        IF failures > 0 AND studytime <= 2 THEN Fail
        ```
        
        **Why useful?** Teachers can understand and act on these rules.
        
        ### Hyperparameters
        
        - **max_depth**: Limits tree height (prevents overfitting)
        - **min_samples_split**: Min samples to split a node (controls granularity)
        - **criterion**: gini (default) or entropy (information gain)
        
        **Overfitting risk**: Deep trees memorize training data → poor generalization.
        **Solution**: Cross-validation to find optimal depth.
        """)
    
    st.markdown("## 🌳 Decision Tree (CART)")
    
    # Check if data is ready
    from ui.state_manager import get_state, set_state, StateKeys
    
    X_ready = get_state(StateKeys.X_PREPARED, None)
    y_ready = get_state(StateKeys.Y_PREPARED, None)
    
    if X_ready is None or y_ready is None:
        st.warning("⚠️ No prepared data found!")
        st.info("👈 Go to **Dataset Review** first to prepare your data.")
        return
    
    st.success(f"✅ Data loaded: {X_ready.shape[0]} samples, {X_ready.shape[1]} features")
    
    # Hyperparameter controls
    st.markdown("### ⚙️ Hyperparameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        max_depth = st.slider(
            "Max Depth",
            min_value=1,
            max_value=20,
            value=5,
            help="WHY: Controls tree complexity. Lower = simpler rules, higher = more specific but risk overfitting."
        )
    
    with col2:
        min_samples_split = st.slider(
            "Min Samples Split",
            min_value=2,
            max_value=20,
            value=10,
            help="WHY: Minimum samples needed to split a node. Higher = more conservative, prevents tiny splits."
        )
    
    with col3:
        criterion = st.selectbox(
            "Split Criterion",
            ["gini", "entropy"],
            help="WHY: Gini = faster, Entropy (info gain) = slightly more accurate. Usually similar results."
        )
    
    st.markdown("---")
    
    # Train button
    if st.button("🚀 Train Decision Tree", type="primary"):
        with st.spinner("🌀 Training CART model..."):
            try:
                # Import and use our implemented functions!
                from core.decision_tree import train_cart, extract_rules, rank_rules, cross_validate, get_feature_importance
                from core.evaluation import evaluate_classification
                from sklearn.model_selection import train_test_split
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(
                    X_ready, y_ready, test_size=0.2, random_state=42
                )
                
                # Train model
                model = train_cart(
                    X_train, y_train,
                    max_depth=max_depth,
                    min_samples_split=min_samples_split,
                    criterion=criterion,
                    random_state=42
                )
                
                # Make predictions
                y_pred = model.predict(X_test)
                
                # Evaluate
                metrics = evaluate_classification(y_test, y_pred)
                
                # Extract rules
                feature_names = [f"feature_{i}" for i in range(X_ready.shape[1])]  # TODO: Get real names
                rules = extract_rules(model, feature_names, class_names=["Fail", "Pass"])
                ranked_rules = rank_rules(rules, criterion="combined")
                
                # Cross-validation
                cv_results = cross_validate(
                    X_ready, y_ready,
                    model_params={
                        "max_depth": max_depth,
                        "min_samples_split": min_samples_split,
                        "criterion": criterion,
                        "random_state": 42
                    },
                    cv=5
                )
                
                # Feature importance
                feature_importance = get_feature_importance(model, feature_names, top_n=10)
                
                # Store in state
                set_state(StateKeys.DT_MODEL, model)
                set_state(StateKeys.DT_RULES, ranked_rules)
                
                st.success("✅ Model trained successfully!")
                
                # Display results
                st.markdown("### 📊 Results")
                
                # Metrics
                metric_cols = st.columns(4)
                with metric_cols[0]:
                    st.metric("Accuracy", f"{metrics['accuracy']:.3f}")
                with metric_cols[1]:
                    st.metric("Precision", f"{metrics['precision']:.3f}")
                with metric_cols[2]:
                    st.metric("Recall", f"{metrics['recall']:.3f}")
                with metric_cols[3]:
                    st.metric("F1-Score", f"{metrics['f1_score']:.3f}")
                
                # Cross-validation
                st.markdown("#### ✅ Cross-Validation (5-fold)")
                st.info(f"Mean Accuracy: **{cv_results['mean']:.3f}** ± {cv_results['std']:.3f}")
                st.caption("WHY: Single train/test split can be lucky/unlucky. CV gives robust estimate.")
                
                # Confusion Matrix
                st.markdown("#### 🎯 Confusion Matrix")
                cm = np.array(metrics['confusion_matrix'])
                fig_cm, ax_cm = plt.subplots(figsize=(6, 5))
                im = ax_cm.imshow(cm, cmap='Blues')
                ax_cm.set_xticks([0, 1])
                ax_cm.set_yticks([0, 1])
                ax_cm.set_xticklabels(["Fail", "Pass"])
                ax_cm.set_yticklabels(["Fail", "Pass"])
                ax_cm.set_xlabel("Predicted")
                ax_cm.set_ylabel("True")
                ax_cm.set_title("Confusion Matrix")
                
                # Add text annotations
                for i in range(2):
                    for j in range(2):
                        ax_cm.text(j, i, str(cm[i, j]), ha="center", va="center", color="black", fontsize=20)
                
                plt.colorbar(im, ax=ax_cm)
                st.pyplot(fig_cm)
                plt.close()
                
                # Tree visualization
                st.markdown("#### 🌳 Tree Structure")
                fig_tree, ax_tree = plt.subplots(figsize=(20, 10))
                plot_tree(
                    model,
                    feature_names=feature_names,
                    class_names=["Fail", "Pass"],
                    filled=True,
                    ax=ax_tree,
                    fontsize=8
                )
                st.pyplot(fig_tree)
                plt.close()
                st.caption(f"Tree depth: {model.get_depth()}, Leaves: {model.get_n_leaves()}")
                
                # Feature Importance
                st.markdown("#### ⭐ Top 10 Feature Importance")
                fig_imp, ax_imp = plt.subplots(figsize=(10, 6))
                features = list(feature_importance.keys())
                importances = list(feature_importance.values())
                ax_imp.barh(features, importances, color='steelblue')
                ax_imp.set_xlabel("Importance Score")
                ax_imp.set_title("Feature Importance (Gini Impurity Reduction)")
                ax_imp.invert_yaxis()
                st.pyplot(fig_imp)
                plt.close()
                st.caption("WHY: Shows which features are most useful for splitting. Higher = more important.")
                
                # RULES DISPLAY
                st.markdown("#### 📜 Extracted Rules (Top 10)")
                st.info("These are IF-THEN rules extracted from the tree. Ranked by combined score (support × confidence × simplicity).")
                
                for idx, rule in enumerate(ranked_rules[:10], 1):
                    with st.expander(f"Rule #{idx}: {rule['prediction']} (Support: {rule['support']}, Confidence: {rule['confidence']:.2f})"):
                        st.markdown(f"**IF** {rule['conditions']}")
                        st.markdown(f"**THEN** predict: **{rule['prediction']}**")
                        st.markdown(f"- Support: {rule['support']} students ({rule['support_pct']:.1f}%)")
                        st.markdown(f"- Confidence: {rule['confidence']:.3f}")
                        st.markdown(f"- Depth: {rule['depth']} conditions")
                        st.json(rule['class_distribution'])
                
            except Exception as e:
                st.error(f"❌ Error training model: {str(e)}")
                logger.error(f"Decision tree training error: {e}", exc_info=True)
    
    # Show cached model if exists
    cached_model = get_state(StateKeys.DT_MODEL, None)
    if cached_model and not st.session_state.get("_training_now"):
        st.info("✅ A trained model is cached. Click 'Train' to retrain with new parameters.")

