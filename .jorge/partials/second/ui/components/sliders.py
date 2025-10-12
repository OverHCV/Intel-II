"""
Slider and Selector Components - Interactive controls
"""

from typing import Any, List, Union
    
import streamlit as st


def NumericSlider(
    label: str,
    min_value: float,
    max_value: float,
    default_value: float = None,
    step: float = None,
    key: str = None,
    log_scale: bool = False,
    help_text: str = None,
) -> float:
    """
    Numeric slider component

    Args:
        label: Slider label
        min_value: Minimum value
        max_value: Maximum value
        default_value: Starting value
        step: Step size
        key: Unique key for state management
        log_scale: If True, use logarithmic scale
        help_text: Help tooltip

    Returns:
        Selected value
    """
    if default_value is None:
        default_value = (min_value + max_value) / 2

    if log_scale:
        import numpy as np

        log_min = np.log10(min_value)
        log_max = np.log10(max_value)
        log_default = np.log10(default_value)

        log_value = st.slider(
            label,
            min_value=log_min,
            max_value=log_max,
            value=log_default,
            key=key,
            help=help_text,
            format="%.2f",
        )

        value = 10**log_value
        st.caption(f"Value: {value:.4f}")
        return value
    else:
        return st.slider(
            label,
            min_value=min_value,
            max_value=max_value,
            value=default_value,
            step=step,
            key=key,
            help=help_text,
        )


def DiscreteSlider(
    label: str,
    min_value: int,
    max_value: int,
    default_value: int = None,
    key: str = None,
    help_text: str = None,
) -> int:
    """
    Discrete integer slider component

    Args:
        label: Slider label
        min_value: Minimum value
        max_value: Maximum value
        default_value: Starting value
        key: Unique key
        help_text: Help tooltip

    Returns:
        Selected integer value
    """
    if default_value is None:
        default_value = (min_value + max_value) // 2

    return st.slider(
        label,
        min_value=min_value,
        max_value=max_value,
        value=default_value,
        step=1,
        key=key,
        help=help_text,
    )


def Selector(
    label: str,
    options: List[Any],
    default_index: int = 0,
    key: str = None,
    help_text: str = None,
    format_func: callable = None,
) -> Any:
    """
    Dropdown selector component

    Args:
        label: Selector label
        options: List of options
        default_index: Index of default option
        key: Unique key
        help_text: Help tooltip
        format_func: Function to format option display

    Returns:
        Selected option
    """
    kwargs = {
        "label": label,
        "options": options,
        "index": default_index,
        "key": key,
        "help": help_text,
    }

    # Only pass format_func if provided (avoid passing None)
    if format_func is not None:
        kwargs["format_func"] = format_func

    return st.selectbox(**kwargs)


def MultiSelector(
    label: str,
    options: List[Any],
    default: List[Any] = None,
    key: str = None,
    help_text: str = None,
) -> List[Any]:
    """
    Multi-select component

    Args:
        label: Selector label
        options: List of options
        default: Default selected options
        key: Unique key
        help_text: Help tooltip

    Returns:
        List of selected options
    """
    if default is None:
        default = []

    return st.multiselect(
        label,
        options=options,
        default=default,
        key=key,
        help=help_text,
    )
