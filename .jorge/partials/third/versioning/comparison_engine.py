"""
Comparison Engine - Multi-experiment comparison and visualization.

This module enables side-by-side comparison of different experiments,
parameter differences, and metric improvements.

WHY: Learning requires comparison - "What changed between v1 and v2?"
     "Which hyperparameter matters most?"
"""

from typing import Dict, List, Tuple, Optional, Any
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import logging

from .experiment_store import load_experiment

logger = logging.getLogger(__name__)


def compare_metrics(
    version_ids: List[str],
    algorithm_types: List[str]
) -> Dict[str, Any]:
    """
    Compare metrics across multiple experiments.
    
    WHY: Side-by-side metric comparison reveals which configuration wins.
    
    Args:
        version_ids: List of experiment version IDs
        algorithm_types: Corresponding algorithm types
        
    Returns:
        Comparison table with all metrics
    """
    if len(version_ids) != len(algorithm_types):
        raise ValueError("version_ids and algorithm_types must have same length")
    
    comparisons = []
    
    for vid, alg in zip(version_ids, algorithm_types):
        try:
            exp = load_experiment(vid, alg)
            comparisons.append({
                "version_id": vid,
                "algorithm": alg,
                "timestamp": exp.get("timestamp", ""),
                "metrics": exp.get("metrics", {}),
                "parameters": exp.get("parameters", {})
            })
        except FileNotFoundError:
            logger.warning(f"Experiment not found: {alg}/{vid}")
    
    # Calculate best for each metric
    all_metrics = set()
    for comp in comparisons:
        all_metrics.update(comp["metrics"].keys())
    
    best_per_metric = {}
    for metric in all_metrics:
        values = [
            (i, comp["metrics"].get(metric, float('-inf')))
            for i, comp in enumerate(comparisons)
        ]
        best_idx, best_value = max(values, key=lambda x: x[1])
        best_per_metric[metric] = {
            "best_index": best_idx,
            "best_value": best_value,
            "best_version": comparisons[best_idx]["version_id"]
        }
    
    result = {
        "experiments": comparisons,
        "best_per_metric": best_per_metric,
        "n_compared": len(comparisons)
    }
    
    logger.info(f"Compared {len(comparisons)} experiments")
    return result


def compare_parameters(
    version_ids: List[str],
    algorithm_types: List[str]
) -> Dict[str, Any]:
    """
    Compare parameters across experiments to find what changed.
    
    WHY: "What did I change that made accuracy jump from 0.80 to 0.85?"
    
    Args:
        version_ids: List of experiment version IDs
        algorithm_types: Corresponding algorithm types
        
    Returns:
        Parameter diff report
    """
    experiments = []
    for vid, alg in zip(version_ids, algorithm_types):
        try:
            exp = load_experiment(vid, alg)
            experiments.append(exp)
        except FileNotFoundError:
            continue
    
    if len(experiments) < 2:
        return {"error": "Need at least 2 experiments to compare"}
    
    # Find all parameter names
    all_params = set()
    for exp in experiments:
        all_params.update(exp.get("parameters", {}).keys())
    
    # Compare each parameter
    differences = {}
    constants = {}
    
    for param in all_params:
        values = [exp.get("parameters", {}).get(param) for exp in experiments]
        unique_values = set(str(v) for v in values if v is not None)
        
        if len(unique_values) == 1:
            constants[param] = list(unique_values)[0]
        else:
            differences[param] = [
                {"version_id": exp["version_id"], "value": v}
                for exp, v in zip(experiments, values)
            ]
    
    result = {
        "differences": differences,
        "constants": constants,
        "n_varying_params": len(differences),
        "n_constant_params": len(constants),
        "interpretation": (
            f"{len(differences)} parameters varied across experiments. "
            f"These are candidates for performance impact."
        )
    }
    
    logger.info(f"Found {len(differences)} parameter differences")
    return result


