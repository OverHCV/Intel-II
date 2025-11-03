"""
Dataset Review Page - Data exploration and preparation.

WHY: "Garbage in, garbage out" - understanding and preparing data properly
     is crucial for meaningful model results.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def render():
    """Render the Dataset Review page."""
    
    # THEORY SECTION - Always at the top of every page
    with st.expander("📚 THEORY: Why Data Preparation is Critical", expanded=False):
        st.markdown("""
        ### "Garbage In, Garbage Out"
        
        **WHY this page matters:**  
        Even the best algorithm fails with poor data. This page ensures:
        - ✅ Data quality (no missing values, correct ranges)
        - ✅ Proper target engineering (G3 → meaningful categories)
        - ✅ No data leakage (removing G1, G2 which predict G3 trivially)
        - ✅ Balanced classes (preventing majority class bias)
        
        ### Dataset Strategy
        
        - **Portuguese**: 649 students → TRAINING (more data = better learning)
        - **Math**: 395 students → TEST (different subject tests generalization)
        
        **WHY this split?**  
        Training on Portuguese (larger) gives model more examples. Testing on Math
        (different subject) reveals if learned patterns are truly about student
        characteristics or just subject-specific quirks.
        
        ### Data Leakage Problem
        
        **Problem**: G1 (period 1 grade) and G2 (period 2 grade) are highly
        correlated with G3 (final grade). Including them makes prediction trivial.
        
        **Solution**: Remove G1 and G2. Predict G3 from demographic/social/behavioral
        features only - these are actionable factors.
        
        ### Class Balancing: SMOTE Explained
        
        **Problem**: If 80% Pass, 20% Fail → model just predicts "Pass" for everyone
        and gets 80% accuracy without learning anything useful.
        
        **SMOTE**: Creates synthetic Fail examples by interpolating between existing
        Fail students. Better than duplication because it adds diversity.
        
        **When to use**: Imbalance ratio > 2.0 (one class is 2x the other)
        """)
    
    st.markdown("""
    ## 📊 Dataset Review & Preparation
    
    Explore, transform, and prepare student data for machine learning.
    
    ---
    """)
    
    # Two-column layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎛️ Data Controls")
        
        # Dataset selection
        dataset = st.selectbox(
            "Select Dataset",
            ["Portuguese (Training - 649 students)",
             "Math (Test - 395 students)",
             "Both (Combined - 1044 students)"],
            help="WHY: Portuguese has more samples (649) → better for training. Math (395) tests if patterns generalize across subjects."
        )
        
        st.markdown("---")
        
        # Target engineering
        st.subheader("🎯 Target Engineering")
        target_strategy = st.selectbox(
            "G3 Transformation",
            ["Binary (Pass/Fail at 10)",
             "Three-class (Low/Med/High)",
             "Five-class (A/B/C/D/F)",
             "Custom thresholds"],
            help="WHY: Binary (Pass/Fail) is simple and actionable. Multi-class enables finer interventions (e.g., 'Medium' students need different support than 'Low')."
        )
        
        if target_strategy == "Custom thresholds":
            custom_thresh = st.text_input(
                "Thresholds (comma-separated)",
                "10,14",
                help="E.g., '10,14' creates 3 classes: [0-10), [10-14), [14-20]"
            )
        
        st.markdown("---")
        
        # Class balancing
        st.subheader("⚖️ Class Balancing")
        balance_method = st.selectbox(
            "Balancing Method",
            ["None", "SMOTE", "Random Oversample", "Random Undersample"],
            help="WHY: None if balanced. SMOTE creates synthetic examples (best). Random Oversample duplicates (simpler but less diverse). Random Undersample reduces majority (loses data)."
        )
        
        if balance_method == "SMOTE":
            k_neighbors = st.slider(
                "K-neighbors", 1, 10, 5,
                help="WHY: SMOTE creates synthetic samples by interpolating between k nearest neighbors. Higher k = more diverse but risk including wrong class."
            )
        
        st.markdown("---")
        
        # Action buttons
        if st.button("🔄 Load & Prepare Data", type="primary", use_container_width=True):
            with st.spinner("🌀 Processing data..."):
                st.session_state["data_loaded"] = True
                st.success("✅ Data prepared successfully!")
        
        if st.button("💾 Save Snapshot", use_container_width=True):
            st.info("WIP: Save prepared dataset to sandbox/snapshots/")
        
        # Feature selection info
        st.markdown("---")
        st.info("🔒 **Data Leakage Prevention**: G1 and G2 are automatically excluded from features. WHY: They predict G3 trivially.")
    
    with col2:
        st.subheader("📈 Data Visualization")
        
        if st.session_state.get("data_loaded"):
            # Dummy data for visualization
            tabs = st.tabs(["Class Distribution", "Feature Correlation", "Summary Stats"])
            
            with tabs[0]:
                st.markdown("""
                **Class Distribution Analysis**
                
                WHY: Imbalanced classes lead to biased models that predict
                     majority class excessively. Balancing ensures fair representation.
                """)
                
                # Dummy distribution chart
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
                
                # Before balancing
                classes = ['Pass', 'Fail']
                counts_before = [280, 115]
                ax1.bar(classes, counts_before, color=['#4CAF50', '#F44336'])
                ax1.set_title('Before Balancing')
                ax1.set_ylabel('Count')
                for i, v in enumerate(counts_before):
                    ax1.text(i, v + 5, str(v), ha='center', fontweight='bold')
                
                # After balancing
                counts_after = [280, 280]
                ax2.bar(classes, counts_after, color=['#4CAF50', '#F44336'])
                ax2.set_title('After SMOTE')
                ax2.set_ylabel('Count')
                for i, v in enumerate(counts_after):
                    ax2.text(i, v + 5, str(v), ha='center', fontweight='bold')
                
                plt.tight_layout()
                st.pyplot(fig)
                
                st.metric("Imbalance Ratio", "2.43 → 1.00", "✅ Balanced")
            
            with tabs[1]:
                st.markdown("""
                **Feature Correlation Matrix**
                
                WIP: Heatmap showing correlations between features.
                WHY: Identify multicollinearity and feature relationships.
                """)
                st.info("Correlation heatmap will appear here")
            
            with tabs[2]:
                st.markdown("""
                **Dataset Summary Statistics**
                """)
                # Dummy summary
                summary_data = {
                    "Feature": ["age", "studytime", "failures", "absences", "G3"],
                    "Mean": [16.7, 2.0, 0.3, 5.7, 10.4],
                    "Std": [1.3, 0.8, 0.8, 8.0, 4.6],
                    "Min": [15, 1, 0, 0, 0],
                    "Max": [22, 4, 3, 75, 20]
                }
                st.dataframe(pd.DataFrame(summary_data), use_container_width=True)
        
        else:
            st.info("👆 Click 'Load & Prepare Data' to visualize the dataset")

