# Streamlit Layout Patterns

## Two-Column Layouts

### Basic Pattern

```python
import streamlit as st

# Create two columns with equal width
col1, col2 = st.columns(2)

with col1:
    st.write("Left column content")
    
with col2:
    st.write("Right column content")
```

### Custom Ratios

```python
# 60/40 split (col1 is wider)
col1, col2 = st.columns([3, 2])  # or [0.6, 0.4]

# 70/30 split
col_left, col_right = st.columns([7, 3])

# Common ratio for controls | visualizations
col_controls, col_viz = st.columns([1, 2])  # Controls 33%, Viz 67%
```

### Controls Left, Visualizations Right

```python
# Best practice for ML apps
col_controls, col_viz = st.columns([1, 2])

with col_controls:
    # Model configuration
    kernel = st.selectbox("Kernel", ["linear", "rbf"])
    C = st.slider("C", 0.1, 100.0)
    
    if st.button("Train"):
        train_model()

with col_viz:
    # Visualizations
    if st.session_state["is_trained"]:
        st.pyplot(confusion_matrix_fig)
        st.pyplot(metrics_bar_fig)
```

### Side-by-Side Graphs

```python
# Equal-width graphs
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Confusion Matrix**")
    st.pyplot(cm_fig)

with col2:
    st.markdown("**Metrics**")
    st.pyplot(metrics_fig)
```

```python
# Slightly wider left column (better for some plots)
col_cm, col_metrics = st.columns([1.2, 1])

with col_cm:
    st.markdown("**Confusion Matrix**")
    st.pyplot(cm_fig)

with col_metrics:
    st.markdown("**Performance Metrics**")
    st.pyplot(metrics_bar_fig)
    st.caption("⏱️ Training time: 2.3s")
```

## Tab Layouts

### Basic Tabs

```python
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Details", "⚙️ Settings"])

with tab1:
    st.write("Overview content")

with tab2:
    st.write("Details content")
    
with tab3:
    st.write("Settings content")
```

### Visualization Organization

```python
# Organize multiple visualizations in tabs
viz_tabs = st.tabs([
    "📊 Model Performance",
    "🔬 Feature Analysis",
    "🗺️ Data Exploration"
])

with viz_tabs[0]:  # Model Performance
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(confusion_matrix)
    with col2:
        st.pyplot(metrics_bar)

with viz_tabs[1]:  # Feature Analysis
    st.pyplot(correlation_heatmap)
    st.pyplot(box_plots)

with viz_tabs[2]:  # Data Exploration
    st.plotly_chart(scatter_3d)
```

### Main Navigation Tabs

```python
# Page-level navigation
main_tabs = st.tabs(["⚙️ Config", "🔍 SVM", "🧠 ANN", "📊 PCA"])

with main_tabs[0]:
    config_page()
    
with main_tabs[1]:
    svm_page()
    
with main_tabs[2]:
    ann_page()
    
with main_tabs[3]:
    pca_page()
```

## Expanders (Collapsible Sections)

### Basic Expander

```python
with st.expander("📚 Theory & Documentation", expanded=False):
    st.markdown("""
    ## Support Vector Machines
    
    SVMs find the optimal hyperplane...
    """)
```

### Dynamic Expansion

```python
# Expand when no model trained, collapse after training
is_trained = st.session_state.get("is_trained", False)

with st.expander("⚙️ Model Configuration", expanded=not is_trained):
    kernel = st.selectbox("Kernel", ["linear", "rbf"])
    C = st.slider("C", 0.1, 100.0)
    
    if st.button("Train"):
        train_model()
        st.session_state["is_trained"] = True
```

### Multiple Expanders

```python
# Documentation
with st.expander("📚 Documentation"):
    st.write("Theory and usage guide")

# Advanced Settings
with st.expander("🔧 Advanced Settings"):
    st.write("Expert options")

# Debug Info
with st.expander("🐛 Debug Information"):
    st.json(st.session_state)
```

