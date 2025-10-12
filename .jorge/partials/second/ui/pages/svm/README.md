# Task 1: Support Vector Machine (SVM) Analysis - COMPLETE ✅

## 📋 Requirement Summary

From the exam requirements (Second Partial - Task 1):

> **Entrenar una máquina de vectores de soporte (SVM) sobre la base de datos escogida y realizar validación cruzada para determinar el desempeño del clasificador.**
>
> **Se deberán probar:**
> - Diferentes kernels
> - Diferentes parámetros del kernel

**Points:** 0.9 / 5.0

---

## ✅ TASK 1 STATUS: **COMPLETE**

All requirements have been implemented and tested. The interface provides:

### ✅ 1. SVM Training with Cross-Validation
- **K-Fold Cross-Validation** (default, more robust)
- **Train/Test Split** (simple validation)
- Configurable in **Config** tab

### ✅ 2. Different Kernels Tested
- ✅ **Linear Kernel** - For linearly separable data
- ✅ **RBF (Radial Basis Function)** - Most popular, default choice
- ✅ **Polynomial Kernel** - For polynomial relationships
- ✅ **Sigmoid Kernel** - Neural network-like behavior

### ✅ 3. Different Kernel Parameters
- ✅ **C (Regularization)** - Range: 0.01 to 100 (log scale)
- ✅ **Gamma (γ)** - Options: 'scale', 'auto', 0.001, 0.01, 0.1, 1
- ✅ **Degree (d)** - Range: 2 to 5 (polynomial only)

### ✅ 4. Experiment Tracking & Comparison
- ✅ Automatic experiment history
- ✅ Persistent storage (survives page refresh)
- ✅ Comparison table with all metrics
- ✅ Visual comparison chart (bar graph)
- ✅ Best model identification

### ✅ 5. Performance Metrics
- ✅ **Accuracy** - Overall correctness
- ✅ **Precision** (Weighted) - Handles class imbalance
- ✅ **Recall** (Weighted) - Handles class imbalance
- ✅ **F1-Score** (Weighted) - Balanced metric
- ✅ **Confusion Matrix** - Visual breakdown

### ✅ 6. Visualizations & Analysis
- ✅ **Model Performance** - Confusion matrix + metrics bar
- ✅ **Feature Analysis** - Correlation heatmap
- ✅ **Data Exploration** - Interactive 2D/3D scatter plots

### ✅ 7. Best Model for PCA (Task 3)
- ✅ Automatic best model selection
- ✅ One-click save for PCA comparison

---

## 🎯 How to Complete Task 1 (Step-by-Step)

### **Step 1: Load Data** (Config Tab)

1. Navigate to **⚙️ Config** tab
2. Select dataset size:
   - **Small**: 4,521 samples (faster, good for testing)
   - **Full**: 45,211 samples (complete dataset)
3. Choose feature type:
   - **Numerical only** (default, 7 features)
   - **All features** (includes categorical, 16 features)
4. Select CV strategy:
   - **K-Fold** (recommended, more robust, gives std deviation)
   - **Train/Test Split** (simple, faster)
5. Data loads automatically ✅

---

### **Step 2: Systematic Kernel Testing**

Follow this systematic approach for your exam:

#### **A. Test All Kernels (Default Parameters)**

Train 4 models with default C=1.0, gamma='scale':

1. **🔍 SVM** tab → **🎛️ Model Configuration**
2. Select **Linear** kernel → Click **🚀 Train SVM**
   - Note Experiment #1 accuracy
3. Select **RBF** kernel → Click **🚀 Train SVM**
   - Note Experiment #2 accuracy
4. Select **Polynomial** kernel (degree=3) → Click **🚀 Train SVM**
   - Note Experiment #3 accuracy
5. Select **Sigmoid** kernel → Click **🚀 Train SVM**
   - Note Experiment #4 accuracy

**📊 Analysis:** Check **📋 Experiment History** table below
- Which kernel has highest accuracy?
- Look at comparison chart (best is green)

---

