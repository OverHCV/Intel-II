# PCA Feature Mismatch Fix - Model Comparison

**Date**: October 20, 2025  
**Status**: ✅ FIXED  
**Error**: `ValueError: X has 16 features, but MLPClassifier is expecting 7 features as input`

---

## 🐛 PROBLEM IDENTIFIED

### Error Context:
```
ValueError: X has 16 features, but MLPClassifier is expecting 7 features as input.
Location: .jorge/partials/second/ui/pages/pca/components/model_comparison.py:432
Operation: y_pred_original = original_model.predict(X)
```

### Root Cause:
When a "best model" is saved for PCA comparison, it's trained on whatever data is currently loaded in the session state. If PCA has been applied before saving the model, the model is trained on PCA-transformed data (7 features). However, when the model comparison tries to evaluate the original model, it uses `get_data()` which returns the original full dataset (16 features).

**Timeline of the bug:**
1. User applies PCA transformation (16 → 7 features)
2. User trains a model on PCA-transformed data (7 features)
3. User saves best model → model.fit(X_pca_7_features, y)
4. User goes to PCA comparison tab
5. Code tries: `original_model.predict(X_original_16_features)` ❌

---

## ✅ SOLUTION IMPLEMENTED

### Strategy:
Track whether a saved model was trained on PCA data or not, and use the appropriate feature set for evaluation.

### Files Modified:

#### 1. `ui/pages/pca/components/model_comparison.py`

**Before:**
```python
def _render_confusion_matrices_comparison(model_type):
    X, y, _, data_info = get_data()
    
    if model_type == "svm":
        original_model = st.session_state.svm.get("best_model")
    else:
        original_model = st.session_state.ann.get("best_model")
    
    # ❌ Always uses original X (16 features)
    y_pred_original = original_model.predict(X)
```

**After:**
```python
def _render_confusion_matrices_comparison(model_type):
    X, y, _, data_info = get_data()
    
    if model_type == "svm":
        original_model = st.session_state.svm.get("best_model")
        trained_on_pca = st.session_state.svm.get("trained_on_pca", False)
    else:
        original_model = st.session_state.ann.get("best_model")
        trained_on_pca = st.session_state.ann.get("trained_on_pca", False)
    
    # ✅ Use appropriate feature set based on training
    if trained_on_pca:
        X_original = st.session_state.pca["X_pca"]  # 7 features
    else:
        X_original = X  # 16 features
    
    y_pred_original = original_model.predict(X_original)
```

#### 2. `ui/pages/ann/components/best_model_saver.py`

**Added tracking:**
```python
model.fit(X, y)

# Check if trained on PCA data
trained_on_pca = (
    st.session_state.pca.get("pca_applied", False) and 
    X.shape[1] == st.session_state.pca.get("n_components", 0)
)

# Save to session state
st.session_state.ann["best_model"] = model
st.session_state.ann["trained_on_pca"] = trained_on_pca  # ✅ NEW
```

**Logic:**
- Check if PCA has been applied: `pca_applied == True`
- Check if current X has PCA dimensions: `X.shape[1] == n_components`
- If both true → model trained on PCA data

#### 3. `ui/pages/svm/components/best_model_saver.py`

**Same tracking added:**
```python
model.fit(X, y)

# Check if trained on PCA data
trained_on_pca = (
    st.session_state.pca.get("pca_applied", False) and 
    X.shape[1] == st.session_state.pca.get("n_components", 0)
)

# Save as best model
st.session_state.svm["best_model"] = model
st.session_state.svm["trained_on_pca"] = trained_on_pca  # ✅ NEW
```

---

## 🎯 HOW IT WORKS NOW

### Scenario 1: Model Saved BEFORE PCA
```
1. Train SVM on original data (16 features)
2. Save best model
   ├─ model trained on 16 features
   └─ trained_on_pca = False
3. Go to PCA tab → Apply PCA (16 → 7)
4. Model comparison:
   ├─ Original model: predict(X_original_16) ✅
   └─ PCA model: predict(X_pca_7) ✅
```

### Scenario 2: Model Saved AFTER PCA
```
1. Apply PCA (16 → 7 features)
2. Train ANN on PCA data (7 features)
3. Save best model
   ├─ model trained on 7 features
   └─ trained_on_pca = True
4. Model comparison:
   ├─ Original model: predict(X_pca_7) ✅  [Uses PCA data!]
   └─ PCA model: predict(X_pca_7) ✅
```

