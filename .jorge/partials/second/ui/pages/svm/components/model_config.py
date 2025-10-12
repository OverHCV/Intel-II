"""
Model Configuration Component
Handles SVM parameter selection and training
"""

import time

import numpy as np
import streamlit as st
from funcs.persistence import save_experiments_to_file
from settings.config import CONF, Keys
from settings.imports import SVC, cross_val_score, train_test_split
from settings.options import SVMKernel
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from ui.components import NumericSlider, Selector
from ui.utils.state_manager import get_config, get_data


def render_model_configuration():
    """
    Render model configuration UI and training logic
    """
    with st.expander(
        "🎛️ Model Configuration", expanded=not st.session_state.svm["is_trained"]
    ):
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
        if kernel == SVMKernel.POLY:
            degree = st.slider(
                "Degree",
                min_value=2,
                max_value=5,
                value=3,
                key="svm_degree",
                help="Polynomial degree. Higher → more complex boundary (overfitting risk). Typical: 2-4.",
            )
        else:
            degree = 3

        st.divider()

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

        else:
            # K-Fold CV
            n_folds = get_config("n_folds")

            # Fit full model
            model.fit(X, y)

            # Get CV scores
            cv_scores = cross_val_score(model, X, y, cv=n_folds, scoring="accuracy")

            # For visualization, use predictions on full dataset
            y_pred = model.predict(X)

            metrics = {
                "CV Accuracy": cv_scores.mean(),
                "CV Std": cv_scores.std(),
                "Min Fold": cv_scores.min(),
                "Max Fold": cv_scores.max(),
            }

            st.session_state.svm["y_true"] = y
            st.session_state.svm["y_pred"] = y_pred

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

        experiment = {
            "id": len(st.session_state.svm["experiment_history"]) + 1,
            "kernel": kernel,
            "C": C,
            "gamma": str(gamma),
            "degree": degree if kernel == SVMKernel.POLY else "-",
            "cv_strategy": cv_strategy,
            "metrics": metrics.copy(),
            "training_time": training_time,
        }
        st.session_state.svm["experiment_history"].append(experiment)

        # Persist experiments to disk
        save_experiments_to_file(st.session_state.svm["experiment_history"], "svm")

        st.success(
            f"✅ Training complete! ({training_time:.2f}s) - Experiment #{experiment['id']} saved"
        )

