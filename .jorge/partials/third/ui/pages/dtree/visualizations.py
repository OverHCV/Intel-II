"""
Visualizations for Decision Tree results.

Single Responsibility: Render all result visualizations (metrics, plots, rules).
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import logging
from typing import Dict, Any, List

from constants.base import get_feature_description

logger = logging.getLogger(__name__)


def render_data_info(results: Dict[str, Any]):
    """
    Render data split information and accuracy context.
    
    Args:
        results: Training results dict
    """
    X_train = results['X_train']
    X_test = results['X_test']
    n_classes = results['n_classes']
    metrics = results['metrics']
    
    st.info(f"""
    📊 **Datos utilizados**: 
    - Total después de SMOTE: **{len(X_train) + len(X_test)} estudiantes** ({len(X_train)} train, {len(X_test)} test)
    - Features: **{X_train.shape[1]} características**
    - Target: **{n_classes} clases** balanceadas (cada clase tiene {len(X_train)//n_classes} samples en train)
    - Test set: **~{len(X_test)//n_classes} samples por clase** (total {len(X_test)})
    """)
    
    st.success("✅ Modelo CART entrenado exitosamente!")
    
    st.warning(f"""
    ⚠️ **Sobre el Accuracy ({metrics['accuracy']:.1%})**:
    - Predecir G3 (nota final) sin G1/G2 es MUY difícil
    - Solo usamos factores demográficos/sociales/comportamentales
    - Random baseline (adivinar): {100/n_classes:.1f}% para {n_classes} clases
    - Nuestro modelo: {metrics['accuracy']*100:.1f}% (mejor que random!)
    - En producción, G1/G2 mejorarían esto a ~80%+, pero causarían data leakage
    """)


def render_metrics(metrics: Dict[str, Any]):
    """
    Render evaluation metrics (accuracy, precision, recall, F1).
    
    Args:
        metrics: Evaluation metrics dict
    """
    st.markdown("### 📊 Resultados")
    
    metric_cols = st.columns(4)
    with metric_cols[0]:
        st.metric("Accuracy", f"{metrics['accuracy']:.3f}")
    with metric_cols[1]:
        st.metric("Precision", f"{metrics['precision']:.3f}")
    with metric_cols[2]:
        st.metric("Recall", f"{metrics['recall']:.3f}")
    with metric_cols[3]:
        st.metric("F1-Score", f"{metrics['f1_score']:.3f}")


def render_cross_validation(cv_results: Dict[str, float], cv_folds: int):
    """
    Render cross-validation results.
    
    Args:
        cv_results: CV results with 'mean' and 'std'
        cv_folds: Number of folds used
    """
    st.markdown(f"#### ✅ Cross-Validation ({cv_folds}-fold)")
    st.info(f"Mean Accuracy: **{cv_results['mean']:.3f}** ± {cv_results['std']:.3f}")
    st.caption(f"Un solo split train/test puede ser suerte/mala suerte. CV con {cv_folds} folds da estimación robusta.")


def render_confusion_matrix(metrics: Dict[str, Any], class_names: List[str], n_test_samples: int):
    """
    Render confusion matrix heatmap.
    
    Args:
        metrics: Evaluation metrics dict (contains confusion_matrix)
        class_names: List of class labels
        n_test_samples: Total test samples
    """
    st.markdown("#### 🎯 Matriz de Confusión")
    

    
    cm = np.array(metrics['confusion_matrix'])
    fig_cm, ax_cm = plt.subplots(figsize=(6, 5))
    im = ax_cm.imshow(cm, cmap='Blues')
    
    # Set ticks
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
            ax_cm.text(
                j, i, str(cm[i, j]), 
                ha="center", va="center", 
                color="white" if cm[i, j] > cm.max()/2 else "black", 
                fontsize=16
            )
    
    plt.colorbar(im, ax=ax_cm)
    st.pyplot(fig_cm)

    st.caption(f"""
    📈 **Interpretación**: Matriz de {n_test_samples} predicciones del test set.
    - Diagonal (azul oscuro) = predicciones correctas
    - Fuera de diagonal = errores del modelo
    - Cada fila suma ~{n_test_samples // len(class_names)} (test set balanceado con {n_test_samples} samples ÷ {len(class_names)} clases)
    """)
    plt.close()


def render_tree_structure(model, feature_names: List[str], class_names: List[str]):
    """
    Render tree structure visualization.
    
    Args:
        model: Trained DecisionTreeClassifier
        feature_names: List of feature names
        class_names: List of class labels
    """
    st.markdown("#### 🌳 Estructura del Árbol")
    
    actual_depth = model.get_depth()
    display_depth = min(actual_depth, 4)  # Max 4 levels for readability
    n_leaves = model.get_n_leaves()
    
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
    ax_tree.set_title(
        f"Árbol CART (Profundidad {actual_depth}, mostrando {display_depth} niveles)", 
        fontsize=14
    )
    st.pyplot(fig_tree)
    plt.close()
    
    st.caption(
        f"📏 Profundidad real: {actual_depth} | Hojas: {n_leaves} | "
        f"Visualización limitada a {display_depth} niveles por legibilidad."
    )


def render_feature_importance(feature_importance: Dict[str, float]):
    """
    Render feature importance bar chart.
    
    Args:
        feature_importance: Dict mapping feature names to importance scores
    """
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


def render_rules(rules: List[Dict[str, Any]], n_train_samples: int):
    """
    Render extracted rules in two columns.
    
    Args:
        rules: List of extracted rules (top 10)
        n_train_samples: Total training samples (for context)
    """
    st.markdown("#### 📜 Reglas Extraídas (Top 10)")
    
    st.info(f"""
    🔍 **Interpretación del Soporte**: 
    - Soporte = número de estudiantes del **train set** ({n_train_samples} estudiantes) que cumplen esta regla específica
    - Confianza = % de estudiantes en el nodo hoja que pertenecen a la clase predicha
    - Profundidad = número de condiciones en la regla (menor = más simple)
    """)
    
    # Split rules into two columns (5 + 5)
    col_rules1, col_rules2 = st.columns(2)
    
    for idx, rule in enumerate(rules[:10], 1):
        # Alternate between columns
        target_col = col_rules1 if idx <= 5 else col_rules2
        
        with target_col:
            with st.expander(
                f"#{idx}: {rule['prediction']} "
                f"(Soporte: {rule['support']}, Conf: {rule['confidence']:.2f})"
            ):
                st.markdown(f"**SI** {rule['conditions']}")
                st.markdown(f"**ENTONCES** → **{rule['prediction']}**")
                st.markdown(
                    f"- 📊 Soporte: {rule['support']} estudiantes "
                    f"({rule['support_pct']:.1f}% del train set)"
                )
                st.markdown(
                    f"- 🎯 Confianza: {rule['confidence']:.3f} "
                    f"({rule['confidence']*100:.1f}% precisión)"
                )
                st.markdown(f"- 🔢 Profundidad: {rule['depth']} condiciones")
                
                # Show class distribution
                st.markdown("**Distribución en el nodo:**")
                dist_df = pd.DataFrame(
                    list(rule['class_distribution'].items()), 
                    columns=['Clase', 'Cantidad']
                )
                st.dataframe(dist_df, hide_index=True, width="stretch")


def render_all_results(results: Dict[str, Any], cv_folds: int):
    """
    Render all training results visualizations.
    
    Args:
        results: Complete training results dict
        cv_folds: Number of CV folds (for display)
    """
    # Data info and context
    render_data_info(results)
    
    # Metrics
    render_metrics(results['metrics'])
    
    # Cross-validation
    render_cross_validation(results['cv_results'], cv_folds)
    
    # Confusion matrix + Feature importance in two columns
    col_cm, col_fi = st.columns(2)
    
    with col_cm:
        render_confusion_matrix(
            results['metrics'], 
            results['class_names'], 
            len(results['X_test'])
        )
    
    with col_fi:
        render_feature_importance(results['feature_importance'])
    
    # Tree structure (full width)
    render_tree_structure(
        results['model'], 
        results['feature_names'], 
        results['class_names']
    )
    
    # Extracted rules (full width)
    render_rules(results['rules'], len(results['X_train']))

