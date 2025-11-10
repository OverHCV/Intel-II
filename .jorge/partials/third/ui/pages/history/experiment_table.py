"""Interactive experiment table with filters and sorting."""
import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime


def render_experiment_table(experiments: List[Dict[str, Any]]) -> Optional[List[str]]:
    """
    Render interactive table of experiments with selection capability.
    
    Args:
        experiments: List of experiment metadata dictionaries
        
    Returns:
        List of selected version_ids for comparison
    """
    if not experiments:
        st.info("📭 No experiments recorded yet.")
        return None
    
    st.subheader("📋 Experiment Table")
    
    # Convert to DataFrame
    df = pd.DataFrame(experiments)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Filters in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        algo_filter = st.multiselect(
            "🔍 Filter by Algorithm",
            options=df['algorithm_type'].unique().tolist(),
            default=df['algorithm_type'].unique().tolist()
        )
    
    with col2:
        date_range = st.date_input(
            "📅 Date Range",
            value=(df['timestamp'].min(), df['timestamp'].max()),
            max_value=datetime.now()
        )
    
    with col3:
        sort_by = st.selectbox(
            "📊 Sort By",
            options=['Newest First', 'Oldest First', 'Algorithm Type'],
            index=0
        )
    
    # Apply filters
    filtered_df = df[df['algorithm_type'].isin(algo_filter)]
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['timestamp'].dt.date >= start_date) &
            (filtered_df['timestamp'].dt.date <= end_date)
        ]
    
    # Apply sorting
    if sort_by == 'Newest First':
        filtered_df = filtered_df.sort_values('timestamp', ascending=False)
    elif sort_by == 'Oldest First':
        filtered_df = filtered_df.sort_values('timestamp', ascending=True)
    else:
        filtered_df = filtered_df.sort_values(['algorithm_type', 'timestamp'], ascending=[True, False])
    
    # Format for display
    display_df = filtered_df.copy()
    display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    display_df['algorithm'] = display_df['algorithm_type'].str.replace('_', ' ').str.title()
    
    # Extract key metrics (depends on algorithm type)
    display_df['key_metric'] = display_df.apply(_extract_key_metric, axis=1)
    
    # Select columns for display
    display_columns = ['version_id', 'algorithm', 'timestamp', 'key_metric']
    
    # Add checkbox column for comparison
    st.caption("💡 Select experiments to compare (max 5)")
    
    # Use session state to track selections
    if 'selected_exp_ids' not in st.session_state:
        st.session_state.selected_exp_ids = []
    
    # Display table with checkboxes
    for idx, row in display_df.iterrows():
        cols = st.columns([0.5, 2, 2, 3, 2])
        
        with cols[0]:
            is_selected = row['version_id'] in st.session_state.selected_exp_ids
            if st.checkbox("", value=is_selected, key=f"exp_{row['version_id']}"):
                if row['version_id'] not in st.session_state.selected_exp_ids:
                    if len(st.session_state.selected_exp_ids) < 5:
                        st.session_state.selected_exp_ids.append(row['version_id'])
            else:
                if row['version_id'] in st.session_state.selected_exp_ids:
                    st.session_state.selected_exp_ids.remove(row['version_id'])
        
        with cols[1]:
            st.text(row['algorithm'])
        
        with cols[2]:
            st.text(row['timestamp'])
        
        with cols[3]:
            st.text(row['key_metric'])
        
        with cols[4]:
            # Action buttons
            if st.button("🗑️", key=f"del_{row['version_id']}", help="Delete experiment"):
                st.session_state[f'confirm_delete_{row["version_id"]}'] = True
                st.rerun()
    
    st.caption(f"Showing {len(display_df)} of {len(df)} experiments")
    
    return st.session_state.selected_exp_ids if st.session_state.selected_exp_ids else None


def _extract_key_metric(row: pd.Series) -> str:
    """
    Extract the most relevant metric for each algorithm type.
    
    Args:
        row: DataFrame row with experiment data
        
    Returns:
        Formatted string with key metric
    """
    metrics = row.get('metrics', {})
    algo = row['algorithm_type']
    
    if algo == 'decision_tree':
        acc = metrics.get('accuracy', 0)
        f1 = metrics.get('f1', 0)
        return f"Acc: {acc:.3f}, F1: {f1:.3f}"
    
    elif algo == 'hierarchical':
        silhouette = metrics.get('silhouette_avg', 0)
        j4 = metrics.get('fisher_j4', 0)
        k = metrics.get('n_clusters', 'N/A')
        return f"K={k}, Sil: {silhouette:.3f}, J4: {j4:.3f}"
    
    elif algo == 'kmeans':
        silhouette = metrics.get('silhouette_avg', 0)
        inertia = metrics.get('inertia', 0)
        k = metrics.get('n_clusters', 'N/A')
        return f"K={k}, Sil: {silhouette:.3f}, Inertia: {inertia:.1f}"
    
    return "N/A"

