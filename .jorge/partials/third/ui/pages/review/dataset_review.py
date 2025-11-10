"""
Dataset Review Page - Orchestrator.

Single Responsibility: Coordinate theory, controls, processing, and visualizations.

Refactored from 388 LOC monolith into modular components:
- theory.py: Educational content (40 LOC)
- controls.py: UI controls (150 LOC)
- processor.py: Data processing (130 LOC)
- visualizations.py: Plots and tables (180 LOC)
- dataset_review.py: Orchestration (60 LOC) ← YOU ARE HERE

Total: ~560 LOC across 5 files vs 388 LOC in 1 file
Benefit: Each file has single responsibility, < 200 LOC, easily testable
"""

import streamlit as st
import logging

from .theory import render_theory_section
from .controls import render_controls
from .processor import process_data
from .visualizations import render_visualizations
from states import get_state, set_state, StateKeys

logger = logging.getLogger(__name__)


def render():
    """
    Orchestrate the Dataset Review page.
    
    Flow:
    1. Render theory expander
    2. Render controls (left column) and get user selections
    3. Process data based on selections
    4. Render visualizations (right column)
    """
    # 1. Theory section (top of page)
    render_theory_section()
    
    st.markdown("""
    ## 📊 Dataset Review & Preparation
    
    Explore, transform, and prepare student data for machine learning.
    
    ---
    """)
    
    # 2. Two-column layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Render controls and get user selections
        user_selections = render_controls()
    
    with col2:
        # Process data and render visualizations
        X_viz = get_state(StateKeys.X_PREPARED, None)
        y_viz = get_state(StateKeys.Y_PREPARED, None)
        
        # Check if current parameters match stored ones
        stored_params = get_state("dataset_review_params", {})
        current_params = {
            'dataset': user_selections['dataset'],
            'target_strategy': user_selections['target_strategy'],
            'include_g1': user_selections['include_g1'],
            'include_g2': user_selections['include_g2'],
            'balance_method': user_selections['balance_method'],
            'k_neighbors': user_selections['k_neighbors']
        }
        
        params_changed = (stored_params != current_params)
        
        # Auto-process data when selections change OR data doesn't exist
        process_needed = (
            X_viz is None or 
            y_viz is None or 
            params_changed or
            not get_state("data_loaded", False)
        )
        
        if process_needed:
            with st.spinner("🌀 Processing data..."):
                try:
                    X_final, y_final, df_raw = process_data(user_selections)
                    
                    # Store current params
                    set_state("dataset_review_params", current_params)
                    
                    st.success(f"✅ Data prepared: {X_final.shape[0]} samples, {X_final.shape[1]} features!")
                    
                    # Render visualizations with fresh data
                    render_visualizations(X_final, y_final, user_selections['balance_method'])
                    
                except Exception as e:
                    st.error(f"❌ Error preparing data: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
                    logger.exception("Data processing failed")
        else:
            # Data already processed, just render visualizations
            render_visualizations(X_viz, y_viz, user_selections['balance_method'])
