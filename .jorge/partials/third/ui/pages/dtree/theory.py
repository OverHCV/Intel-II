"""
Theory content for Decision Tree page.

Single Responsibility: Render educational content explaining CART algorithm.
"""

import streamlit as st


def render_theory_section():
    """
    Render theory expander with educational content about Decision Trees.
    
    Returns:
        None (renders directly to Streamlit)
    """
    with st.expander("📚 THEORY: Decision Trees & Rule Extraction", expanded=False):
        st.markdown("""
        ### What are Decision Trees?
        
        **CART (Classification and Regression Trees)**: Creates a tree structure
        where each internal node tests a feature, each branch represents the test
        outcome, and each leaf assigns a class label.
        
        ### Why Decision Trees for Education?
        
        - **Interpretable**: Can be converted to IF-THEN rules
        - **No assumptions**: Works with any data distribution
        - **Non-linear**: Captures complex student patterns
        - **Feature importance**: Shows which factors matter most
        
        ### Rule Extraction
        
        Each path from root to leaf = one decision rule:
        ```
        IF failures > 0 AND studytime <= 2 THEN Fail
        ```
        
        **Why useful?** Teachers can understand and act on these rules.
        
        ### Hyperparameters
        
        - **max_depth**: Limits tree height (prevents overfitting)
        - **min_samples_split**: Min samples to split a node (controls granularity)
        - **criterion**: gini (default) or entropy (information gain)
        
        **Overfitting risk**: Deep trees memorize training data → poor generalization.
        **Solution**: Cross-validation to find optimal depth.
        """)

