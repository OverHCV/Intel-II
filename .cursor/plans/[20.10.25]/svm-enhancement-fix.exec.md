# SVM Enhancement & Fix - Execution Plan

**STATUS_POINTER** = obj_1: IMPLEMENT: cv_fix

---

## IMPLEMENT obj_1: Fix Cross-Validation Logic

IN(
  @model_config.py,
  @evaluator.py,
  @sidebar.py
)
OUT(
  @model_config.py (modified),
  session_state structure (y_proba added)
)

### UNDERSTAND IN(@model_config.py:145-166, @evaluator.py:14-138) OUT(cv_bug_analysis)

**Current Bug** (lines 145-152):
```python
else:
    # K-Fold CV
    n_folds = get_config("n_folds")
    
    model.fit(X, y)  # ❌ Fits once on ALL data
    cv_scores = cross_val_score(model, X, y, cv=n_folds, scoring="accuracy")
```

**Why it's wrong**:
- Model fitted ONCE on full dataset (fast: 0.5-4s)
- cross_val_score ignores pre-fitted model, does internal CV
- Predictions use full training data (data leakage)
- Training time doesn't reflect K-fold cost

**Correct approach**:
- Use `cross_val_predict` for held-out predictions (proper CV)
- Use `cross_val_score` for metrics (no pre-fit needed)
- For final model: fit on full data AFTER CV evaluation
- Store probability predictions for ROC curves

**Note**: evaluator.py has `kfold_cross_validation` function but not currently used

### ANALYZE IN(cv_bug_analysis, user_requirements) OUT(implementation_strategy)

**User Requirements** (from plan lines 131-132):
> "make it default for train/test mode, but in k-fold is on the slider a selectable with default as that predict_proba or select to 'Fit all'"

**Implementation Strategy**:
1. For **train/test mode**: No changes needed (already correct)
2. For **K-Fold mode**: Add option to choose prediction source:
   - Option A (default): "CV Predictions" - use cross_val_predict (proper held-out)
   - Option B: "Fit All Data" - fit on full dataset after CV (current behavior but explicit)
3. Always store probability predictions (`predict_proba`) for ROC curves
4. Fix timing to reflect actual computational cost

**Validation**:
- 10-fold CV on 5K samples should take ~8-15 seconds (realistic)
- Predictions are from held-out folds (no data leakage)
- Probabilities available for ROC curves

### CREATE IN(implementation_strategy) OUT(@model_config.py)

**Changes to model_config.py**:

1. **Add prediction mode selector** (K-Fold only):
```python
if cv_strategy == "kfold":
    prediction_mode = st.radio(
        "Predictions for Visualization",
        options=["cv_predict", "fit_all"],
        format_func=lambda x: "CV Predictions (held-out)" if x == "cv_predict" else "Fit All Data",
        index=0,
        help="CV Predictions: proper cross-validated held-out predictions. Fit All: train on full dataset after CV."
    )
```

2. **Fix K-Fold CV logic** (lines 144-166):
```python
else:
    # K-Fold CV
    n_folds = get_config("n_folds")
    prediction_mode = ...  # from UI control above
    
    # Get CV scores (no pre-fit needed)
    cv_scores = cross_val_score(model, X, y, cv=n_folds, scoring="accuracy")
    
    # Get predictions based on mode
    if prediction_mode == "cv_predict":
        # Proper held-out predictions from CV
        from sklearn.model_selection import cross_val_predict
        y_pred = cross_val_predict(model, X, y, cv=n_folds)
        
        # For probabilities (ROC curve)
        try:
            y_proba = cross_val_predict(model, X, y, cv=n_folds, method='predict_proba')
        except:
            y_proba = None
            
        # Fit final model on all data for saving
        model.fit(X, y)
    else:
        # Fit on all data (explicit choice)
        model.fit(X, y)
        y_pred = model.predict(X)
        try:
            y_proba = model.predict_proba(X)
        except:
            y_proba = None
    
    metrics = {
        "CV Accuracy": cv_scores.mean(),
        "CV Std": cv_scores.std(),
        "Min Fold": cv_scores.min(),
        "Max Fold": cv_scores.max(),
    }
    
    st.session_state.svm["y_true"] = y
    st.session_state.svm["y_pred"] = y_pred
    st.session_state.svm["y_proba"] = y_proba  # NEW: for ROC curves
```

