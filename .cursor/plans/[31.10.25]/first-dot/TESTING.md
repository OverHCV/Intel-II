# Testing Instructions - November 1, 2025

## What to Test:

### 1. Run the App
```bash
cd /Users/oh/World/Study/UC/Intel-II/.jorge/partials/third
streamlit run app.py
```

### 2. Expected Behavior:

#### **Home Page**
- ✅ Shows exam requirements (4 tasks in Spanish)
- ✅ Dataset info (Portuguese 649, Math 395)
- ✅ Progress bars for each task

#### **Sidebar (Most Important Fix!)**
- ✅ Shows **APP STATE** not project development status
- ✅ "⚠️ No dataset loaded" initially
- ✅ After preparing data:
  - "✅ Dataset: Portuguese"
  - "🎯 Target: Binary"
  - "⚖️ Balance: SMOTE"
  - "✅ Data Ready: 649 samples"
- ✅ Model status (Decision Tree, Hierarchical, K-means)

#### **Dataset Review Page**
1. **Theory at TOP** (collapsible) ✅
2. Click "Apply & Prepare" button
3. Sidebar should update with dataset info
4. Should see dummy visualizations

#### **Decision Tree Page** (THE BIG ONE!)
1. Theory at top ✅
2. If no data: Shows warning "Go to Dataset Review first"
3. After data prepared:
   - Shows "✅ Data loaded: X samples, Y features"
   - Hyperparameter sliders (max_depth, min_samples_split, criterion)
   - "🚀 Train Decision Tree" button
   - Click button → **REAL TRAINING HAPPENS**:
     - Metrics (Accuracy, Precision, Recall, F1)
     - 5-fold Cross-Validation results
     - Confusion Matrix plot
     - Tree Structure visualization
     - Top 10 Feature Importance chart
     - **Top 10 Extracted Rules** with:
       - IF-THEN conditions
       - Support, Confidence
       - Class distribution
   - Sidebar updates to "✅ Decision Tree trained"

### 3. What ACTUALLY Works Now:

- ✅ Rule extraction (recursive tree traversal)
- ✅ Rule ranking (by support/confidence/simplicity)
- ✅ J4 criterion calculation (for clustering)
- ✅ Full decision tree training pipeline
- ✅ Cross-validation
- ✅ Feature importance
- ✅ Confusion matrix
- ✅ Tree visualization

### 4. What to Look For:

1. **Sidebar shows REAL app state** (not "Phase 1: BFS")
2. **Theory expander at BEGINNING** of Dataset Review and Decision Tree
3. **No "Load" button** - just "Apply & Prepare"
4. **Decision Tree actually trains** and shows real scikit-learn results
5. **Rules are extracted** and displayed in expandable sections

### 5. Known Issues:

- Dataset Review still uses dummy data (need to wire up data layer)
- Feature names show as "feature_0, feature_1" (need real column names)
- Hierarchical and K-means pages still WIP

### 6. Next Steps:

- Wire up REAL data loading in Dataset Review
- Implement Hierarchical Clustering page
- Implement K-means page with optimal k finding

---

## Expected Terminal Output:

```bash
INFO:core.decision_tree:CART trained: depth=5, leaves=23
INFO:core.decision_tree:Extracted 23 rules from decision tree
INFO:core.decision_tree:Ranked 23 rules by combined
INFO:core.evaluation:Classification: Acc=0.853, F1=0.841
```

## What Changed:

1. **Sidebar**: Now shows actual app state variables
2. **Theory**: Moved to beginning of pages
3. **Decision Tree**: Fully working with rule extraction
4. **State Management**: Added keys for models, rules, labels
5. **Button text**: "Load & Prepare" → "Apply & Prepare"

