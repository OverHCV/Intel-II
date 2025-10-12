"""
ANN Experiment Tracking and Visualization
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from funcs.persistence import clear_experiments_file


def render_experiment_history(session_state_ann):
    """
    Render experiment history table and comparisons

    Args:
        session_state_ann: st.session_state.ann dictionary
    """
    if (
        "experiment_history" not in session_state_ann
        or not session_state_ann["experiment_history"]
    ):
        return

    st.divider()
    st.subheader("📋 Experiment History - Compare All Runs")

    history = session_state_ann["experiment_history"]

    # Prepare data for table
    table_data = []
    for exp in history:
        row = {
            "ID": exp["id"],
            "Architecture": str(exp["architecture"]),  # Keep tuple format (20, 10)
            "Activation": exp["activation"],
            "Solver": exp["solver"],
            "Max Iter": exp["max_iter"],
        }

        # Add metrics
        for metric_name, metric_value in exp["metrics"].items():
            if isinstance(metric_value, (int, float)):
                row[metric_name] = f"{metric_value:.4f}"
            else:
                row[metric_value] = str(metric_value)

        row["Time (s)"] = f"{exp['training_time']:.2f}"
        table_data.append(row)

    df = pd.DataFrame(table_data)

    # Display table
    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
    )

    # Statistics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Experiments", len(history))

    with col2:
        # Find best experiment
        best_idx, best_acc = _find_best_experiment(history)
        st.metric("Best Accuracy", f"{best_acc:.4f}", f"Exp #{history[best_idx]['id']}")

    with col3:
        if st.button("🗑️ Clear History", width="stretch", key="ann_clear_history"):
            session_state_ann["experiment_history"] = []
            clear_experiments_file("ann")  # Clear persisted file
            st.rerun()

    # Visualization: Compare metrics across experiments
    if len(history) > 1:
        _render_comparison_chart(history, best_idx)

    st.caption(
        f"💡 **Tip:** Experiment ID #{history[best_idx]['id']} has the best accuracy. "
        "Use the 'Save Best Model' button below to save it for PCA comparison."
    )


def get_best_experiment(history):
    """
    Get the best experiment from history based on accuracy

    Args:
        history: List of experiment dictionaries

    Returns:
        Best experiment dictionary or None
    """
    if not history:
        return None

    best_idx, _ = _find_best_experiment(history)
    return history[best_idx]


def _find_best_experiment(history):
    """
    Find experiment with highest accuracy

    Args:
        history: List of experiment dictionaries

    Returns:
        Tuple of (best_index, best_accuracy)
    """
    best_idx = 0
    best_acc = 0

    for idx, exp in enumerate(history):
        # Get accuracy metric (handle both train_test and kfold metrics)
        acc = exp["metrics"].get("Accuracy", exp["metrics"].get("CV Accuracy", 0))

        if acc > best_acc:
            best_acc = acc
            best_idx = idx

    return best_idx, best_acc


def _render_comparison_chart(history, best_idx):
    """
    Render comparison chart for experiments

    Args:
        history: List of experiment dictionaries
        best_idx: Index of best experiment
    """
    st.markdown("#### 📊 Accuracy Trend Across Experiments")

    # Extract data
    exp_ids = [exp["id"] for exp in history]
    accuracies = [
        exp["metrics"].get("Accuracy", exp["metrics"].get("CV Accuracy", 0))
        for exp in history
    ]

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 4))

    # Plot line
    ax.plot(exp_ids, accuracies, marker="o", linewidth=2, markersize=8, alpha=0.7)

    # Highlight best
    ax.scatter(
        [history[best_idx]["id"]],
        [accuracies[best_idx]],
        color="gold",
        s=200,
        zorder=5,
        edgecolors="black",
        linewidth=2,
        label=f"Best (#{history[best_idx]['id']})",
    )

    # Styling
    ax.set_xlabel("Experiment ID", fontsize=11)
    ax.set_ylabel("Accuracy", fontsize=11)
    ax.set_title("Model Performance Across Experiments", fontsize=12, fontweight="bold")
    ax.grid(alpha=0.3, linestyle="--")
    ax.legend(loc="best")
    ax.set_ylim([0, 1])

    # Add value labels
    for i, (x, y) in enumerate(zip(exp_ids, accuracies)):
        ax.annotate(
            f"{y:.3f}",
            (x, y),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontsize=8,
            alpha=0.7,
        )

    plt.tight_layout()
    st.pyplot(fig)

    st.caption(
        f"📈 **Insight:** {'Accuracy is improving!' if accuracies[-1] > accuracies[0] else 'Try different configurations!'}"
    )

