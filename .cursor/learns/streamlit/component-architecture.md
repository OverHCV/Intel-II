# Streamlit Component Architecture & Modularization

## The Problem: Monolithic Files

Large files (>300 LOC) with all logic in one function violate Single Responsibility Principle and become unmaintainable.

## Example: Before Modularization

```python
# ui/pages/svm/tab.py - 439 LINES! ❌
def svm_page():
    # Data loading (5 lines)
    X, y, features, info = get_data()
    
    # Documentation (2 lines)
    render_docs()
    
    # Model configuration (168 lines!) ❌
    with st.expander("Model Configuration"):
        kernel = st.selectbox(...)
        C = st.slider(...)
        # ... 160 more lines of config and training logic
    
    # Visualizations (131 lines!) ❌
    with st.columns([1, 2]):
        # ... all visualization logic here
    
    # Experiment history (2 lines)
    render_history()
    
    # Save best model (81 lines!) ❌
    with st.expander("Save Best Model"):
        # ... all saving logic here
```

**Problems**:
- Hard to find specific functionality
- Can't reuse components
- Testing is difficult
- Merge conflicts
- Violates <300 LOC rule

## Solution: Component-Based Architecture

### Folder Structure

```
ui/pages/svm/
├── __init__.py
├── tab.py                      # 45 lines - Orchestrator only
├── docs.py                     # 197 lines - Theory documentation
├── experiments.py              # 198 lines - Experiment tracking
├── README.md                   # User guide
└── components/
    ├── __init__.py             # 15 lines - Exports
    ├── model_config.py         # 218 lines - Configuration & training
    ├── visualizations.py       # 148 lines - All visualization tabs
    └── best_model_saver.py     # 86 lines - Best model selector
```

### Tab.py: The Orchestrator (45 lines)

```python
# ui/pages/svm/tab.py
import streamlit as st
from ui.utils.data_loader import get_data
from ui.pages.svm.docs import render_documentation
from ui.pages.svm.experiments import render_experiment_history
from ui.pages.svm.components import (
    render_model_configuration,
    render_visualizations,
    render_best_model_saver
)

def svm_page():
    """SVM Analysis Tab - Main orchestrator"""
    st.title("🔍 Support Vector Machine (SVM)")
    
    # Load data
    X, y, feature_names, data_info = get_data()
    
    # Documentation (collapsible)
    render_documentation()
    
    # Two-column layout
    col_controls, col_viz = st.columns([1, 2])
    
    with col_controls:
        render_model_configuration(X, y, data_info)
    
    with col_viz:
        render_visualizations(X, y, feature_names, data_info)
    
    # Experiment tracking
    render_experiment_history(st.session_state.svm)
    
    # Best model saver
    render_best_model_saver(X, y, data_info)
```

**Key Points**:
- Only 45 lines!
- Pure orchestration - no business logic
- Clear structure at a glance
- Easy to modify layout

### Component: Model Configuration

```python
# ui/pages/svm/components/model_config.py
import streamlit as st
from sklearn.svm import SVC

def render_model_configuration(X, y, data_info):
    """Render SVM configuration controls and training logic"""
    
    with st.expander("⚙️ Model Configuration", expanded=not st.session_state.svm["is_trained"]):
        # Kernel selector
        kernel = st.selectbox(
            "Kernel",
            ["linear", "rbf", "poly", "sigmoid"],
            key="svm_kernel"
        )
        
        # Parameter controls based on kernel
        C = st.slider("C (Regularization)", 0.1, 100.0, 1.0, key="svm_c")
        
        if kernel in ["rbf", "poly", "sigmoid"]:
            gamma = st.selectbox("Gamma", ["scale", "auto"], key="svm_gamma")
        
        if kernel == "poly":
            degree = st.slider("Degree", 2, 5, 3, key="svm_degree")
        
        # Train button
        if st.button("🚀 Train SVM", key="svm_train_button"):
            with st.spinner("Training..."):
                _train_model(X, y, kernel, C, gamma, degree)

def _train_model(X, y, kernel, C, gamma, degree):
    """Private function: Training logic"""
    # ... training code ...
    pass
```

**Key Points**:
- Single responsibility: configuration UI + training
- Private helper `_train_model()` for logic
- All keys prefixed with `svm_`
- Under 220 lines

### Component: Visualizations

```python
# ui/pages/svm/components/visualizations.py
import streamlit as st
from funcs.visualizers import plot_confusion_matrix, plot_metrics_bars

def render_visualizations(X, y, feature_names, data_info):
    """Render visualization tabs"""
    
    if not st.session_state.svm["is_trained"]:
        st.info("Train a model to see visualizations")
        return
    
    viz_tabs = st.tabs([
        "📊 Model Performance",
        "🔬 Feature Analysis",
        "🗺️ Data Exploration"
    ])
    
    with viz_tabs[0]:
        _render_model_performance_tab()
    
    with viz_tabs[1]:
        _render_feature_analysis_tab(X, feature_names)
    
    with viz_tabs[2]:
        _render_data_exploration_tab(X, y, feature_names)

def _render_model_performance_tab():
    """Private: Model performance visualizations"""
    st.markdown("### Confusion Matrix & Metrics")
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("**Confusion Matrix**")
        cm_fig = plot_confusion_matrix(...)
        st.pyplot(cm_fig)
    
    with col2:
        st.markdown("**Performance Metrics**")
        metrics_fig = plot_metrics_bars(...)
        st.pyplot(metrics_fig)

def _render_feature_analysis_tab(X, feature_names):
    """Private: Feature analysis visualizations"""
    # ... correlation heatmap, box plots, etc.
    pass

def _render_data_exploration_tab(X, y, feature_names):
    """Private: Data exploration visualizations"""
    # ... scatter plots, 3D plots, etc.
    pass
```

