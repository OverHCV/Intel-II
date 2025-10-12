"""
ANN Page - Artificial Neural Network Interactive Analysis
"""

import time

import streamlit as st
from funcs.visualizers import plot_confusion_matrix, plot_metrics_bars
from settings.config import CONF, Keys
from settings.imports import MLPClassifier, cross_val_score, train_test_split
from settings.options import ANNActivation, ANNSolver
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from ui.components import MetricsGrid, Selector
from ui.utils.state_manager import get_config, get_data


def ann_page():
    """
    ANN interactive tab content
    Task 2: Test different architectures and activations
    """
    st.title("🧠 Artificial Neural Network (ANN)")
    st.markdown("Explore architectures and activation functions")

    # Check if data is loaded
    X, y, feature_names, data_info = get_data()

    if X is None:
        st.warning("⚠️ Please load data in the **Config** tab first!")
        return

    st.divider()

    # Two-column layout
    col_viz, col_controls = st.columns([2, 1])

    with col_controls:
        st.subheader("🎛️ Model Configuration")

        # Architecture selection
        arch_options = CONF[Keys.ANN_ARCHITECTURES]
        arch_display = [str(arch) for arch in arch_options]

        selected_arch_idx = st.selectbox(
            "Architecture",
            options=range(len(arch_options)),
            format_func=lambda i: arch_display[i],
            key="ann_architecture",
            help="Number of neurons in each hidden layer",
        )
        architecture = arch_options[selected_arch_idx]

        # Activation function
        activation = Selector(
            label="Activation Function",
            options=[
                ANNActivation.RELU,
                ANNActivation.TANH,
                ANNActivation.LOGISTIC,
            ],
            key="ann_activation",
            help_text="Activation function for hidden layers",
        )

        # Solver
        solver = Selector(
            label="Solver",
            options=[
                ANNSolver.ADAM,
                ANNSolver.SGD,
                ANNSolver.LBFGS,
            ],
            key="ann_solver",
            help_text="Optimization algorithm",
        )

        # Max iterations
        max_iter = st.slider(
            "Max Iterations",
            min_value=100,
            max_value=2000,
            value=CONF[Keys.ANN_MAX_ITER],
            step=100,
            key="ann_max_iter",
            help="Maximum training iterations",
        )

        st.divider()

        # Train button
        if st.button("🚀 Train ANN", type="primary", use_container_width=True):
            with st.spinner("Training ANN..."):
                # Get CV config
                cv_strategy = get_config("cv_strategy")

                # Create model
                model = MLPClassifier(
                    hidden_layer_sizes=architecture,
                    activation=activation,
                    solver=solver,
                    max_iter=max_iter,
                    random_state=CONF[Keys.RANDOM_STATE],
                    learning_rate=CONF[Keys.ANN_LEARNING_RATE],
                    alpha=CONF[Keys.ANN_ALPHA],
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

                    st.session_state.ann["y_true"] = y_test
                    st.session_state.ann["y_pred"] = y_pred

                else:
                    # K-Fold CV
                    n_folds = get_config("n_folds")

                    model.fit(X, y)
                    cv_scores = cross_val_score(
                        model, X, y, cv=n_folds, scoring="accuracy"
                    )

                    y_pred = model.predict(X)

                    metrics = {
                        "CV Accuracy": cv_scores.mean(),
                        "CV Std": cv_scores.std(),
                        "Min Fold": cv_scores.min(),
                        "Max Fold": cv_scores.max(),
                    }

                    st.session_state.ann["y_true"] = y
                    st.session_state.ann["y_pred"] = y_pred

                training_time = time.time() - start_time

                # Store results
                st.session_state.ann["model"] = model
                st.session_state.ann["params"] = {
                    "architecture": architecture,
                    "activation": activation,
                    "solver": solver,
                    "max_iter": max_iter,
                }
                st.session_state.ann["metrics"] = metrics
                st.session_state.ann["training_time"] = training_time
                st.session_state.ann["is_trained"] = True

                st.success(f"✅ Training complete! ({training_time:.2f}s)")

        # Show current metrics
        if st.session_state.ann["is_trained"]:
            st.divider()
            st.subheader("📊 Current Results")

            metrics = st.session_state.ann["metrics"]
            MetricsGrid(metrics, columns=2, format_string="{:.4f}")

            st.caption(f"⏱️ Training time: {st.session_state.ann['training_time']:.2f}s")

    with col_viz:
        st.subheader("📈 Visualizations")

        if st.session_state.ann["is_trained"]:
            # Confusion Matrix
            y_true = st.session_state.ann["y_true"]
            y_pred = st.session_state.ann["y_pred"]

            if data_info:
                labels = data_info["classes"]
            else:
                labels = ["Class 0", "Class 1"]

            fig_cm = plot_confusion_matrix(y_true, y_pred, labels=labels)
            st.pyplot(fig_cm)

            # Metrics bar chart
            metrics = st.session_state.ann["metrics"]
            plot_metrics = {k: v for k, v in metrics.items() if 0 <= v <= 1}

            if plot_metrics:
                fig_metrics = plot_metrics_bars(plot_metrics)
                st.pyplot(fig_metrics)
        else:
            st.info("🦜 Configure parameters and click **Train ANN** to see results 👉")

    # Save best model button
    if st.session_state.ann["is_trained"]:
        st.divider()
        if st.button(
            "💾 Save as Best Model (for PCA comparison)",
            use_container_width=True,
            key="ann_save_best_model",
        ):
            st.session_state.ann["best_model"] = st.session_state.ann["model"]
            st.session_state.ann["best_metrics"] = st.session_state.ann["metrics"]
            st.session_state.ann["best_params"] = st.session_state.ann["params"]
            st.success("✅ Model saved for PCA comparison!")
