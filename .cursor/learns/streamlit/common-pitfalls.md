# Streamlit Common Pitfalls & Solutions

## Deprecation: use_container_width

### Problem

**Warning**: `use_container_width is deprecated. Use width='stretch' or width='content'`

### Old Code (Deprecated)

```python
# ❌ DEPRECATED
st.button("Click me", use_container_width=True)
st.selectbox("Choose", options, use_container_width=True)
st.pyplot(fig, use_container_width=True)
```

### New Code (Streamlit 1.x+)

```python
# ✅ CORRECT (Streamlit 1.x+)
st.button("Click me", width="stretch")      # Full width
st.selectbox("Choose", options, width="stretch")
st.dataframe(df, width="stretch")

# Or for compact width
st.button("Click me", width="content")      # Auto width
```

### Fix Across Codebase

```bash
# Find all occurrences
grep -r "use_container_width" .

# Replace with width='stretch'
# Update each file manually or use:
# sed -i 's/use_container_width=True/width="stretch"/g' file.py
```

## Button ID Collisions (Already Covered in 03-widget-keys-duplicates.md)

See dedicated file for full details.

## Rerun Loops

### Problem: Infinite Reruns

```python
# ❌ INFINITE LOOP
if st.button("Increment"):
    st.session_state.counter += 1
    st.rerun()  # ❌ Triggers another button click!
    
# Result: App freezes, infinite loop
```

### Solution: Let Streamlit Handle Reruns

```python
# ✅ CORRECT
if st.button("Increment"):
    st.session_state.counter += 1
    # No manual rerun needed - Streamlit reruns automatically!
```

### When to Use st.rerun()

```python
# ✅ VALID USE: After programmatic state change
def background_process():
    # Some long-running task
    st.session_state.status = "complete"

if st.button("Start Process"):
    background_process()
    st.rerun()  # Refresh UI after background change

# ✅ VALID USE: After file operations
if st.button("Load Config"):
    config = load_from_file()
    st.session_state.config = config
    st.rerun()
```

## State Initialization Errors

### Problem: State Not Initialized

```python
# ❌ ERROR: KeyError if counter doesn't exist
counter = st.session_state.counter  # Crashes on first run!
```

### Solution: Always Check Before Access

```python
# ✅ CORRECT: Check if key exists
if "counter" not in st.session_state:
    st.session_state.counter = 0

counter = st.session_state.counter  # Safe!
```

### Better: Centralized Initialization

```python
# ui/utils/state_manager.py
def init_session_state():
    """Initialize all state on first run"""
    if "counter" not in st.session_state:
        st.session_state.counter = 0
    
    if "data" not in st.session_state:
        st.session_state.data = None

# app.py - Call once at top
from ui.utils.state_manager import init_session_state
init_session_state()
```

## File Upload Handling

### Problem: File Lost on Rerun

```python
# ❌ WRONG: File lost after widget interaction
uploaded_file = st.file_uploader("Choose file")
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write(data)  # ← Works first time
    
# User clicks button → rerun → uploaded_file might be None!
```

### Solution: Store in Session State

```python
# ✅ CORRECT: Persist uploaded file
uploaded_file = st.file_uploader("Choose file", key="file_uploader")

if uploaded_file and "data" not in st.session_state:
    st.session_state.data = pd.read_csv(uploaded_file)

if st.session_state.get("data") is not None:
    st.write(st.session_state.data)  # Persists across reruns
```

## Widget Value Access

### Problem: Value Not Updated Immediately

```python
# ❌ WRONG: Value accessed before rerun
value = st.slider("Value", 0, 100)
st.write(f"Value: {value}")  # Shows OLD value

if st.button("Process"):
    process(value)  # Uses OLD value!
```

### Explanation

Streamlit reruns script on interaction. Value updated AFTER current run.

### Solution: Use on_change Callback

```python
# ✅ CORRECT: Callback for immediate action
def on_value_change():
    st.session_state.processed = process(st.session_state.slider_value)

st.slider(
    "Value",
    0, 100,
    key="slider_value",
    on_change=on_value_change
)

if "processed" in st.session_state:
    st.write(f"Processed: {st.session_state.processed}")
```

## Expensive Computation on Every Rerun

### Problem: Slow Reruns

