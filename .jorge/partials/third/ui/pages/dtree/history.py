"""
Experiment History tracking for Decision Tree page.

Single Responsibility: Display and compare saved experiments.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import logging
from typing import List, Dict, Any

from states import get_state, set_state

logger = logging.getLogger(__name__)


def render_experiment_history():
    """
    Render experiment history table and comparison charts.
    
    Displays:
    - Saved experiments table
    - Accuracy evolution chart
    - Features vs Accuracy scatter plot
    - Clear history button
    """
    st.markdown("### 📊 Experimentos Guardados")
    
    history = get_state("experiment_history", [])
    
    if len(history) == 0:
        st.info("No hay experimentos guardados aún. Entrena un modelo para empezar!")
        return
    
    st.success(f"✅ {len(history)} experimento(s) guardado(s) en esta sesión")
    
    # Create comparison table
    df_history = _create_history_table(history)
    st.dataframe(df_history, width="stretch", height=300)
    
    # Comparison charts
    st.markdown("#### 📈 Comparación Visual")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        _render_accuracy_evolution(history)
    
    with col_chart2:
        _render_features_vs_accuracy(history)
    
    # Clear history button
    if st.button("🗑️ Limpiar Historial", type="secondary"):
        set_state("experiment_history", [])
        st.rerun()


def _create_history_table(history: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Create a DataFrame from experiment history.
    
    Args:
        history: List of experiment dicts
    
    Returns:
        DataFrame with experiment details
    """
    history_data = []
    for exp in history:
        history_data.append({
            "ID": exp["id"],
            "Timestamp": exp["timestamp"].split("T")[1][:8] if "T" in exp["timestamp"] else exp["timestamp"],
            "Max Depth": exp["params"]["max_depth"],
            "Min Split": exp["params"]["min_samples_split"],
            "Criterion": exp["params"]["criterion"],
            "Test %": f"{exp['params']['test_size']*100:.0f}%",
            "CV Folds": exp["params"]["cv_folds"],
            "Features": exp["data"]["n_features"],
            "Accuracy": f"{exp['metrics']['accuracy']:.3f}",
            "F1": f"{exp['metrics']['f1_score']:.3f}",
            "CV Mean": f"{exp['metrics']['cv_mean']:.3f}",
            "CV Std": f"{exp['metrics']['cv_std']:.3f}",
            "Depth": exp["tree_info"]["depth"],
            "Leaves": exp["tree_info"]["n_leaves"],
            "Rules": exp["tree_info"]["n_rules"]
        })
    
    return pd.DataFrame(history_data)


def _render_accuracy_evolution(history: List[Dict[str, Any]]):
    """
    Render accuracy evolution line chart.
    
    Args:
        history: List of experiment dicts
    """
    fig_acc, ax_acc = plt.subplots(figsize=(8, 5))
    
    accuracies = [float(exp["metrics"]["accuracy"]) for exp in history]
    labels = [exp["id"].split("_")[1] for exp in history]  # Just timestamp
    
    ax_acc.plot(
        range(len(accuracies)), 
        accuracies, 
        marker='o', 
        linewidth=2, 
        markersize=8, 
        color='steelblue'
    )
    ax_acc.set_xlabel("Experimento")
    ax_acc.set_ylabel("Accuracy")
    ax_acc.set_title("Evolución del Accuracy")
    ax_acc.set_xticks(range(len(labels)))
    ax_acc.set_xticklabels(labels, rotation=45, ha='right')
    ax_acc.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig_acc)
    plt.close()


def _render_features_vs_accuracy(history: List[Dict[str, Any]]):
    """
    Render features vs accuracy scatter plot.
    
    Args:
        history: List of experiment dicts
    """
    fig_feat, ax_feat = plt.subplots(figsize=(8, 5))
    
    n_features = [exp["data"]["n_features"] for exp in history]
    accuracies = [float(exp["metrics"]["accuracy"]) for exp in history]
    
    # Color code by feature count (green=30, orange=31, red=32)
    colors = [
        'green' if f == 30 else 'orange' if f == 31 else 'red' 
        for f in n_features
    ]
    
    ax_feat.scatter(n_features, accuracies, s=100, c=colors, alpha=0.6)
    ax_feat.set_xlabel("Número de Features")
    ax_feat.set_ylabel("Accuracy")
    ax_feat.set_title("Features vs Accuracy")
    ax_feat.grid(True, alpha=0.3)
    
    # Add legend
    ax_feat.plot([], [], 'o', color='green', label='30 feat (sin G1/G2)')
    ax_feat.plot([], [], 'o', color='orange', label='31 feat (G1 o G2)')
    ax_feat.plot([], [], 'o', color='red', label='32 feat (G1 + G2)')
    ax_feat.legend()
    
    plt.tight_layout()
    st.pyplot(fig_feat)
    plt.close()

