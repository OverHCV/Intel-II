"""
Model Configuration Component
Handles SVM parameter selection and training
"""

import time

import numpy as np
import streamlit as st
from funcs.persistence import save_experiments_to_file
from settings.config import CONF, Keys
from settings.imports import SVC, cross_val_predict, train_test_split
from settings.options import SVMKernel
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from ui.components import NumericSlider, Selector
from ui.utils.state_manager import get_config, get_data


def render_model_configuration():
    """
    Render model configuration UI and training logic
    """
    st.subheader("🎛️ Model Configuration")
    st.markdown("**Configure SVM parameters and train a new model**")

    # Kernel selection
    kernel = Selector(
        label="Kernel",
        options=[
            SVMKernel.LINEAR,
            SVMKernel.RBF,
            SVMKernel.POLY,
            SVMKernel.SIGMOID,
        ],
        key="svm_kernel",
        help_text="Kernel function for the SVM",
    )

    # C parameter
    C = NumericSlider(
        label="C (Regularization)",
        min_value=0.01,
        max_value=100,
        default_value=1.0,
        log_scale=True,
        key="svm_c",
        help_text="Trade-off between margin and errors. Small C → wide margin (underfitting). Large C → narrow margin (overfitting).",
    )

    # Gamma (only for rbf, poly, sigmoid)
    if kernel != SVMKernel.LINEAR:
        gamma_options = ["scale", "auto"] + CONF[Keys.SVM_GAMMA_VALUES][2:]
        gamma = st.selectbox(
            "Gamma",
            options=gamma_options,
            index=0,
            key="svm_gamma",
            help="Kernel coefficient. Small γ → smooth boundary. Large γ → complex boundary (overfitting risk).",
        )
    else:
        gamma = "scale"

    # Degree (only for poly)
    degree = 3
    if kernel == SVMKernel.POLY:
        degree = st.slider(
            "Degree",
            min_value=2,
            max_value=5,
            value=3,
            key="svm_degree",
            help="Polynomial degree. Higher → more complex boundary (overfitting risk). Typical: 2-4.",
        )

    st.divider()

    # Prediction mode selector (only for K-Fold CV)
    cv_strategy = get_config("cv_strategy")
    if cv_strategy == "kfold":
        prediction_mode = st.radio(
            "Predictions for Visualization",
            options=["cv_predict", "fit_all"],
            format_func=lambda x: "CV Predictions (held-out)"
            if x == "cv_predict"
            else "Fit All Data",
            index=0,
            key="svm_prediction_mode",
            help="CV Predictions: proper cross-validated held-out predictions. Fit All: train on full dataset after CV.",
        )
        st.session_state.svm["prediction_mode"] = prediction_mode

    # Train button
    if st.button("🚀 Train SVM", type="primary", width="stretch"):
        _train_svm_model(kernel, C, gamma, degree)