3. **Add probabilities for train/test mode** (lines 111-142):
```python
if cv_strategy == "train_test":
    # ... existing code ...
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    # Add probabilities for ROC curve
    try:
        y_proba = model.predict_proba(X_test)
    except:
        y_proba = None
    
    # ... metrics calculation ...
    
    st.session_state.svm["y_true"] = y_test
    st.session_state.svm["y_pred"] = y_pred
    st.session_state.svm["y_proba"] = y_proba  # NEW: for ROC curves
```

4. **Add prediction_mode to experiment** (line 191):
```python
experiment = {
    "id": len(st.session_state.svm["experiment_history"]) + 1,
    "kernel": kernel,
    "C": C,
    "gamma": str(gamma),
    "degree": degree if kernel == SVMKernel.POLY else "-",
    "cv_strategy": cv_strategy,
    "prediction_mode": prediction_mode if cv_strategy == "kfold" else "N/A",  # NEW
    "metrics": metrics.copy(),
    "training_time": training_time,
}
```

### VALIDATE IN(@model_config.py) OUT(validation_results)

**Acceptance Criteria**:
- [ ] K-Fold CV with 10 folds on 5K samples takes ~8-15 seconds (not < 1s)
- [ ] Predictions are from held-out folds when "CV Predictions" selected
- [ ] Probabilities stored in session_state for ROC curves
- [ ] User can choose between CV predictions and Fit All
- [ ] Default is "CV Predictions" (proper CV methodology)

---

## IMPLEMENT obj_2: Match ANN UI Layout

IN(
  @svm/tab.py,
  @ann/tab.py (reference),
  @svm/components/visualizations.py
)
OUT(
  @svm/tab.py (modified),
  @svm/components/visualizations.py (modified)
)

### UNDERSTAND IN(@ann/tab.py:36-43) OUT(ann_layout_pattern)

**ANN Layout Structure**:
```python
# Two-column layout: controls on left, visualizations on right
col_controls, col_viz = st.columns([1, 2])

with col_controls:
    render_model_configuration(X, y, data_info)

with col_viz:
    render_visualizations(X, y, data_info)
```

**Benefits**:
- Compact controls on left (1/3 width)
- Large visualization area on right (2/3 width)
- Side-by-side confusion matrix + metrics
- Better use of horizontal space

### CREATE IN(ann_layout_pattern) OUT(@svm/tab.py, @svm/visualizations.py)

**Modify svm/tab.py** (lines 36-49):
```python
# Documentation Section
render_svm_documentation()

st.divider()

# Two-column layout: controls on left, visualizations on right
col_controls, col_viz = st.columns([1, 2])

with col_controls:
    render_model_configuration()

with col_viz:
    render_visualizations()

# Experiment History Section (full width)
render_experiment_history(st.session_state.svm)

# Save Best Model Section (full width)
render_best_model_saver()
```

**Modify svm/visualizations.py**:
- Remove expander from model_configuration (now in column)
- Keep side-by-side confusion matrix + metrics
- Prepare for ROC curve below

### VALIDATE IN(@svm/tab.py) OUT(layout_validation)

**Acceptance Criteria**:
- [ ] SVM layout matches ANN structure
- [ ] Controls in left column (1/3 width)
- [ ] Visualizations in right column (2/3 width)
- [ ] Confusion matrix and metrics side-by-side
- [ ] Experiment history full-width below

---

## IMPLEMENT obj_3: Add ROC AUC Curve Visualization

IN(
  @funcs/visual/basic_visuals.py,
  @svm/components/visualizations.py,
  session_state.svm (with y_proba)
)
OUT(
  @funcs/visual/basic_visuals.py (new function),
  @svm/components/visualizations.py (ROC display)
)

### CREATE IN(@basic_visuals.py) OUT(plot_roc_curve function)

