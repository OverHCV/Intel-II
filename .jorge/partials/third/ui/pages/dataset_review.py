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
from constants.base import FEATURE_DESCRIPTIONS, FEATURE_SHORT_NAMES, get_feature_description

logger = logging.getLogger(__name__)


def render():
    """Render the Dataset Review page."""
    
    # THEORY FIRST - As requested
    with st.expander("📚 TEORÍA: Por qué la Preparación de Datos es Crítica", expanded=False):
        st.markdown("""
        ### "Basura Entra, Basura Sale"
        
        **Importancia de esta página:**  
        Incluso el mejor algoritmo falla con datos pobres. Esta página asegura:
        - ✅ Calidad de datos (sin valores faltantes, rangos correctos)
        - ✅ Ingeniería de target adecuada (G3 → categorías significativas)
        - ✅ Sin fuga de datos (remover G1, G2 que predicen G3 trivialmente)
        - ✅ Clases balanceadas (prevenir sesgo de clase mayoritaria)
        
        ### Estrategia de Datasets
        
        - **Portuguese**: 649 estudiantes → ENTRENAMIENTO (más datos = mejor aprendizaje)
        - **Math**: 395 estudiantes → PRUEBA (materia diferente prueba generalización)
        
        **Razón del split:**  
        Entrenar en Portuguese (más grande) da más ejemplos al modelo. Probar en Math
        (materia diferente) revela si los patrones aprendidos son sobre características
        del estudiante o solo quirks específicos de la materia.
        
        ### Problema de Fuga de Datos
        
        **Problema**: G1 (nota periodo 1) y G2 (nota periodo 2) están altamente
        correlacionadas con G3 (nota final). Incluirlas hace la predicción trivial.
        
        **Solución**: Remover G1 y G2. Predecir G3 solo desde factores demográficos/sociales/
        comportamentales - estos son factores accionables.
        
        ### Balanceo de Clases: SMOTE Explicado
        
        **Problema**: Si 80% Aprueba, 20% Reprueba → modelo solo predice "Aprueba" para todos
        y obtiene 80% accuracy sin aprender nada útil.
        
        **SMOTE**: Crea ejemplos sintéticos de Reprueba interpolando entre estudiantes
        Reprobados existentes. Mejor que duplicación porque agrega diversidad.
        
        **Cuándo usar**: Ratio de desbalance > 2.0 (una clase es 2x la otra)
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
            help="Portuguese tiene más muestras (649) → mejor para entrenamiento. Math (395) prueba si los patrones generalizan entre materias."
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
            help="Binary (Pass/Fail) es simple y accionable. Multi-clase permite intervenciones más finas (e.g., estudiantes 'Medios' necesitan diferente apoyo que 'Bajos')."
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
            help="SMOTE (default) crea ejemplos sintéticos (mejor para datos desbalanceados). None si ya está balanceado. Random Oversample duplica. Random Undersample pierde datos."
        )
        
        if balance_method == "SMOTE":
            k_neighbors = st.slider(
                "K-neighbors", 1, 10, 5,
                help="SMOTE crea muestras sintéticas interpolando entre k vecinos más cercanos. Mayor k = más diversidad pero riesgo de incluir clase incorrecta."
            )
        
        st.markdown("---")
        
        # G1/G2 Inclusion Section - NEW!
        st.subheader("📊 Data Leakage Control (G1/G2)")
        st.warning("⚠️ G1 y G2 predicen G3 casi perfectamente (~90%+ accuracy). Incluirlos causa **data leakage** pero permite ver el impacto.")
        
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            include_g1 = st.checkbox(
                "Include G1 (Nota Periodo 1)", 
                value=False,
                help="Incluir G1 mejora accuracy dramáticamente pero causa data leakage. Útil para comparación experimental."
            )
        with col_g2:
            include_g2 = st.checkbox(
                "Include G2 (Nota Periodo 2)", 
                value=False,
                help="Incluir G2 mejora accuracy dramáticamente pero causa data leakage. Útil para comparación experimental."
            )
        with col_g3:
            if include_g1 or include_g2:
                st.metric("⚠️ Data Leakage", "ACTIVO", delta="Cuidado!")
            else:
                st.metric("✅ Clean Data", "ACTIVO", delta="Sin leakage")
        
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
                    
                    # 3. Remove leakage features (conditional on toggles)
                    features_to_remove = []
                    if not include_g1:
                        features_to_remove.append("G1")
                    if not include_g2:
                        features_to_remove.append("G2")
                    
                    if features_to_remove:
                        df_clean = remove_leakage_features(df_raw, features_to_remove=features_to_remove)
                    else:
                        # Keep all features except dataset_source
                        df_clean = remove_leakage_features(df_raw, features_to_remove=["dataset_source"])
                    
                    # Log what features were removed
                    logger.info(f"Removed features: {features_to_remove if features_to_remove else ['dataset_source only']}")
                    
                    # 4. Split X and y
                    X, _ = split_features_target(df_clean.assign(target=y), "target")
                    
                    # 5. Encode categorical
                    X_encoded, encoders = encode_categorical(X, method="label")
                    
                    # 6. Scale numerical
                    X_scaled, scalers = scale_numerical(X_encoded, method="standard")
                    
                    # 7. Apply balancing (CRITICAL: use the engineered y, not raw!)
                    balance_map = {
                        "SMOTE": "smote",
                        "None": "none",
                        "Random Oversample": "random_over",
                        "Random Undersample": "random_under"
                    }
                    X_final, y_final = balance_classes(
                        X_scaled, y,  # y is the engineered target from step 2
                        method=balance_map[balance_method],
                        random_state=42
                    )
                    
                    # Verify balancing worked
                    logger.info(f"Final shapes after balancing: X={X_final.shape}, y={len(y_final)}")
                    
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
        st.info("🔒 **Prevención Fuga de Datos**: G1 y G2 se excluyen automáticamente. Predicen G3 trivialmente.")
    
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
                st.caption(f"Ratio de desbalance: {imbalance_ratio:.2f}. Si >2.0 una clase domina → sesgo del modelo")
            
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
                
                st.caption("💡 Rojo = correlación positiva, Azul = negativa. Colores oscuros = correlación fuerte. Alta correlación (>0.9) = características redundantes.")
                
                # Show top correlations
                corr_pairs = []
                for i in range(n_features):
                    for j in range(i+1, n_features):
                        corr_pairs.append((i, j, abs(corr_matrix.iloc[i, j])))
                corr_pairs.sort(key=lambda x: x[2], reverse=True)
                
                if corr_pairs:
                    st.markdown("**Top 5 Correlated Feature Pairs:**")
                    # Get actual feature names from raw data
                    raw_df = get_state(StateKeys.RAW_DATA, None)
                    if raw_df is not None:
                        feature_names = list(raw_df.columns)
                        for i, j, corr in corr_pairs[:5]:
                            feat_i = feature_names[i] if i < len(feature_names) else f"F{i}"
                            feat_j = feature_names[j] if j < len(feature_names) else f"F{j}"
                            desc_i = get_feature_description(feat_i)
                            desc_j = get_feature_description(feat_j)
                            st.markdown(f"**{feat_i}** ⋈ **{feat_j}**: {corr:.3f}")
                            st.caption(f"   {desc_i} ↔ {desc_j}")
                    else:
                        for i, j, corr in corr_pairs[:5]:
                            st.markdown(f"Feature {i} ⋈ Feature {j}: {corr:.3f}")
            
            with tabs[2]:
                # REAL Summary statistics with feature descriptions
                st.markdown("#### 📊 Feature Statistics")
                
                # Get actual feature names
                raw_df = get_state(StateKeys.RAW_DATA, None)
                df_stats = pd.DataFrame(X_viz)
                summary = df_stats.describe().T
                
                if raw_df is not None:
                    feature_names = list(raw_df.columns)
                    # Remove G1, G2, G3, dataset_source if present
                    feature_names = [f for f in feature_names if f not in ['G1', 'G2', 'G3', 'dataset_source']]
                    
                    # Reset index to make it a column
                    summary = summary.reset_index()
                    
                    # Map numeric indices to actual feature names (if lengths match)
                    if len(feature_names) == len(summary):
                        summary.insert(0, 'Feature', feature_names)
                        summary.insert(1, 'Description', summary['Feature'].apply(get_feature_description))
                        # Select only relevant columns
                        summary = summary[['Feature', 'Description', 'mean', 'std', 'min', 'max']]
                        summary.columns = ['Feature', 'Descripción', 'Media', 'Desv. Est.', 'Mín', 'Máx']
                    else:
                        # Fallback if mismatch
                        summary.insert(0, 'Feature', [f"Feature_{i}" for i in range(len(summary))])
                        summary = summary[['Feature', 'mean', 'std', 'min', 'max']]
                        summary.columns = ['Feature', 'Media', 'Desv. Est.', 'Mín', 'Máx']
                else:
                    summary = summary.reset_index()
                    summary.insert(0, 'Feature', [f"Feature_{i}" for i in range(len(summary))])
                    summary = summary[['Feature', 'mean', 'std', 'min', 'max']]
                    summary.columns = ['Feature', 'Media', 'Desv. Est.', 'Mín', 'Máx']
                
                st.dataframe(summary, width="stretch", height=400)
                st.caption("💡 Estadísticas descriptivas de cada característica. Comprender las características es clave para interpretar decisiones del modelo.")
        
        else:
            st.info("Processing data... Visualizations will appear automatically")

