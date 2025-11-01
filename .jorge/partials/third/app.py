"""
Student Performance Analysis - Main Application Entry Point

Run with: streamlit run app.py
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure page
st.set_page_config(
    page_title="Student Performance Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title
st.title("📊 Student Performance Analysis")
st.markdown("---")

# Welcome message
st.markdown("""
### Welcome to the Student Performance Analysis Tool

This application provides interactive analysis of student performance data using:
- **Decision Trees** (CART) for classification and rule extraction
- **Hierarchical Clustering** with J4 criterion analysis
- **K-means Clustering** with optimal k selection
- **Cross-Domain Validation** (Math → Portuguese)

#### 🚀 Quick Start

1. **Dataset Review** - Explore and prepare your data
2. **Decision Trees** - Train CART models and extract rules
3. **Hierarchical Clustering** - Analyze dendrogram and find optimal clusters
4. **K-means** - Compare with hierarchical results
5. **Experiment History** - Review and compare past experiments

#### 📁 Datasets

- **Math**: 395 students (Training set)
- **Portuguese**: 649 students (Test set for cross-validation)
- **Features**: 33 attributes (demographic, social, school-related)
- **Target**: G3 score (0-20) transformed to categorical

#### 🎯 Objectives

1. Build classification models with interpretable rules
2. Discover natural groupings in student data
3. Validate generalization across subjects
4. Compare clustering algorithms

---

**Note**: Use the sidebar to navigate between different analysis tabs.
""")

# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("""
Select a page from above to begin analysis.

**Current Status**:
- ✅ Data layer implemented
- 🚧 Logic layer in progress
- ⏳ UI components pending
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Student Performance Analysis | Universidad de Caldas | 2025</p>
</div>
""", unsafe_allow_html=True)