### Key Insight:
The term "original model" in PCA comparison means "the model saved before retraining on PCA", NOT "model trained on original features". Both the "original" and "PCA" models in the comparison might be trained on PCA data if the user applied PCA before saving.

---

## 🚀 USER WORKFLOW

### Correct Usage (to compare PCA impact):

1. **Train on Original Data First:**
   ```
   1. Load dataset (16 features)
   2. Train SVM/ANN models
   3. Save best model → [trained_on_pca = False]
   ```

2. **Apply PCA:**
   ```
   4. Go to PCA tab
   5. Apply PCA transformation (16 → 7)
   ```

3. **Compare:**
   ```
   6. Go to Model Comparison
   7. Retrain on PCA data
   8. See BEFORE vs AFTER comparison:
      ├─ Original: 16 features
      └─ PCA: 7 features
   ```

### Alternative Workflow (if user applied PCA first):
```
1. Load dataset (16 features)
2. Apply PCA (16 → 7)
3. Train models on PCA data (7 features)
4. Save best model → [trained_on_pca = True]
5. Model comparison:
   ├─ Original: Uses PCA data (7 features) ✅
   └─ PCA: Retrains on same PCA data (7 features) ✅
   [Not really comparing PCA impact, but won't crash!]
```

---

## 📝 TECHNICAL DETAILS

### Feature Dimension Tracking:
```python
# When PCA is applied:
st.session_state.pca = {
    "pca_applied": True,
    "n_components": 7,
    "X_pca": array([...])  # Shape: (4521, 7)
}

# When model is saved:
X, y, _, _ = get_data()  # Gets current data from session state
if X.shape[1] == 7 and pca_applied:
    trained_on_pca = True  # Model trained on reduced features
else:
    trained_on_pca = False  # Model trained on original features
```

### Data Flow:
```
Session State Data:
├─ data["X"]: Can be original (16) OR PCA (7) depending on state
├─ pca["X_pca"]: Always PCA-transformed (7)
├─ svm["best_model"]: Trained on whatever X was at save time
├─ svm["trained_on_pca"]: Flag to remember training data type
└─ ann["best_model"]: Trained on whatever X was at save time
    └─ ann["trained_on_pca"]: Flag to remember training data type
```

---

## 🎓 KEY LEARNINGS

### Bug Pattern:
**"Dimension Mismatch After Transformation"**
- Common in ML pipelines with dimensionality reduction
- Model expects same feature dimensions as training data
- Session state can hold different data at different times

### Prevention:
1. ✅ Always track transformation state with data
2. ✅ Store flags about data provenance (`trained_on_pca`)
3. ✅ Match feature dimensions at prediction time
4. ✅ Default to safe behavior (`trained_on_pca = False`)

### Debugging Strategy:
1. Identify feature dimension mismatch (16 vs 7)
2. Trace where model was trained (what X?)
3. Trace where model is being used (what X?)
4. Add tracking to connect training and inference data

---

## ⚠️ EDGE CASES HANDLED

### Case 1: No PCA Applied
```python
trained_on_pca = False  # Default
X_original = X  # Use original data
```

### Case 2: PCA Applied But Model Saved Before PCA
```python
trained_on_pca = False  # Saved before PCA
X_original = X  # Use original data (would be from before PCA)
```

### Case 3: Model Saved After PCA
```python
trained_on_pca = True  # X was PCA at save time
X_original = st.session_state.pca["X_pca"]  # Use PCA data
```

### Case 4: Multiple PCA Applications
```python
# Last applied PCA is used
X_pca = st.session_state.pca["X_pca"]
n_components = st.session_state.pca["n_components"]

# Comparison checks: X.shape[1] == n_components
```

---

## 🎉 SUMMARY

### Problem:
- Model trained on 7 PCA features
- Prediction attempted with 16 original features
- ValueError: Feature dimension mismatch

### Solution:
- Track whether model was trained on PCA data
- Use appropriate feature set for prediction
- Default to safe behavior (assume original features)

### Files Changed:
1. ✅ `model_comparison.py`: Check `trained_on_pca` flag
2. ✅ `ann/components/best_model_saver.py`: Set `trained_on_pca` flag
3. ✅ `svm/components/best_model_saver.py`: Set `trained_on_pca` flag

### Result:
- ✅ No more feature dimension errors
- ✅ Correct data used for each model
- ✅ Handles all edge cases gracefully

---

**The bug is now fixed! Users can save models before or after PCA without crashes.** 🎯


