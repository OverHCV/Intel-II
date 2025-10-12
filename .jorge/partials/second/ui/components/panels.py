"""
Panel Components - Layout utilities
"""

import streamlit as st
from typing import Callable, Any


def TwoColumnLayout(
    left_content: Callable[[], Any],
    right_content: Callable[[], Any],
    ratio: list[int] = None,
):
    """
    Two-column layout component (React-like)
    
    Args:
        left_content: Function to render in left column
        right_content: Function to render in right column
        ratio: Column width ratio [left, right]. Default [2, 1]
    """
    if ratio is None:
        ratio = [2, 1]
    
    col_left, col_right = st.columns(ratio)
    
    with col_left:
        left_content()
    
    with col_right:
        right_content()


def VerticalSeparator(height: int = 20):
    """Add vertical space between sections"""
    st.markdown(f"<div style='height: {height}px'></div>", unsafe_allow_html=True)


def HorizontalDivider(text: str = None):
    """Add horizontal divider with optional text"""
    if text:
        st.divider()
        st.markdown(f"**{text}**")
    else:
        st.divider()

