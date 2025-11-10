"""
Experiment History Page - Timeline, Table, Comparison, and Management.

This page provides a comprehensive view of all experiments conducted across
all algorithms (Decision Trees, Hierarchical Clustering, K-means).
"""
import streamlit as st
from versioning.experiment_store import list_experiments
from ui.pages.history.timeline import render_timeline
from ui.pages.history.experiment_table import render_experiment_table
from ui.pages.history.comparison import render_comparison
from ui.pages.history.management import render_management_section
import logging

logger = logging.getLogger(__name__)


def render() -> None:
    """Main entry point for Experiment History page."""
    
    st.title("📚 Experiment History")
    st.markdown("""
    Visualize, compare, and manage all your experiments across different algorithms.
    Track your progress and find the best performing models.
    """)
    
    # Load all experiments
    try:
        all_experiments = list_experiments()
    except Exception as e:
        st.error(f"❌ Error loading experiments: {e}")
        logger.error(f"Failed to load experiments: {e}", exc_info=True)
        return
    
    if not all_experiments:
        st.info("""
        📭 **No experiments yet!**
        
        Start training models on the following pages:
        - 🌳 **Decision Trees**: Build classification models
        - 🌲 **Hierarchical Clustering**: Explore hierarchical patterns
        - 🎯 **K-means Clustering**: Find natural groupings
        
        All experiments will be automatically tracked here for comparison and analysis.
        """)
        return
    
    # Section 1: Timeline
    st.markdown("---")
    render_timeline(all_experiments)
    
    # Section 2: Experiment Table (with selection)
    st.markdown("---")
    selected_ids = render_experiment_table(all_experiments)
    
    # Section 3: Comparison Tool
    if selected_ids:
        st.markdown("---")
        render_comparison(selected_ids, all_experiments)
    
    # Section 4: Management
    st.markdown("---")
    deleted = render_management_section(all_experiments)
    
    if deleted:
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.caption("""
    💡 **Tips:**
    - Select experiments in the table to compare them side-by-side
    - Filter by algorithm type or date range to focus your analysis
    - Delete old or failed experiments to keep your workspace clean
    - Use the timeline to track your experimentation velocity
    """)
