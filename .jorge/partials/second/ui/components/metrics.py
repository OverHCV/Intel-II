"""
Metrics Display Components - Show performance metrics
"""

import streamlit as st
from typing import Dict, Optional


def MetricCard(
    label: str,
    value: float,
    delta: Optional[float] = None,
    icon: str = "",
    format_string: str = "{:.4f}",
):
    """
    Single metric card component
    
    Args:
        label: Metric label
        value: Metric value
        delta: Change from previous (optional)
        icon: Emoji icon (optional)
        format_string: Format for value display
    """
    display_label = f"{icon} {label}" if icon else label
    formatted_value = format_string.format(value)
    
    if delta is not None:
        delta_formatted = format_string.format(delta)
        st.metric(label=display_label, value=formatted_value, delta=delta_formatted)
    else:
        st.metric(label=display_label, value=formatted_value)


def MetricsGrid(
    metrics: Dict[str, float],
    icons: Dict[str, str] = None,
    columns: int = 2,
    format_string: str = "{:.4f}",
):
    """
    Grid of metric cards
    
    Args:
        metrics: Dictionary of metric_name: value
        icons: Dictionary of metric_name: icon
        columns: Number of columns in grid
        format_string: Format for value display
    """
    if icons is None:
        icons = {}
    
    metric_items = list(metrics.items())
    cols = st.columns(columns)
    
    for idx, (name, value) in enumerate(metric_items):
        col_idx = idx % columns
        with cols[col_idx]:
            icon = icons.get(name, "")
            MetricCard(name, value, icon=icon, format_string=format_string)


def TrainingStatus(is_training: bool, message: str = "Training in progress..."):
    """
    Show training status indicator
    
    Args:
        is_training: Whether model is currently training
        message: Status message
    """
    if is_training:
        st.info(f"⏳ {message}")
    else:
        st.success("✅ Ready")