def _train_svm_model(kernel, C, gamma, degree):
    """
    Train SVM model with given parameters
    
    Pipeline:
    1. Split into train/test (held-out test set)
    2. Apply SMOTE to training set if enabled
    3. Train with CV strategy on balanced training set
    4. Final evaluation on imbalanced test set (real world)
    
    Args:
        kernel: Kernel function (linear, rbf, poly, sigmoid)
        C: Regularization parameter
        gamma: Kernel coefficient
        degree: Polynomial degree
    """
    with st.spinner("Training SVM..."):
        # Get data and configuration
        X, y, feature_names, data_info = get_data()
        cv_strategy = get_config("cv_strategy")
        use_balancing = get_config("use_balancing")
        balancing_technique = get_config("balancing_technique")
        test_size = get_config("test_size")
        
        # Step 1: Create held-out test set (NEVER balanced - represents real world)
        X_train_full, X_test, y_train_full, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=CONF[Keys.RANDOM_STATE],
            stratify=y,  # Maintain class distribution in both sets
        )
        
        st.info(
            f"📊 Split: {len(X_train_full)} training ({(1-test_size)*100:.0f}%), "
            f"{len(X_test)} testing ({test_size*100:.0f}%) - "
            f"Test set kept imbalanced (real world)"
        )
        
        # Step 2: Apply class balancing to training set if enabled
        if use_balancing:
            try:
                if balancing_technique == "SMOTE":
                    from imblearn.over_sampling import SMOTE
                    balancer = SMOTE(random_state=CONF[Keys.RANDOM_STATE])
                elif balancing_technique == "RandomOverSampler":
                    from imblearn.over_sampling import RandomOverSampler
                    balancer = RandomOverSampler(random_state=CONF[Keys.RANDOM_STATE])
                elif balancing_technique == "RandomUnderSampler":
                    from imblearn.under_sampling import RandomUnderSampler
                    balancer = RandomUnderSampler(random_state=CONF[Keys.RANDOM_STATE])
                else:
                    balancer = None
                
                if balancer:
                    X_train, y_train = balancer.fit_resample(X_train_full, y_train_full)
                    
                    # Show balancing stats
                    original_dist = np.bincount(y_train_full)
                    balanced_dist = np.bincount(y_train)
                    st.success(
                        f"✅ {balancing_technique} applied! "
                        f"Training set: {original_dist[0]}/{original_dist[1]} → "
                        f"{balanced_dist[0]}/{balanced_dist[1]} (balanced)"
                    )
                else:
                    X_train, y_train = X_train_full, y_train_full
            except ImportError:
                st.error(
                    "❌ imbalanced-learn not installed! "
                    "Install with: pip install imbalanced-learn"
                )
                return
        else:
            X_train, y_train = X_train_full, y_train_full
            st.caption("⚠️ Training with imbalanced data (balancing disabled)")

        # Create model
        model = SVC(
            kernel=kernel,
            C=C,
            gamma=gamma if kernel != SVMKernel.LINEAR else "scale",
            degree=degree if kernel == SVMKernel.POLY else 3,
            probability=True,  # Enable predict_proba for ROC curves
            random_state=CONF[Keys.RANDOM_STATE],
        )

        # Step 3: Train model on balanced training set
        start_time = time.time()

        if cv_strategy == "train_test":
            # Further split training set into train/val
            X_train_split, X_val_split, y_train_split, y_val_split = train_test_split(
                X_train,
                y_train,
                test_size=0.2,  # 80/20 of the training set
                random_state=CONF[Keys.RANDOM_STATE],
                stratify=y_train,
            )

            model.fit(X_train_split, y_train_split)
            
            # Evaluate on validation set (from balanced training data)
            y_pred_val = model.predict(X_val_split)
            
            # Get probability predictions for ROC curve
            try:
                y_proba_val = model.predict_proba(X_val_split)
            except AttributeError:
                y_proba_val = None

            # Calculate metrics with weighted averaging
            n_classes = len(np.unique(y_train))
            avg_strategy = "binary" if n_classes == 2 else "weighted"

            metrics = {
                "Accuracy": accuracy_score(y_val_split, y_pred_val),
                "Precision": precision_score(
                    y_val_split, y_pred_val, average=avg_strategy, zero_division=0
                ),
                "Recall": recall_score(
                    y_val_split, y_pred_val, average=avg_strategy, zero_division=0
                ),
                "F1-Score": f1_score(
                    y_val_split, y_pred_val, average=avg_strategy, zero_division=0
                ),
            }

            # Store validation results for visualization
            st.session_state.svm["y_true"] = y_val_split
            st.session_state.svm["y_pred"] = y_pred_val
            st.session_state.svm["y_proba"] = y_proba_val

        else:
            # K-Fold CV on balanced training set
            n_folds = get_config("n_folds")

            # Calculate multiple metrics using cross_validate
            from sklearn.model_selection import cross_validate

            n_classes = len(np.unique(y_train))
            
            # Use correct sklearn scorer names
            # For binary: use plain names, for multi-class: use _weighted suffix
            if n_classes == 2:
                scoring = {
                    "accuracy": "accuracy",
                    "precision": "precision",
                    "recall": "recall",
                    "f1": "f1",
                }
            else:
                scoring = {
                    "accuracy": "accuracy",
                    "precision": "precision_weighted",
                    "recall": "recall_weighted",
                    "f1": "f1_weighted",
                }

            cv_results = cross_validate(
                model, X_train, y_train, cv=n_folds, scoring=scoring, return_train_score=False
            )

            # Get prediction mode from session state (set in UI)
            prediction_mode = st.session_state.svm.get("prediction_mode", "cv_predict")

            if prediction_mode == "cv_predict":
                # Proper held-out predictions from cross-validation
                y_pred = cross_val_predict(model, X_train, y_train, cv=n_folds)

                # Get probability predictions for ROC curve
                try:
                    y_proba = cross_val_predict(
                        model, X_train, y_train, cv=n_folds, method="predict_proba"
                    )
                except (AttributeError, ValueError):
                    y_proba = None

                # Fit final model on all balanced training data (for saving/future use)
                model.fit(X_train, y_train)

            else:
                # Fit on all balanced training data (explicit user choice)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_train)

                # Get probability predictions
                try:
                    y_proba = model.predict_proba(X_train)
                except (AttributeError, ValueError):
                    y_proba = None

            # Aggregate metrics from all folds
            metrics = {
                "CV Accuracy": cv_results["test_accuracy"].mean(),
                "CV Precision": cv_results["test_precision"].mean(),
                "CV Recall": cv_results["test_recall"].mean(),
                "CV F1-Score": cv_results["test_f1"].mean(),
                "Accuracy Std": cv_results["test_accuracy"].std(),
                "Min Fold Acc": cv_results["test_accuracy"].min(),
                "Max Fold Acc": cv_results["test_accuracy"].max(),
            }

            st.session_state.svm["y_true"] = y_train
            st.session_state.svm["y_pred"] = y_pred
            st.session_state.svm["y_proba"] = y_proba

        training_time = time.time() - start_time

        # Step 4: Evaluate on held-out test set (IMBALANCED - REAL WORLD)
        y_pred_test = model.predict(X_test)
        try:
            y_proba_test = model.predict_proba(X_test)
        except (AttributeError, ValueError):
            y_proba_test = None
        
        # Calculate real-world metrics on imbalanced test set
        n_classes_test = len(np.unique(y_test))
        avg_strategy_test = "binary" if n_classes_test == 2 else "weighted"
        
        test_accuracy = accuracy_score(y_test, y_pred_test)
        test_precision = precision_score(y_test, y_pred_test, average=avg_strategy_test, zero_division=0)
        test_recall = recall_score(y_test, y_pred_test, average=avg_strategy_test, zero_division=0)
        test_f1 = f1_score(y_test, y_pred_test, average=avg_strategy_test, zero_division=0)
        
        test_metrics = {
            "Test Accuracy": test_accuracy,
            "Test Precision": test_precision,
            "Test Recall": test_recall,
            "Test F1-Score": test_f1,
        }

        # Compare training vs test performance
        if "F1-Score" in metrics:
            train_f1 = metrics["F1-Score"]
        elif "CV F1-Score" in metrics:
            train_f1 = metrics["CV F1-Score"]
        else:
            train_f1 = 0
        
        f1_drop = train_f1 - test_f1
        
        # Store comparison results for display
        st.session_state.svm["performance_comparison"] = {
            "train_f1": train_f1,
            "test_f1": test_f1,
            "f1_drop": f1_drop
        }

        # Store results (use test set for visualization since it's real world)
        st.session_state.svm["model"] = model
        st.session_state.svm["params"] = {
            "kernel": kernel,
            "C": C,
            "gamma": gamma,
            "degree": degree,
        }
        st.session_state.svm["metrics"] = metrics  # Training/CV metrics
        st.session_state.svm["test_metrics"] = test_metrics  # Real-world metrics
        st.session_state.svm["training_time"] = training_time
        st.session_state.svm["is_trained"] = True
        
        # Override visualization data with test set (real world)
        st.session_state.svm["y_true"] = y_test
        st.session_state.svm["y_pred"] = y_pred_test
        st.session_state.svm["y_proba"] = y_proba_test

        # Add to experiment history
        if "experiment_history" not in st.session_state.svm:
            st.session_state.svm["experiment_history"] = []

        prediction_mode = st.session_state.svm.get("prediction_mode", "cv_predict")

        experiment = {
            "id": len(st.session_state.svm["experiment_history"]) + 1,
            "kernel": kernel,
            "C": C,
            "gamma": str(gamma),
            "degree": degree if kernel == SVMKernel.POLY else "-",
            "cv_strategy": cv_strategy,
            "prediction_mode": prediction_mode if cv_strategy == "kfold" else "N/A",
            "balancing_enabled": use_balancing,
            "balancing_technique": balancing_technique if use_balancing else "None",
            "test_size": test_size,
            "metrics": metrics.copy(),  # Training/CV metrics
            "test_metrics": test_metrics.copy(),  # Real-world test metrics
            "training_time": training_time,
        }
        st.session_state.svm["experiment_history"].append(experiment)

        # Persist experiments to disk
        save_experiments_to_file(st.session_state.svm["experiment_history"], "svm")

        st.success(
            f"✅ Training complete! ({training_time:.2f}s) | "
            f"Test F1-Score: {test_metrics['Test F1-Score']:.4f} | "
            f"Experiment #{experiment['id']} saved"
        )


