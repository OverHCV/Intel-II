# Streamlit Experiment Tracking & Persistence

## JSON-Based Persistence Pattern

### Why JSON?

- Human-readable
- Easy to debug
- No database setup required
- Survives app restarts
- Portable across environments

### Folder Structure

```
project/
├── .cache/                    # Gitignored
│   ├── svm_experiments.json
│   ├── ann_experiments.json
│   └── pca_experiments.json
├── funcs/
│   └── persistence.py        # Persistence utilities
└── ui/
    └── pages/
        ├── svm/
        │   └── experiments.py  # SVM experiment display
        └── ann/
            └── experiments.py  # ANN experiment display
```

### Persistence Module

```python
# funcs/persistence.py
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Cache directory
CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)

def save_experiments_to_file(experiments: List[Dict], model_type: str = "svm"):
    """
    Save experiments to JSON file
    
    Args:
        experiments: List of experiment dictionaries
        model_type: "svm", "ann", or "pca"
    """
    filepath = CACHE_DIR / f"{model_type}_experiments.json"
    
    # Wrap with metadata
    data = {
        "timestamp": datetime.now().isoformat(),
        "model_type": model_type,
        "count": len(experiments),
        "experiments": experiments
    }
    
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to save experiments: {e}")

def load_experiments_from_file(model_type: str = "svm") -> List[Dict]:
    """
    Load experiments from JSON file
    
    Args:
        model_type: "svm", "ann", or "pca"
    
    Returns:
        List of experiment dictionaries (empty list if file doesn't exist)
    """
    filepath = CACHE_DIR / f"{model_type}_experiments.json"
    
    if not filepath.exists():
        return []
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            return data.get("experiments", [])
    except Exception as e:
        print(f"Failed to load experiments: {e}")
        return []

def clear_experiments_file(model_type: str = "svm"):
    """Clear experiments file"""
    filepath = CACHE_DIR / f"{model_type}_experiments.json"
    
    if filepath.exists():
        filepath.unlink()

def export_experiments_to_csv(experiments: List[Dict], output_path: str):
    """Export experiments to CSV for analysis"""
    import pandas as pd
    
    df = pd.DataFrame(experiments)
    df.to_csv(output_path, index=False)
```

## Experiment Structure

### SVM Experiment

```python
experiment = {
    "id": 1,
    "timestamp": "2025-10-31T14:30:00",
    "kernel": "rbf",
    "C": 10.0,
    "gamma": "scale",
    "degree": 3,  # Only for poly
    "cv_strategy": "kfold",
    "n_folds": 5,
    "metrics": {
        "accuracy": 0.9567,
        "precision": 0.9423,
        "recall": 0.9612,
        "f1_score": 0.9516
    },
    "training_time": 2.34,
    "data_info": {
        "n_samples": 4521,
        "n_features": 7,
        "is_full_dataset": False
    }
}
```

### ANN Experiment

```python
experiment = {
    "id": 1,
    "timestamp": "2025-10-31T14:30:00",
    "architecture": (20, 10),  # Tuple of layer sizes
    "activation": "relu",
    "solver": "adam",
    "max_iter": 500,
    "cv_strategy": "kfold",
    "n_folds": 5,
    "metrics": {
        "accuracy": 0.9612,
        "precision": 0.9534,
        "recall": 0.9689,
        "f1_score": 0.9611
    },
    "training_time": 5.67,
    "converged": True
}
```

## Integration with Session State

### State Manager: Load on Init

```python
# ui/utils/state_manager.py
from funcs.persistence import load_experiments_from_file

def init_session_state():
    """Initialize session state on first app load"""
    
    # SVM state
    if "svm" not in st.session_state:
        st.session_state.svm = {
            "model": None,
            "is_trained": False,
            "metrics": {},
            "experiment_history": load_experiments_from_file("svm")  # ← Load from disk
        }
    
    # ANN state
    if "ann" not in st.session_state:
        st.session_state.ann = {
            "model": None,
            "is_trained": False,
            "metrics": {},
            "experiment_history": load_experiments_from_file("ann")  # ← Load from disk
        }
```

### Training: Save After Each Run

```python
# In training function
def train_svm(kernel, C, gamma, degree):
    # ... training code ...
    
    # Create experiment record
    experiment = {
        "id": len(st.session_state.svm["experiment_history"]) + 1,
        "timestamp": datetime.now().isoformat(),
        "kernel": kernel,
        "C": C,
        "gamma": gamma,
        "degree": degree,
        "metrics": metrics,
        "training_time": training_time
    }
    
    # Add to history
    st.session_state.svm["experiment_history"].append(experiment)
    
    # Persist to disk
    from funcs.persistence import save_experiments_to_file
    save_experiments_to_file(st.session_state.svm["experiment_history"], "svm")
```

## Experiment Display Component

### Experiments.py Structure

