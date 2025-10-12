"""
Best Model Saver Component
Handles saving the best model from experiment history
"""

import streamlit as st
from settings.config import CONF, Keys
from settings.imports import SVC
from ui.pages.svm.experiments import get_best_experiment
from ui.utils.state_manager import get_data


def render_best_model_saver():
    """
    Render best model saver section
    Automatically identifies best experiment and allows saving for PCA comparison
    Shows whenever experiment history exists (even from previous sessions)
    """
    # Show if ANY experiments exist (current or historical)
    if not st.session_state.svm.get("experiment_history"):
        return

    st.divider()
    st.subheader("💾 Save Best Model for PCA Comparison")

    # Get best experiment from history
    best_exp, best_idx = get_best_experiment(st.session_state.svm["experiment_history"])

    if not best_exp:
        st.info("No experiments found. Train a model first.")
        return

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

        st.info(
            f"""
        **Best Experiment: #{best_exp["id"]}**
        - Kernel: **{best_exp["kernel"]}**
        - C: **{best_exp["C"]:.2f}**
        - Gamma: **{best_exp["gamma"]}**
        - {metric_name}: **{acc:.4f}**
        """
        )

    with col_button:
        if st.button(
            f"💾 Save Best Model\n(Exp #{best_exp['id']})",
            width="stretch",
            type="primary",
            key="svm_save_best_model",
        ):
            _save_best_model(best_exp, metric_name, acc)

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


def _save_best_model(best_exp, metric_name, acc):
    """
    Save best model by retraining with best parameters
    
    Args:
        best_exp: Best experiment dictionary
        metric_name: Name of the metric (Accuracy or CV Accuracy)
        acc: Accuracy value
    """
    with st.spinner(f"⏳ Retraining best model (Exp #{best_exp['id']})..."):
        # Retrain model with best parameters
        model = SVC(
            kernel=best_exp["kernel"],
            C=best_exp["C"],
            gamma=best_exp["gamma"] if best_exp["gamma"] not in ["-", ""] else "scale",
            degree=best_exp["degree"] if isinstance(best_exp["degree"], int) else 3,
            random_state=CONF[Keys.RANDOM_STATE],
        )

        # Use same data
        X, y, _, _ = get_data()
        model.fit(X, y)

        # Save as best model
        st.session_state.svm["best_model"] = model
        st.session_state.svm["best_params"] = best_exp.copy()
        st.session_state.svm["best_metrics"] = best_exp["metrics"].copy()

        st.success(
            f"✅ Best model saved: Experiment #{best_exp['id']} ({metric_name}: {acc:.4f})"
        )
        st.balloons()

