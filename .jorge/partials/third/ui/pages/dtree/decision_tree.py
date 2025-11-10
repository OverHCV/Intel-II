import streamlit as st
import logging

from .theory import render_theory_section
from .controls import render_controls
from .trainer import train_model
from .visualizations import render_all_results
from .history import render_experiment_history
from states import get_state, StateKeys

logger = logging.getLogger(__name__)


def render():
    """
    Orchestrate the Decision Tree page.

    Flow:
    1. Render theory expander
    2. Check if data is ready
    3. Render hyperparameter controls
    4. Train button → train model → display results
    5. Show experiment history
    """
    # Theory section
    render_theory_section()
    
    st.markdown("## 🌳 Decision Tree (CART)")
    
    # Check if data is ready
    X_ready = get_state(StateKeys.X_PREPARED, None)
    y_ready = get_state(StateKeys.Y_PREPARED, None)
    
    if X_ready is None or y_ready is None:
        st.warning("⚠️ No prepared data found!")
        st.info("👈 Go to **Dataset Review** first to prepare your data.")
        return
    
    st.success(f"✅ Data loaded: {X_ready.shape[0]} samples, {X_ready.shape[1]} features")
    
    # Render controls and get parameters
    params = render_controls()
    
    # Train button
    if st.button("🚀 Train Decision Tree", type="primary"):
        with st.spinner("🌀 Training CART model..."):
            try:
                # Train model and get all results
                results = train_model(X_ready, y_ready, params)
                
                # Display all results
                render_all_results(results, params['cv_folds'])
                
            except Exception as e:
                st.error(f"❌ Error training model: {str(e)}")
                logger.error(f"Decision tree training error: {e}", exc_info=True)
                import traceback
                st.code(traceback.format_exc())
    
    st.markdown("---")
    
    # Experiment history
    render_experiment_history()
    
    # Show cached model info if exists
    cached_model = get_state(StateKeys.DT_MODEL, None)
    if cached_model and not st.session_state.get("_training_now"):
        st.info("✅ Un modelo entrenado está en cache. Click 'Train' para reentrenar con nuevos parámetros.")
