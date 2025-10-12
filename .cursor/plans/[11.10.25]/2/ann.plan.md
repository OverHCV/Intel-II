# ANN Section Implementation Plan 🧠

> **Goal**: Implement a comprehensive, modular, and professional ANN interface matching the quality of the SVM section

---

## CONTEXT

```parlang
CONTEXT IN(@svm/, @6-ANN.ipynb, @ann/tab.py, @parlang-guide.md) OUT(environment_map) {
  project: [Streamlit ML Analysis Dashboard, Python, scikit-learn MLPClassifier],
  
  rules: [
    @parlang-guide.md - methodology to follow,
    @svm/ - reference architecture (mirror this structure),
    @README.md - task requirements (0.9 points for ANN)
  ],
  
  current_state: [
    @ann/tab.py - basic implementation (216 LOC, NOT modular),
    @6-ANN.ipynb - theory and documentation source,
    @funcs/visualizers.py - shared visualization functions,
    @ui/components/ - reusable UI components available
  ],
  
  reference_quality: [@svm/ section - THIS is our standard],
  
  constraints: [
    "Match SVM interface quality and organization",
    "NO 2D/3D scatter plots (those are for PCA section)",
    "NO distribution/correlation graphs (those are for PCA)",
    "Focus ONLY on ANN-specific analysis",
    "Graphs side-by-side (confusion matrix + metrics bar)",
    "Experiment history must be persistent (JSON files)",
    "Keep code modular (<100 LOC per file ideal)"
  ]
}
```

---

## OBJECTIVES

```parlang
OBJECTIVES as obj OUT(goal_list) [
  "theory_and_docs": {
    why: "Users need to understand ANN theory before using the tool",
    DoD: "
      - README.md in ui/pages/ann/ with comprehensive ANN theory
      - Theory from @6-ANN.ipynb translated to markdown
      - Includes: perceptron, activation functions, backpropagation
      - Math equations rendered properly
      - Architecture visualization concepts explained
      - Similar to svm/README.md structure
    "
  },
  
  "modularize_components": {
    why: "tab.py is 216 LOC, violates modularity (should be <100)",
    DoD: "
      - ui/pages/ann/components/__init__.py created
      - ui/pages/ann/components/model_config.py (architecture, activation, solver controls)
      - ui/pages/ann/components/visualizations.py (confusion matrix + metrics side-by-side)
      - ui/pages/ann/components/best_model_saver.py (save best for PCA)
      - ui/pages/ann/tab.py reduced to <50 LOC (orchestrator only)
      - Each component file <150 LOC
    "
  },
  
  "experiment_history": {
    why: "Users need to compare runs across sessions (persistent storage)",
    DoD: "
      - ui/pages/ann/experiments.py created (like svm/experiments.py)
      - Renders experiment history table with all runs
      - Shows: ID, architecture, activation, solver, accuracy, precision, recall, f1
      - Comparison chart: accuracy across experiments
      - Clear History button with confirmation
      - Save to JSON file in .cache/ (persistent)
      - Auto-load from JSON on startup
      - Integrate with state_manager.py for loading
    "
  },
  
  "improve_visualizations": {
    why: "Current layout has graphs stacked vertically (UGLY)",
    DoD: "
      - Confusion matrix + metrics bar chart in same row (st.columns(2))
      - Reduce graph sizes to fit side-by-side
      - Clean, professional layout
      - Similar to svm visualizations but WITHOUT extra tabs
      - NO Feature Analysis tab (not ANN-specific)
      - NO Data Exploration tab (not ANN-specific)
      - Just: Model Performance view
    "
  },
  
  "fix_metrics_calculation": {
    why: "Need proper handling for imbalanced datasets (like SVM fix)",
    DoD: "
      - Use average='weighted' for multi-class
      - Use average='binary' for two classes
      - Add zero_division=0 parameter
      - Handle class imbalance properly
      - Calculate metrics on TEST set (not train)
    "
  },
  
  "best_model_clarity": {
    why: "User needs to know which experiment is being saved",
    DoD: "
      - Auto-identify best experiment from history
      - Display best experiment details (ID, architecture, metrics)
      - Button shows: 'Save Best Model (Exp #X)'
      - Retrain on full dataset before saving
      - Clear feedback when saved
      - Similar to svm/components/best_model_saver.py
    "
  },
  
  "documentation_component": {
    why: "Theory should be accessible within the interface",
    DoD: "
      - ui/pages/ann/docs.py created
      - render_ann_documentation() function
      - Expandable section with theory
      - Links to README.md for full details
      - Similar to svm/docs.py
    "
  },
  
  "deprecation_fixes": {
    why: "Fix Streamlit warnings (use_container_width deprecated)",
    DoD: "
      - Replace all use_container_width with width='stretch'
      - No deprecation warnings in console
    "
  }
]
```

