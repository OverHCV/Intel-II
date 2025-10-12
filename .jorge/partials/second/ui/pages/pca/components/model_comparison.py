"""
Model Comparison Component
Retrain SVM and ANN on PCA-transformed data and compare with original performance
"""

import time

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from settings.config import CONF, Keys
from settings.imports import MLPClassifier, SVC
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

from funcs.visual.basic_visuals import plot_confusion_matrix


def render_model_comparison():
    """
    Render model comparison section with two tabs: SVM and ANN
    Each tab shows BEFORE (original) vs AFTER (PCA) comparison
    """
    st.markdown("### 🔍 Model Comparison: Original vs PCA")
    st.markdown("Retrain best models on PCA data and compare performance")

    # Check if PCA has been applied
    if not st.session_state.pca.get("pca_applied"):
        st.warning("⚠️ Please apply PCA transformation first (see **PCA Transformation** tab)")
        return

    # Check if at least one best model exists
    has_svm = st.session_state.svm.get("best_model") is not None
    has_ann = st.session_state.ann.get("best_model") is not None

    if not has_svm and not has_ann:
        st.info(
            "📝 **No best models saved yet!**\n\n"
            "Please save best models from SVM and/or ANN tabs first.\n"
            "The system will auto-select the best experiment from history."
        )
        return

    # Create tabs for each model
    tabs = []
    tab_names = []

    if has_svm:
        tab_names.append("🔍 SVM Comparison")
        tabs.append("svm")
    
    if has_ann:
        tab_names.append("🧠 ANN Comparison")
        tabs.append("ann")

    tab_objects = st.tabs(tab_names)

    # Render each tab
    for tab_obj, model_type in zip(tab_objects, tabs):
        with tab_obj:
            if model_type == "svm":
                _render_svm_comparison()
            else:
                _render_ann_comparison()


def _render_svm_comparison():
    """Render SVM BEFORE vs AFTER PCA comparison"""
    st.markdown("#### 🔍 SVM Performance: Original vs PCA")

    # Get original model and metrics
    original_model = st.session_state.svm.get("best_model")
    original_params = st.session_state.svm.get("best_params", {})
    original_metrics = st.session_state.svm.get("best_metrics", {})

    if not original_model:
        st.warning("No SVM best model found!")
        return

    # Display original model info
    st.info(
        f"""
**Original Model Configuration**
- **Kernel**: {original_params.get('kernel', 'N/A')}
- **C**: {original_params.get('C', 'N/A')}
- **Gamma**: {original_params.get('gamma', 'N/A')}
"""
    )

    # Check if already retrained on PCA data
    if not st.session_state.pca.get("svm_pca_trained"):
        if st.button("🔄 Retrain SVM on PCA Data", type="primary", key="retrain_svm_pca"):
            _retrain_svm_on_pca(original_params)
            st.rerun()
        return

    # Show comparison
    st.divider()
    _render_comparison_metrics(
        original_metrics,
        st.session_state.pca["svm_pca_metrics"],
        st.session_state.pca["svm_pca_training_time"],
        original_params.get("training_time", 0),
    )

    st.divider()
    
    # Show confusion matrices side by side
    st.markdown("#### 📊 Confusion Matrices Comparison")
    _render_confusion_matrices_comparison("svm")


def _render_ann_comparison():
    """Render ANN BEFORE vs AFTER PCA comparison"""
    st.markdown("#### 🧠 ANN Performance: Original vs PCA")

    # Get original model and metrics
    original_model = st.session_state.ann.get("best_model")
    original_params = st.session_state.ann.get("best_params", {})
    original_metrics = st.session_state.ann.get("best_metrics", {})

    if not original_model:
        st.warning("No ANN best model found!")
        return

    # Display original model info
    st.info(
        f"""
**Original Model Configuration**
- **Architecture**: {original_params.get('architecture', 'N/A')}
- **Activation**: {original_params.get('activation', 'N/A')}
- **Solver**: {original_params.get('solver', 'N/A')}
- **Max Iterations**: {original_params.get('max_iter', 'N/A')}
"""
    )

    # Check if already retrained on PCA data
    if not st.session_state.pca.get("ann_pca_trained"):
        if st.button("🔄 Retrain ANN on PCA Data", type="primary", key="retrain_ann_pca"):
            _retrain_ann_on_pca(original_params)
            st.rerun()
        return

    # Show comparison
    st.divider()
    _render_comparison_metrics(
        original_metrics,
        st.session_state.pca["ann_pca_metrics"],
        st.session_state.pca["ann_pca_training_time"],
        original_params.get("training_time", 0),
    )

    st.divider()
    
    # Show confusion matrices side by side
    st.markdown("#### 📊 Confusion Matrices Comparison")
    _render_confusion_matrices_comparison("ann")


