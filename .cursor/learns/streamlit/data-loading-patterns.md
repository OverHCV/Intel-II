# Streamlit Data Loading & Management Patterns

## Centralized Data Loader Pattern

### Structure

```
ui/utils/
├── __init__.py
├── state_manager.py    # Session state initialization
└── data_loader.py      # Data loading and preprocessing
```

### Data Loader Module

```python
# ui/utils/data_loader.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

def load_and_preprocess_data(
    use_full_dataset=False,
    use_categorical=False,
    random_state=42
):
    """
    Centralized data loading and preprocessing
    
    Returns:
        X_scaled: np.ndarray - Scaled features
        y: np.ndarray - Encoded labels
        feature_names: list - Feature names
        data_info: dict - Metadata about dataset
    """
    
    # Load data
    if use_full_dataset:
        filepath = "data/bank_full.csv"
    else:
        filepath = "data/bank.csv"
    
    df = pd.read_csv(filepath, sep=';')
    
    # Separate features and target
    target_col = 'y'
    X_cols = [col for col in df.columns if col != target_col]
    
    # Handle categorical features
    if use_categorical:
        X = pd.get_dummies(df[X_cols], drop_first=True)
        feature_names = X.columns.tolist()
        X = X.values
    else:
        # Only numerical features
        numeric_cols = df[X_cols].select_dtypes(include=[np.number]).columns
        X = df[numeric_cols].values
        feature_names = numeric_cols.tolist()
    
    # Encode target
    y = df[target_col].values
    le = LabelEncoder()
    y = le.fit_transform(y)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Metadata
    data_info = {
        "n_samples": len(X),
        "n_features": X.shape[1],
        "class_names": le.classes_.tolist(),
        "class_distribution": {
            cls: int(np.sum(y == i)) 
            for i, cls in enumerate(le.classes_)
        },
        "feature_names": feature_names,
        "is_full_dataset": use_full_dataset
    }
    
    return X_scaled, y, feature_names, data_info
```

## Auto-Loading Pattern

### Initialize with Data Loading

```python
# ui/utils/state_manager.py
import streamlit as st
from ui.utils.data_loader import load_and_preprocess_data

def init_session_state():
    """Initialize session state on first app load"""
    
    # Data state
    if "data" not in st.session_state:
        st.session_state.data = {
            "X": None,
            "y": None,
            "feature_names": [],
            "data_info": {},
            "is_loaded": False
        }
        
        # Auto-load on first run
        try:
            X, y, features, info = load_and_preprocess_data(use_full=False)
            st.session_state.data.update({
                "X": X,
                "y": y,
                "feature_names": features,
                "data_info": info,
                "is_loaded": True
            })
        except Exception as e:
            st.error(f"Failed to auto-load data: {e}")
```

### Benefits

- Data available immediately when app starts
- No "Load Data" button needed
- Consistent data access across tabs
- Error handling centralized

## Accessing Data Across Components

### Helper Function

```python
# ui/utils/data_loader.py
def get_data():
    """Convenience function to get current data from session state"""
    if not st.session_state.data["is_loaded"]:
        raise ValueError("Data not loaded. Call load_and_preprocess_data() first.")
    
    return (
        st.session_state.data["X"],
        st.session_state.data["y"],
        st.session_state.data["feature_names"],
        st.session_state.data["data_info"]
    )
```

### Usage in Components

```python
# In any page/component
from ui.utils.data_loader import get_data

def svm_page():
    # Simple access to data
    X, y, feature_names, data_info = get_data()
    
    st.write(f"Samples: {data_info['n_samples']}")
    st.write(f"Features: {data_info['n_features']}")
```

## Dataset Toggle Pattern

### Config Page Implementation

```python
# ui/pages/config.py
import streamlit as st
from ui.utils.data_loader import load_and_preprocess_data

def config_page():
    st.title("⚙️ Configuration")
    
    # Dataset selector
    use_full = st.toggle(
        "Use Full Dataset",
        value=st.session_state.data["data_info"].get("is_full_dataset", False),
        key="use_full_dataset"
    )
    
    # Reload if toggle changed
    if use_full != st.session_state.data["data_info"].get("is_full_dataset", False):
        with st.spinner("Loading dataset..."):
            X, y, features, info = load_and_preprocess_data(use_full=use_full)
            st.session_state.data.update({
                "X": X,
                "y": y,
                "feature_names": features,
                "data_info": info,
                "is_loaded": True
            })
        st.success(f"Loaded {'full' if use_full else 'small'} dataset: {info['n_samples']} samples")
    
    # Show dataset info
    if st.session_state.data["is_loaded"]:
        info = st.session_state.data["data_info"]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Samples", info["n_samples"])
        col2.metric("Features", info["n_features"])
        col3.metric("Classes", len(info["class_names"]))
        
        # Class distribution
        st.subheader("Class Distribution")
        for cls, count in info["class_distribution"].items():
            pct = count / info["n_samples"] * 100
            st.write(f"**{cls}**: {count} ({pct:.1f}%)")
```

