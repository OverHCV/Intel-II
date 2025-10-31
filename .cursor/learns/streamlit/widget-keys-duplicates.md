# Streamlit Widget Keys & Duplicate ID Prevention

## The Critical Problem

**Error**: `StreamlitDuplicateElementId: There are multiple identical st.button widgets with the same generated key`

**Root Cause**: Streamlit generates widget IDs from (type, label, parameters). Identical widgets = ID collision.

## When Duplicates Happen

### Scenario 1: Same Label in Multiple Pages

```python
# ❌ COLLISION: Both SVM and ANN tabs have this button
# svm/tab.py
if st.button("💾 Save as Best Model"):  # ID: button_💾-Save-as-Best-Model
    save_svm()

# ann/tab.py  
if st.button("💾 Save as Best Model"):  # ID: button_💾-Save-as-Best-Model (DUPLICATE!)
    save_ann()
```

### Scenario 2: Widgets Inside Loops

```python
# ❌ ALL BUTTONS HAVE SAME ID
for exp in experiments:
    if st.button("Delete"):  # All have ID: button_Delete
        delete_experiment(exp)
```

### Scenario 3: Conditional Rendering

```python
# ❌ SAME BUTTON RENDERED IN DIFFERENT CONTEXTS
if mode == "train":
    if st.button("Run"):  # ID: button_Run
        train()
elif mode == "test":
    if st.button("Run"):  # ID: button_Run (DUPLICATE!)
        test()
```

## Solution: Unique Keys

### Basic Syntax

```python
st.button(label, key="unique_identifier")
st.selectbox(label, options, key="unique_identifier")
st.slider(label, min, max, key="unique_identifier")
st.checkbox(label, key="unique_identifier")
```

**Rule**: EVERY stateful widget should have a unique key.

## Naming Convention

### Pattern: `{page}_{widget}_{purpose}`

```python
# ✅ GOOD: Descriptive and unique
st.button("💾 Save", key="svm_save_best_model")
st.button("💾 Save", key="ann_save_best_model")

st.selectbox("Kernel", options, key="svm_kernel_selector")
st.slider("C", 0.1, 100, key="svm_c_parameter")

st.button("Clear History", key="svm_clear_history")
st.button("Clear History", key="ann_clear_history")
```

### Pattern: Loop with Index/ID

```python
# ✅ GOOD: Each button has unique key
for i, exp in enumerate(experiments):
    if st.button("Delete", key=f"delete_exp_{i}"):
        delete_experiment(exp)

# Or with unique IDs
for exp in experiments:
    if st.button("Delete", key=f"delete_exp_{exp['id']}"):
        delete_experiment(exp)
```

### Pattern: Tab-Prefixed Widgets

```python
# ✅ GOOD: Tab name prefix prevents cross-tab collisions
# In Feature Analysis tab
st.selectbox("X Axis", features, key="pca_feature_analysis_x_axis")

# In Data Exploration tab  
st.selectbox("X Axis", features, key="pca_data_exploration_x_axis")
```

## Which Widgets Need Keys?

### Always Need Keys (Stateful)
- `st.button()`
- `st.checkbox()`
- `st.radio()`
- `st.selectbox()`
- `st.multiselect()`
- `st.slider()`
- `st.text_input()`
- `st.text_area()`
- `st.number_input()`
- `st.date_input()`
- `st.time_input()`
- `st.file_uploader()`
- `st.color_picker()`

### Don't Need Keys (Display Only)
- `st.write()`
- `st.markdown()`
- `st.title()` / `st.header()` / `st.subheader()`
- `st.caption()`
- `st.metric()`
- `st.pyplot()` / `st.plotly_chart()`
- `st.dataframe()` / `st.table()`

## Real-World Example

### Before (With Duplicates)

```python
# svm/components/visualizations.py
def render_visualizations():
    viz_tabs = st.tabs(["Model Performance", "Feature Analysis", "Data Exploration"])
    
    with viz_tabs[1]:  # Feature Analysis
        selected_features = st.multiselect("Select features", all_features)  # No key
        x_axis = st.selectbox("X Axis", features)  # No key

# pca/components/visualizations.py
def render_visualizations():
    viz_tabs = st.tabs(["Feature Analysis", "PCA Transform"])
    
    with viz_tabs[0]:  # Feature Analysis
        selected_features = st.multiselect("Select features", all_features)  # DUPLICATE!
        x_axis = st.selectbox("X Axis", features)  # DUPLICATE!
```

### After (With Unique Keys)

```python
# svm/components/visualizations.py
def render_visualizations():
    viz_tabs = st.tabs(["Model Performance", "Feature Analysis", "Data Exploration"])
    
    with viz_tabs[1]:
        selected_features = st.multiselect(
            "Select features", 
            all_features,
            key="svm_feature_analysis_selected_features"  # ✅ Unique
        )
        x_axis = st.selectbox(
            "X Axis", 
            features,
            key="svm_feature_analysis_x_axis"  # ✅ Unique
        )

# pca/components/visualizations.py
def render_visualizations():
    viz_tabs = st.tabs(["Feature Analysis", "PCA Transform"])
    
    with viz_tabs[0]:
        selected_features = st.multiselect(
            "Select features",
            all_features,
            key="pca_feature_analysis_selected_features"  # ✅ Different key
        )
        x_axis = st.selectbox(
            "X Axis",
            features,
            key="pca_feature_analysis_x_axis"  # ✅ Different key
        )
```

## Debugging Duplicate IDs

### Error Message

```
StreamlitDuplicateElementId: There are multiple identical st.button widgets 
with key='None' or no key at all. To fix, assign unique keys to each widget.
```

### How to Find the Duplicate

1. **Look at the line numbers** in the error traceback
2. **Search for the widget label** across all files: `grep -r "Save as Best Model"`
3. **Check loops** for widgets without indexed keys
4. **Check conditional branches** for same widget in multiple branches

## Key Takeaways

1. **Unique Keys Always**: Add `key=` to ALL stateful widgets
2. **Naming Convention**: Use `{page}_{widget}_{purpose}` pattern
3. **Loops Need Indices**: Use `key=f"widget_{i}"` or `key=f"widget_{item.id}"`
4. **Tab Prefixes**: Prevent collisions across different tabs/pages
5. **Test Early**: Try to click all buttons to catch duplicates during development

## Prevention Checklist

- [ ] Every button has unique key
- [ ] Every selectbox has unique key
- [ ] Widgets in loops have indexed keys
- [ ] Cross-tab widgets have page-specific keys
- [ ] Key naming is descriptive and follows convention