---

## DEPENDENCIES

```parlang
DEPENDENCIES [
  obj["theory_and_docs"] BLOCKS obj["documentation_component"],
  obj["modularize_components"] REQUIRES obj["improve_visualizations"],
  obj["experiment_history"] REQUIRES obj["fix_metrics_calculation"],
  obj["best_model_clarity"] REQUIRES obj["experiment_history"]
]
```

**Execution Order:**

1. ✅ Theory & Docs (can start immediately)
2. ✅ Fix metrics calculation (foundational)
3. ✅ Improve visualizations (needed for modularization)
4. ✅ Modularize components (structure)
5. ✅ Experiment history (persistence)
6. ✅ Best model clarity (depends on history)
7. ✅ Documentation component (integrates theory)
8. ✅ Deprecation fixes (polish)

---

## ARCHITECTURE

### Target File Structure

```
ui/pages/ann/
├── __init__.py
├── README.md                  # NEW: Comprehensive ANN theory guide
├── tab.py                     # REFACTOR: <50 LOC (orchestrator)
├── docs.py                    # NEW: Theory documentation component
├── experiments.py             # NEW: Experiment history with persistence
└── components/
    ├── __init__.py            # NEW: Export all components
    ├── model_config.py        # NEW: Architecture, activation, solver controls
    ├── visualizations.py      # NEW: Side-by-side graphs
    └── best_model_saver.py    # NEW: Save best model for PCA
```

### Component Responsibilities

**tab.py** (Orchestrator - <50 LOC)

```python
def ann_page():
    st.title("🧠 ANN")
    X, y, feature_names, data_info = get_data()
    
    render_ann_documentation()  # Theory expander
    
    col_controls, col_viz = st.columns([1, 2])
    with col_controls:
        render_model_configuration(X, y, data_info)
    with col_viz:
        render_visualizations(X, y, data_info)
    
    render_experiment_history(st.session_state.ann)
    render_best_model_saver(X, y, data_info)
```

**components/model_config.py** (~150 LOC)

- Architecture selector
- Activation function selector
- Solver selector
- Max iterations slider
- Train button
- Training logic
- Metrics calculation (weighted averaging)
- Save to experiment history

**components/visualizations.py** (~80 LOC)

- Side-by-side layout: col1, col2 = st.columns(2)
- Col1: Confusion matrix
- Col2: Metrics bar chart
- Training time caption
- No redundant metrics display

**experiments.py** (~120 LOC)

- Load experiments from JSON on init
- Display experiment table
- Comparison chart (accuracy over time)
- Clear History button
- Save to .cache/ann_experiments.json
- Similar to svm/experiments.py

**components/best_model_saver.py** (~100 LOC)

- Get best experiment from history
- Display best experiment details
- Button: "💾 Save Best Model (Exp #X)"
- Retrain on full dataset
- Save to session state
- Similar to svm/components/best_model_saver.py

**docs.py** (~50 LOC)

- Expandable theory section
- Summary of ANN concepts
- Link to README.md

**README.md** (Theory Guide)

- Neural network fundamentals
- Activation functions (ReLU, tanh, logistic)
- Backpropagation algorithm
- Architecture considerations
- MLPClassifier parameters
- When to use different solvers
- Translated from @6-ANN.ipynb

---

## IMPLEMENTATION DETAILS

### 1. Theory Content (from @6-ANN.ipynb)

**Key Concepts to Include:**

1. **Linear Discriminant with Activation**
   ```
   d_i = activation(w^T * φ(x_i))
   ```


            - Replace sign() with differentiable activation
            - Enable gradient descent

2. **Activation Functions**

            - Sign function (non-differentiable)
            - Tanh: tanh(x)
            - Sigmoid: σ(x) = 1/(1+e^(-x))
            - ReLU (modern standard)

3. **Neural Network Architecture**

            - Input layer → Hidden layers → Output layer
            - Each neuron: weighted sum + activation
            - Multi-layer perceptron (MLP) / Feedforward
            - Parameters: all weights across all layers