**Add new function to basic_visuals.py**:
```python
def plot_roc_curve(y_true, y_proba, title="ROC Curve"):
    """
    Plot ROC curve with AUC score
    
    Args:
        y_true: True labels
        y_proba: Probability predictions (n_samples, n_classes) or (n_samples,) for binary
        title: Plot title
        
    Returns:
        matplotlib Figure or None if not binary classification
    """
    from sklearn.metrics import roc_curve, auc
    
    # Check if binary classification
    unique_classes = np.unique(y_true)
    if len(unique_classes) != 2:
        return None
    
    # Get probabilities for positive class
    if y_proba.ndim == 2:
        y_score = y_proba[:, 1]  # Probability of positive class
    else:
        y_score = y_proba
    
    # Calculate ROC curve
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)
    
    # Create plot
    fig, ax = plt.subplots(figsize=CONF[Keys.FIGURE_SIZE_SMALL])
    
    # Plot ROC curve
    ax.plot(fpr, tpr, color='darkorange', lw=2, 
            label=f'ROC curve (AUC = {roc_auc:.3f})')
    
    # Plot diagonal reference line
    ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', 
            label='Random Classifier')
    
    # Styling
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate', fontsize=11)
    ax.set_ylabel('True Positive Rate', fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.legend(loc="lower right", fontsize=10)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    return fig
```

### INTEGRATE IN(plot_roc_curve, @svm/visualizations.py) OUT(@svm/visualizations.py)

**Add ROC curve display** (after confusion matrix + metrics):
```python
def _render_model_performance():
    """Render Model Performance with confusion matrix, metrics, and ROC curve"""
    X, y, feature_names, data_info = get_data()
    y_true = st.session_state.svm["y_true"]
    y_pred = st.session_state.svm["y_pred"]
    y_proba = st.session_state.svm.get("y_proba", None)
    
    if data_info:
        labels = data_info["classes"]
    else:
        labels = ["Class 0", "Class 1"]
    
    # Side-by-side: confusion matrix + metrics
    col_cm, col_metrics = st.columns([1.2, 1])
    
    with col_cm:
        fig_cm = plot_confusion_matrix(y_true, y_pred, labels=labels)
        st.pyplot(fig_cm)
    
    with col_metrics:
        metrics = st.session_state.svm["metrics"]
        plot_metrics = {k: v for k, v in metrics.items() if 0 <= v <= 1}
        
        if plot_metrics:
            fig_metrics = plot_metrics_bars(plot_metrics)
            st.pyplot(fig_metrics)
    
    st.caption(f"⏱️ Training time: {st.session_state.svm['training_time']:.2f}s")
    
    # ROC Curve (full width below)
    if y_proba is not None:
        st.markdown("---")
        st.markdown("**ROC Curve**")
        
        from funcs.visual.basic_visuals import plot_roc_curve
        fig_roc = plot_roc_curve(y_true, y_proba, title="Receiver Operating Characteristic")
        
        if fig_roc:
            st.pyplot(fig_roc)
        else:
            st.info("ROC curve only available for binary classification")
    else:
        st.caption("💡 ROC curve requires probability predictions")
```

### VALIDATE IN(@svm/visualizations.py) OUT(roc_validation)

**Acceptance Criteria**:
- [ ] ROC curve displays below confusion matrix + metrics
- [ ] AUC score shown in legend
- [ ] Diagonal reference line visible
- [ ] Works with both train/test and K-Fold CV
- [ ] Gracefully handles multi-class (shows message)
- [ ] Only displays when probabilities available

---

## POST_CHANGE_VALIDATION

**System Coherence Check**:
- [ ] Run Streamlit app: `streamlit run ui/app.py`
- [ ] Navigate to SVM tab
- [ ] Test train/test mode: Fast training, ROC curve appears
- [ ] Test K-Fold mode with 10 folds: Slower training (~8-15s on 5K)
- [ ] Test prediction mode selector: CV Predictions vs Fit All
- [ ] Verify layout matches ANN structure
- [ ] Check experiment history displays correctly
- [ ] No console errors or warnings

---

## COMPLETED

**STATUS_POINTER** = "COMPLETED: ALL OBJECTIVES"

**Final Outputs**:
- @model_config.py: Fixed CV logic, prediction mode selector, probability storage
- @svm/tab.py: 2-column layout matching ANN
- @svm/visualizations.py: ROC curve display
- @funcs/visual/basic_visuals.py: plot_roc_curve function

**Performance Expectations**:
- Small dataset (5K) + 10-fold CV: ~8-15 seconds ✅
- Train/Test split: ~0.5-2 seconds ✅
- ROC curves displaying correctly ✅
- Layout consistent with ANN ✅

