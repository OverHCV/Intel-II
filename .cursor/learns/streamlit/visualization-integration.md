# Streamlit Visualization Integration

## Matplotlib Integration

### Basic Pattern

```python
import streamlit as st
import matplotlib.pyplot as plt

def create_plot():
    """Create matplotlib figure"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot([1, 2, 3], [1, 4, 9])
    ax.set_title("My Plot")
    return fig

# Render in Streamlit
fig = create_plot()
st.pyplot(fig)
```

### Best Practices

```python
# ✅ GOOD: Return figure, clean up
def plot_confusion_matrix(y_true, y_pred):
    import matplotlib.pyplot as plt
    from sklearn.metrics import confusion_matrix
    
    cm = confusion_matrix(y_true, y_pred)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(cm, cmap='Blues')
    
    # Annotations, labels, etc.
    
    plt.tight_layout()
    return fig  # Return figure, don't call plt.show()

# In Streamlit
fig = plot_confusion_matrix(y_test, y_pred)
st.pyplot(fig)
plt.close(fig)  # Clean up to prevent memory leaks
```

```python
# ❌ BAD: Side effects, no return
def plot_confusion_matrix(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    plt.imshow(cm)
    plt.show()  # ❌ Don't call show() in Streamlit
    # ❌ Doesn't return figure
```

### Side-by-Side Matplotlib Plots

```python
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Plot A**")
    fig1 = create_plot_a()
    st.pyplot(fig1)
    plt.close(fig1)

with col2:
    st.markdown("**Plot B**")
    fig2 = create_plot_b()
    st.pyplot(fig2)
    plt.close(fig2)
```

### Responsive Sizing

```python
# Configuration-based sizing
CONF = {
    "FIGURE_SIZE_SMALL": (8, 6),
    "FIGURE_SIZE_MEDIUM": (10, 8),
    "FIGURE_SIZE_LARGE": (12, 10)
}

def plot_with_size(data, size="medium"):
    sizes = {
        "small": CONF["FIGURE_SIZE_SMALL"],
        "medium": CONF["FIGURE_SIZE_MEDIUM"],
        "large": CONF["FIGURE_SIZE_LARGE"]
    }
    
    fig, ax = plt.subplots(figsize=sizes[size])
    ax.plot(data)
    return fig
```

## Plotly Integration

### Basic Pattern

```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Method 1: Express (simpler)
fig = px.scatter(df, x='col1', y='col2', color='class')
st.plotly_chart(fig, use_container_width=True)

# Method 2: Graph Objects (more control)
fig = go.Figure()
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 4, 9]))
st.plotly_chart(fig)
```

### Interactive 3D Scatter

```python
def plot_interactive_scatter_3d(X, y, feature_names, x_idx, y_idx, z_idx):
    """Interactive 3D scatter with Plotly"""
    import plotly.graph_objects as go
    
    fig = go.Figure(data=[
        go.Scatter3d(
            x=X[:, x_idx],
            y=X[:, y_idx],
            z=X[:, z_idx],
            mode='markers',
            marker=dict(
                size=5,
                color=y,
                colorscale='Viridis',
                showscale=True
            ),
            text=[f"Sample {i}" for i in range(len(X))],
            hoverinfo='text'
        )
    ])
    
    fig.update_layout(
        scene=dict(
            xaxis_title=feature_names[x_idx],
            yaxis_title=feature_names[y_idx],
            zaxis_title=feature_names[z_idx]
        ),
        title="Interactive 3D Scatter Plot",
        height=600
    )
    
    return fig

# Usage
fig = plot_interactive_scatter_3d(X, y, features, 0, 1, 2)
st.plotly_chart(fig, use_container_width=True)
```

### Plotly vs Matplotlib Decision

**Use Matplotlib When**:
- Static plots are sufficient
- Consistency with existing plots
- Simpler plots (line, bar, scatter 2D)
- Publication-quality figures needed
- Already familiar with matplotlib

**Use Plotly When**:
- Interactivity needed (zoom, pan, rotate)
- 3D visualizations
- Hover tooltips important
- Real-time updates
- Modern, web-friendly look

### Hybrid Approach (Recommended)

```python
def plot_scatter(X, y, feature_names, x_idx, y_idx, z_idx=None, use_plotly=True):
    """Hybrid: Use plotly for 3D, matplotlib for 2D"""
    
    if z_idx is not None and use_plotly:
        # 3D with Plotly (better interactivity)
        return _plot_3d_plotly(X, y, feature_names, x_idx, y_idx, z_idx)
    else:
        # 2D with Matplotlib (simpler, more familiar)
        return _plot_2d_matplotlib(X, y, feature_names, x_idx, y_idx)
```

## Seaborn Integration

### Pattern