def render_test_evaluation():
    """
    Render the test set evaluation section
    Displays real-world performance metrics on held-out imbalanced data
    """
    if not st.session_state.svm.get("is_trained"):
        return
    
    test_metrics = st.session_state.svm.get("test_metrics")
    if not test_metrics:
        return
    
    st.divider()
    st.markdown("### 🎯 Final Evaluation on Held-Out Test Set (Real World)")
    st.caption("📊 These are REAL WORLD metrics on imbalanced data (never seen during training)")
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Test Accuracy", f"{test_metrics['Test Accuracy']:.4f}")
    with col2:
        st.metric("Test Precision", f"{test_metrics['Test Precision']:.4f}")
    with col3:
        st.metric("Test Recall", f"{test_metrics['Test Recall']:.4f}")
    with col4:
        st.metric("Test F1-Score", f"{test_metrics['Test F1-Score']:.4f}")
    
    # Show performance comparison warning/success
    comparison = st.session_state.svm.get("performance_comparison")
    if comparison:
        train_f1 = comparison["train_f1"]
        test_f1 = comparison["test_f1"]
        f1_drop = comparison["f1_drop"]
        
        if f1_drop > 0.1:
            st.warning(
                f"⚠️ Significant performance drop on test set! "
                f"Training F1: {train_f1:.3f} → Test F1: {test_f1:.3f} "
                f"(drop: {f1_drop:.3f}). Model may be overfitting."
            )
        elif test_f1 > train_f1:
            st.success(
                f"✅ Model generalizes well! "
                f"Test F1 ({test_f1:.3f}) ≥ Training F1 ({train_f1:.3f})"
            )
