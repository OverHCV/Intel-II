# SVM Implementation - Usage Guide

## 🎯 What Was Implemented

Successfully completed **Task 1** from your exam (README.md):
> Train a Support Vector Machine (SVM) with different kernels and parameters using cross-validation

### Key Features

1. **📚 Interactive Documentation**
   - Complete theory about SVM and the kernel trick
   - Mathematical formulas (LaTeX rendered)
   - Explanation of each kernel type (Linear, RBF, Polynomial, Sigmoid)
   - Parameter guide (C, gamma, degree) with WHY and WHEN to use them
   - Practical tips for the exam

2. **🎛️ Interactive Controls**
   - Select kernel type
   - Adjust C (regularization)
   - Adjust gamma (kernel coefficient)
   - Adjust degree (for polynomial kernel)
   - Enhanced tooltips explaining each parameter

3. **📊 Experiment Tracking**
   - All training runs are saved automatically
   - History table showing all experiments
   - Comparison chart highlighting best performing model
   - Automatic insights (best kernel, performance range, variance)
   - Clear history button to start fresh

4. **📈 Visualizations**
   - Confusion matrix for each run
   - Metrics bar charts
   - Comparison chart across all experiments
   - Best experiment highlighted in green

---

## 🚀 How to Run

```powershell
uv run streamlit run ui/app.py
```

This will open the application in your browser at `http://localhost:8501`

---

## 📖 How to Use (Step-by-Step)

### Step 1: Load Data
1. Click the **"⚙️ Config"** tab
2. Load the bank marketing dataset
3. Configure cross-validation strategy (K-Fold recommended for exam)

### Step 2: Learn the Theory
1. Click the **"🔍 SVM"** tab
2. Click **"📚 Theory & Documentation"** expander at the top
3. Read about:
   - Why we use SVMs
   - The kernel trick (HOW it works and WHY)
   - Different kernel types
   - Parameter meanings
   - Practical tips

### Step 3: Run Experiments
1. Select a kernel (start with RBF - most popular)
2. Adjust parameters:
   - Try C values: [0.1, 1, 10, 100]
   - Try gamma values: ['scale', 0.01, 0.1, 1]
3. Click **"🚀 Train SVM"**
4. Wait for results (a few seconds)
5. Examine confusion matrix and metrics

### Step 4: Compare Multiple Runs
1. Try different kernels (Linear, RBF, Poly, Sigmoid)
2. Try different parameter combinations
3. Each run is automatically saved to **Experiment History**
4. Scroll down to see the comparison table
5. The best experiment is highlighted in **green**
6. Read the automatic **insights** at the bottom

### Step 5: Analyze Results
The system shows you:
- **Best performing kernel** and its ID
- **Best parameters** (C, gamma, degree)
- **Performance range** (min to max accuracy)
- **Performance variance** (how consistent the results are)

Use this information to:
- Write your analysis for the exam
- Understand WHY certain kernels work better
- Identify if you're overfitting (high variance)
- Identify if you're underfitting (low accuracy)

### Step 6: Save Best Model
1. Once you find the best configuration
2. Click **"💾 Save as Best Model (for PCA comparison)"**
3. This saves the model for Task 3 (PCA analysis)

---

## 💡 Tips for the Exam

### Systematic Testing Strategy

**Phase 1: Kernel Comparison**
1. Train with all 4 kernels using default parameters
2. Identify which kernel works best
3. Note the results in your report

**Phase 2: Parameter Tuning**
1. Take the best kernel from Phase 1
2. Try different C values: [0.1, 1, 10, 100]
3. Try different gamma values (if applicable): ['scale', 0.01, 0.1, 1]
4. Record best configuration

**Phase 3: Analysis**
1. Look at the experiment history table
2. Identify patterns:
   - Does RBF always outperform Linear?
   - What happens with high C values?
   - What happens with high gamma values?
3. Explain WHY in your report using theory from docs

### What to Write in Your Report

Based on the experiment history, you can write:

```
"Se entrenaron [N] configuraciones diferentes de SVM probando los kernels
Linear, RBF, Polynomial y Sigmoid. Se utilizó validación cruzada con K=5 folds.

Los resultados muestran que el kernel [BEST_KERNEL] obtuvo el mejor desempeño
con una precisión de [ACCURACY] usando parámetros C=[C_VALUE] y gamma=[GAMMA_VALUE].

El kernel lineal obtuvo una precisión de [LINEAR_ACC], sugiriendo que los datos
[son/no son] linealmente separables. El kernel RBF mostró [mejor/peor] desempeño,
lo cual indica que [análisis basado en teoría].

La varianza en el desempeño fue de [VARIANCE], lo que sugiere [conclusión sobre
estabilidad del modelo]."
```

### Understanding the Results

**If RBF works best:**
- Data has non-linear patterns
- Complex decision boundary needed
- Mention in report: "El kernel RBF mapea los datos a un espacio de dimensión infinita..."

**If Linear works best:**
- Data is (nearly) linearly separable
- Simple boundary is sufficient
- Mention: "Los datos muestran separabilidad lineal, por lo que el kernel lineal es suficiente..."

**If CV variance is high (>0.05):**
- Model might be overfitting
- Try reducing C or gamma
- Mention: "Alta varianza sugiere posible sobreajuste..."

**If accuracy is low (<0.75):**
- Model might be underfitting
- Try increasing C or gamma
- Try different kernel
- Mention: "Bajo desempeño sugiere que el modelo no captura la complejidad..."

---

## 📁 File Structure

The implementation follows clean architecture:

```
ui/pages/
├── svm.py (209 lines)           # Main page: controls + training logic
├── svm_docs.py (178 lines)      # Documentation and theory
└── svm_experiments.py (146 lines) # Experiment tracking + visualization
```

Each file has a single responsibility and is under 300 lines as required.

---

## ✅ What's Ready for the Exam

- ✅ SVM training with multiple kernels
- ✅ Parameter exploration (C, gamma, degree)
- ✅ Cross-validation support
- ✅ Metrics tracking (accuracy, precision, recall, F1)
- ✅ Experiment comparison
- ✅ Documentation for learning
- ✅ Confusion matrices
- ✅ Visual comparisons
- ✅ Best model identification
- ✅ Ready for PCA comparison (Task 3)

---

## 🔜 Next Steps

1. **Now**: Test the SVM implementation
2. **Next**: Implement Task 2 (ANN)
3. **Then**: Implement Task 3 (PCA comparison)
4. **Finally**: Prepare oral presentation

---

## 📞 Questions?

If something doesn't work or you need clarification:
1. Check the documentation section in the UI
2. Look at the experiment history for patterns
3. Read the insights provided automatically
4. Refer back to this guide

Good luck with your exam! 🎓

