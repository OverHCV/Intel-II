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

    Args:
        kernel: Kernel function (linear, rbf, poly, sigmoid)
        C: Regularization parameter
        gamma: Kernel coefficient
        degree: Polynomial degree
    """
    with st.spinner("Training SVM..."):
        # Get data and CV config
        X, y, feature_names, data_info = get_data()
        cv_strategy = get_config("cv_strategy")

        # Create model
        model = SVC(
            kernel=kernel,
            C=C,
            gamma=gamma if kernel != SVMKernel.LINEAR else "scale",
            degree=degree if kernel == SVMKernel.POLY else 3,
            probability=True,  # Enable predict_proba for ROC curves
            random_state=CONF[Keys.RANDOM_STATE],
        )

        start_time = time.time()

        if cv_strategy == "train_test":
            # Simple train/test split
            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=CONF[Keys.TEST_SIZE],
                random_state=CONF[Keys.RANDOM_STATE],
            )

            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            # Get probability predictions for ROC curve
            try:
                y_proba = model.predict_proba(X_test)
            except AttributeError:
                y_proba = None

            # Calculate metrics with weighted averaging to handle class imbalance
            n_classes = len(np.unique(y))
            avg_strategy = "binary" if n_classes == 2 else "weighted"

            metrics = {
                "Accuracy": accuracy_score(y_test, y_pred),
                "Precision": precision_score(
                    y_test, y_pred, average=avg_strategy, zero_division=0
                ),
                "Recall": recall_score(
                    y_test, y_pred, average=avg_strategy, zero_division=0
                ),
                "F1-Score": f1_score(
                    y_test, y_pred, average=avg_strategy, zero_division=0
                ),
            }

            # Store for visualization
            st.session_state.svm["y_true"] = y_test
            st.session_state.svm["y_pred"] = y_pred
            st.session_state.svm["y_proba"] = y_proba

        else:
            # K-Fold CV
            n_folds = get_config("n_folds")

            # Calculate multiple metrics using cross_validate
            from sklearn.model_selection import cross_validate

            n_classes = len(np.unique(y))

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
                model, X, y, cv=n_folds, scoring=scoring, return_train_score=False
            )

            # Get prediction mode from session state (set in UI)
            prediction_mode = st.session_state.svm.get("prediction_mode", "cv_predict")

            if prediction_mode == "cv_predict":
                # Proper held-out predictions from cross-validation
                y_pred = cross_val_predict(model, X, y, cv=n_folds)

                # Get probability predictions for ROC curve
                try:
                    y_proba = cross_val_predict(
                        model, X, y, cv=n_folds, method="predict_proba"
                    )
                except (AttributeError, ValueError):
                    y_proba = None

                # Fit final model on all data (for saving/future use)
                model.fit(X, y)

            else:
                # Fit on all data (explicit user choice)
                model.fit(X, y)
                y_pred = model.predict(X)

                # Get probability predictions
                try:
                    y_proba = model.predict_proba(X)
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

            st.session_state.svm["y_true"] = y
            st.session_state.svm["y_pred"] = y_pred
            st.session_state.svm["y_proba"] = y_proba

        training_time = time.time() - start_time

        # Store results
        st.session_state.svm["model"] = model
        st.session_state.svm["params"] = {
            "kernel": kernel,
            "C": C,
            "gamma": gamma,
            "degree": degree,
        }
        st.session_state.svm["metrics"] = metrics
        st.session_state.svm["training_time"] = training_time
        st.session_state.svm["is_trained"] = True

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
            "metrics": metrics.copy(),
            "training_time": training_time,
        }
        st.session_state.svm["experiment_history"].append(experiment)

        # Persist experiments to disk
        save_experiments_to_file(st.session_state.svm["experiment_history"], "svm")

        st.success(
            f"✅ Training complete! ({training_time:.2f}s) - Experiment #{experiment['id']} saved"
        )
