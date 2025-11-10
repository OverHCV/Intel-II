"""Side-by-side comparison tool for selected experiments."""
import streamlit as st
import pandas as pd
from typing import List, Dict, Any
import matplotlib.pyplot as plt
from versioning.experiment_store import load_experiment


def render_comparison(selected_ids: List[str], all_experiments: List[Dict[str, Any]]) -> None:
    """
    Render side-by-side comparison of selected experiments.
    
    Args:
        selected_ids: List of selected version IDs
        all_experiments: Full list of experiments for lookup
    """
    if not selected_ids:
        st.info("👆 Select experiments from the table above to compare")
        return
    
    st.subheader("🔬 Experiment Comparison")
    
    if len(selected_ids) > 5:
        st.warning("⚠️ Maximum 5 experiments can be compared at once")
        selected_ids = selected_ids[:5]
    
    # Load full experiment data
    experiments = []
    for exp in all_experiments:
        if exp['version_id'] in selected_ids:
            experiments.append(exp)
    
    if not experiments:
        st.error("❌ Could not load selected experiments")
        return
    
    # Organize by algorithm type
    by_algo = {}
    for exp in experiments:
        algo = exp['algorithm_type']
        if algo not in by_algo:
            by_algo[algo] = []
        by_algo[algo].append(exp)
    
    # Render comparison for each algorithm type
    for algo, algo_exps in by_algo.items():
        with st.expander(f"🔍 {algo.replace('_', ' ').title()} Comparison ({len(algo_exps)} experiments)", expanded=True):
            if algo == 'decision_tree':
                _compare_decision_trees(algo_exps)
            elif algo == 'hierarchical':
                _compare_hierarchical(algo_exps)
            elif algo == 'kmeans':
                _compare_kmeans(algo_exps)


def _compare_decision_trees(experiments: List[Dict[str, Any]]) -> None:
    """Compare Decision Tree experiments."""
    
    # Create comparison table
    comparison_data = []
    for exp in experiments:
        params = exp.get('parameters', {})
        metrics = exp.get('metrics', {})
        
        comparison_data.append({
            'Version ID': exp['version_id'][:16] + '...',
            'Max Depth': params.get('max_depth', 'N/A'),
            'Min Samples Split': params.get('min_samples_split', 'N/A'),
            'Criterion': params.get('criterion', 'N/A'),
            'Accuracy': f"{metrics.get('accuracy', 0):.4f}",
            'Precision': f"{metrics.get('precision', 0):.4f}",
            'Recall': f"{metrics.get('recall', 0):.4f}",
            'F1-Score': f"{metrics.get('f1', 0):.4f}",
            'CV Mean': f"{metrics.get('cv_mean', 0):.4f}",
            'Timestamp': exp['timestamp'][:19]
        })
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, width='stretch')
    
    # Metrics comparison chart
    if len(experiments) > 1:
        _plot_metrics_comparison(experiments, ['accuracy', 'precision', 'recall', 'f1'])


def _compare_hierarchical(experiments: List[Dict[str, Any]]) -> None:
    """Compare Hierarchical Clustering experiments."""
    
    comparison_data = []
    for exp in experiments:
        params = exp.get('parameters', {})
        metrics = exp.get('metrics', {})
        
        comparison_data.append({
            'Version ID': exp['version_id'][:16] + '...',
            'K': params.get('n_clusters', 'N/A'),
            'Linkage': params.get('linkage_method', 'N/A'),
            'Distance': params.get('distance_metric', 'N/A'),
            'Silhouette': f"{metrics.get('silhouette_avg', 0):.4f}",
            'Fisher J4': f"{metrics.get('fisher_j4', 0):.4f}",
            'Timestamp': exp['timestamp'][:19]
        })
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, width='stretch')
    
    if len(experiments) > 1:
        _plot_metrics_comparison(experiments, ['silhouette_avg', 'fisher_j4'])


def _compare_kmeans(experiments: List[Dict[str, Any]]) -> None:
    """Compare K-means experiments."""
    
    comparison_data = []
    for exp in experiments:
        params = exp.get('parameters', {})
        metrics = exp.get('metrics', {})
        
        comparison_data.append({
            'Version ID': exp['version_id'][:16] + '...',
            'K': params.get('n_clusters', 'N/A'),
            'Init': params.get('init_method', 'N/A'),
            'N Init': params.get('n_init', 'N/A'),
            'Max Iter': params.get('max_iter', 'N/A'),
            'Silhouette': f"{metrics.get('silhouette_avg', 0):.4f}",
            'Fisher J4': f"{metrics.get('fisher_j4', 0):.4f}",
            'Inertia': f"{metrics.get('inertia', 0):.2f}",
            'Timestamp': exp['timestamp'][:19]
        })
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, width='stretch')
    
    if len(experiments) > 1:
        _plot_metrics_comparison(experiments, ['silhouette_avg', 'fisher_j4', 'inertia'])


def _plot_metrics_comparison(experiments: List[Dict[str, Any]], metric_names: List[str]) -> None:
    """
    Plot bar chart comparing metrics across experiments.
    
    Args:
        experiments: List of experiment data
        metric_names: List of metric keys to plot
    """
    # Extract metrics
    data = {metric: [] for metric in metric_names}
    labels = []
    
    for exp in experiments:
        metrics = exp.get('metrics', {})
        labels.append(exp['version_id'][:12])
        for metric in metric_names:
            data[metric].append(metrics.get(metric, 0))
    
    # Create figure
    fig, axes = plt.subplots(1, len(metric_names), figsize=(5 * len(metric_names), 4))
    
    if len(metric_names) == 1:
        axes = [axes]
    
    colors = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#F8B500', '#A8E6CF']
    
    for idx, metric in enumerate(metric_names):
        ax = axes[idx]
        
        bars = ax.bar(labels, data[metric], color=colors[:len(labels)], alpha=0.7)
        
        ax.set_title(metric.replace('_', ' ').title(), fontsize=12, fontweight='bold')
        ax.set_ylabel('Value')
        ax.set_xlabel('Experiment')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}',
                   ha='center', va='bottom', fontsize=9)
        
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Highlight best performer
    st.caption("💡 **Best Performers:**")
    for metric in metric_names:
        values = data[metric]
        if not values:
            continue
        
        # For inertia, lower is better; for others, higher is better
        if 'inertia' in metric.lower():
            best_idx = values.index(min(values))
            best_value = min(values)
        else:
            best_idx = values.index(max(values))
            best_value = max(values)
        
        st.caption(f"- **{metric.replace('_', ' ').title()}**: {labels[best_idx]} ({best_value:.4f})")

