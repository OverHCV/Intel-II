"""
Theory content for Dataset Review page.

Single Responsibility: Render educational content explaining data preparation.
"""

import streamlit as st


def render_theory_section():
    """
    Render theory expander with educational content.
    
    Returns:
        None (renders directly to Streamlit)
    """
    with st.expander("📚 TEORÍA: Por qué la Preparación de Datos es Crítica", expanded=False):
        st.markdown("""
        ### "Basura Entra, Basura Sale"
        
        **Importancia de esta página:**  
        Incluso el mejor algoritmo falla con datos pobres. Esta página asegura:
        - ✅ Calidad de datos (sin valores faltantes, rangos correctos)
        - ✅ Ingeniería de target adecuada (G3 → categorías significativas)
        - ✅ Features relevantes (factores demográficos, sociales, comportamentales)
        - ✅ Clases balanceadas (prevenir sesgo de clase mayoritaria)
        
        ### Estrategia de Datasets
        
        - **Portuguese**: 649 estudiantes → ENTRENAMIENTO (más datos = mejor aprendizaje)
        - **Math**: 395 estudiantes → PRUEBA (materia diferente prueba generalización)
        
        **Razón del split:**  
        Entrenar en Portuguese (más grande) da más ejemplos al modelo. Probar en Math
        (materia diferente) revela si los patrones aprendidos son sobre características
        del estudiante o solo quirks específicos de la materia.
        
        ### Balanceo de Clases: SMOTE Explicado
        
        **Problema**: Si 80% Aprueba, 20% Reprueba → modelo solo predice "Aprueba" para todos
        y obtiene 80% accuracy sin aprender nada útil.
        
        **SMOTE**: Crea ejemplos sintéticos de Reprueba interpolando entre estudiantes
        Reprobados existentes. Mejor que duplicación porque agrega diversidad.
        
        **Cuándo usar**: Ratio de desbalance > 2.0 (una clase es 2x la otra)
        """)

