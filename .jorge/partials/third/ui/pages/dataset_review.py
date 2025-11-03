"""
Dataset Review Page - Data exploration and preparation.

WHY: "Garbage in, garbage out" - understanding and preparing data properly
     is crucial for meaningful model results.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging

# ALL IMPORTS AT TOP - NO LAZY IMPORTS!
from data.loader import load_dataset
from data.transformer import engineer_target, remove_leakage_features, split_features_target
from data.preprocessor import encode_categorical, scale_numerical
from data.balancer import balance_classes
from ui.state_manager import get_state, set_state, StateKeys

logger = logging.getLogger(__name__)


def render():
    """Render the Dataset Review page."""
    
    # THEORY FIRST - As requested
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
            ["Five-class (A/B/C/D/F)",
            "Binary (Pass/Fail at 10)",
             "Three-class (Low/Med/High)",
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
            ["SMOTE", "None", "Random Oversample", "Random Undersample"],
            help="WHY: SMOTE (default) creates synthetic examples (best for imbalanced data). None if already balanced. Random Oversample duplicates. Random Undersample loses data."
        )
        
        if balance_method == "SMOTE":
            k_neighbors = st.slider(
                "K-neighbors", 1, 10, 5,
                help="WHY: SMOTE creates synthetic samples by interpolating between k nearest neighbors. Higher k = more diverse but risk including wrong class."
            )
        
        st.markdown("---")
        
        # Action button - ALWAYS process when parameters change
        # Auto-trigger processing
        process_data = True  # Always process on page load
        
        if process_data:
            with st.spinner("🌀 Processing data..."):
                try:
                    # All imports are at the top now!
                    
                    # 1. Load dataset
                    dataset_choice = dataset.split(" ")[0].lower()  # "Portuguese" or "Math"
                    df_raw = load_dataset(dataset_choice)
                    
                    # 2. Engineer target
                    target_type = target_strategy.split(" ")[0].lower()  # "binary", "three-class", etc.
                    target_map = {
                        "binary": "binary",
                        "three-class": "three_class",
                        "five-class": "five_class"
                    }
                    y = engineer_target(df_raw, target_map.get(target_type, "binary"))
                    
                    # 3. Remove leakage features
                    df_clean = remove_leakage_features(df_raw)
                    
                    # 4. Split X and y
                    X, _ = split_features_target(df_clean.assign(target=y), "target")
                    
                    # 5. Encode categorical
                    X_encoded, encoders = encode_categorical(X, method="label")
                    
                    # 6. Scale numerical
                    X_scaled, scalers = scale_numerical(X_encoded, method="standard")
                    
                    # 7. Apply balancing
                    balance_map = {
                        "SMOTE": "smote",
                        "None": "none",
                        "Random Oversample": "random_over",
                        "Random Undersample": "random_under"
                    }
                    X_final, y_final = balance_classes(
                        X_scaled, y,
                        method=balance_map[balance_method],
                        random_state=42
                    )
                    
                    # Store in session state
                    set_state(StateKeys.RAW_DATA, df_raw)
                    set_state(StateKeys.X_PREPARED, X_final)
                    set_state(StateKeys.Y_PREPARED, y_final)
                    set_state(StateKeys.DATASET_NAME, dataset.split(" ")[0])
                    set_state(StateKeys.TARGET_STRATEGY, target_strategy.split(" ")[0])
                    set_state(StateKeys.BALANCE_METHOD, balance_method)
                    
                    st.session_state["data_loaded"] = True
                    st.success(f"✅ Data prepared: {X_final.shape[0]} samples, {X_final.shape[1]} features!")
                    
                except Exception as e:
                    st.error(f"❌ Error preparing data: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
        
        # Feature selection info
        st.markdown("---")
        st.info("🔒 **Data Leakage Prevention**: G1 and G2 are automatically excluded from features. WHY: They predict G3 trivially.")
    
    with col2:
        st.subheader("📈 Data Visualization")
        
        X_viz = get_state(StateKeys.X_PREPARED, None)
        y_viz = get_state(StateKeys.Y_PREPARED, None)
        
        if X_viz is not None and y_viz is not None:
            # REAL data visualization
            tabs = st.tabs(["Class Distribution", "Feature Correlation", "Summary Stats"])
            
            with tabs[0]:
                # REAL Class distribution
                fig, ax = plt.subplots(figsize=(8, 5))
                unique, counts = np.unique(y_viz, return_counts=True)
                colors = plt.cm.Set3(np.linspace(0, 1, len(unique)))
                ax.bar([f"Class {u}" for u in unique], counts, color=colors)
                ax.set_ylabel("Number of Students")
                ax.set_title(f"Class Distribution (After {balance_method})")
                ax.set_ylim(0, max(counts) * 1.2)
                
                # Add count labels
                for i, v in enumerate(counts):
                    ax.text(i, v + max(counts)*0.02, str(v), ha='center', fontweight='bold')
                
                st.pyplot(fig)
                plt.close()
                
                imbalance_ratio = max(counts) / min(counts) if len(counts) > 1 else 1.0
                st.caption(f"Imbalance ratio: {imbalance_ratio:.2f}. WHY: Ratio > 2.0 means one class dominates → model bias")
            
            with tabs[1]:
                # REAL Correlation heatmap
                st.markdown("#### 🔥 Feature Correlation Matrix")
                
                # Compute correlation
                corr_matrix = pd.DataFrame(X_viz).corr()
                
                # Plot heatmap
                fig_corr, ax_corr = plt.subplots(figsize=(12, 10))
                im = ax_corr.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1, aspect='auto')
                
                # Add colorbar
                cbar = plt.colorbar(im, ax=ax_corr)
                cbar.set_label("Correlation Coefficient", rotation=270, labelpad=20)
                
                # Set ticks (show every 5th feature to avoid clutter)
                n_features = corr_matrix.shape[0]
                tick_positions = list(range(0, n_features, max(1, n_features // 10)))
                ax_corr.set_xticks(tick_positions)
                ax_corr.set_yticks(tick_positions)
                ax_corr.set_xticklabels([f"F{i}" for i in tick_positions], rotation=45)
                ax_corr.set_yticklabels([f"F{i}" for i in tick_positions])
                
                ax_corr.set_title("Feature Correlation Heatmap", fontsize=14, pad=20)
                plt.tight_layout()
                st.pyplot(fig_corr)
                plt.close()
                
                st.caption("💡 Red = positive correlation, Blue = negative. Dark colors = strong correlation. WHY: High correlation (>0.9) = redundant features.")
                
                # Show top correlations
                corr_pairs = []
                for i in range(n_features):
                    for j in range(i+1, n_features):
                        corr_pairs.append((i, j, abs(corr_matrix.iloc[i, j])))
                corr_pairs.sort(key=lambda x: x[2], reverse=True)
                
                if corr_pairs:
                    st.markdown("**Top 5 Correlated Feature Pairs:**")
                    for i, j, corr in corr_pairs[:5]:
                        st.text(f"Feature {i} ⋈ Feature {j}: {corr:.3f}")
            
            with tabs[2]:
                # REAL Summary statistics
                st.markdown("#### 📊 Feature Statistics")
                df_stats = pd.DataFrame(X_viz)
                summary = df_stats.describe().T
                summary['Feature'] = [f"Feature_{i}" for i in range(len(summary))]
                summary = summary[['Feature', 'mean', 'std', 'min', 'max']]
                summary.columns = ['Feature', 'Mean', 'Std Dev', 'Min', 'Max']
                st.dataframe(summary, use_container_width=True, height=400)
        
        else:
            st.info("Processing data... Visualizations will appear automatically")

