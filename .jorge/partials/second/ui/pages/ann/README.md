# ANN Tab - User Guide 🧠

> **Quick Start Guide for the Artificial Neural Network Interface**

This guide will help you effectively use the ANN tab to train, evaluate, and compare neural network models on your dataset.

---

## 🎯 What You'll Learn

- How to configure and train ANNs
- Choosing the right architecture
- Interpreting results and metrics
- Comparing different configurations
- Best practices for achieving great results

---

## 🚀 Getting Started

### Step 1: Load Your Data

Before using the ANN tab, ensure you've loaded your dataset in the **sidebar configuration**:

1. Choose dataset size (Small: 4.5K / Full: 45K)
2. Select validation strategy (Train/Test or K-Fold)
3. Review data summary to understand class balance

**💡 Tip**: Start with the small dataset for faster experimentation!

---

### Step 2: Configure Your Network

In the **🎛️ Model Configuration** panel, you'll find:

#### **Architecture**
Choose the network structure (number of neurons in each hidden layer):

- **`(10,)`**: Simple, 1 layer with 10 neurons
  - Fast training
  - Good for linearly separable data
  
- **`(20,)` or `(50,)`**: Medium complexity
  - Balanced performance
  - **Recommended starting point**
  
- **`(20, 10)` or `(50, 30)`**: Deep networks (2 layers)
  - Can learn complex patterns
  - Requires more training time
  
- **`(100, 50, 20)`**: Very deep (3 layers)
  - Most complex patterns
  - Risk of overfitting on small datasets

**💡 Pro Tip**: Start simple `(20,)`, then increase complexity if needed!

#### **Activation Function**
Choose how neurons process information:

- **ReLU** ✅ **RECOMMENDED**
  - Fast and effective
  - Modern standard
  - Best choice for most cases
  
- **tanh**
  - Good for normalized data
  - Output range: -1 to 1
  - Can work better than ReLU sometimes
  
- **logistic (Sigmoid)**
  - Classic activation
  - Rarely used in modern networks
  - Can suffer from vanishing gradients

**💡 Default Choice**: Use **ReLU** unless you have a specific reason not to!

#### **Solver**
Choose the optimization algorithm:

- **adam** ✅ **RECOMMENDED**
  - Adaptive learning rate
  - Robust and reliable
  - Works well on most datasets
  
- **lbfgs**
  - Fast convergence on small datasets
  - Good for <1000 samples
  - Uses more memory
  
- **sgd**
  - Simple stochastic gradient descent
  - Requires careful tuning
  - Good for very large datasets

**💡 Default Choice**: Use **adam** - it's the most reliable!

#### **Max Iterations**
Number of training epochs (100-2000):

- **100-500**: Quick experiments
- **500-1000**: Standard training
- **1000-2000**: Thorough training (if convergence warning appears)

**💡 Tip**: Start with 500, increase if you see "ConvergenceWarning"

---

### Step 3: Train Your Model

1. Configure your network (see Step 2)
2. Click **🚀 Train ANN**
3. Wait for training to complete (spinner will show progress)
4. View results in the visualization panel

**⏱️ Training Time**: 
- Small dataset + simple network: ~2-5 seconds
- Full dataset + deep network: ~30-60 seconds

---

## 📊 Understanding Results

### Visualizations

After training, you'll see **side-by-side visualizations**:

#### **Left: Confusion Matrix**
Shows correct vs incorrect predictions:

```
              Predicted
              No    Yes
Actual  No   [TN]  [FP]
        Yes  [FN]  [TP]
```

- **Diagonal** (TN, TP): Correct predictions ✅
- **Off-diagonal** (FP, FN): Errors ❌

**💡 Goal**: Maximize diagonal values!

#### **Right: Metrics Bar Chart**
Visual comparison of performance metrics:

- **Accuracy**: Overall correctness
- **Precision**: Of predicted "yes", how many are correct?
- **Recall**: Of actual "yes", how many did we catch?
- **F1-Score**: Harmonic mean of precision and recall

**💡 For Imbalanced Data**: Focus on **Precision**, **Recall**, and **F1-Score** more than Accuracy!

---

## 📈 Experiment History

All your training runs are automatically saved and compared!

### Features:
- **Persistent Storage**: Experiments saved across sessions
- **Comparison Table**: See all configurations and results
- **Trend Analysis**: Accuracy chart shows improvement over time
- **Best Model Tracking**: Automatically identifies best performer

### Using Experiment History:

1. **Train multiple configurations** (try different architectures, activations, solvers)
2. **Compare results** in the history table
3. **Identify patterns**: Which configuration works best?
4. **Save best model** for PCA comparison

**💡 Strategy**: Run 5-10 experiments with different configs to find optimal setup!

---

## 💾 Saving Your Best Model

Once you've found your best configuration:

