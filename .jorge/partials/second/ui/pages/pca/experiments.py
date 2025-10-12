"""
PCA Experiment Tracking and Persistence
Stores PCA transformation parameters and comparison results
"""

import json
from pathlib import Path

import streamlit as st

# Get absolute path to cache directory (works on Streamlit Cloud)
CACHE_DIR = Path(__file__).resolve().parent.parent.parent.parent / ".cache"
CACHE_FILE = CACHE_DIR / "pca_experiments.json"


def save_pca_experiment():
    """
    Save current PCA experiment to history
    Stores: n_components, variance retained, model comparisons
    """
    if not st.session_state.pca.get("pca_applied"):
        return

    experiment = {
        "id": len(st.session_state.pca.get("experiment_history", [])) + 1,
        "n_components": st.session_state.pca.get("n_components_used", 0),
        "explained_variance": float(
            st.session_state.pca.get("cumulative_variance", [0])[-1]
        ),
        "selection_method": st.session_state.get("pca_selection_method", "Fixed Number"),
    }

    # Add SVM comparison if available
    if st.session_state.pca.get("svm_pca_trained"):
        experiment["svm_comparison"] = {
            "original_accuracy": st.session_state.svm.get("best_metrics", {}).get(
                "Accuracy",
                st.session_state.svm.get("best_metrics", {}).get("CV Accuracy", 0),
            ),
            "pca_accuracy": st.session_state.pca.get("svm_pca_metrics", {}).get(
                "Accuracy", 0
            ),
            "training_time_original": st.session_state.svm.get("best_params", {}).get(
                "training_time", 0
            ),
            "training_time_pca": st.session_state.pca.get("svm_pca_training_time", 0),
        }

    # Add ANN comparison if available
    if st.session_state.pca.get("ann_pca_trained"):
        experiment["ann_comparison"] = {
            "original_accuracy": st.session_state.ann.get("best_metrics", {}).get(
                "Accuracy",
                st.session_state.ann.get("best_metrics", {}).get("CV Accuracy", 0),
            ),
            "pca_accuracy": st.session_state.pca.get("ann_pca_metrics", {}).get(
                "Accuracy", 0
            ),
            "training_time_original": st.session_state.ann.get("best_params", {}).get(
                "training_time", 0
            ),
            "training_time_pca": st.session_state.pca.get("ann_pca_training_time", 0),
        }

    # Append to history
    if "experiment_history" not in st.session_state.pca:
        st.session_state.pca["experiment_history"] = []

    st.session_state.pca["experiment_history"].append(experiment)

    # Persist to file
    _persist_experiments()


def load_pca_experiments():
    """Load PCA experiments from persistent storage"""
    if not CACHE_FILE.exists():
        return []

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def _persist_experiments():
    """Persist experiments to cache file"""
    CACHE_DIR.mkdir(exist_ok=True, parents=True)

    experiments = st.session_state.pca.get("experiment_history", [])

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(experiments, f, indent=2)


def clear_pca_experiments():
    """Clear PCA experiment history"""
    st.session_state.pca["experiment_history"] = []
    
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()


def render_experiment_history():
    """
    Render PCA experiment history
    Shows all PCA transformations and their impact on model performance
    """
    if not st.session_state.pca.get("experiment_history"):
        return

    st.divider()
    st.subheader("📋 PCA Experiment History")

    history = st.session_state.pca["experiment_history"]

    # Create table data
    table_data = []
    for exp in history:
        row = {
            "ID": exp["id"],
            "n_components": exp["n_components"],
            "Variance": f"{exp['explained_variance']*100:.2f}%",
            "Method": exp.get("selection_method", "N/A"),
        }

        # Add SVM comparison
        if "svm_comparison" in exp:
            svm = exp["svm_comparison"]
            delta_acc = svm["pca_accuracy"] - svm["original_accuracy"]
            row["SVM Δ Acc"] = f"{delta_acc:+.4f}"
        else:
            row["SVM Δ Acc"] = "-"

        # Add ANN comparison
        if "ann_comparison" in exp:
            ann = exp["ann_comparison"]
            delta_acc = ann["pca_accuracy"] - ann["original_accuracy"]
            row["ANN Δ Acc"] = f"{delta_acc:+.4f}"
        else:
            row["ANN Δ Acc"] = "-"

        table_data.append(row)

    import pandas as pd

    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Statistics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Experiments", len(history))

    with col2:
        avg_variance = sum(exp["explained_variance"] for exp in history) / len(history)
        st.metric("Avg Variance Retained", f"{avg_variance*100:.1f}%")

    with col3:
        if st.button("🗑️ Clear History", width="stretch", key="pca_clear_history"):
            clear_pca_experiments()
            st.rerun()

    st.caption(
        "💡 **Tip:** Compare different n_components to find the optimal "
        "dimensionality for your dataset."
    )