def generate_comparison_plots(
    version_ids: List[str],
    algorithm_types: List[str],
    metrics: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Generate matplotlib figures comparing experiments.
    
    WHY: Visuals make comparisons immediate - bar charts show winner clearly.
    
    WIP: Generate actual matplotlib figures and save to files.
    WHY: Need to create bar charts, radar plots, and timeline charts.
    
    Args:
        version_ids: List of experiment version IDs
        algorithm_types: Corresponding algorithm types
        metrics: Optional list of metrics to plot
        
    Returns:
        Dictionary with plot paths and figure objects
    """
    # WIP: Create actual plots
    # WHY: Need to visualize metric comparisons for easy interpretation
    
    plots = {
        "bar_chart": "WIP: Bar chart comparing key metrics across experiments",
        "radar_plot": "WIP: Radar plot showing multi-dimensional performance",
        "timeline_chart": "WIP: Line chart showing metric evolution over time",
        "why": {
            "bar_chart": "Quick visual comparison - highest bar wins",
            "radar_plot": "Shows trade-offs - high in one metric, low in another",
            "timeline": "Shows improvement trajectory - are we getting better?"
        }
    }
    
    logger.info(f"Generated comparison plots (WIP) for {len(version_ids)} experiments")
    return plots


def calculate_improvement(
    baseline_id: str,
    baseline_alg: str,
    new_id: str,
    new_alg: str
) -> Dict[str, Any]:
    """
    Calculate improvement from baseline to new experiment.
    
    WHY: "Did this change make things better?" - quantify the delta.
    
    Args:
        baseline_id: Baseline experiment version ID
        baseline_alg: Baseline algorithm type
        new_id: New experiment version ID
        new_alg: New algorithm type
        
    Returns:
        Dictionary with improvement deltas for each metric
    """
    baseline = load_experiment(baseline_id, baseline_alg)
    new_exp = load_experiment(new_id, new_alg)
    
    baseline_metrics = baseline.get("metrics", {})
    new_metrics = new_exp.get("metrics", {})
    
    improvements = {}
    for metric in set(baseline_metrics.keys()) | set(new_metrics.keys()):
        base_val = baseline_metrics.get(metric)
        new_val = new_metrics.get(metric)
        
        if base_val is not None and new_val is not None:
            delta = new_val - base_val
            pct_change = (delta / base_val * 100) if base_val != 0 else 0
            
            improvements[metric] = {
                "baseline": base_val,
                "new": new_val,
                "delta": delta,
                "percent_change": pct_change,
                "improved": delta > 0
            }
    
    # Overall verdict
    improved_count = sum(1 for imp in improvements.values() if imp["improved"])
    total_count = len(improvements)
    
    result = {
        "baseline_id": baseline_id,
        "new_id": new_id,
        "improvements": improvements,
        "summary": f"{improved_count}/{total_count} metrics improved",
        "overall_better": improved_count > total_count / 2
    }
    
    logger.info(
        f"Improvement analysis: {improved_count}/{total_count} metrics improved"
    )
    return result


def create_timeline_chart(
    metric_name: str,
    algorithm_type: Optional[str] = None
) -> Any:
    """
    Create matplotlib line chart showing metric evolution over time.
    
    WHY: Timeline visualization shows learning progress - are we improving?
         Plateaus indicate need for new strategies.
    
    WIP: Implement actual matplotlib figure generation.
    WHY: Need to create interactive, informative timeline visualization.
    
    Args:
        metric_name: Metric to plot
        algorithm_type: Optional algorithm filter
        
    Returns:
        Matplotlib figure object
    """
    # WIP: Create actual matplotlib figure
    # Steps needed:
    # 1. Get timeline data with timeline_manager
    # 2. Extract metric values and timestamps
    # 3. Create line plot with markers
    # 4. Add annotations for best/worst points
    # 5. Add trend line
    # 6. Style for readability
    
    logger.info(f"Creating timeline chart for {metric_name} (WIP)")
    
    return {
        "type": "line_chart",
        "x_axis": "Timestamp (chronological)",
        "y_axis": f"{metric_name} value",
        "markers": "Points for each experiment",
        "annotations": "Label best/worst experiments",
        "trend_line": "Linear regression showing improvement direction",
        "why": "Shows if we're making progress or stuck in local optimum"
    }


# Module metadata
__version__ = "1.0.0"
__capabilities__ = ["metric_comparison", "parameter_diff", "improvement_calc", "timeline_viz"]