1. Review experiment history
2. The interface automatically identifies the best model (highest accuracy)
3. Click **💾 Save Best Model (Exp #X)**
4. Model is saved for later PCA comparison

**💡 Note**: The system retrains on the full dataset before saving for best performance!

---

## 🎓 Tips for Great Results

### 1. **Start Simple, Then Increase Complexity**
```
Try: (10,) → (20,) → (50,) → (20,10) → (50,30)
```
Don't jump to deep networks immediately!

### 2. **Experiment with Activation Functions**
Most datasets work best with **ReLU**, but try **tanh** if ReLU doesn't perform well.

### 3. **Use Adequate Training Iterations**
If you see "ConvergenceWarning", increase `max_iter` to 1000-2000.

### 4. **Leverage Experiment History**
Run multiple experiments and compare systematically:
- Fix activation and solver, vary architecture
- Fix architecture, try different activations
- Compare adam vs lbfgs on your data

### 5. **Watch for Overfitting**
If training accuracy is high but validation is low:
- Use simpler architecture
- Increase regularization (not exposed in UI yet)
- Get more data

### 6. **Handle Class Imbalance**
For imbalanced datasets (like Bank Marketing: 88% "no", 12% "yes"):
- Focus on **F1-Score** and **Recall** metrics
- Don't rely solely on Accuracy
- The interface automatically uses weighted averaging

---

## 🔍 Common Scenarios

### Scenario 1: Quick Baseline
**Goal**: Get a quick sense of ANN performance

**Configuration**:
- Architecture: `(20,)`
- Activation: ReLU
- Solver: adam
- Max Iter: 500

**Expected Time**: ~5 seconds

---

### Scenario 2: Comprehensive Search
**Goal**: Find optimal configuration

**Strategy**:
1. Test 3 architectures: `(20,)`, `(50,)`, `(20,10)`
2. Test 2 activations: ReLU, tanh
3. = 6 experiments total
4. Compare in history table
5. Save best model

**Expected Time**: ~30 seconds total

---

### Scenario 3: Deep Network Experiment
**Goal**: See if deep network helps

**Configuration**:
- Architecture: `(100, 50, 20)`
- Activation: ReLU
- Solver: adam
- Max Iter: 1000 (deep networks need more iterations)

**Expected Time**: ~20-30 seconds

**⚠️ Warning**: May overfit on small datasets!

---

## ❓ Troubleshooting

### "ConvergenceWarning"
**Problem**: Model didn't finish training

**Solutions**:
1. Increase `max_iter` to 1000-2000
2. Try `lbfgs` solver (converges faster)
3. Ensure data is properly scaled (done automatically)

---

### Poor Performance
**Problem**: Low accuracy/F1-score

**Solutions**:
1. Try deeper architecture: `(20,)` → `(50,30)`
2. Change activation: ReLU → tanh
3. Increase training iterations
4. Check if data is suitable for neural networks
   - Linear problems may need SVM instead
   - Consider PCA for dimensionality reduction

---

### Training Takes Too Long
**Problem**: Training exceeds 1 minute

**Solutions**:
1. Use smaller dataset (toggle in sidebar)
2. Use simpler architecture: `(100,50,20)` → `(20,)`
3. Reduce max_iter to 500
4. Try `adam` solver (faster than `lbfgs` on large data)

---

### All Predictions Same Class
**Problem**: Confusion matrix shows all predictions in one column

**Solutions**:
1. Increase network complexity: `(10,)` → `(50,30)`
2. Train longer: increase max_iter
3. Try different activation function
4. Check class balance in sidebar data summary

---

## 📚 Next Steps

After finding your best ANN configuration:

1. **Document Results**: Note which configuration works best
2. **Save Best Model**: Use the save button for PCA comparison
3. **Move to PCA Tab**: Compare performance with/without PCA
4. **Prepare for Exam**: Explain why certain configurations work better

---

## 🎯 Exam Tips

When presenting your results:

### What to Say:
✅ "I tested multiple architectures: `(20,)`, `(50,30)`, and `(100,50,20)`"
✅ "ReLU activation performed best on this dataset"
✅ "Adam solver converged faster than SGD"
✅ "I found that deeper networks (`(50,30)`) improved F1-score by X%"
✅ "For this imbalanced dataset, I focused on F1-score rather than accuracy"

### What to Show:
✅ Experiment history table with multiple configurations
✅ Confusion matrix of best model
✅ Metrics comparison chart
✅ Explanation of why certain configs work better

---

## 🔗 Additional Resources

- **Theory**: Click the "📚 Theory" expander in the ANN tab
- **Course Materials**: Review notebook 6-ANN.ipynb
- **Comparison**: Use PCA tab to see dimensionality reduction effects

---

**Happy Training! 🚀** 

*Remember: Start simple, experiment systematically, and compare results!*