**Key Points**:
- Organized by visualization category
- Public `render_*()` for main entry point
- Private `_render_*_tab()` for each tab
- Under 150 lines

### Component: Best Model Saver

```python
# ui/pages/svm/components/best_model_saver.py
import streamlit as st
from ui.pages.svm.experiments import get_best_experiment

def render_best_model_saver(X, y, data_info):
    """Render best model selection and saving"""
    
    if not st.session_state.svm["experiment_history"]:
        return  # No experiments yet
    
    st.divider()
    st.subheader("💾 Save Best Model")
    
    # Find best experiment
    best_idx, best_exp = get_best_experiment(st.session_state.svm["experiment_history"])
    
    # Show best experiment info
    with st.container(border=True):
        st.markdown(f"**Best: Experiment #{best_exp['id']}**")
        st.write(f"Kernel: {best_exp['kernel']}")
        st.write(f"Accuracy: {best_exp['accuracy']:.4f}")
    
    # Save button
    if st.button(
        f"💾 Save Best Model (Exp #{best_exp['id']})",
        key="svm_save_best_model"
    ):
        with st.spinner("Retraining best model..."):
            _retrain_and_save_best(X, y, best_exp)

def _retrain_and_save_best(X, y, best_exp):
    """Private: Retrain best model and save"""
    # ... retraining logic ...
    st.success(f"✅ Best model saved: Exp #{best_exp['id']}")
    st.balloons()
```

**Key Points**:
- Single responsibility: best model selection
- Uses helper from experiments.py
- Under 90 lines

## Components __init__.py: Clean Exports

```python
# ui/pages/svm/components/__init__.py
"""SVM Components - Modular UI pieces"""

from .model_config import render_model_configuration
from .visualizations import render_visualizations
from .best_model_saver import render_best_model_saver

__all__ = [
    "render_model_configuration",
    "render_visualizations",
    "render_best_model_saver"
]
```

## Benefits of This Architecture

### 1. Maintainability ⭐⭐⭐⭐⭐
- Each file has single, clear purpose
- Easy to find and fix bugs
- Obvious where to add new features

### 2. Testability ⭐⭐⭐⭐⭐
```python
# Can test components in isolation
def test_model_config():
    render_model_configuration(X_test, y_test, info)
    assert st.session_state.svm["kernel"] == "rbf"
```

### 3. Reusability ⭐⭐⭐⭐⭐
```python
# Reuse visualizations in different contexts
from ui.pages.svm.components import render_visualizations

def comparison_page():
    render_visualizations(X_pca, y, features, info)
```

### 4. Collaboration ⭐⭐⭐⭐⭐
- Different devs work on different components
- Fewer merge conflicts
- Parallel development possible

### 5. Readability ⭐⭐⭐⭐⭐
- tab.py tells the full story in 45 lines
- Components tell their own story
- Self-documenting architecture

## When to Modularize?

### Triggers for Refactoring

1. **File > 300 lines**: Always split
2. **Function > 100 lines**: Extract helpers
3. **Multiple responsibilities**: Separate into components
4. **Code duplication**: Extract to shared module
5. **Hard to find code**: Needs better organization

## Modularization Process

### Step 1: Identify Sections

```python
# Original monolithic file
def page():
    # Section A: Configuration (100 lines)
    # Section B: Visualization (150 lines)
    # Section C: Results (80 lines)
```

### Step 2: Extract Components

```python
# components/config.py
def render_configuration():
    # 100 lines from Section A

# components/visualization.py  
def render_visualization():
    # 150 lines from Section B

# components/results.py
def render_results():
    # 80 lines from Section C
```

### Step 3: Create Orchestrator

```python
# tab.py
from .components import render_configuration, render_visualization, render_results

def page():
    render_configuration()
    render_visualization()
    render_results()
```

## Common Mistakes

```python
# ❌ WRONG: Still too much logic in tab.py
def svm_page():
    X, y = load_data()
    kernel = st.selectbox(...)  # ← Config logic in orchestrator
    C = st.slider(...)          # ← Config logic in orchestrator
    model = train_svm(...)      # ← Training logic in orchestrator

# ✅ CORRECT: Delegate to components
def svm_page():
    X, y = load_data()
    render_model_configuration(X, y)  # ← Component handles it
```

## Key Takeaways

1. **Tab.py = Orchestrator**: Only layout + component calls (<100 LOC)
2. **Components = Logic**: Each handles one responsibility (<300 LOC)
3. **Private Helpers**: Use `_function()` for internal logic
4. **Clean Exports**: Use `__init__.py` for clean imports
5. **Consistent Structure**: Apply same pattern across all tabs

