"""Experiment management utilities (delete, export, etc.)."""
import streamlit as st
from typing import List, Dict, Any
from versioning.experiment_store import delete_experiment, SANDBOX_DIR
import logging

logger = logging.getLogger(__name__)


def render_management_section(experiments: List[Dict[str, Any]]) -> bool:
    """
    Render experiment management controls.
    
    Args:
        experiments: List of all experiments
        
    Returns:
        True if any experiment was deleted (triggers refresh)
    """
    if not experiments:
        return False
    
    st.subheader("🗑️ Experiment Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💾 Total Experiments", len(experiments))
    
    with col2:
        total_size = _calculate_storage_size()
        st.metric("📦 Storage Used", f"{total_size:.2f} MB")
    
    with col3:
        if st.button("🗑️ Clear All Experiments", type="secondary"):
            st.session_state['confirm_clear_all'] = True
    
    # Confirmation dialog for clear all
    if st.session_state.get('confirm_clear_all', False):
        st.warning("⚠️ Are you sure? This will delete ALL experiments permanently!")
        
        col_confirm, col_cancel = st.columns(2)
        
        with col_confirm:
            if st.button("✅ Yes, Delete All", type="primary"):
                _delete_all_experiments(experiments)
                st.session_state['confirm_clear_all'] = False
                st.success("✅ All experiments deleted!")
                st.rerun()
        
        with col_cancel:
            if st.button("❌ Cancel"):
                st.session_state['confirm_clear_all'] = False
                st.rerun()
    
    # Individual deletion confirmations
    deleted_any = False
    for exp in experiments:
        confirm_key = f'confirm_delete_{exp["version_id"]}'
        if st.session_state.get(confirm_key, False):
            st.warning(f"⚠️ Delete experiment: {exp['version_id'][:20]}...?")
            
            col_yes, col_no = st.columns(2)
            
            with col_yes:
                if st.button("✅ Confirm", key=f"yes_{exp['version_id']}"):
                    success = delete_experiment(exp['version_id'], exp['algorithm_type'])
                    if success:
                        st.success(f"✅ Deleted {exp['version_id'][:20]}...")
                        deleted_any = True
                    else:
                        st.error("❌ Failed to delete experiment")
                    st.session_state[confirm_key] = False
                    st.rerun()
            
            with col_no:
                if st.button("❌ Cancel", key=f"no_{exp['version_id']}"):
                    st.session_state[confirm_key] = False
                    st.rerun()
    
    return deleted_any


def _calculate_storage_size() -> float:
    """
    Calculate total storage used by experiments.
    
    Returns:
        Size in MB
    """
    import os
    
    if not SANDBOX_DIR.exists():
        return 0.0
    
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(SANDBOX_DIR):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(filepath)
            except OSError:
                pass
    
    return total_size / (1024 * 1024)


def _delete_all_experiments(experiments: List[Dict[str, Any]]) -> None:
    """
    Delete all experiments.
    
    Args:
        experiments: List of all experiments
    """
    for exp in experiments:
        try:
            delete_experiment(exp['version_id'], exp['algorithm_type'])
        except Exception as e:
            logger.error(f"Failed to delete {exp['version_id']}: {e}")
    
    logger.info("Deleted all experiments")

