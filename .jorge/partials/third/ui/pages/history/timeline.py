"""Timeline visualization for experiment history."""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from typing import List, Dict, Any
import numpy as np


def render_timeline(experiments: List[Dict[str, Any]]) -> None:
    """
    Render interactive timeline chart showing experiments over time.
    
    Args:
        experiments: List of experiment metadata dictionaries
    """
    if not experiments:
        st.info("📭 No experiments yet. Train some models first!")
        return
    
    st.subheader("📈 Experiment Timeline")
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(experiments)
    
    # Parse timestamps
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    
    # Color map for algorithms
    algo_colors = {
        'decision_tree': '#FF6B6B',
        'hierarchical': '#4ECDC4',
        'kmeans': '#95E1D3'
    }
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Plot 1: Experiments over time (scatter)
    for algo in df['algorithm_type'].unique():
        algo_df = df[df['algorithm_type'] == algo]
        ax1.scatter(
            algo_df['timestamp'],
            [algo] * len(algo_df),
            c=algo_colors.get(algo, '#999'),
            s=100,
            alpha=0.6,
            label=algo.replace('_', ' ').title()
        )
    
    ax1.set_ylabel('Algorithm Type')
    ax1.set_xlabel('Time')
    ax1.legend(loc='upper left')
    ax1.set_title('Experiments Timeline', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Plot 2: Experiments per day (bar chart)
    daily_counts = df.groupby(['date', 'algorithm_type']).size().unstack(fill_value=0)
    
    daily_counts.plot(
        kind='bar',
        stacked=True,
        ax=ax2,
        color=[algo_colors.get(col, '#999') for col in daily_counts.columns],
        alpha=0.7
    )
    
    ax2.set_ylabel('Number of Experiments')
    ax2.set_xlabel('Date')
    ax2.set_title('Daily Experiment Count', fontsize=14, fontweight='bold')
    ax2.legend(title='Algorithm', loc='upper left')
    ax2.grid(True, alpha=0.3, axis='y')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Experiments", len(experiments))
    
    with col2:
        dt_count = len(df[df['algorithm_type'] == 'decision_tree'])
        st.metric("🌳 Decision Trees", dt_count)
    
    with col3:
        hc_count = len(df[df['algorithm_type'] == 'hierarchical'])
        st.metric("🌲 Hierarchical", hc_count)
    
    with col4:
        km_count = len(df[df['algorithm_type'] == 'kmeans'])
        st.metric("🎯 K-means", km_count)