def _retrain_svm_on_pca(original_params):
    """
    Retrain SVM on PCA-transformed data with same hyperparameters
    
    Args:
        original_params: Dictionary with original model parameters
    """
    with st.spinner("⏳ Retraining SVM on PCA-transformed data..."):
        # Get PCA-transformed data
        X_pca = st.session_state.pca["X_pca"]
        
        # Get original labels
        from ui.utils.state_manager import get_data
        _, y, _, _ = get_data()

        # Create model with same hyperparameters
        model = SVC(
            kernel=original_params.get("kernel", "rbf"),
            C=original_params.get("C", 1.0),
            gamma=original_params.get("gamma", "scale") 
                if original_params.get("gamma") not in ["-", ""] 
                else "scale",
            degree=original_params.get("degree", 3) 
                if isinstance(original_params.get("degree"), int) 
                else 3,
            random_state=CONF[Keys.RANDOM_STATE],
        )

        # Train and measure time
        start_time = time.time()
        model.fit(X_pca, y)
        training_time = time.time() - start_time

        # Evaluate on same data (consistent with original)
        y_pred = model.predict(X_pca)
        
        # Calculate metrics
        metrics = {
            "Accuracy": accuracy_score(y, y_pred),
            "Precision": precision_score(y, y_pred, average="weighted", zero_division=0),
            "Recall": recall_score(y, y_pred, average="weighted", zero_division=0),
            "F1-Score": f1_score(y, y_pred, average="weighted", zero_division=0),
        }

        # Calculate confusion matrix
        cm = confusion_matrix(y, y_pred)

        # Save results
        st.session_state.pca["svm_pca_model"] = model
        st.session_state.pca["svm_pca_metrics"] = metrics
        st.session_state.pca["svm_pca_training_time"] = training_time
        st.session_state.pca["svm_pca_confusion_matrix"] = cm
        st.session_state.pca["svm_pca_trained"] = True

        st.success(
            f"✅ SVM retrained on PCA data! "
            f"Accuracy: {metrics['Accuracy']:.4f} "
            f"(Training time: {training_time:.2f}s)"
        )


def _retrain_ann_on_pca(original_params):
    """
    Retrain ANN on PCA-transformed data with same architecture
    
    Args:
        original_params: Dictionary with original model parameters
    """
    with st.spinner("⏳ Retraining ANN on PCA-transformed data..."):
        # Get PCA-transformed data
        X_pca = st.session_state.pca["X_pca"]
        
        # Get original labels
        from ui.utils.state_manager import get_data
        _, y, _, _ = get_data()

        # Create model with same architecture
        model = MLPClassifier(
            hidden_layer_sizes=original_params.get("architecture", (100,)),
            activation=original_params.get("activation", "relu"),
            solver=original_params.get("solver", "adam"),
            max_iter=original_params.get("max_iter", 200),
            random_state=CONF[Keys.RANDOM_STATE],
            learning_rate=CONF.get(Keys.ANN_LEARNING_RATE, "constant"),
            alpha=CONF.get(Keys.ANN_ALPHA, 0.0001),
        )

        # Train and measure time
        start_time = time.time()
        model.fit(X_pca, y)
        training_time = time.time() - start_time

        # Evaluate on same data
        y_pred = model.predict(X_pca)
        
        # Calculate metrics
        metrics = {
            "Accuracy": accuracy_score(y, y_pred),
            "Precision": precision_score(y, y_pred, average="weighted", zero_division=0),
            "Recall": recall_score(y, y_pred, average="weighted", zero_division=0),
            "F1-Score": f1_score(y, y_pred, average="weighted", zero_division=0),
        }

        # Calculate confusion matrix
        cm = confusion_matrix(y, y_pred)

        # Save results
        st.session_state.pca["ann_pca_model"] = model
        st.session_state.pca["ann_pca_metrics"] = metrics
        st.session_state.pca["ann_pca_training_time"] = training_time
        st.session_state.pca["ann_pca_confusion_matrix"] = cm
        st.session_state.pca["ann_pca_trained"] = True

        st.success(
            f"✅ ANN retrained on PCA data! "
            f"Accuracy: {metrics['Accuracy']:.4f} "
            f"(Training time: {training_time:.2f}s)"
        )


