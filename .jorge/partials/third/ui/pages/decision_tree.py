"""Decision Tree Page - CART classification with rule extraction."""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import logging

logger = logging.getLogger(__name__)


def render():
    """Render Decision Tree page with WORKING implementation."""
    
    # THEORY FIRST
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
    
    st.markdown("## 🌳 Decision Tree (CART)")
    
    # Check if data is ready
    from ui.state_manager import get_state, set_state, StateKeys
    
    X_ready = get_state(StateKeys.X_PREPARED, None)
    y_ready = get_state(StateKeys.Y_PREPARED, None)
    
    if X_ready is None or y_ready is None:
        st.warning("⚠️ No prepared data found!")
        st.info("👈 Go to **Dataset Review** first to prepare your data.")
        return
    
    st.success(f"✅ Data loaded: {X_ready.shape[0]} samples, {X_ready.shape[1]} features")
    
    # Hyperparameter controls
    st.markdown("### ⚙️ Hyperparameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        max_depth = st.slider(
            "Max Depth",
            min_value=1,
            max_value=20,
            value=5,
            help="WHY: Controls tree complexity. Lower = simpler rules, higher = more specific but risk overfitting."
        )
    
    with col2:
        min_samples_split = st.slider(
            "Min Samples Split",
            min_value=2,
            max_value=20,
            value=10,
            help="WHY: Minimum samples needed to split a node. Higher = more conservative, prevents tiny splits."
        )
    
    with col3:
        criterion = st.selectbox(
            "Split Criterion",
            ["gini", "entropy"],
            help="WHY: Gini = faster, Entropy (info gain) = slightly more accurate. Usually similar results."
        )
    
    st.markdown("---")
    
    # Train button
    if st.button("🚀 Train Decision Tree", type="primary"):
        with st.spinner("🌀 Training CART model..."):
            try:
                # Import and use our implemented functions!
                from core.decision_tree import train_cart, extract_rules, rank_rules, cross_validate, get_feature_importance
                from core.evaluation import evaluate_classification
                from sklearn.model_selection import train_test_split
                
                # Get feature names from raw data
                raw_df = get_state(StateKeys.RAW_DATA, None)
                if raw_df is not None:
                    # Exclude G1, G2, G3, and dataset_source
                    feature_names = [col for col in raw_df.columns 
                                   if col not in ['G1', 'G2', 'G3', 'dataset_source']]
                else:
                    feature_names = [f"feature_{i}" for i in range(X_ready.shape[1])]
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(
                    X_ready, y_ready, test_size=0.2, random_state=42, stratify=y_ready
                )
                
                # Train model
                model = train_cart(
                    X_train, y_train,
                    max_depth=max_depth,
                    min_samples_split=min_samples_split,
                    criterion=criterion,
                    random_state=42
                )
                
                # Make predictions
                y_pred = model.predict(X_test)
                
                # Evaluate
                metrics = evaluate_classification(y_test, y_pred)
                
                # Get class names
                unique_classes = np.unique(y_ready)
                if len(unique_classes) == 2:
                    class_names = ["Reprueba", "Aprueba"]
                elif len(unique_classes) == 3:
                    class_names = ["Bajo", "Medio", "Alto"]
                elif len(unique_classes) == 5:
                    class_names = ["F", "D", "C", "B", "A"]
                else:
                    class_names = [f"Clase {i}" for i in unique_classes]
                
                # Extract rules
                rules = extract_rules(model, feature_names, class_names=class_names)
                ranked_rules = rank_rules(rules, criterion="combined")
                
                # Cross-validation
                cv_results = cross_validate(
                    X_ready, y_ready,
                    model_params={
                        "max_depth": max_depth,
                        "min_samples_split": min_samples_split,
                        "criterion": criterion,
                        "random_state": 42
                    },
                    cv=5
                )
                
                # Feature importance
                feature_importance = get_feature_importance(model, feature_names, top_n=10)
                
                # Store in state
                set_state(StateKeys.DT_MODEL, model)
                set_state(StateKeys.DT_RULES, ranked_rules)
                
                # Show data split info
                st.info(f"""
                📊 **Datos utilizados**: 
                - Total después de SMOTE: **{len(X_ready)} estudiantes** ({len(X_train)} train, {len(X_test)} test)
                - Features: **{X_ready.shape[1]} características**
                - Target: **{len(np.unique(y_ready))} clases** balanceadas
                """)
                
                st.success("✅ Modelo CART entrenado exitosamente!")
                
                # Display results
                st.markdown("### 📊 Resultados")
                
                # Metrics
                metric_cols = st.columns(4)
                with metric_cols[0]:
                    st.metric("Accuracy", f"{metrics['accuracy']:.3f}")
                with metric_cols[1]:
                    st.metric("Precision", f"{metrics['precision']:.3f}")
                with metric_cols[2]:
                    st.metric("Recall", f"{metrics['recall']:.3f}")
                with metric_cols[3]:
                    st.metric("F1-Score", f"{metrics['f1_score']:.3f}")
                
                # Cross-validation
                st.markdown("#### ✅ Cross-Validation (5-fold)")
                st.info(f"Mean Accuracy: **{cv_results['mean']:.3f}** ± {cv_results['std']:.3f}")
                st.caption("WHY: Single train/test split can be lucky/unlucky. CV gives robust estimate.")
                
                # Confusion Matrix
                st.markdown("#### 🎯 Matriz de Confusión")
                cm = np.array(metrics['confusion_matrix'])
                fig_cm, ax_cm = plt.subplots(figsize=(6, 5))
                im = ax_cm.imshow(cm, cmap='Blues')
                
                # Set ticks based on number of classes
                n_classes = len(class_names)
                ax_cm.set_xticks(range(n_classes))
                ax_cm.set_yticks(range(n_classes))
                ax_cm.set_xticklabels(class_names)
                ax_cm.set_yticklabels(class_names)
                ax_cm.set_xlabel("Predicho")
                ax_cm.set_ylabel("Verdadero")
                ax_cm.set_title("Matriz de Confusión")
                
                # Add text annotations
                for i in range(n_classes):
                    for j in range(n_classes):
                        ax_cm.text(j, i, str(cm[i, j]), ha="center", va="center", 
                                  color="white" if cm[i, j] > cm.max()/2 else "black", fontsize=16)
                
                plt.colorbar(im, ax=ax_cm)
                st.pyplot(fig_cm)
                plt.close()
                
                # Tree visualization
                st.markdown("#### 🌳 Estructura del Árbol")
                fig_tree, ax_tree = plt.subplots(figsize=(20, 10))
                plot_tree(
                    model,
                    feature_names=feature_names,
                    class_names=class_names,
                    filled=True,
                    ax=ax_tree,
                    fontsize=8,
                    max_depth=3  # Only show first 3 levels for readability
                )
                ax_tree.set_title(f"Árbol CART (primeros 3 niveles)", fontsize=14)
                st.pyplot(fig_tree)
                plt.close()
                st.caption(f"Profundidad total: {model.get_depth()}, Hojas: {model.get_n_leaves()}. Se muestran solo 3 niveles por legibilidad.")
                
                # Feature Importance with descriptions
                st.markdown("#### ⭐ Top 10 Importancia de Características")
                
                # Import feature descriptions
                from constants import get_feature_description
                
                fig_imp, ax_imp = plt.subplots(figsize=(10, 6))
                features = list(feature_importance.keys())[:10]  # Top 10
                importances = list(feature_importance.values())[:10]
                
                # Add descriptions
                labels_with_desc = []
                for feat in features:
                    desc = get_feature_description(feat)
                    # Shorten description for plot
                    short_desc = desc.split("(")[0].strip()[:30]
                    labels_with_desc.append(f"{feat}\n({short_desc})")
                
                ax_imp.barh(range(len(features)), importances, color='steelblue')
                ax_imp.set_yticks(range(len(features)))
                ax_imp.set_yticklabels(labels_with_desc, fontsize=9)
                ax_imp.set_xlabel("Importancia (reducción Gini)")
                ax_imp.set_title("Importancia de Características")
                ax_imp.invert_yaxis()
                plt.tight_layout()
                st.pyplot(fig_imp)
                plt.close()
                st.caption("Muestra qué características son más útiles para dividir nodos. Mayor = más importante.")
                
                # RULES DISPLAY - TWO COLUMNS
                st.markdown("#### 📜 Reglas Extraídas (Top 10)")
                st.info(f"""
                🔍 **Interpretación del Soporte**: 
                - Soporte = número de estudiantes del **train set** ({len(X_train)} estudiantes) que cumplen esta regla específica
                - Confianza = % de estudiantes en el nodo hoja que pertenecen a la clase predicha
                - Profundidad = número de condiciones en la regla (menor = más simple)
                """)
                
                # Split rules into two columns (5 + 5)
                col_rules1, col_rules2 = st.columns(2)
                
                for idx, rule in enumerate(ranked_rules[:10], 1):
                    # Alternate between columns
                    target_col = col_rules1 if idx <= 5 else col_rules2
                    
                    with target_col:
                        with st.expander(f"#{idx}: {rule['prediction']} (Soporte: {rule['support']}, Conf: {rule['confidence']:.2f})"):
                            st.markdown(f"**SI** {rule['conditions']}")
                            st.markdown(f"**ENTONCES** → **{rule['prediction']}**")
                            st.markdown(f"- 📊 Soporte: {rule['support']} estudiantes ({rule['support_pct']:.1f}% del train set)")
                            st.markdown(f"- 🎯 Confianza: {rule['confidence']:.3f} ({rule['confidence']*100:.1f}% precisión)")
                            st.markdown(f"- 🔢 Profundidad: {rule['depth']} condiciones")
                            
                            # Show class distribution in a more readable format
                            st.markdown("**Distribución en el nodo:**")
                            dist_df = pd.DataFrame(list(rule['class_distribution'].items()), columns=['Clase', 'Cantidad'])
                            st.dataframe(dist_df, hide_index=True, width="stretch")
                
            except Exception as e:
                st.error(f"❌ Error training model: {str(e)}")
                logger.error(f"Decision tree training error: {e}", exc_info=True)
    
    # Show cached model if exists
    cached_model = get_state(StateKeys.DT_MODEL, None)
    if cached_model and not st.session_state.get("_training_now"):
        st.info("✅ A trained model is cached. Click 'Train' to retrain with new parameters.")

