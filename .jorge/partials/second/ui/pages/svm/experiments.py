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
        # Find best experiment (using F1-Score for imbalanced data)
        best_idx, best_score, metric_name = _find_best_experiment(history)
        st.metric(f"Best {metric_name}", f"{best_score:.4f}", f"Exp #{history[best_idx]['id']}")

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
    Find the experiment with the best F1-Score (better for imbalanced data)
    Falls back to accuracy if F1 not available
    
    Returns:
        tuple: (best_index, best_score, metric_name)
    """
    if not history:
        return None, None, None

    def get_best_metric(exp):
        """
        Get best evaluation metric - prioritizes F1-Score for imbalanced data
        Falls back to accuracy if F1 not available
        """
        metrics = exp["metrics"]
        
        # Prioritize F1-Score (better for imbalanced datasets)
        f1 = metrics.get("CV F1-Score", metrics.get("F1-Score", None))
        if f1 is not None and f1 > 0:
            return f1, "F1-Score"
        
        # Fallback to accuracy
        acc = metrics.get("CV Accuracy", metrics.get("Accuracy", 0))
        return acc, "Accuracy"

    best_idx = max(range(len(history)), key=lambda i: get_best_metric(history[i])[0])
    best_score, metric_name = get_best_metric(history[best_idx])

    return best_idx, best_score, metric_name


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

    best_idx, _, _ = _find_best_experiment(history)

    if best_idx is None:
        return None, None

    return history[best_idx], best_idx


def _render_comparison_chart(history, best_idx):
    """Render comparison chart showing REAL METRICS (Precision, Recall, F1)"""
    st.markdown("### 📊 Comparison Across Experiments")

    # Define metrics to compare (prioritize F1, Precision, Recall over Accuracy)
    metrics_to_compare = [
        ("CV F1-Score", "F1-Score", "F1"),
        ("CV Precision", "Precision", "Prec"),
        ("CV Recall", "Recall", "Rec"),
        ("CV Accuracy", "Accuracy", "Acc"),
    ]
    
    # Find which metrics are available in ALL experiments
    available_metrics = []
    for cv_name, tt_name, short_name in metrics_to_compare:
        # Check if metric exists in all experiments (either CV or train/test version)
        if all(cv_name in exp["metrics"] or tt_name in exp["metrics"] for exp in history):
            available_metrics.append((cv_name, tt_name, short_name))
    
    if not available_metrics:
        st.info("💡 No common metrics across experiments. Train experiments with the same CV strategy to compare.")
        return

    # Prepare data for grouped bar chart
    exp_ids = [exp["id"] for exp in history]
    x = np.arange(len(exp_ids))
    width = 0.8 / len(available_metrics)  # Width of bars
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot each metric as a grouped bar
    for i, (cv_name, tt_name, short_name) in enumerate(available_metrics):
        values = []
        for exp in history:
            # Try CV version first, then train/test version
            val = exp["metrics"].get(cv_name, exp["metrics"].get(tt_name, 0))
            values.append(val)
        
        offset = (i - len(available_metrics)/2) * width + width/2
        bars = ax.bar(x + offset, values, width, label=short_name, alpha=0.8)
        
        # Add value labels on bars
        for j, (bar, val) in enumerate(zip(bars, values)):
            if val > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    bar.get_height() + 0.01,
                    f"{val:.3f}",
                    ha="center",
                    va="bottom",
                    fontsize=7,
                    rotation=0,
                )
    
    # Highlight best experiment with a marker
    ax.scatter([best_idx], [1.05], marker='v', s=200, color='gold', 
               edgecolors='black', linewidth=2, zorder=5, label='Best')
    
    # Styling
    ax.set_xlabel("Experiment ID", fontsize=12, fontweight='bold')
    ax.set_ylabel("Score", fontsize=12, fontweight='bold')
    ax.set_title(
        "Multi-Metric Comparison: F1, Precision, Recall",
        fontsize=13,
        fontweight="bold",
    )
    ax.set_xticks(x)
    ax.set_xticklabels([f"#{exp_id}" for exp_id in exp_ids])
    ax.set_ylim([0, 1.1])
    ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
    ax.grid(axis="y", alpha=0.3, linestyle='--')
    
    # Add kernel labels below x-axis
    kernel_labels = [exp['kernel'][:3] for exp in history]
    for i, label in enumerate(kernel_labels):
        ax.text(i, -0.08, label, ha='center', va='top', fontsize=8, 
                style='italic', color='gray')
    
    plt.tight_layout()
    st.pyplot(fig)

    # Add insights with REAL metrics
    _render_insights(history, best_idx, available_metrics)


def _render_insights(history, best_idx, available_metrics):
    """Render insights about experiments with REAL metrics focus"""
    st.markdown("**💡 Key Insights (Focus on F1-Score for Imbalanced Data):**")

    best_exp = history[best_idx]
    best_kernel = best_exp["kernel"]
    best_c = best_exp["C"]
    best_gamma = best_exp["gamma"]
    
    # Get F1-Score for best experiment
    best_f1 = best_exp["metrics"].get("CV F1-Score", best_exp["metrics"].get("F1-Score", 0))
    best_prec = best_exp["metrics"].get("CV Precision", best_exp["metrics"].get("Precision", 0))
    best_rec = best_exp["metrics"].get("CV Recall", best_exp["metrics"].get("Recall", 0))
    
    # Calculate F1 scores for all experiments
    f1_scores = []
    for exp in history:
        f1 = exp["metrics"].get("CV F1-Score", exp["metrics"].get("F1-Score", 0))
        f1_scores.append(f1)
    
    st.markdown(f"""
    - **Best Model** (Exp #{best_exp["id"]}): {best_kernel} kernel, C={best_c:.2f}, gamma={best_gamma}
    - **Best F1-Score**: {best_f1:.4f} (Precision: {best_prec:.4f}, Recall: {best_rec:.4f})
    - **F1 Range Across Experiments**: {min(f1_scores):.4f} - {max(f1_scores):.4f}
    - **F1 Variance**: {np.std(f1_scores):.4f} {'(high variance - unstable)' if np.std(f1_scores) > 0.1 else '(stable)'}
    
    ⚠️ **Remember**: High accuracy with low F1-Score means the model is biased toward the majority class!
    """)
    
    # Warn about accuracy trap
    best_acc = best_exp["metrics"].get("CV Accuracy", best_exp["metrics"].get("Accuracy", 0))
    if best_acc > 0.85 and best_f1 < 0.5:
        st.warning(
            f"⚠️ **Accuracy Trap Detected!** "
            f"Accuracy={best_acc:.3f} but F1={best_f1:.3f}. "
            f"This model is likely just predicting the majority class. "
            f"Focus on improving Precision and Recall!"
        )