def _render_comparison_metrics(original_metrics, pca_metrics, pca_time, original_time):
    """
    Render side-by-side comparison of metrics
    
    Args:
        original_metrics: Original model metrics dictionary
        pca_metrics: PCA model metrics dictionary
        pca_time: PCA training time
        original_time: Original training time
    """
    st.markdown("#### 📈 Performance Metrics Comparison")

    # Extract metrics (handle both Accuracy and CV Accuracy)
    orig_acc = original_metrics.get("Accuracy", original_metrics.get("CV Accuracy", 0))
    pca_acc = pca_metrics.get("Accuracy", pca_metrics.get("CV Accuracy", 0))

    orig_prec = original_metrics.get("Precision", original_metrics.get("CV Precision", 0))
    pca_prec = pca_metrics.get("Precision", pca_metrics.get("CV Precision", 0))

    orig_rec = original_metrics.get("Recall", original_metrics.get("CV Recall", 0))
    pca_rec = pca_metrics.get("Recall", pca_metrics.get("CV Recall", 0))

    orig_f1 = original_metrics.get("F1-Score", original_metrics.get("CV F1-Score", 0))
    pca_f1 = pca_metrics.get("F1-Score", pca_metrics.get("CV F1-Score", 0))

    # Create metrics columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        delta_acc = pca_acc - orig_acc
        st.metric(
            "Accuracy",
            f"{pca_acc:.4f}",
            f"{delta_acc:+.4f}" if delta_acc != 0 else "0.0000",
            delta_color="normal",
        )
        st.caption(f"Original: {orig_acc:.4f}")

    with col2:
        delta_prec = pca_prec - orig_prec
        st.metric(
            "Precision",
            f"{pca_prec:.4f}",
            f"{delta_prec:+.4f}" if delta_prec != 0 else "0.0000",
            delta_color="normal",
        )
        st.caption(f"Original: {orig_prec:.4f}")

    with col3:
        delta_rec = pca_rec - orig_rec
        st.metric(
            "Recall",
            f"{pca_rec:.4f}",
            f"{delta_rec:+.4f}" if delta_rec != 0 else "0.0000",
            delta_color="normal",
        )
        st.caption(f"Original: {orig_rec:.4f}")

    with col4:
        delta_f1 = pca_f1 - orig_f1
        st.metric(
            "F1-Score",
            f"{pca_f1:.4f}",
            f"{delta_f1:+.4f}" if delta_f1 != 0 else "0.0000",
            delta_color="normal",
        )
        st.caption(f"Original: {orig_f1:.4f}")

    # Training time comparison
    st.divider()
    col_time1, col_time2 = st.columns(2)

    with col_time1:
        st.metric("Original Training Time", f"{original_time:.2f}s")

    with col_time2:
        time_delta = pca_time - original_time
        st.metric(
            "PCA Training Time",
            f"{pca_time:.2f}s",
            f"{time_delta:+.2f}s",
            delta_color="inverse",
        )

    # Bar chart comparison
    _render_metrics_bar_chart(orig_acc, pca_acc, orig_prec, pca_prec, orig_rec, pca_rec, orig_f1, pca_f1)


def _render_metrics_bar_chart(orig_acc, pca_acc, orig_prec, pca_prec, orig_rec, pca_rec, orig_f1, pca_f1):
    """Render bar chart comparing metrics"""
    st.markdown("#### 📊 Visual Comparison")

    metrics_names = ["Accuracy", "Precision", "Recall", "F1-Score"]
    original_values = [orig_acc, orig_prec, orig_rec, orig_f1]
    pca_values = [pca_acc, pca_prec, pca_rec, pca_f1]

    x = np.arange(len(metrics_names))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))

    bars1 = ax.bar(x - width/2, original_values, width, label="Original", alpha=0.8, color="#1f77b4")
    bars2 = ax.bar(x + width/2, pca_values, width, label="PCA", alpha=0.8, color="#ff7f0e")

    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{height:.3f}",
                ha="center",
                va="bottom",
                fontsize=9,
            )

    ax.set_xlabel("Metrics", fontsize=11, fontweight="bold")
    ax.set_ylabel("Score", fontsize=11, fontweight="bold")
    ax.set_title("Original vs PCA Performance", fontsize=13, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_names)
    ax.set_ylim([0, 1.1])
    ax.legend(loc="upper right")
    ax.grid(axis="y", alpha=0.3, linestyle="--")

    plt.tight_layout()
    st.pyplot(fig)


def _render_confusion_matrices_comparison(model_type):
    """
    Render side-by-side confusion matrices
    
    Args:
        model_type: 'svm' or 'ann'
    """
    from ui.utils.state_manager import get_data

    X, y, _, data_info = get_data()
    
    # Get class names
    class_names = data_info.get("classes") if data_info else None

    # Get original and PCA models/predictions
    if model_type == "svm":
        original_model = st.session_state.svm.get("best_model")
        pca_model = st.session_state.pca.get("svm_pca_model")
    else:
        original_model = st.session_state.ann.get("best_model")
        pca_model = st.session_state.pca.get("ann_pca_model")

    # Get predictions for original model
    y_pred_original = original_model.predict(X)
    
    # Get predictions for PCA model
    X_pca = st.session_state.pca["X_pca"]
    y_pred_pca = pca_model.predict(X_pca)

    # Side-by-side confusion matrices
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Original Model**")
        fig_original = plot_confusion_matrix(
            y,
            y_pred_original,
            class_names,
            "Confusion Matrix (Original)",
        )
        st.pyplot(fig_original)

    with col2:
        st.markdown("**PCA Model**")
        fig_pca = plot_confusion_matrix(
            y,
            y_pred_pca,
            class_names,
            "Confusion Matrix (PCA)",
        )
        st.pyplot(fig_pca)

    st.caption(
        "💡 **Confusion Matrix:** Diagonal = correct predictions, off-diagonal = errors. "
        "Darker colors = higher values."
    )

