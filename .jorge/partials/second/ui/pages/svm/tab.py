"""
SVM Page - Support Vector Machine Interactive Analysis
"""

import time

import numpy as np
import streamlit as st
from funcs.persistence import clear_experiments_file, save_experiments_to_file
from funcs.visualizers import (
    plot_confusion_matrix,
    plot_correlation_heatmap,
    plot_interactive_scatter_2d,
    plot_interactive_scatter_3d,
    plot_metrics_bars,
)
from settings.config import CONF, Keys
from settings.imports import SVC, cross_val_score, train_test_split
from settings.options import SVMKernel
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from ui.components import MetricsGrid, NumericSlider, Selector
from ui.pages.svm.docs import render_svm_documentation
from ui.pages.svm.experiments import get_best_experiment, render_experiment_history
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

                    # Calculate metrics with weighted averaging to handle class imbalance
                    # Weighted average accounts for class imbalance by weighting metrics by support
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

                # Persist experiments to disk
                save_experiments_to_file(
                    st.session_state.svm["experiment_history"], "svm"
                )

                st.success(
                    f"✅ Training complete! ({training_time:.2f}s) - Experiment #{experiment['id']} saved"
                )

    with col_viz:
        st.subheader("📈 Visualizations")

        if st.session_state.svm["is_trained"]:
            # Create tabs for organized visualizations
            viz_tabs = st.tabs(
                ["📊 Model Performance", "🔬 Feature Analysis", "🗺️ Data Exploration"]
            )

            # Tab 1: Model Performance
            with viz_tabs[0]:
                st.markdown("### Confusion Matrix & Metrics")

                y_true = st.session_state.svm["y_true"]
                y_pred = st.session_state.svm["y_pred"]

                if data_info:
                    labels = data_info["classes"]
                else:
                    labels = ["Class 0", "Class 1"]

                # Confusion Matrix
                fig_cm = plot_confusion_matrix(y_true, y_pred, labels=labels)
                st.pyplot(fig_cm)

                # Metrics bar chart
                metrics = st.session_state.svm["metrics"]
                # Only plot metrics that are between 0 and 1
                plot_metrics = {k: v for k, v in metrics.items() if 0 <= v <= 1}

                if plot_metrics:
                    fig_metrics = plot_metrics_bars(plot_metrics)
                    st.pyplot(fig_metrics)

                st.caption(
                    f"⏱️ Training time: {st.session_state.svm['training_time']:.2f}s"
                )

            # Tab 2: Feature Analysis
            with viz_tabs[1]:
                st.markdown("### Feature Correlation Analysis")
                st.markdown(
                    "Understand relationships and dependencies between features"
                )

                # Plot correlation heatmap
                fig_corr = plot_correlation_heatmap(
                    X, feature_names, "Feature Correlation Matrix"
                )
                st.pyplot(fig_corr)

                st.caption(
                    "💡 **Interpretation:** Strong correlations (±0.7+) may indicate redundant features. "
                    "Red = negative correlation, Blue = positive correlation."
                )

            # Tab 3: Data Exploration
            with viz_tabs[2]:
                st.markdown("### Interactive Data Exploration")
                st.markdown("Explore relationships between features visually")

                # Axis selectors
                col_x, col_y, col_z = st.columns(3)

                with col_x:
                    x_feature = st.selectbox(
                        "X Axis", options=feature_names, index=0, key="svm_scatter_x"
                    )

                with col_y:
                    y_feature = st.selectbox(
                        "Y Axis",
                        options=feature_names,
                        index=min(1, len(feature_names) - 1),
                        key="svm_scatter_y",
                    )

                with col_z:
                    enable_3d = st.checkbox(
                        "Enable 3D", value=False, key="svm_scatter_3d"
                    )

                # Get indices
                x_idx = feature_names.index(x_feature)
                y_idx = feature_names.index(y_feature)

                # Get class names from data_info
                if data_info and "classes" in data_info:
                    class_names = data_info["classes"]
                else:
                    class_names = None

                if enable_3d:
                    # 3D scatter plot
                    z_feature = st.selectbox(
                        "Z Axis",
                        options=feature_names,
                        index=min(2, len(feature_names) - 1),
                        key="svm_scatter_z",
                    )
                    z_idx = feature_names.index(z_feature)

                    # Try plotly 3D first, fallback to matplotlib 2D
                    fig_3d = plot_interactive_scatter_3d(
                        X, y, feature_names, x_idx, y_idx, z_idx, class_names
                    )

                    if fig_3d is not None:
                        st.plotly_chart(fig_3d, use_container_width=True)
                        st.caption(
                            "💡 **Tip:** Drag to rotate, scroll to zoom, double-click to reset"
                        )
                    else:
                        st.warning("⚠️ Plotly not available. Showing 2D plot instead.")
                        fig_2d = plot_interactive_scatter_2d(
                            X, y, feature_names, x_idx, y_idx, class_names
                        )
                        st.pyplot(fig_2d)
                else:
                    # 2D scatter plot
                    fig_2d = plot_interactive_scatter_2d(
                        X, y, feature_names, x_idx, y_idx, class_names
                    )
                    st.pyplot(fig_2d)
                    st.caption(
                        "💡 **Tip:** Enable 3D to explore three features simultaneously"
                    )
        else:
            st.info("🦜 Configure parameters and click **Train SVM** to see results 👉")

    # Experiment History Section (imported from svm_experiments.py)
    render_experiment_history(st.session_state.svm)

    # Save best model button
    if st.session_state.svm["is_trained"] and st.session_state.svm.get(
        "experiment_history"
    ):
        st.divider()
        st.subheader("💾 Save Best Model for PCA Comparison")

        # Get best experiment from history
        best_exp, best_idx = get_best_experiment(
            st.session_state.svm["experiment_history"]
        )

        if best_exp:
            # Show best experiment info
            col_info, col_button = st.columns([2, 1])

            with col_info:
                # Determine which metric to display
                if "CV Accuracy" in best_exp["metrics"]:
                    acc = best_exp["metrics"]["CV Accuracy"]
                    metric_name = "CV Accuracy"
                else:
                    acc = best_exp["metrics"]["Accuracy"]
                    metric_name = "Accuracy"

                st.info(f"""
                **Best Experiment: #{best_exp["id"]}**
                - Kernel: **{best_exp["kernel"]}**
                - C: **{best_exp["C"]:.2f}**
                - Gamma: **{best_exp["gamma"]}**
                - {metric_name}: **{acc:.4f}**
                """)

            with col_button:
                if st.button(
                    f"💾 Save Best Model\n(Exp #{best_exp['id']})",
                    use_container_width=True,
                    type="primary",
                    key="svm_save_best_model",
                ):
                    with st.spinner(
                        f"⏳ Retraining best model (Exp #{best_exp['id']})..."
                    ):
                        # Retrain model with best parameters
                        model = SVC(
                            kernel=best_exp["kernel"],
                            C=best_exp["C"],
                            gamma=best_exp["gamma"]
                            if best_exp["gamma"] not in ["-", ""]
                            else "scale",
                            degree=best_exp["degree"]
                            if isinstance(best_exp["degree"], int)
                            else 3,
                            random_state=CONF[Keys.RANDOM_STATE],
                        )

                        # Use same data
                        X, y, _, _ = get_data()
                        model.fit(X, y)

                        # Save as best model
                        st.session_state.svm["best_model"] = model
                        st.session_state.svm["best_params"] = best_exp.copy()
                        st.session_state.svm["best_metrics"] = best_exp[
                            "metrics"
                        ].copy()

                        st.success(
                            f"✅ Best model saved: Experiment #{best_exp['id']} ({metric_name}: {acc:.4f})"
                        )
                        st.balloons()

            # Show current saved model info
            if st.session_state.svm.get("best_model"):
                st.divider()
                saved_params = st.session_state.svm.get("best_params", {})
                if saved_params:
                    st.caption(
                        f"✅ **Currently saved model:** Experiment #{saved_params.get('id', 'N/A')} - "
                        f"Kernel: {saved_params.get('kernel', 'N/A')}, "
                        f"C: {saved_params.get('C', 'N/A')}"
                    )