## Sidebar Layout

### Basic Sidebar

```python
# Sidebar for global controls
with st.sidebar:
    st.title("⚙️ Configuration")
    
    dataset = st.selectbox("Dataset", ["Small (4.5K)", "Full (45K)"])
    cv_strategy = st.radio("CV Strategy", ["Train/Test", "K-Fold"])
    
    if cv_strategy == "K-Fold":
        n_folds = st.slider("Folds", 2, 10, 5)
```

### Sidebar + Main Content

```python
# Sidebar for navigation/settings
with st.sidebar:
    st.title("Navigation")
    page = st.radio("Go to", ["SVM", "ANN", "PCA"])
    
    st.divider()
    
    st.title("Settings")
    theme = st.selectbox("Theme", ["Light", "Dark"])

# Main content area
if page == "SVM":
    svm_page()
elif page == "ANN":
    ann_page()
else:
    pca_page()
```

## Container Layouts

### Basic Container

```python
# Grouping related content
with st.container():
    st.subheader("Results")
    st.metric("Accuracy", "0.95")
    st.metric("F1-Score", "0.93")
```

### Styled Container

```python
# Container with border
with st.container(border=True):
    st.markdown("**Best Model Saved**")
    st.write("Experiment #5: RBF kernel, C=10")
    st.metric("Accuracy", "0.9567")
```

## Row Patterns

### Three-Column Row

```python
# Three graphs in a row
col1, col2, col3 = st.columns(3)

with col1:
    st.pyplot(plot1)
    
with col2:
    st.pyplot(plot2)
    
with col3:
    st.pyplot(plot3)
```

### Four-Column Grid

```python
# Metrics dashboard
metric_cols = st.columns(4)

metric_cols[0].metric("Accuracy", "95.6%", delta="2.3%")
metric_cols[1].metric("Precision", "93.2%", delta="-1.1%")
metric_cols[2].metric("Recall", "94.8%", delta="0.5%")
metric_cols[3].metric("F1-Score", "94.0%", delta="0.8%")
```

## Nested Layouts

### Tabs Inside Columns

```python
col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("Controls")
    param1 = st.slider("Parameter 1", 0, 100)

with col_right:
    viz_tabs = st.tabs(["Plot 1", "Plot 2"])
    
    with viz_tabs[0]:
        st.pyplot(plot1)
        
    with viz_tabs[1]:
        st.pyplot(plot2)
```

### Columns Inside Tabs

```python
main_tabs = st.tabs(["Analysis", "Comparison"])

with main_tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        st.write("Graph A")
    with col2:
        st.write("Graph B")

with main_tabs[1]:
    col1, col2 = st.columns(2)
    with col1:
        st.write("Before")
    with col2:
        st.write("After")
```

## Spacing & Dividers

```python
# Add vertical space
st.write("")  # Small space
st.markdown("<br>", unsafe_allow_html=True)  # Custom space

# Horizontal divider
st.divider()

# Section separator
st.markdown("---")
```

## Common Layout Mistakes

```python
# ❌ WRONG: Columns outside context manager
col1, col2 = st.columns(2)
st.write("This goes to main area, not columns!")

# ✅ CORRECT
col1, col2 = st.columns(2)
with col1:
    st.write("This goes in column 1")
```

```python
# ❌ WRONG: Forgetting to use 'with'
col1, col2 = st.columns(2)
col1.write("Column 1")  # Works but less readable

# ✅ CORRECT
with col1:
    st.write("Column 1")
```

## Key Takeaways

1. **Two-Column**: Use `[1, 2]` ratio for controls|visualizations
2. **Side-by-Side Graphs**: Use `columns(2)` or `[1.2, 1]` for unequal widths
3. **Tabs**: Organize related content, don't overuse
4. **Expanders**: Collapse optional content (theory, advanced settings)
5. **Nested Layouts**: Tabs-in-columns or columns-in-tabs both work
6. **Always use `with`**: More readable and Pythonic