## Train/Test Split Pattern

### Integrated with CV Strategy

```python
def get_train_test_split(cv_strategy="train_test", n_folds=5, random_state=42):
    """
    Get train/test split based on CV strategy
    
    Args:
        cv_strategy: "train_test" or "kfold"
        n_folds: Number of folds for k-fold CV
        random_state: Random seed
    
    Returns:
        If train_test: (X_train, X_test, y_train, y_test)
        If kfold: KFold object
    """
    X, y, _, _ = get_data()
    
    if cv_strategy == "train_test":
        return train_test_split(X, y, test_size=0.2, random_state=random_state)
    else:
        from sklearn.model_selection import KFold
        return KFold(n_splits=n_folds, shuffle=True, random_state=random_state)
```

### Usage in Training

```python
def train_model():
    cv_strategy = st.session_state.config["cv_strategy"]
    
    if cv_strategy == "train_test":
        X_train, X_test, y_train, y_test = get_train_test_split()
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        metrics = calculate_metrics(y_test, y_pred)
    
    else:  # K-Fold
        from sklearn.model_selection import cross_val_score
        X, y, _, _ = get_data()
        
        scores = cross_val_score(
            model, X, y,
            cv=st.session_state.config["n_folds"],
            scoring='accuracy'
        )
        
        metrics = {
            "accuracy": scores.mean(),
            "std": scores.std()
        }
```

## Caching Expensive Data Operations

### Pattern: Cache with Hash

```python
import streamlit as st
import hashlib

@st.cache_data
def load_and_preprocess_cached(filepath, use_categorical):
    """Cache data loading based on filepath and options"""
    df = pd.read_csv(filepath)
    # ... preprocessing ...
    return X, y, features, info

# Usage
X, y, features, info = load_and_preprocess_cached(
    "data/bank.csv",
    use_categorical=False
)
```

### Cache Invalidation Strategy

```python
# When data options change, pass as parameters to force recache
def reload_data(use_full, use_categorical):
    # Different parameters = different cache entry
    return load_and_preprocess_cached(
        "data/bank_full.csv" if use_full else "data/bank.csv",
        use_categorical
    )
```

## Data Validation

### Validation Function

```python
def validate_data(X, y):
    """Validate loaded data"""
    assert X.shape[0] == y.shape[0], "X and y must have same length"
    assert X.shape[0] > 0, "Dataset is empty"
    assert X.shape[1] > 0, "No features found"
    assert not np.isnan(X).any(), "X contains NaN values"
    assert not np.isnan(y).any(), "y contains NaN values"
    return True
```

### Usage

```python
def load_and_preprocess_data(...):
    # ... loading code ...
    
    # Validate before returning
    validate_data(X_scaled, y)
    
    return X_scaled, y, feature_names, data_info
```

## Feature Subset Selection

### Pattern: User-Selectable Features

```python
def select_features_ui():
    """UI for feature selection"""
    _, _, feature_names, _ = get_data()
    
    selected_features = st.multiselect(
        "Select Features",
        options=feature_names,
        default=feature_names[:5],  # First 5 by default
        key="selected_features"
    )
    
    return selected_features

def get_filtered_data():
    """Get data with only selected features"""
    X, y, feature_names, info = get_data()
    
    selected = st.session_state.get("selected_features", feature_names)
    selected_indices = [feature_names.index(f) for f in selected]
    
    X_filtered = X[:, selected_indices]
    
    return X_filtered, y, selected, info
```

## Key Takeaways

1. **Centralized Loader**: Single `data_loader.py` for all data operations
2. **Auto-Load**: Load data on app initialization for immediate availability
3. **Helper Function**: `get_data()` for convenient access across components
4. **State Storage**: Store in `st.session_state.data` dictionary
5. **Cache Operations**: Use `@st.cache_data` for expensive preprocessing
6. **Validate Data**: Always validate after loading
7. **Metadata**: Return `data_info` dict with useful information
8. **Consistent Interface**: All pages use same `get_data()` function

