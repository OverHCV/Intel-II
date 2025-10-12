"""
Model Configuration Component
Architecture, activation, solver selection and training logic
"""

import time
from datetime import datetime

import numpy as np
import streamlit as st
from funcs.persistence import save_experiments_to_file
from settings.config import CONF, Keys
from settings.imports import MLPClassifier, cross_val_score, train_test_split
from settings.options import ANNActivation, ANNSolver
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from ui.components import Selector
from ui.utils.state_manager import get_config, get_data


def render_model_configuration(X, y, data_info):
    """
    Render model configuration panel with training logic
    
    Args:
        X: Feature matrix
        y: Target labels
        data_info: Dataset information dictionary
    """
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
    if st.button("🚀 Train ANN", type="primary", width="stretch"):
        _train_ann_model(X, y, architecture, activation, solver, max_iter, data_info)


def _train_ann_model(X, y, architecture, activation, solver, max_iter, data_info):
    """
    Train ANN model with given parameters
    
    Args:
        X: Feature matrix
        y: Target labels
        architecture: Hidden layer sizes tuple
        activation: Activation function
        solver: Solver algorithm
        max_iter: Maximum iterations
        data_info: Dataset information
    """
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

            # Calculate metrics with weighted averaging for imbalanced data
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

            st.session_state.ann["y_true"] = y_test
            st.session_state.ann["y_pred"] = y_pred

        else:
            # K-Fold CV
            n_folds = get_config("n_folds")

            model.fit(X, y)
            cv_scores = cross_val_score(model, X, y, cv=n_folds, scoring="accuracy")

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

        # Save to experiment history
        _save_to_history(architecture, activation, solver, max_iter, metrics, training_time, cv_strategy)

        st.success(f"✅ Training complete! ({training_time:.2f}s)")


def _save_to_history(architecture, activation, solver, max_iter, metrics, training_time, cv_strategy):
    """
    Save experiment to history with persistence
    
    Args:
        architecture: Network architecture tuple
        activation: Activation function
        solver: Solver algorithm
        max_iter: Maximum iterations
        metrics: Performance metrics dictionary
        training_time: Training duration
        cv_strategy: Validation strategy
    """
    history = st.session_state.ann["experiment_history"]

    # Create experiment object
    experiment = {
        "id": len(history) + 1,
        "timestamp": datetime.now().isoformat(),
        "architecture": architecture,  # Keep as tuple
        "activation": activation,
        "solver": solver,
        "max_iter": max_iter,
        "metrics": metrics,
        "training_time": training_time,
        "cv_strategy": cv_strategy,
    }

    # Add to history
    history.append(experiment)
    st.session_state.ann["experiment_history"] = history

    # Save to disk (persistent)
    save_experiments_to_file(history, "ann")