4. **Backpropagation**

            - Gradient descent for all layers
            - Chain rule for derivatives
            - Forward pass: compute activations
            - Backward pass: propagate errors
            - Update weights using gradients

5. **MLPClassifier Parameters**

            - hidden_layer_sizes: architecture (e.g., (10,), (20,10), (50,30,10))
            - activation: 'relu', 'tanh', 'logistic'
            - solver: 'adam' (adaptive), 'sgd' (stochastic), 'lbfgs' (quasi-Newton)
            - max_iter: training iterations
            - alpha: L2 regularization
            - learning_rate: 'constant', 'adaptive', 'invscaling'

### 2. Metrics Calculation Fix

```python
# Calculate metrics with weighted averaging for imbalanced data
import numpy as np

n_classes = len(np.unique(y))
avg_strategy = "binary" if n_classes == 2 else "weighted"

metrics = {
    "Accuracy": accuracy_score(y_test, y_pred),
    "Precision": precision_score(y_test, y_pred, average=avg_strategy, zero_division=0),
    "Recall": recall_score(y_test, y_pred, average=avg_strategy, zero_division=0),
    "F1-Score": f1_score(y_test, y_pred, average=avg_strategy, zero_division=0),
}
```

### 3. Visualization Layout

```python
# Side-by-side graphs
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Confusion Matrix**")
    fig_cm = plot_confusion_matrix(y_true, y_pred, labels)
    st.pyplot(fig_cm)

with col2:
    st.markdown("**Performance Metrics**")
    fig_metrics = plot_metrics_bars(metrics)
    st.pyplot(fig_metrics)

st.caption(f"⏱️ Training time: {training_time:.2f}s")
```

### 4. Experiment History Structure

```python
# Experiment object
experiment = {
    "id": len(history) + 1,
    "timestamp": datetime.now().isoformat(),
    "architecture": tuple,  # e.g., (20, 10)
    "activation": str,      # 'relu', 'tanh', 'logistic'
    "solver": str,          # 'adam', 'sgd', 'lbfgs'
    "max_iter": int,
    "metrics": {
        "accuracy": float,
        "precision": float,
        "recall": float,
        "f1_score": float,
    },
    "training_time": float,
    "cv_strategy": str,     # 'train_test' or 'kfold'
}

# Save to .cache/ann_experiments.json
save_experiments_to_file(history, "ann")
```

### 5. Architecture Options

```python
# ui/settings/config.py
ANN_ARCHITECTURES = [
    (10,),           # 1 hidden layer, 10 neurons
    (20,),           # 1 hidden layer, 20 neurons
    (50,),           # 1 hidden layer, 50 neurons
    (20, 10),        # 2 hidden layers
    (50, 30),        # 2 hidden layers
    (50, 30, 10),    # 3 hidden layers
    (100, 50, 20),   # 3 hidden layers (deep)
]
```

---

## ASK Questions

```parlang
ASK USER {
  Q1: "Should we include a learning curve visualization (loss over iterations)?
       - PRO: Shows convergence, helps debug
       - CON: Adds complexity, not in SVM
       - RECOMMENDATION: Skip for now, add in PCA section if needed", 
> Think that yes, don't have clear what's the difference to do it in PCA
> if we can do it earlier better

  Q2: "Should we allow custom architecture input or just predefined options?
       - PRO: More flexibility
       - CON: Can break with invalid inputs
       - RECOMMENDATION: Predefined dropdown (like kernel selector)",

> I mean, I'ld love an input text so I can put the (a,b,c, ...) values in tuple correctly, else send an error validator message
> But if you think is EXTREMELY complex to allow that (and will always crash) maybe we do it on a next feature and keep it selectable then.
  
  Q3: "Should experiment history show architecture as tuple or formatted string?
       - Option A: (20, 10) - raw
       - Option B: '20 → 10' - readable
       - RECOMMENDATION: Formatted string for better UX",

> Silly question, tuple as program is intended for programmers (me)
  
  Q4: "Confirm: NO Feature Analysis tab, NO Data Exploration tab for ANN?
       - These are dataset-level, not model-specific
       - Should live in PCA section
       - CONFIRM: Correct, skip for ANN",
}

> Skip for ann!
```

---

## RISK ANALYSIS

**High Risk:**

- ⚠️ **Long training times** for deep architectures
        - Mitigation: Show progress spinner, add training time estimates
        - Mitigation: Default to moderate architectures (20, 10) # As I told you, if is possible to set the tuple dinamically I can put it and this just trains the network with that size.