```python
import seaborn as sns
import matplotlib.pyplot as plt

def plot_correlation_heatmap(X, feature_names):
    """Correlation heatmap with seaborn"""
    import pandas as pd
    
    df = pd.DataFrame(X, columns=feature_names)
    corr = df.corr()
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Seaborn heatmap
    sns.heatmap(
        corr,
        annot=True,
        fmt='.2f',
        cmap='RdBu_r',
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8},
        ax=ax
    )
    
    plt.title("Feature Correlation Matrix")
    plt.tight_layout()
    return fig

# Usage
fig = plot_correlation_heatmap(X, feature_names)
st.pyplot(fig)
```

## Visualization Organization

### Pattern: Tabs for Multiple Plots

```python
def render_visualizations(X, y, features, data_info):
    """Organize multiple visualizations in tabs"""
    
    if not st.session_state["is_trained"]:
        st.info("Train a model first")
        return
    
    viz_tabs = st.tabs([
        "📊 Model Performance",
        "🔬 Feature Analysis",
        "🗺️ Data Exploration"
    ])
    
    with viz_tabs[0]:
        _render_model_performance(y_test, y_pred)
    
    with viz_tabs[1]:
        _render_feature_analysis(X, features)
    
    with viz_tabs[2]:
        _render_data_exploration(X, y, features)

def _render_model_performance(y_test, y_pred):
    """Model performance visualizations"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Confusion Matrix**")
        fig_cm = plot_confusion_matrix(y_test, y_pred)
        st.pyplot(fig_cm)
        plt.close(fig_cm)
    
    with col2:
        st.markdown("**Metrics**")
        fig_metrics = plot_metrics_bars(metrics)
        st.pyplot(fig_metrics)
        plt.close(fig_metrics)

def _render_feature_analysis(X, features):
    """Feature analysis visualizations"""
    st.subheader("🔗 Correlations")
    fig_corr = plot_correlation_heatmap(X, features)
    st.pyplot(fig_corr)
    plt.close(fig_corr)
    
    st.subheader("📦 Distributions")
    fig_dist = plot_feature_distributions(X, features)
    st.pyplot(fig_dist)
    plt.close(fig_dist)

def _render_data_exploration(X, y, features):
    """Data exploration with interactive selector"""
    st.subheader("🗺️ Interactive Scatter")
    
    col1, col2 = st.columns(2)
    with col1:
        x_idx = st.selectbox("X Axis", range(len(features)), 
                            format_func=lambda i: features[i],
                            key="scatter_x_axis")
    with col2:
        y_idx = st.selectbox("Y Axis", range(len(features)),
                            format_func=lambda i: features[i],
                            key="scatter_y_axis")
    
    enable_3d = st.checkbox("Enable 3D", key="scatter_3d")
    
    if enable_3d:
        z_idx = st.selectbox("Z Axis", range(len(features)),
                            format_func=lambda i: features[i],
                            key="scatter_z_axis")
        fig = plot_scatter_3d(X, y, features, x_idx, y_idx, z_idx)
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = plot_scatter_2d(X, y, features, x_idx, y_idx)
        st.pyplot(fig)
        plt.close(fig)
```

## Memory Management

### Issue: Memory Leaks

```python
# ❌ BAD: Figures accumulate in memory
for i in range(100):
    fig = plt.figure()
    plt.plot(data[i])
    st.pyplot(fig)
    # ❌ No cleanup!
```

### Solution: Always Close Figures

```python
# ✅ GOOD: Close figures after displaying
for i in range(100):
    fig = plt.figure()
    plt.plot(data[i])
    st.pyplot(fig)
    plt.close(fig)  # ✅ Clean up
```

### Pattern: Context Manager

```python
from contextlib import contextmanager

@contextmanager
def create_plot():
    """Context manager for plot creation"""
    fig, ax = plt.subplots()
    try:
        yield fig, ax
    finally:
        plt.close(fig)

# Usage
with create_plot() as (fig, ax):
    ax.plot([1, 2, 3], [1, 4, 9])
    st.pyplot(fig)
# Automatically closed!
```

## Caching Expensive Plots

```python
import streamlit as st
import hashlib

@st.cache_data
def generate_expensive_plot(data_hash):
    """Cache plot generation"""
    # data_hash ensures cache invalidation when data changes
    fig, ax = plt.subplots(figsize=(12, 8))
    # ... expensive plotting operations ...
    return fig

# Usage
data_hash = hashlib.md5(X.tobytes()).hexdigest()
fig = generate_expensive_plot(data_hash)
st.pyplot(fig)
```

## Key Takeaways

1. **Return Figures**: Don't use `plt.show()`, return fig object
2. **Close Figures**: Always `plt.close(fig)` after `st.pyplot(fig)`
3. **Plotly for 3D**: Use Plotly for interactive 3D, Matplotlib for 2D
4. **Organize in Tabs**: Group related visualizations
5. **Side-by-Side**: Use `st.columns()` for comparison plots
6. **Cache Expensive**: Use `@st.cache_data` for slow plots
7. **Responsive Width**: Use `use_container_width=True` for Plotly

