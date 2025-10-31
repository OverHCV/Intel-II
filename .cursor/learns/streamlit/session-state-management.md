# Streamlit Session State Management

## What is Session State?

Streamlit reruns the entire script on every interaction. `st.session_state` preserves data across reruns.

## Basic Pattern

```python
import streamlit as st

# Initialize state (runs only once if key doesn't exist)
if "counter" not in st.session_state:
    st.session_state.counter = 0

# Use state
st.write(f"Counter: {st.session_state.counter}")

# Modify state
if st.button("Increment"):
    st.session_state.counter += 1
```

## Centralized State Management

### Pattern: State Manager Module

```python
# ui/utils/state_manager.py
import streamlit as st

def init_session_state():
    """Initialize all session state on first run"""
    
    # Data state
    if "data" not in st.session_state:
        st.session_state.data = {
            "X": None,
            "y": None,
            "feature_names": [],
            "is_loaded": False
        }
    
    # Model state for each tab
    if "svm" not in st.session_state:
        st.session_state.svm = {
            "model": None,
            "is_trained": False,
            "metrics": {},
            "experiment_history": [],
            "best_model": None
        }
    
    if "ann" not in st.session_state:
        st.session_state.ann = {
            "model": None,
            "is_trained": False,
            "metrics": {},
            "experiment_history": [],
            "best_model": None
        }
```

### Usage in Main App

```python
# app.py
import streamlit as st
from ui.utils.state_manager import init_session_state

# Call ONCE at top of main file
init_session_state()

# Now all pages can access state
def svm_page():
    if st.session_state.svm["is_trained"]:
        st.write("Model already trained!")
```

## Nested Dictionaries (Recommended for Complex Apps)

```python
# ✅ GOOD: Organized by feature/tab
st.session_state.svm = {
    "model": model_object,
    "params": {"C": 1.0, "kernel": "rbf"},
    "metrics": {"accuracy": 0.95},
    "experiment_history": [...]
}

# Access
model = st.session_state.svm["model"]
accuracy = st.session_state.svm["metrics"]["accuracy"]
```

```python
# ❌ BAD: Flat namespace
st.session_state.svm_model = model_object
st.session_state.svm_C = 1.0
st.session_state.svm_kernel = "rbf"
st.session_state.svm_accuracy = 0.95
# Gets cluttered fast!
```

## Auto-Loading Data Pattern

```python
def init_session_state():
    if "data" not in st.session_state:
        st.session_state.data = {
            "X": None,
            "y": None,
            "is_loaded": False
        }
        
        # Auto-load on first run
        try:
            from ui.utils.data_loader import load_and_preprocess_data
            X, y, features, info = load_and_preprocess_data(use_full=False)
            
            st.session_state.data["X"] = X
            st.session_state.data["y"] = y
            st.session_state.data["feature_names"] = features
            st.session_state.data["is_loaded"] = True
        except Exception as e:
            st.error(f"Auto-load failed: {e}")
```

## Persistent Storage (JSON Files)

### Pattern: Experiment History Persistence

```python
# funcs/persistence.py
import json
from pathlib import Path
from datetime import datetime

CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)

def save_experiments_to_file(experiments, model_type="svm"):
    """Save experiments to JSON for persistence across sessions"""
    filepath = CACHE_DIR / f"{model_type}_experiments.json"
    
    data = {
        "timestamp": datetime.now().isoformat(),
        "count": len(experiments),
        "experiments": experiments
    }
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def load_experiments_from_file(model_type="svm"):
    """Load experiments from JSON"""
    filepath = CACHE_DIR / f"{model_type}_experiments.json"
    
    if not filepath.exists():
        return []
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            return data.get("experiments", [])
    except Exception:
        return []
```

### Integration with State Manager

```python
# ui/utils/state_manager.py
from funcs.persistence import load_experiments_from_file

def init_session_state():
    if "svm" not in st.session_state:
        st.session_state.svm = {
            "experiment_history": load_experiments_from_file("svm")  # Load from disk
        }
```

### Saving After Training

```python
# In training function
def train_model():
    # ... training code ...
    
    # Add to history
    experiment = {
        "id": len(st.session_state.svm["experiment_history"]) + 1,
        "params": params,
        "metrics": metrics
    }
    st.session_state.svm["experiment_history"].append(experiment)
    
    # Persist to disk
    from funcs.persistence import save_experiments_to_file
    save_experiments_to_file(st.session_state.svm["experiment_history"], "svm")
```

## State Scope: Tabs vs Entire App

```python
# ✅ CORRECT: State persists across tabs
if st.button("Train"):
    st.session_state.svm["is_trained"] = True
    
# Later, in a different tab:
if st.session_state.svm["is_trained"]:
    st.write("SVM was trained in another tab!")
```

```python
# ❌ WRONG: Using local variables
trained = False  # Resets on every rerun!

if st.button("Train"):
    trained = True  # Lost on next interaction
```

## Common Pitfall: Rerun Loops

```python
# ❌ INFINITE LOOP
if st.button("Click me"):
    st.session_state.counter += 1
    st.rerun()  # Triggers button click again! Infinite loop!

# ✅ CORRECT
if st.button("Click me"):
    st.session_state.counter += 1
    # No manual rerun needed - Streamlit reruns automatically
```

## State Reset Pattern

```python
def reset_model_state():
    """Clear model state without losing other data"""
    st.session_state.svm = {
        "model": None,
        "is_trained": False,
        "metrics": {},
        "experiment_history": st.session_state.svm["experiment_history"]  # Keep history
    }

if st.button("Reset Model"):
    reset_model_state()
    st.success("Model state cleared!")
```

## Key Takeaways

1. **Initialize Early**: Call `init_session_state()` at top of main app
2. **Nested Dicts**: Organize state by feature/tab
3. **Persist Important Data**: Use JSON files for experiment history
4. **Avoid Rerun Loops**: Don't call `st.rerun()` after button clicks
5. **Load Once**: Use `if key not in st.session_state` to initialize only once

