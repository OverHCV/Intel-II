"""
Main Streamlit Application - Bank Marketing ML Analysis
Interactive UI for SVM, ANN, and PCA analysis
"""

import streamlit as st
from settings.config import CONF, Keys
from ui.components.sidebar import sidebar_render
from ui.pages.ann.tab import ann_page
from ui.pages.pca.tab import pca_page
from ui.pages.svm.tab import svm_page
from ui.utils import init_session_state

# Page configuration
st.set_page_config(
    page_title="Bank Marketing ML Analysis",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
init_session_state()

# Sidebar with Configuration
with st.sidebar:
    st.title("🏦 Bank Marketing")
    st.markdown("**ML Analysis Dashboard**")

    # Render all configuration controls
    sidebar_render()

    st.divider()

    st.caption("Universidad de Caldas")
    st.caption("Sistemas Inteligentes II")
    st.caption(f"Random State: {CONF[Keys.RANDOM_STATE]}")

# Main content area - Create tabs (removed Config tab)
tab_svm, tab_ann, tab_pca = st.tabs(
    [
        "🔍 SVM",
        "🧠 ANN",
        "📈 PCA",
    ]
)

# Render tab content
with tab_svm:
    svm_page()

with tab_ann:
    ann_page()

with tab_pca:
    pca_page()

# Footer
st.divider()
st.caption("Streamlit | UCI Machine Learning Repository - Bank Marketing Dataset")
