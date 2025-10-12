"""
Best Model Saver Component
Auto-identifies and saves best model for PCA comparison
"""

import streamlit as st
from settings.config import CONF, Keys
from settings.imports import MLPClassifier
from ui.pages.ann.experiments import get_best_experiment


def render_best_model_saver(X, y, data_info):
    """
    Render best model saver with auto-identification
    Shows whenever experiment history exists (even from previous sessions)
    
    Args:
        X: Feature matrix
        y: Target labels
        data_info: Dataset information dictionary
    """
    # Show if ANY experiments exist (current or historical)
    history = st.session_state.ann.get("experiment_history", [])

    if not history:
        return  # No experiments yet

    st.divider()
    st.subheader("💾 Save Best Model for PCA Comparison")

    # Auto-identify best experiment
    best_exp = get_best_experiment(history)

    if not best_exp:
        st.warning("⚠️ No experiments found. Train a model first!")
        return

    # Display best experiment details
    col_info, col_button = st.columns([2, 1])

    with col_info:
        # Get accuracy metric
        acc = best_exp["metrics"].get(
            "Accuracy", best_exp["metrics"].get("CV Accuracy", 0)
        )
        metric_name = "Accuracy" if "Accuracy" in best_exp["metrics"] else "CV Accuracy"

        st.markdown(
            f"""
**Best Model Configuration (Experiment #{best_exp["id"]})**

- **Architecture**: `{best_exp["architecture"]}`
- **Activation**: {best_exp["activation"]}
- **Solver**: {best_exp["solver"]}
- **Max Iter**: {best_exp["max_iter"]}
- {metric_name}: **{acc:.4f}**
"""
        )

    with col_button:
        if st.button(
            f"💾 Save Best Model\n(Exp #{best_exp['id']})",
            width="stretch",
            type="primary",
            key="ann_save_best_model",
        ):
            _save_best_model(best_exp, metric_name, acc, X, y)

    # Show current saved model info
    if st.session_state.ann.get("best_model"):
        st.divider()
        st.success(
            f"✅ **Saved Model**: Exp #{st.session_state.ann.get('saved_exp_id', '?')} "
            f"({st.session_state.ann['best_metrics'].get(metric_name, 0):.4f} {metric_name})"
        )
        st.caption("This model is ready for PCA comparison in the PCA tab →")


def _save_best_model(best_exp, metric_name, acc, X, y):
    """
    Retrain and save best model configuration
    
    Args:
        best_exp: Best experiment dictionary
        metric_name: Name of the metric used
        acc: Accuracy value
        X: Feature matrix
        y: Target labels
    """
    with st.spinner(f"Retraining best model (Exp #{best_exp['id']}) on full dataset..."):
        # Retrain on full dataset
        model = MLPClassifier(
            hidden_layer_sizes=best_exp["architecture"],
            activation=best_exp["activation"],
            solver=best_exp["solver"],
            max_iter=best_exp["max_iter"],
            random_state=CONF[Keys.RANDOM_STATE],
            learning_rate=CONF[Keys.ANN_LEARNING_RATE],
            alpha=CONF[Keys.ANN_ALPHA],
        )

        model.fit(X, y)

        # Save to session state
        st.session_state.ann["best_model"] = model
        st.session_state.ann["best_metrics"] = best_exp["metrics"]
        st.session_state.ann["best_params"] = {
            "architecture": best_exp["architecture"],
            "activation": best_exp["activation"],
            "solver": best_exp["solver"],
            "max_iter": best_exp["max_iter"],
        }
        st.session_state.ann["saved_exp_id"] = best_exp["id"]

        st.success(
            f"✅ Model saved! Experiment #{best_exp['id']} with {acc:.4f} {metric_name}"
        )

