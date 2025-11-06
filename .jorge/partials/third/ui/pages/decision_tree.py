"""Decision Tree Page - CART classification with rule extraction."""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import logging

# Import state management and feature descriptions
from states import get_state, set_state, StateKeys
from constants.base import get_feature_description

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
            help="Controla complejidad del árbol. Menor = reglas simples, mayor = más específico pero riesgo overfitting."
        )
    
    with col2:
        min_samples_split = st.slider(
            "Min Samples Split",
            min_value=2,
            max_value=20,
            value=10,
            help="Mínimo de muestras necesarias para dividir un nodo. Mayor = más conservador, previene divisiones pequeñas."
        )
    
    with col3:
        criterion = st.selectbox(
            "Split Criterion",
            ["gini", "entropy"],
            help="Gini = más rápido, Entropy (info gain) = ligeramente más preciso. Resultados similares."
        )
    
    st.markdown("---")
    
    # Validation controls - NEW!
    st.markdown("### 🎯 Validation Settings")
    
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        test_size = st.slider(
            "Test Size (%)",
            min_value=10,
            max_value=40,
            value=20,
            step=5,
            help="Porcentaje de datos para testing. 20% es estándar (80% train, 20% test)."
        ) / 100
    
    with col_v2:
        cv_folds = st.slider(
            "Cross-Validation Folds",
            min_value=2,
            max_value=10,
            value=5,
            help="Número de folds para CV. 5-10 es estándar. Mayor = más robusto pero más lento."
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
                
                # Get feature names from raw data (DYNAMIC based on what was included)
                raw_df = get_state(StateKeys.RAW_DATA, None)
                if raw_df is not None:
                    # Start with all columns
                    all_cols = list(raw_df.columns)
                    # Remove G3 (always target) and dataset_source (always metadata)
                    exclude_list = ['G3', 'dataset_source']
                    
                    # Check what G features are actually in X_ready
                    # If X_ready has 31 features, one of G1/G2 is included
                    # If X_ready has 32 features, both G1/G2 are included
                    # If X_ready has 30 features, neither is included
                    
                    if X_ready.shape[1] == 30:
                        # Neither G1 nor G2
                        exclude_list.extend(['G1', 'G2'])
                    elif X_ready.shape[1] == 31:
                        # One of them is included - need to check which was removed
                        # For now, assume it matches the raw data minus exclusions
                        pass
                    # else 32 features = both included
                    
                    feature_names = [col for col in all_cols if col not in exclude_list]
                    
                    # Ensure feature_names matches X_ready shape
                    if len(feature_names) != X_ready.shape[1]:
                        logger.warning(f"Feature name mismatch: {len(feature_names)} names vs {X_ready.shape[1]} features. Using generic names.")
                        feature_names = [f"feature_{i}" for i in range(X_ready.shape[1])]
                else:
                    feature_names = [f"feature_{i}" for i in range(X_ready.shape[1])]
                
                # Split data (use user-defined test_size)
                X_train, X_test, y_train, y_test = train_test_split(
                    X_ready, y_ready, test_size=test_size, random_state=42, stratify=y_ready
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
                
                # Cross-validation (use user-defined cv_folds)
                cv_results = cross_validate(
                    X_ready, y_ready,
                    model_params={
                        "max_depth": max_depth,
                        "min_samples_split": min_samples_split,
                        "criterion": criterion,
                        "random_state": 42
                    },
                    cv=cv_folds
                )
                
                # Feature importance
                feature_importance = get_feature_importance(model, feature_names, top_n=10)
                
                # Store in state
                set_state(StateKeys.DT_MODEL, model)
                set_state(StateKeys.DT_RULES, ranked_rules)
                
                # SAVE EXPERIMENT TO HISTORY
                import datetime
                experiment_id = f"DT_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                experiment_data = {
                    "id": experiment_id,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "algorithm": "Decision Tree (CART)",
                    "params": {
                        "max_depth": max_depth,
                        "min_samples_split": min_samples_split,
                        "criterion": criterion,
                        "test_size": test_size,
                        "cv_folds": cv_folds
                    },
                    "data": {
                        "total_samples": len(X_ready),
                        "n_features": X_ready.shape[1],
                        "n_classes": len(unique_classes),
                        "train_samples": len(X_train),
                        "test_samples": len(X_test)
                    },
                    "metrics": {
                        "accuracy": metrics['accuracy'],
                        "precision": metrics['precision'],
                        "recall": metrics['recall'],
                        "f1_score": metrics['f1_score'],
                        "cv_mean": cv_results['mean'],
                        "cv_std": cv_results['std']
                    },
                    "tree_info": {
                        "depth": model.get_depth(),
                        "n_leaves": model.get_n_leaves(),
                        "n_rules": len(rules)
                    }
                }
                
                # Append to experiment history
                history = get_state("experiment_history", [])
                history.append(experiment_data)
                set_state("experiment_history", history)
                
                logger.info(f"Saved experiment {experiment_id} to history")
                
                # Show data split info
                st.info(f"""
                📊 **Datos utilizados**: 
                - Total después de SMOTE: **{len(X_ready)} estudiantes** ({len(X_train)} train, {len(X_test)} test)
                - Features: **{X_ready.shape[1]} características**
                - Target: **{len(np.unique(y_ready))} clases** balanceadas (cada clase tiene {len(X_train)//len(np.unique(y_ready))} samples en train)
                - Test set: **~{len(X_test)//len(np.unique(y_ready))} samples por clase** (total {len(X_test)})
                """)
                
                st.success("✅ Modelo CART entrenado exitosamente!")
                
                st.warning(f"""
                ⚠️ **Sobre el Accuracy ({metrics['accuracy']:.1%})**:
                - Predecir G3 (nota final) sin G1/G2 es MUY difícil
                - Solo usamos factores demográficos/sociales/comportamentales
                - Random baseline (adivinar): {100/len(np.unique(y_ready)):.1f}% para {len(np.unique(y_ready))} clases
                - Nuestro modelo: {metrics['accuracy']*100:.1f}% (mejor que random!)
                - En producción, G1/G2 mejorarían esto a ~80%+, pero causarían data leakage
                """)
                
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
                st.markdown(f"#### ✅ Cross-Validation ({cv_folds}-fold)")
                st.info(f"Mean Accuracy: **{cv_results['mean']:.3f}** ± {cv_results['std']:.3f}")
                st.caption(f"Un solo split train/test puede ser suerte/mala suerte. CV con {cv_folds} folds da estimación robusta.")
                
                # Confusion Matrix
                st.markdown("#### 🎯 Matriz de Confusión")
                
                st.caption(f"""
                📈 **Interpretación**: Matriz de {len(X_test)} predicciones del test set.
                - Diagonal (azul oscuro) = predicciones correctas
                - Fuera de diagonal = errores del modelo
                - Cada fila suma ~{len(X_test)//len(class_names)} (test set balanceado con {len(X_test)} samples ÷ {len(class_names)} clases)
                """)
                
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
                
                actual_depth = model.get_depth()
                display_depth = min(actual_depth, 4)  # Max 4 levels for readability
                
                fig_tree, ax_tree = plt.subplots(figsize=(20, max(10, actual_depth * 2)))
                plot_tree(
                    model,
                    feature_names=feature_names,
                    class_names=class_names,
                    filled=True,
                    ax=ax_tree,
                    fontsize=max(6, 10 - actual_depth),  # Smaller font for deeper trees
                    max_depth=display_depth  # Show first N levels
                )
                ax_tree.set_title(f"Árbol CART (Profundidad {actual_depth}, mostrando {display_depth} niveles)", fontsize=14)
                st.pyplot(fig_tree)
                plt.close()
                st.caption(f"📏 Profundidad real: {actual_depth} | Hojas: {model.get_n_leaves()} | Reglas: {len(rules)}. Visualización limitada a {display_depth} niveles por legibilidad.")
                
                # Feature Importance with descriptions
                st.markdown("#### ⭐ Top 10 Importancia de Características")
                
                
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
                import traceback
                st.code(traceback.format_exc())
    
    st.markdown("---")
    
    # EXPERIMENT HISTORY TABLE
    st.markdown("### 📊 Experimentos Guardados")
    
    history = get_state("experiment_history", [])
    
    if len(history) == 0:
        st.info("No hay experimentos guardados aún. Entrena un modelo para empezar!")
    else:
        st.success(f"✅ {len(history)} experimento(s) guardado(s) en esta sesión")
        
        # Create comparison table
        history_data = []
        for exp in history:
            history_data.append({
                "ID": exp["id"],
                "Timestamp": exp["timestamp"].split("T")[1][:8] if "T" in exp["timestamp"] else exp["timestamp"],
                "Max Depth": exp["params"]["max_depth"],
                "Min Split": exp["params"]["min_samples_split"],
                "Criterion": exp["params"]["criterion"],
                "Test %": f"{exp['params']['test_size']*100:.0f}%",
                "CV Folds": exp["params"]["cv_folds"],
                "Features": exp["data"]["n_features"],
                "Accuracy": f"{exp['metrics']['accuracy']:.3f}",
                "F1": f"{exp['metrics']['f1_score']:.3f}",
                "CV Mean": f"{exp['metrics']['cv_mean']:.3f}",
                "CV Std": f"{exp['metrics']['cv_std']:.3f}",
                "Depth": exp["tree_info"]["depth"],
                "Leaves": exp["tree_info"]["n_leaves"],
                "Rules": exp["tree_info"]["n_rules"]
            })
        
        df_history = pd.DataFrame(history_data)
        st.dataframe(df_history, width="stretch", height=300)
        
        # Comparison charts
        st.markdown("#### 📈 Comparación Visual")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Accuracy comparison
            fig_acc, ax_acc = plt.subplots(figsize=(8, 5))
            accuracies = [float(exp["metrics"]["accuracy"]) for exp in history]
            labels = [exp["id"].split("_")[1] for exp in history]  # Just timestamp
            ax_acc.plot(range(len(accuracies)), accuracies, marker='o', linewidth=2, markersize=8, color='steelblue')
            ax_acc.set_xlabel("Experimento")
            ax_acc.set_ylabel("Accuracy")
            ax_acc.set_title("Evolución del Accuracy")
            ax_acc.set_xticks(range(len(labels)))
            ax_acc.set_xticklabels(labels, rotation=45, ha='right')
            ax_acc.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig_acc)
            plt.close()
        
        with col_chart2:
            # Feature count vs Accuracy
            fig_feat, ax_feat = plt.subplots(figsize=(8, 5))
            n_features = [exp["data"]["n_features"] for exp in history]
            accuracies = [float(exp["metrics"]["accuracy"]) for exp in history]
            colors = ['green' if f == 30 else 'orange' if f == 31 else 'red' for f in n_features]
            ax_feat.scatter(n_features, accuracies, s=100, c=colors, alpha=0.6)
            ax_feat.set_xlabel("Número de Features")
            ax_feat.set_ylabel("Accuracy")
            ax_feat.set_title("Features vs Accuracy")
            ax_feat.grid(True, alpha=0.3)
            # Add legend
            ax_feat.plot([], [], 'o', color='green', label='30 feat (sin G1/G2)')
            ax_feat.plot([], [], 'o', color='orange', label='31 feat (G1 o G2)')
            ax_feat.plot([], [], 'o', color='red', label='32 feat (G1 + G2)')
            ax_feat.legend()
            plt.tight_layout()
            st.pyplot(fig_feat)
            plt.close()
        
        # Clear history button
        if st.button("🗑️ Limpiar Historial", type="secondary"):
            set_state("experiment_history", [])
            st.rerun()
    
    # Show cached model if exists
    cached_model = get_state(StateKeys.DT_MODEL, None)
    if cached_model and not st.session_state.get("_training_now"):
        st.info("✅ Un modelo entrenado está en cache. Click 'Train' para reentrenar con nuevos parámetros.")