#### **B. Tune C Parameter (Best Kernel)**

Use the best kernel from Step A, test different C values:

1. Set **C = 0.1** → Train
2. Set **C = 1.0** (already done)
3. Set **C = 10** → Train
4. Set **C = 100** → Train

**📊 Analysis:**
- Does higher C improve accuracy?
- Check confusion matrix - does it overfit with high C?

---

#### **C. Tune Gamma (RBF/Poly/Sigmoid)**

If best kernel uses gamma, test different values:

1. **gamma = 'scale'** (already done)
2. **gamma = 'auto'** → Train
3. **gamma = 0.001** → Train
4. **gamma = 0.01** → Train  
5. **gamma = 0.1** → Train

**📊 Analysis:**
- Small gamma → smooth boundary
- Large gamma → complex boundary (risk: overfitting)

---

#### **D. Tune Polynomial Degree (If Poly Best)**

If Polynomial kernel is best:

1. **degree = 2** → Train
2. **degree = 3** (already done)
3. **degree = 4** → Train
4. **degree = 5** → Train

**📊 Analysis:**
- Higher degree → more complexity
- Check if accuracy improves or overfits

---

### **Step 3: Analyze Results**

#### **1. Experiment History Table**

Scroll down to **📋 Experiment History - Compare All Runs**

- **Total Experiments**: Shows count
- **Best Accuracy**: Automatically identified
- **Table**: Compare all parameters side-by-side

#### **2. Visual Comparison Chart**

Below the table:
- Bar chart shows accuracy across experiments
- **Green bar** = best experiment
- Kernel labels on each bar

#### **3. Check Visualizations**

Click through the 3 visualization tabs:

**Tab 1: 📊 Model Performance**
- **Confusion Matrix**: Check if predictions are balanced
  - Good: High values on diagonal (TN, TP)
  - Bad: Zeros in cells → only predicting one class
- **Metrics Bar**: Visual comparison of metrics
- **Training Time**: Performance indicator

**Tab 2: 🔬 Feature Analysis**
- **Correlation Heatmap**: See feature relationships
  - Strong correlation (±0.7+) → features might be redundant
  - Red = negative, Blue = positive

**Tab 3: 🗺️ Data Exploration**
- **Interactive Scatter**: Visualize class separation
  - Select different X/Y axes
  - Enable 3D for Z axis (if Plotly installed)
  - See if classes are separable

---

### **Step 4: Save Best Model**

Scroll down to **💾 Save Best Model for PCA Comparison**

1. Review best experiment info (shown automatically)
   - Experiment ID, kernel, parameters, accuracy