```python
# ❌ SLOW: Recomputes on every interaction
def expensive_function():
    time.sleep(5)  # Expensive operation
    return result

result = expensive_function()  # ← Runs on EVERY rerun!
st.write(result)
```

### Solution: Cache Results

```python
# ✅ FAST: Cache expensive computation
import streamlit as st

@st.cache_data
def expensive_function():
    time.sleep(5)
    return result

result = expensive_function()  # Cached after first run!
st.write(result)
```

### Cache Invalidation

```python
# Cache invalidates when parameters change
@st.cache_data
def load_data(filepath, use_full):
    return pd.read_csv(filepath)

# Different parameters = different cache
data1 = load_data("data.csv", use_full=False)  # Cached
data2 = load_data("data.csv", use_full=True)   # Different cache entry
```

## Widget in Conditional Not Rendering

### Problem: Widget Doesn't Appear

```python
# ❌ ISSUE: Widget may not render
show_widget = st.checkbox("Show advanced")

if show_widget:
    value = st.slider("Advanced Setting", 0, 100)
    # If checkbox unchecked, slider doesn't render
    # But st.session_state might still have old value!
```

### Solution: Clear State When Hidden

```python
# ✅ CORRECT: Clear state when widget hidden
show_widget = st.checkbox("Show advanced", key="show_advanced")

if show_widget:
    value = st.slider("Advanced Setting", 0, 100, key="advanced_setting")
else:
    # Clear state when hidden
    if "advanced_setting" in st.session_state:
        del st.session_state.advanced_setting
```

## Hot Reload Not Working

### Problem: Changes Don't Reflect

**Cause**: Hot reload not enabled or file not being watched.

### Solution 1: Enable in UI

1. Click hamburger menu (☰)
2. Go to "Settings"
3. Enable "Always rerun"

### Solution 2: Config File

```toml
# .streamlit/config.toml
[server]
runOnSave = true
```

### Solution 3: Command Line

```bash
streamlit run app.py --server.runOnSave=true
```

## Dataframe Not Updating

### Problem: DataFrame Shows Old Data

```python
# ❌ ISSUE: DataFrame not refreshing
if st.button("Update"):
    st.session_state.df = load_new_data()

st.dataframe(st.session_state.df)  # Shows old data!
```

### Solution: Force Refresh

```python
# ✅ CORRECT: Use key to force refresh
if st.button("Update"):
    st.session_state.df = load_new_data()
    st.session_state.df_version = st.session_state.get("df_version", 0) + 1

st.dataframe(
    st.session_state.df,
    key=f"df_{st.session_state.df_version}"  # New key forces refresh
)
```

## Form Not Submitting

### Problem: Form Values Don't Update

```python
# ❌ WRONG: Missing form submit
name = st.text_input("Name")
age = st.number_input("Age")

if st.button("Submit"):  # ← Button outside form!
    save_data(name, age)
```

### Solution: Use st.form

```python
# ✅ CORRECT: Proper form usage
with st.form("my_form"):
    name = st.text_input("Name")
    age = st.number_input("Age")
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        save_data(name, age)
```

## Error: Widget Outside Correct Context

### Problem

```
StreamlitAPIException: st.columns() can only be called inside a form or main area
```

### Cause

```python
# ❌ WRONG: Columns in sidebar
with st.sidebar:
    col1, col2 = st.columns(2)  # ❌ Not allowed in sidebar!
```

### Solution

```python
# ✅ CORRECT: Avoid columns in sidebar
with st.sidebar:
    st.selectbox("Option 1", options)
    st.selectbox("Option 2", options)

# Or use main area
col1, col2 = st.columns(2)
with col1:
    st.write("Left")
with col2:
    st.write("Right")
```

## Key Takeaways

1. **No Manual Reruns**: Streamlit reruns automatically after interactions
2. **Initialize State Early**: Use centralized `init_session_state()`
3. **Cache Expensive Operations**: Use `@st.cache_data` liberally
4. **Unique Widget Keys**: Always provide `key=` for stateful widgets
5. **Store in Session State**: Files, data, model objects
6. **Update Deprecated APIs**: `use_container_width` → `width="stretch"`
7. **Clear Hidden Widget State**: Prevent stale values
8. **Enable Hot Reload**: For faster development