- ⚠️ **MLPClassifier convergence warnings**
        - Mitigation: Suppress warnings or increase max_iter
        - Mitigation: Show convergence status in UI

**Medium Risk:**

- ⚠️ **Experiment history grows large over time**
        - Mitigation: Implement pagination for history table	# What? I mean one execution should create one experiment, no? If in ANN you're doing it bad then that thing grows exponentially I guess?? But if you refered to making lots of experiments make a long table then two options.
# B. You don't care, I delete the table and reset it's content anyway. A. You make pagination.
# So you decide, is simple.  
        - Mitigation: Add "Export to CSV" option		# Review my previous comment!

**Low Risk:**

- ⚠️ **Metrics calculation on wrong split**
        - Mitigation: Clear comments, code review
        - Mitigation: Follow SVM pattern exactly	# Not exactly, we're now with ANN so maybe one or two things change! The architecture/folders/files is the thing I think we can most reproduce.

---

## SUCCESS CRITERIA

### Code Quality

- ✅ tab.py < 50 LOC
- ✅ All component files < 200 LOC
- ✅ 0 linting errors
- ✅ 0 deprecation warnings
- ✅ Proper type hints and docstrings

### Functionality

- ✅ Theory documentation accessible and complete
- ✅ Multiple architectures and activations testable
- ✅ Experiment history persists across sessions
- ✅ Graphs display side-by-side cleanly
- ✅ Best model saving works correctly
- ✅ Metrics calculated properly for imbalanced data

### UX

- ✅ Interface matches SVM quality
- ✅ No redundant information
- ✅ Clear visual hierarchy
- ✅ Responsive layout
- ✅ Helpful tooltips and captions

### Testing

- ✅ Train with different architectures
- ✅ Train with different activations
- ✅ Train with different solvers
- ✅ Experiment history loads correctly
- ✅ Clear history works
- ✅ Save best model works
- ✅ Reload app → history persists

---

## NOTES

### Why NO Feature Analysis/Exploration?

These tabs were added to SVM but are actually **dataset-level analysis**, not model-specific:

- **Feature correlation** → Dataset property
- **Distribution plots** → Dataset property
- **2D/3D scatter** → Dataset visualization
- **Normality tests** → Dataset property

**Correct placement**: PCA section (where we analyze the dataset and compare before/after PCA)

**ANN-specific analysis**:

- Confusion matrix ✅
- Performance metrics ✅
- Architecture comparison ✅
- Activation function comparison ✅

### Lessons from SVM Implementation

**What worked well:**

- ✅ Modular component structure
- ✅ Persistent experiment history
- ✅ Clear best model saving
- ✅ Side-by-side visualizations
- ✅ Theory documentation

**What to improve:**

- ⚠️ Maybe too many visualization tabs (Feature Analysis, Data Exploration)
- ⚠️ Some graphs not model-specific
- ✅ Solution: Keep ANN focused on model analysis only

---

## EXECUTION READINESS

**Ready to execute?** ✅ YES

- [x] Context is clear
- [x] Objectives are well-defined
- [x] Dependencies are mapped
- [x] Architecture is designed
- [x] Implementation details are specified
- [x] Reference implementation exists (@svm/)
- [x] Theory source is available (@6-ANN.ipynb)

**Estimated Time:** 2-3 hours

**Estimated Tool Calls:** 40-60

**Expected Outcome:** Professional, modular ANN interface matching SVM quality

---

## FINAL CHECKLIST

Before marking complete, verify:

- [ ] README.md in ann/ folder with theory	# NO, the theory is in a file so is displayable. The README intention is a user-guide of how to use the tab and achieve great results.
- [ ] docs.py with expandable documentation
- [ ] tab.py reduced to <50 LOC		# Depends, just follow @rules so files aren't greater than 300 LOC, if less better.
- [ ] model_config.py created and working
- [ ] visualizations.py with side-by-side layout
- [ ] best_model_saver.py created and working
- [ ] experiments.py with persistence
- [ ] Metrics use weighted averaging
- [ ] Experiment history persists across sessions
- [ ] No deprecation warnings
- [ ] 0 linting errors		# Always check for errors when working, that should be something you do on the exec file!
- [ ] All graphs display correctly
- [ ] Best model saving works
- [ ] Interface matches SVM quality

---

**Status:** 🟢 PLAN APPROVED - READY FOR EXECUTION

**Next Step:** Create ann.exec.md and begin implementation