```python
# ui/pages/svm/experiments.py
import streamlit as st
import pandas as pd
from funcs.persistence import clear_experiments_file, save_experiments_to_file

def render_experiment_history(state_dict):
    """
    Render experiment history table and comparison
    
    Args:
        state_dict: st.session_state.svm or st.session_state.ann
    """
    history = state_dict["experiment_history"]
    
    if not history:
        st.info("No experiments yet. Train a model to start tracking.")
        return
    
    st.divider()
    st.subheader("📊 Experiment History")
    
    # Display as table
    _render_experiment_table(history)
    
    # Comparison chart
    _render_comparison_chart(history)
    
    # Statistics
    _render_statistics(history)
    
    # Clear button
    _render_clear_button(history)

def _render_experiment_table(history):
    """Display experiments as table"""
    # Convert to DataFrame
    df = pd.DataFrame(history)
    
    # Format columns
    if "metrics" in df.columns:
        df["Accuracy"] = df["metrics"].apply(lambda m: f"{m['accuracy']:.4f}")
        df["Precision"] = df["metrics"].apply(lambda m: f"{m['precision']:.4f}")
        df["Recall"] = df["metrics"].apply(lambda m: f"{m['recall']:.4f}")
        df["F1"] = df["metrics"].apply(lambda m: f"{m['f1_score']:.4f}")
    
    # Select display columns
    display_cols = ["id", "kernel", "C", "gamma", "Accuracy", "Precision", "Recall", "F1", "training_time"]
    display_df = df[[col for col in display_cols if col in df.columns]]
    
    st.dataframe(display_df, width="stretch")

def _render_comparison_chart(history):
    """Comparison chart of accuracy across experiments"""
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    exp_ids = [exp["id"] for exp in history]
    accuracies = [exp["metrics"]["accuracy"] for exp in history]
    
    # Find best
    best_idx = accuracies.index(max(accuracies))
    colors = ['green' if i == best_idx else 'steelblue' for i in range(len(accuracies))]
    
    ax.bar(exp_ids, accuracies, color=colors, alpha=0.7)
    ax.set_xlabel("Experiment ID")
    ax.set_ylabel("Accuracy")
    ax.set_title("Accuracy Comparison Across Experiments")
    ax.set_ylim(0, 1)
    ax.grid(axis='y', alpha=0.3)
    
    st.pyplot(fig)
    plt.close(fig)
    
    st.caption(f"🏆 Best: Experiment #{history[best_idx]['id']} with {accuracies[best_idx]:.4f} accuracy")

def _render_statistics(history):
    """Display summary statistics"""
    accuracies = [exp["metrics"]["accuracy"] for exp in history]
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Total Experiments", len(history))
    col2.metric("Best Accuracy", f"{max(accuracies):.4f}")
    col3.metric("Avg Accuracy", f"{sum(accuracies)/len(accuracies):.4f}")

def _render_clear_button(history):
    """Clear history button"""
    if st.button("🗑️ Clear History", key="clear_history"):
        if st.session_state.get("confirm_clear"):
            # Clear state
            st.session_state.svm["experiment_history"] = []
            
            # Clear file
            clear_experiments_file("svm")
            
            st.success("Experiment history cleared")
            st.rerun()
        else:
            st.session_state.confirm_clear = True
            st.warning("Click again to confirm")

def get_best_experiment(history):
    """
    Get best experiment from history
    
    Returns:
        (index, experiment_dict)
    """
    if not history:
        return None, None
    
    accuracies = [exp["metrics"]["accuracy"] for exp in history]
    best_idx = accuracies.index(max(accuracies))
    
    return best_idx, history[best_idx]
```

## Best Model Saving Pattern

### Automatic Best Selection

```python
# ui/pages/svm/components/best_model_saver.py
from ui.pages.svm.experiments import get_best_experiment

def render_best_model_saver(X, y, data_info):
    """Render best model saver"""
    
    history = st.session_state.svm["experiment_history"]
    
    if not history:
        return  # No experiments yet
    
    st.divider()
    st.subheader("💾 Save Best Model")
    
    # Auto-identify best
    best_idx, best_exp = get_best_experiment(history)
    
    # Show best info
    with st.container(border=True):
        st.markdown(f"**Best: Experiment #{best_exp['id']}**")
        st.write(f"Kernel: {best_exp['kernel']}, C: {best_exp['C']}")
        st.write(f"Accuracy: {best_exp['metrics']['accuracy']:.4f}")
    
    # Save button (shows which experiment)
    if st.button(
        f"💾 Save Best Model (Exp #{best_exp['id']})",
        key="save_best_model"
    ):
        with st.spinner(f"Retraining Experiment #{best_exp['id']}..."):
            # Retrain with best params
            model = _retrain_with_params(X, y, best_exp)
            
            # Save to state
            st.session_state.svm["best_model"] = {
                "model": model,
                "experiment_id": best_exp["id"],
                "params": best_exp,
                "metrics": best_exp["metrics"]
            }
        
        st.success(f"✅ Saved: Experiment #{best_exp['id']}")
        st.balloons()
```

## CSV Export Pattern

```python
def export_experiments():
    """Export experiments to CSV"""
    from funcs.persistence import export_experiments_to_csv
    
    history = st.session_state.svm["experiment_history"]
    
    if st.button("📥 Export to CSV"):
        output_path = "svm_experiments_export.csv"
        export_experiments_to_csv(history, output_path)
        st.success(f"Exported to {output_path}")
```

## Key Takeaways

1. **JSON Persistence**: Simple, human-readable, no database needed
2. **Load on Init**: `init_session_state()` loads from disk
3. **Save After Training**: Append + save after each experiment
4. **Metadata Wrapper**: Timestamp, count, model type in JSON
5. **Best Model Auto-Select**: Find best by accuracy automatically
6. **History Table**: Display with pandas DataFrame
7. **Comparison Chart**: Visual comparison across experiments
8. **Clear with Confirmation**: Two-click clear to prevent accidents
9. **Export Option**: CSV export for external analysis

