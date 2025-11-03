"""
Timeline Manager - Chronological experiment history management.

This module provides functions to view, filter, and analyze experiments
over time, enabling temporal analysis of model improvements.

WHY: Experiments aren't just isolated runs - they're part of a learning
     journey. Timeline view shows what worked, what failed, and trends.
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import logging

from .experiment_store import list_experiments

logger = logging.getLogger(__name__)


def get_timeline(
    algorithm_type: Optional[str] = None,
    limit: int = 50
) -> List[Dict[str, Any]]:
    """
    Get chronologically ordered experiment timeline.
    
    WHY: See the evolution of experiments over time. When did we get
         the breakthrough? Which period had the most exploration?
    
    Args:
        algorithm_type: Filter by algorithm (None = all)
        limit: Maximum experiments to return
        
    Returns:
        List of experiments ordered by timestamp (most recent first)
    """
    experiments = list_experiments(algorithm_type=algorithm_type, limit=limit)
    
    # Already sorted by timestamp in list_experiments
    logger.info(f"Retrieved timeline with {len(experiments)} experiments")
    return experiments


def filter_by_date_range(
    start_date: datetime,
    end_date: datetime,
    algorithm_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Filter experiments by date range.
    
    WHY: "What did we try last week?" or "Show me experiments from
         the optimization phase"
    
    Args:
        start_date: Start of date range
        end_date: End of date range
        algorithm_type: Optional algorithm filter
        
    Returns:
        Filtered list of experiments
    """
    all_experiments = list_experiments(algorithm_type=algorithm_type)
    
    filtered = []
    for exp in all_experiments:
        exp_date = datetime.fromisoformat(exp["timestamp"])
        if start_date <= exp_date <= end_date:
            filtered.append(exp)
    
    logger.info(
        f"Date filter: {len(filtered)} experiments between "
        f"{start_date.date()} and {end_date.date()}"
    )
    return filtered


def filter_by_metric(
    metric_name: str,
    threshold: float,
    comparison: str = "greater",
    algorithm_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Filter experiments by metric threshold.
    
    WHY: "Show me all runs with accuracy > 0.85" to focus on promising
         configurations.
    
    Args:
        metric_name: Name of metric (e.g., "accuracy", "f1_score")
        threshold: Threshold value
        comparison: "greater", "less", or "equal"
        algorithm_type: Optional algorithm filter
        
    Returns:
        Filtered list of experiments
    """
    all_experiments = list_experiments(algorithm_type=algorithm_type)
    
    filtered = []
    for exp in all_experiments:
        metrics = exp.get("metrics", {})
        if metric_name not in metrics:
            continue
            
        value = metrics[metric_name]
        
        if comparison == "greater" and value >= threshold:
            filtered.append(exp)
        elif comparison == "less" and value <= threshold:
            filtered.append(exp)
        elif comparison == "equal" and abs(value - threshold) < 1e-6:
            filtered.append(exp)
    
    logger.info(
        f"Metric filter: {len(filtered)} experiments with "
        f"{metric_name} {comparison} {threshold}"
    )
    return filtered


def get_best_experiment(
    metric_name: str,
    algorithm_type: Optional[str] = None,
    maximize: bool = True
) -> Optional[Dict[str, Any]]:
    """
    Get best experiment by specified metric.
    
    WHY: "What's our best model so far?" - immediate answer.
    
    Args:
        metric_name: Metric to optimize
        algorithm_type: Optional algorithm filter
        maximize: True to maximize metric, False to minimize
        
    Returns:
        Best experiment or None if no experiments found
    """
    all_experiments = list_experiments(algorithm_type=algorithm_type)
    
    # Filter to experiments with this metric
    valid_experiments = [
        exp for exp in all_experiments
        if metric_name in exp.get("metrics", {})
    ]
    
    if not valid_experiments:
        logger.warning(f"No experiments found with metric '{metric_name}'")
        return None
    
    # Find best
    best = max(
        valid_experiments,
        key=lambda x: x["metrics"][metric_name] * (1 if maximize else -1)
    )
    
    logger.info(
        f"Best experiment: {best['version_id']} with "
        f"{metric_name}={best['metrics'][metric_name]:.3f}"
    )
    return best


def get_recent_experiments(
    n: int = 10,
    algorithm_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get N most recent experiments.
    
    WHY: Quick access to latest work without scrolling through history.
    
    Args:
        n: Number of experiments to return
        algorithm_type: Optional algorithm filter
        
    Returns:
        List of N most recent experiments
    """
    return get_timeline(algorithm_type=algorithm_type, limit=n)


def analyze_progress_over_time(
    metric_name: str,
    algorithm_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyze how a metric evolved over time.
    
    WHY: "Are we improving?" - quantify the learning trajectory.
    
    WIP: Calculate trend line, identify plateaus, detect breakthroughs.
    WHY: Need statistical analysis of improvement patterns.
    
    Args:
        metric_name: Metric to analyze
        algorithm_type: Optional algorithm filter
        
    Returns:
        Analysis dictionary with trend info
    """
    experiments = get_timeline(algorithm_type=algorithm_type)
    
    # Extract metric values with timestamps
    data_points = []
    for exp in experiments:
        if metric_name in exp.get("metrics", {}):
            data_points.append({
                "timestamp": exp["timestamp"],
                "value": exp["metrics"][metric_name],
                "version_id": exp["version_id"]
            })
    
    if len(data_points) < 2:
        return {
            "error": "Not enough data points for trend analysis",
            "count": len(data_points)
        }
    
    # WIP: Calculate trend statistics
    values = [dp["value"] for dp in data_points]
    
    analysis = {
        "n_experiments": len(data_points),
        "first_value": values[-1],  # Reversed because sorted recent first
        "last_value": values[0],
        "improvement": values[0] - values[-1],
        "best_value": max(values),
        "worst_value": min(values),
        "mean_value": sum(values) / len(values),
        "trend": "WIP: Linear regression to show improvement rate",
        "plateau_periods": "WIP: Identify periods with no improvement",
        "breakthroughs": "WIP: Detect significant jumps in performance"
    }
    
    logger.info(
        f"Progress analysis: {metric_name} improved by "
        f"{analysis['improvement']:+.3f}"
    )
    return analysis


def group_by_period(
    period: str = "day",
    algorithm_type: Optional[str] = None
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group experiments by time period.
    
    WHY: "What did we try each day this week?" - organize by calendar.
    
    Args:
        period: "day", "week", or "month"
        algorithm_type: Optional algorithm filter
        
    Returns:
        Dictionary mapping period string to experiment list
    """
    experiments = get_timeline(algorithm_type=algorithm_type)
    
    groups = {}
    for exp in experiments:
        exp_date = datetime.fromisoformat(exp["timestamp"])
        
        if period == "day":
            key = exp_date.strftime("%Y-%m-%d")
        elif period == "week":
            key = exp_date.strftime("%Y-W%W")
        elif period == "month":
            key = exp_date.strftime("%Y-%m")
        else:
            key = "unknown"
        
        if key not in groups:
            groups[key] = []
        groups[key].append(exp)
    
    logger.info(f"Grouped into {len(groups)} {period}s")
    return groups


# Module metadata
__version__ = "1.0.0"
__capabilities__ = ["timeline", "filtering", "best_model", "trend_analysis"]

