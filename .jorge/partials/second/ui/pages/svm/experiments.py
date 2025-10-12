"""
SVM Experiment Tracking and Visualization
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from funcs.persistence import clear_experiments_file


def render_experiment_history(session_state_svm):
    """
    Render experiment history table and comparisons

    Args:
        session_state_svm: st.session_state.svm dictionary
    """
    if (
        "experiment_history" not in session_state_svm
        or not session_state_svm["experiment_history"]
    ):
        return

    st.divider()
    st.subheader("📋 Experiment History - Compare All Runs")

    history = session_state_svm["experiment_history"]

    # Prepare data for table
    table_data = []
    for exp in history:
        row = {
            "ID": exp["id"],
            "Kernel": exp["kernel"],
            "C": f"{exp['C']:.2f}",
            "gamma": exp["gamma"],
            "degree": exp["degree"],
        }

        # Add metrics
        for metric_name, metric_value in exp["metrics"].items():
            if isinstance(metric_value, (int, float)):
                row[metric_name] = f"{metric_value:.4f}"
            else:
                row[metric_name] = str(metric_value)

        row["Time (s)"] = f"{exp['training_time']:.2f}"
        table_data.append(row)

    df = pd.DataFrame(table_data)

    # Display table
    st.dataframe(
        df,
        use_container_width=True,
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
        if st.button("🗑️ Clear History", width="stretch"):
            session_state_svm["experiment_history"] = []
            clear_experiments_file("svm")  # Clear persisted file
            st.rerun()

    # Visualization: Compare metrics across experiments
    if len(history) > 1:
        _render_comparison_chart(history, best_idx)


def _find_best_experiment(history):
    """
    Find the experiment with the best accuracy

    Returns:
        tuple: (best_index, best_accuracy)
    """
    if not history:
        return None, None

    if "CV Accuracy" in history[0]["metrics"]:
        best_idx = max(
            range(len(history)), key=lambda i: history[i]["metrics"]["CV Accuracy"]
        )
        best_acc = history[best_idx]["metrics"]["CV Accuracy"]
    elif "Accuracy" in history[0]["metrics"]:
        best_idx = max(
            range(len(history)), key=lambda i: history[i]["metrics"]["Accuracy"]
        )
        best_acc = history[best_idx]["metrics"]["Accuracy"]
    else:
        best_idx = 0
        best_acc = 0

    return best_idx, best_acc


def get_best_experiment(history):
    """
    Get the best experiment dictionary from history

    Args:
        history: List of experiment dictionaries

    Returns:
        tuple: (best_experiment_dict, best_index) or (None, None) if no history
    """
    if not history:
        return None, None

    best_idx, _ = _find_best_experiment(history)

    if best_idx is None:
        return None, None

    return history[best_idx], best_idx


def _render_comparison_chart(history, best_idx):
    """Render comparison chart for experiments"""
    st.markdown("### 📊 Comparison Across Experiments")

    # Get first metric that's between 0 and 1
    metric_to_plot = None
    for metric_name in history[0]["metrics"].keys():
        if all(0 <= exp["metrics"].get(metric_name, -1) <= 1 for exp in history):
            metric_to_plot = metric_name
            break

    if not metric_to_plot:
        return

    fig, ax = plt.subplots(figsize=(10, 4))

    exp_ids = [exp["id"] for exp in history]
    metric_values = [exp["metrics"][metric_to_plot] for exp in history]
    kernel_labels = [f"{exp['kernel']}" for exp in history]

    # Color best experiment green
    colors = ["#1f77b4" if i != best_idx else "#2ca02c" for i in range(len(history))]

    bars = ax.bar(exp_ids, metric_values, color=colors, alpha=0.7, edgecolor="black")

    # Add value labels on bars
    for bar, value, label in zip(bars, metric_values, kernel_labels):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{value:.4f}\n{label}",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    ax.set_xlabel("Experiment ID", fontsize=12)
    ax.set_ylabel(metric_to_plot, fontsize=12)
    ax.set_title(
        f"{metric_to_plot} Comparison Across Experiments",
        fontsize=14,
        fontweight="bold",
    )
    ax.set_ylim([max(0, min(metric_values) - 0.05), min(1, max(metric_values) + 0.1)])
    ax.grid(axis="y", alpha=0.3)
    ax.set_xticks(exp_ids)

    st.pyplot(fig)

    # Add insights
    _render_insights(history, best_idx, metric_values)


def _render_insights(history, best_idx, metric_values):
    """Render insights about experiments"""
    st.markdown("**💡 Insights:**")

    best_kernel = history[best_idx]["kernel"]
    best_c = history[best_idx]["C"]
    best_gamma = history[best_idx]["gamma"]

    st.markdown(f"""
    - **Best performing kernel**: {best_kernel} (Experiment #{history[best_idx]["id"]})
    - **Best parameters**: C={best_c:.2f}, gamma={best_gamma}
    - **Performance range**: {min(metric_values):.4f} - {max(metric_values):.4f}
    - **Performance variance**: {np.std(metric_values):.4f}
    """)