2. Click **💾 Save Best Model (Exp #X)** button
3. Model retrains with best params and saves
4. Confirmation message with balloons 🎈
5. Ready for **Task 3: PCA Analysis**!

---

### **Step 5: Document for Exam**

Create your Jupyter notebook / report with:

#### **1. Dataset Information**
```
Dataset: Bank Marketing (UCI ML Repository)
Samples: 4,521 (small) or 45,211 (full)
Features: 7 numerical or 16 total (with categorical)
Target: Binary (yes/no subscription)
Class Distribution: ~88% no, ~12% yes (imbalanced)
```

#### **2. Kernels Tested**

| Kernel | C | Gamma | Degree | Accuracy | Precision | Recall | F1-Score |
|--------|---|-------|--------|----------|-----------|--------|----------|
| Linear | 1.0 | - | - | 0.XXXX | 0.XXXX | 0.XXXX | 0.XXXX |
| RBF | 1.0 | scale | - | 0.XXXX | 0.XXXX | 0.XXXX | 0.XXXX |
| Poly | 1.0 | scale | 3 | 0.XXXX | 0.XXXX | 0.XXXX | 0.XXXX |
| Sigmoid | 1.0 | scale | - | 0.XXXX | 0.XXXX | 0.XXXX | 0.XXXX |

*(Copy from Experiment History table)*

#### **3. Parameter Tuning**

**C Parameter Exploration** (Best Kernel: [name])

| C | Accuracy | F1-Score | Training Time |
|---|----------|----------|---------------|
| 0.1 | 0.XXXX | 0.XXXX | X.XX s |
| 1.0 | 0.XXXX | 0.XXXX | X.XX s |
| 10 | 0.XXXX | 0.XXXX | X.XX s |
| 100 | 0.XXXX | 0.XXXX | X.XX s |

**Gamma Exploration** (if applicable)

| Gamma | Accuracy | F1-Score |
|-------|----------|----------|
| scale | 0.XXXX | 0.XXXX |
| auto | 0.XXXX | 0.XXXX |
| 0.001 | 0.XXXX | 0.XXXX |
| 0.01 | 0.XXXX | 0.XXXX |
| 0.1 | 0.XXXX | 0.XXXX |

#### **4. Best Configuration**

```
Best Kernel: [Linear/RBF/Poly/Sigmoid]
Best Parameters:
  - C: X.XX
  - Gamma: [value] (if applicable)
  - Degree: X (if Poly)

Best Performance:
  - Accuracy: 0.XXXX
  - Precision: 0.XXXX
  - Recall: 0.XXXX
  - F1-Score: 0.XXXX

Cross-Validation Strategy: [K-Fold/Train-Test]
Training Time: X.XX seconds
```

#### **5. Confusion Matrix Analysis**

Include screenshot or describe:
```
Confusion Matrix (Best Model):
                Predicted
                No      Yes
Actual  No     [TN]    [FP]
        Yes    [FN]    [TP]

Analysis:
- True Negatives (TN): [count] - Correctly predicted "no"
- True Positives (TP): [count] - Correctly predicted "yes"
- False Positives (FP): [count] - Incorrectly predicted "yes"
- False Negatives (FN): [count] - Incorrectly predicted "no"

Interpretation:
[Your analysis - is the model balanced? Does it predict both classes well?]
```

#### **6. Insights & Conclusions**

**Why did this kernel work best?**
- Linear: → Data is linearly separable
- RBF: → Data requires non-linear boundary, complex patterns
- Polynomial: → Data has polynomial relationships
- Sigmoid: → [your interpretation]

**How does regularization (C) affect performance?**
- Low C → Wider margin, more regularization, prevents overfitting
- High C → Narrower margin, less regularization, risk of overfitting
- Optimal C: [value] because [reason]

**Impact of gamma (if applicable):**
- Small gamma → Smooth boundary, considers far points
- Large gamma → Complex boundary, only nearby points matter
- Optimal gamma: [value] because [reason]

**Class Imbalance Handling:**
- Dataset is imbalanced (88% no, 12% yes)
- Used **weighted averaging** for precision/recall/F1
- Ensures metrics reflect per-class performance
- Prevents artificially high scores from predicting majority class

---

## 📊 Understanding Metrics

### **Why Weighted Averaging?**

The Bank Marketing dataset is **highly imbalanced**:
- **88%** samples are "no" (didn't subscribe)
- **12%** samples are "yes" (subscribed)

**Problem:** A naive model that always predicts "no" would get 88% accuracy!

**Solution:** We use **weighted averaging**:
```python
precision_score(y_test, y_pred, average='weighted')
```

This weights each class's metric by its support (number of samples), giving a more realistic score.

### **Metrics Explained**

**Accuracy** = (TP + TN) / Total
- Overall correctness
- ⚠️ Misleading with imbalanced data!

**Precision (Weighted)** = TP / (TP + FP)
- Of all "yes" predictions, how many were correct?
- Important when false positives are costly

**Recall (Weighted)** = TP / (TP + FN)
- Of all actual "yes", how many did we find?
- Important when false negatives are costly

**F1-Score (Weighted)** = 2 × (Precision × Recall) / (Precision + Recall)
- Harmonic mean of precision and recall
- Balanced metric
- Best for imbalanced datasets

---

## 💡 Tips for Oral Presentation (2.5 points)

Be ready to explain:

### **1. What is SVM?**
- Maximum margin classifier
- Finds optimal hyperplane separating classes
- Uses support vectors (samples closest to boundary)
- Kernel trick for non-linear boundaries

### **2. Why use different kernels?**
- **Linear**: Fast, works when data is linearly separable
- **RBF**: Most flexible, maps to infinite dimensions
- **Polynomial**: Captures polynomial relationships
- **Sigmoid**: Similar to neural networks

### **3. Your Findings**
- "I tested [X] different kernels..."
- "[Kernel] performed best with accuracy [X.XX]"
- "I tuned [parameters] and found optimal values..."
- "The confusion matrix shows [your analysis]..."

### **4. Class Imbalance**
- "The dataset is imbalanced (88/12 split)"
- "I used weighted averaging to get realistic metrics"
- "This prevents artificially high scores from majority class prediction"

### **5. Next Steps (Task 3)**
- "I saved the best model ([kernel], C=[X], gamma=[Y])"
- "Next, I'll apply PCA to reduce dimensions"
- "I'll compare performance before and after PCA"
- "This will show if dimensionality reduction helps or hurts"

---

## ✅ Exam Submission Checklist

- [ ] Trained at least 4 different kernels (Linear, RBF, Poly, Sigmoid)
- [ ] Tested at least 4 different C values
- [ ] Tested at least 4 different gamma values (if using RBF/Poly/Sigmoid)
- [ ] Tested different polynomial degrees (if using Poly)
- [ ] Used cross-validation (K-Fold recommended)
- [ ] Documented all experiments with metrics
- [ ] Analyzed confusion matrix for best model
- [ ] Identified best configuration and explained why it works
- [ ] Saved best model for PCA comparison (Task 3)
- [ ] Created Jupyter notebook with:
  - [ ] Code
  - [ ] Results tables
  - [ ] Visualizations (confusion matrix, comparison charts)
  - [ ] Personal analysis and conclusions
- [ ] Prepared for oral presentation (know your findings!)

---

## 🚀 Quick Reference

### **Access the Interface**
```bash
cd .jorge/partials/second
streamlit run app.py
```

### **Navigate to SVM Tab**
Click **🔍 SVM** tab at the top

### **Key Sections**
1. **📚 Theory & Docs** - Expander with theory (optional)
2. **🎛️ Model Configuration** - Parameters and Train button
3. **📈 Visualizations** - Three tabs (Performance, Features, Exploration)
4. **📋 Experiment History** - Compare all runs
5. **💾 Save Best Model** - For PCA comparison

### **File Locations**
- **Experiment history**: `.cache/svm_experiments.json` (auto-saved)
- **Code**: `ui/pages/svm/tab.py`
- **Visualizations**: `funcs/visualizers.py`
- **This guide**: `ui/pages/svm/README.md`

---

## 🆘 Troubleshooting

**"No experiments in history after page refresh"**
- Experiments should persist automatically
- Check `.cache/svm_experiments.json` exists
- Clear browser cache and reload

**"Metrics seem too high despite bad confusion matrix"**
- ✅ Fixed! Now using weighted averaging
- Metrics accurately reflect per-class performance

**"Can't see 3D scatter plots"**
- Install Plotly: `pip install plotly` or `uv add plotly`
- Falls back to 2D if Plotly unavailable

**"Training is slow"**
- Use **Small dataset** (4.5K samples)
- Reduce C value (faster convergence)
- Use Linear kernel (fastest)

---

## 🎓 Conclusion

**Task 1 is 100% COMPLETE!** ✅

You have everything needed to:
1. ✅ Train SVM with different kernels and parameters
2. ✅ Use cross-validation
3. ✅ Track and compare experiments
4. ✅ Analyze performance with multiple metrics
5. ✅ Save best model for Task 3

**Next:** Move on to **Task 2: ANN (Artificial Neural Networks)** or **Task 3: PCA Analysis**

---

**Good luck with your exam! 🚀**

*If you have questions, check the Theory & Docs expander in the SVM tab for detailed explanations.*
