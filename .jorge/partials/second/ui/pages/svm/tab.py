"""
SVM Page - Support Vector Machine Interactive Analysis
"""

import time

import streamlit as st
from funcs.visualizers import plot_confusion_matrix, plot_metrics_bars
from settings.config import CONF, Keys
from settings.imports import SVC, cross_val_score, train_test_split
from settings.options import SVMKernel
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from ui.components import MetricsGrid, NumericSlider, Selector
from ui.pages.svm.docs import render_svm_documentation
from ui.pages.svm.experiments import render_experiment_history
from ui.utils.state_manager import get_config, get_data


def svm_page():
    """
    SVM interactive tab content
    Task 1: Test different kernels and parameters
    """
    st.title("🔍 Support Vector Machine (SVM)")
    st.markdown("Explore different kernels and hyperparameters for classification")

    # Check if data is loaded
    X, y, feature_names, data_info = get_data()

    if X is None:
        st.warning("⚠️ Please load data in the **Config** tab first!")
        return

    # Documentation Section (imported from svm_docs.py)
    render_svm_documentation()

    st.divider()

    # Two-column layout
    col_viz, col_controls = st.columns([2, 1])

    with col_controls:
        st.subheader("🎛️ Model Configuration")

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
        if st.button("🚀 Train SVM", type="primary", use_container_width=True):
            with st.spinner("Training SVM..."):
                # Get CV config
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

                    metrics = {
                        "Accuracy": accuracy_score(y_test, y_pred),
                        "Precision": precision_score(y_test, y_pred, average="binary"),
                        "Recall": recall_score(y_test, y_pred, average="binary"),
                        "F1-Score": f1_score(y_test, y_pred, average="binary"),
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
                    cv_scores = cross_val_score(
                        model, X, y, cv=n_folds, scoring="accuracy"
                    )

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

                st.success(
                    f"✅ Training complete! ({training_time:.2f}s) - Experiment #{experiment['id']} saved"
                )

        # Show current metrics
        if st.session_state.svm["is_trained"]:
            st.divider()
            st.subheader("📊 Current Results")

            metrics = st.session_state.svm["metrics"]
            MetricsGrid(metrics, columns=2, format_string="{:.4f}")

            st.caption(f"⏱️ Training time: {st.session_state.svm['training_time']:.2f}s")

    with col_viz:
        st.subheader("📈 Visualizations")

        if st.session_state.svm["is_trained"]:
            # Confusion Matrix
            y_true = st.session_state.svm["y_true"]
            y_pred = st.session_state.svm["y_pred"]

            if data_info:
                labels = data_info["classes"]
            else:
                labels = ["Class 0", "Class 1"]

            fig_cm = plot_confusion_matrix(y_true, y_pred, labels=labels)
            st.pyplot(fig_cm)

            # Metrics bar chart
            metrics = st.session_state.svm["metrics"]
            # Only plot metrics that are between 0 and 1
            plot_metrics = {k: v for k, v in metrics.items() if 0 <= v <= 1}

            if plot_metrics:
                fig_metrics = plot_metrics_bars(plot_metrics)
                st.pyplot(fig_metrics)
        else:
            st.info("🦜 Configure parameters and click **Train SVM** to see results 👉")

    # Experiment History Section (imported from svm_experiments.py)
    render_experiment_history(st.session_state.svm)

    # Save best model button
    if st.session_state.svm["is_trained"]:
        st.divider()
        col_save1, col_save2 = st.columns(2)
        with col_save1:
            if st.button(
                "💾 Save as Best Model (for PCA comparison)",
                use_container_width=True,
                key="svm_save_best_model",
            ):
                st.session_state.svm["best_model"] = st.session_state.svm["model"]
                st.session_state.svm["best_metrics"] = st.session_state.svm["metrics"]
                st.session_state.svm["best_params"] = st.session_state.svm["params"]
                st.success("✅ Model saved for PCA comparison!")
        with col_save2:
            if st.session_state.svm.get("best_model"):
                st.success("✅ Best model saved")
                st.caption(
                    f"Kernel: {st.session_state.svm['best_params']['kernel']}, "
                    f"C: {st.session_state.svm['best_params']['C']:.2f}"
                )
