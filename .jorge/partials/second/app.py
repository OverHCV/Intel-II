"""
Main Streamlit Application - Bank Marketing ML Analysis
Interactive UI for SVM, ANN, and PCA analysis
"""

import streamlit as st
from settings.config import CONF, Keys
from ui.pages.ann.tab import ann_page
from ui.pages.conf import config_page
from ui.pages.pca.tab import pca_page
from ui.pages.svm.tab import svm_page
from ui.utils import init_session_state

# Page configuration
st.set_page_config(
    page_title="Bank Marketing ML Analysis",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize session state
init_session_state()

# Sidebar
with st.sidebar:
    st.title("🏦 Bank Marketing ML Analysis")
    st.markdown("### Interactive Exploration of Classification Models")

    st.divider()

    st.caption("Universidad de Caldas")
    st.caption("Sistemas Inteligentes II")
    st.caption(f"Random State: {CONF[Keys.RANDOM_STATE]}")

# Main content area
# st.markdown("# 🏦 Bank Marketing ML Analysis")
# st.markdown("Interactive exploration of classification models")

# Create tabs
tab_config, tab_svm, tab_ann, tab_pca = st.tabs(
    [
        "⚙️ Config",
        "🔍 SVM",
        "🧠 ANN",
        "📈 PCA",
    ]
)

# Render tab content
with tab_config:
    config_page()

with tab_svm:
    svm_page()

with tab_ann:
    ann_page()

with tab_pca:
    pca_page()

# Footer
st.divider()
st.caption("Streamlit | UCI Machine Learning Repository - Bank Marketing Dataset")
