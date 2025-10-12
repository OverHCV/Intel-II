"""
PCA Documentation Component
Theory and fundamentals - comprehensive WHY explanations
"""

import streamlit as st


def render_pca_documentation():
    """
    Render expandable PCA theory documentation with WHY explanations and examples
    """
    with st.expander("📚 **Theory: Principal Component Analysis (PCA)**", expanded=False):
        st.markdown(
            """
### What is PCA?

**The Problem**: You have data with many features (e.g., 16 dimensions), but:
- 🐌 Training is SLOW (more features = more computation)
- 📊 Hard to visualize (can't plot 16D data!)
- 🎯 Some features are **redundant** (highly correlated)

**The Solution**: **Principal Component Analysis (PCA)**
- Reduces dimensions while **preserving important information**
- Finds **new axes** (principal components) that capture maximum variance
- Transforms data to a **lower-dimensional space**

---

### The Core Idea: Variance is Information

**WHY focus on variance?**

Imagine two features:

**Feature A**: [1.0, 1.1, 0.9, 1.0, 1.05] → variance = 0.0025 (almost constant!)  
**Feature B**: [5, 15, 2, 20, 10] → variance = 49 (highly variable!)

**Which feature tells you more?** → Feature B! It varies a lot between samples.

**PCA's goal**: Find directions (axes) where data varies THE MOST.

<details>
<summary><b>🔍 Visual Example: Why Variance Matters</b></summary>

**2D Dataset Example**:
```
Points: (1, 10), (2, 11), (3, 12), (4, 13), (5, 14)
```

**Original axes** (X, Y):
- X varies: 1 → 5 (range = 4)
- Y varies: 10 → 14 (range = 4)

**New axis** (diagonal PC1): along y = x + 9
- PC1 varies: √2 → 5√2 (range ≈ 7.07) ← **MORE variance!**
- PC2 varies: ≈ 0 (all points nearly on line)

**Result**: PC1 captures 99%+ of variance! Can drop PC2 with minimal info loss.

</details>

---

### How PCA Works: Step-by-Step

#### Step 1: Standardize Data

**WHY**: Features with large values dominate the analysis.

**Example**:
- Age: 20-60 (range ≈ 40)
- Income: 20,000-100,000 (range ≈ 80,000)

Without standardization, PCA focuses on Income (bigger numbers!) even if Age is more informative.

**Standardization**:
$$
z = \\frac{x - \\mu}{\\sigma}
$$

**Result**: All features have mean=0, std=1 → Fair comparison!

<details>
<summary><b>🔍 Example: Before vs After Standardization</b></summary>

**Before**:
```
Age:    [25, 30, 35, 40] → mean=32.5, std=6.45
Income: [30000, 50000, 70000, 90000] → mean=60000, std=25820
```

**After standardization**:
```
Age:    [-1.16, -0.39, 0.39, 1.16] → mean=0, std=1
Income: [-1.16, -0.39, 0.39, 1.16] → mean=0, std=1
```

Now both features have **equal weight** in PCA!

</details>

---

#### Step 2: Compute Covariance Matrix

**WHY**: Covariance shows how features vary **together**.

**Covariance Matrix**:
$$
C = \\frac{1}{n-1} X^T X
$$

Where X is the standardized data matrix (n samples × m features).

**What does it tell us?**

$$
C = \\begin{bmatrix}
\\text{var}(f_1) & \\text{cov}(f_1, f_2) & \\cdots \\\\
\\text{cov}(f_2, f_1) & \\text{var}(f_2) & \\cdots \\\\
\\vdots & \\vdots & \\ddots
\\end{bmatrix}
$$

- **Diagonal**: Variance of each feature
- **Off-diagonal**: Covariance between feature pairs
  - Positive → Features increase together
  - Negative → One increases, other decreases
  - Zero → Independent

<details>
<summary><b>🔍 Example: 3-Feature Covariance Matrix</b></summary>

**Features**: Height, Weight, Age

$$
C = \\begin{bmatrix}
1.0 & 0.8 & 0.1 \\\\
0.8 & 1.0 & 0.2 \\\\
0.1 & 0.2 & 1.0
\\end{bmatrix}
$$

**Interpretation**:
- Height & Weight: cov = 0.8 ← **Highly correlated!** (taller → heavier)
- Height & Age: cov = 0.1 ← Weakly correlated
- Weight & Age: cov = 0.2 ← Weakly correlated

**PCA will combine Height & Weight** into one component (they're redundant)!

</details>

---

#### Step 3: Compute Eigenvectors and Eigenvalues

**WHY**: Eigenvectors are the **new axes** (principal components). Eigenvalues tell us **how much variance** each captures.

**Eigendecomposition**:
$$
C \\boldsymbol{v}_i = \\lambda_i \\boldsymbol{v}_i
$$

Where:
- $\\boldsymbol{v}_i$ = eigenvector (direction of PC)
- $\\lambda_i$ = eigenvalue (variance captured by PC)

**Key Properties**:
1. Eigenvectors are **orthogonal** (perpendicular) → Independent components
2. Eigenvalues are **sorted** (λ₁ ≥ λ₂ ≥ ... ≥ λₘ)
3. PC1 (largest λ) captures most variance, PC2 second-most, etc.

<details>
<summary><b>🔍 Example: 2D Case with Actual Numbers</b></summary>

**Covariance matrix**:
$$
C = \\begin{bmatrix}
2 & 1 \\\\
1 & 2
\\end{bmatrix}
$$

**Eigenvalues**: λ₁ = 3, λ₂ = 1

**Eigenvectors**:
- $\\boldsymbol{v}_1 = \\begin{bmatrix} 0.707 \\\\ 0.707 \\end{bmatrix}$ ← PC1 (diagonal direction ↗)
- $\\boldsymbol{v}_2 = \\begin{bmatrix} -0.707 \\\\ 0.707 \\end{bmatrix}$ ← PC2 (perpendicular ↖)

**Variance explained**:
- PC1: λ₁/(λ₁+λ₂) = 3/4 = **75%**
- PC2: λ₂/(λ₁+λ₂) = 1/4 = **25%**

**If we keep only PC1**: We retain 75% of total variance!

</details>

---

#### Step 4: Project Data onto Principal Components

**WHY**: Transform from original features to new PC space.

**Transformation**:
$$
Z = X \\cdot V
$$

Where:
- X = standardized data (n × m)
- V = eigenvector matrix (m × k, k = number of PCs to keep)
- Z = transformed data (n × k)

**Result**: Data in lower-dimensional space!

<details>
<summary><b>🔍 Example: 3D → 2D Projection</b></summary>

**Original data** (3 features):
```
Sample 1: [1.2, 0.5, -0.3]
Sample 2: [-0.8, 1.1, 0.2]
Sample 3: [0.3, -0.9, 0.7]
```

**Top 2 eigenvectors** (keep 2 PCs):
```
V = [[0.58, -0.58],
     [0.58,  0.58],
     [0.58,  0.58]]
```

**Transformed data** (2 components):
```
Z = X · V:
Sample 1: [0.99, -0.41]  ← Now only 2 values!
Sample 2: [0.35,  0.93]
Sample 3: [-0.41, 0.87]
```

**Dimensionality**: 3D → 2D (33% reduction!)

</details>

---

### Choosing Number of Components

**The Question**: How many PCs to keep?

**Methods**:

#### 1. Explained Variance Ratio

**Formula**:
$$
\\text{Explained Variance Ratio}_i = \\frac{\\lambda_i}{\\sum_{j=1}^m \\lambda_j}
$$

**Cumulative Explained Variance**:
$$
\\text{Cumulative} = \\sum_{i=1}^k \\text{Explained Variance Ratio}_i
$$

**Rule of thumb**: Keep PCs until cumulative ≥ **95%** (or 90%, 99%)

<details>
<summary><b>🔍 Example: 7-Feature Dataset</b></summary>

**Eigenvalues**: [4.2, 1.8, 0.7, 0.2, 0.06, 0.03, 0.01]  
**Total variance**: 7.0

| PC | Eigenvalue | Variance % | Cumulative % |
|----|------------|------------|--------------|
| 1  | 4.2        | 60.0%      | **60.0%**    |
| 2  | 1.8        | 25.7%      | **85.7%**    |
| 3  | 0.7        | 10.0%      | **95.7%** ✅ |
| 4  | 0.2        | 2.9%       | 98.6%        |
| 5  | 0.06       | 0.9%       | 99.4%        |
| 6  | 0.03       | 0.4%       | 99.9%        |
| 7  | 0.01       | 0.1%       | 100.0%       |

**Decision**: Keep **3 PCs** → Retain 95.7% variance, reduce 7D → 3D (57% reduction!)

</details>

---

#### 2. Scree Plot

**WHY**: Visual method to find the "elbow" (point where eigenvalues drop sharply).

**How to read**:
- X-axis: PC number
- Y-axis: Eigenvalue (or explained variance %)
- **Look for the "elbow"**: Where slope flattens dramatically

**Interpretation**:
- Before elbow: Important PCs (keep)
- After elbow: Noise PCs (discard)

---

#### 3. Kaiser Criterion

**Rule**: Keep PCs with eigenvalue > 1 (for standardized data).

**WHY > 1?**  
An eigenvalue of 1 means the PC captures as much variance as one original feature.  
If λ < 1, the PC captures **less info than a single feature** → Not useful!

**Example**:
```
Eigenvalues: [3.2, 2.1, 1.5, 0.8, 0.3, 0.1]
```
Keep PCs 1, 2, 3 (λ > 1). Discard PCs 4, 5, 6.

---

### Component Loadings: Understanding PCs

**The Question**: What do the principal components actually represent?

**Component Loadings**: Correlation between original features and PCs.

**Formula**:
$$
\\text{Loading}_{ij} = \\text{corr}(\\text{Feature}_i, \\text{PC}_j) = v_{ij} \\sqrt{\\lambda_j}
$$

Where $v_{ij}$ is the eigenvector coefficient.

<details>
<summary><b>🔍 Example: Interpreting PC1</b></summary>

**Dataset**: Student performance (5 features)

**PC1 Loadings**:
```
Math Score:     0.85  ← Strong positive
Physics Score:  0.82  ← Strong positive
English Score:  0.78  ← Strong positive
Art Score:      0.15  ← Weak
Music Score:    0.10  ← Weak
```

**Interpretation**: PC1 = **"Academic Performance"**  
(combines Math, Physics, English)

**PC2 Loadings**:
```
Math Score:    -0.10
Physics Score: -0.05
English Score:  0.20
Art Score:      0.90  ← Strong!
Music Score:    0.85  ← Strong!
```

**Interpretation**: PC2 = **"Artistic Ability"**  
(combines Art, Music)

**Insight**: PCA discovered two **latent factors** (academic vs artistic) from the data!

</details>

---

### PCA for Classification: Does it Help?

**The Trade-off**:

**Pros** ✅:
- **Faster training** (fewer features)
- **Less overfitting** (removes noise)
- **Removes multicollinearity** (decorrelates features)
- **Easier visualization** (2D/3D plots)

**Cons** ❌:
- **Information loss** (discarded variance might be important!)
- **Interpretability** (PCs are combinations, not original features)
- **May hurt performance** (if discarded PCs contain class-discriminating info)

<details>
<summary><b>🔍 When PCA Helps vs Hurts</b></summary>

**PCA HELPS** ✅:

**Scenario 1**: Highly correlated features
```
Features: Height_cm, Height_inches, Weight_kg, Weight_lbs
→ 4 features, but only 2 pieces of info!
→ PCA: 4D → 2D, performance stays same (99%+ variance)
```

**Scenario 2**: Noisy features
```
Dataset: 50 features, but last 20 are random noise
→ PCA keeps top 30 PCs → Removes noise → Better generalization!
```

**PCA HURTS** ❌:

**Scenario 3**: Class info in low-variance directions
```
Example: Fraud detection
- Feature 1 (Amount): High variance, but similar across classes
- Feature 2 (Time): Low variance, but CRITICAL for fraud detection!
→ PCA might discard Feature 2 → Performance drops!
```

**Scenario 4**: Already optimal features
```
Features carefully engineered, each adds unique info
→ PCA combines them → Loses interpretability, no gain
```

</details>

---

### PCA vs Other Dimensionality Reduction

| Method | Linear? | Supervised? | Best For |
|--------|---------|-------------|----------|
| **PCA** | ✅ Yes | ❌ No | Uncorrelated features, visualization |
| **LDA** | ✅ Yes | ✅ Yes | Maximizing class separation |
| **t-SNE** | ❌ No | ❌ No | Visualization only (2D/3D) |
| **Autoencoder** | ❌ No | ❌ No | Complex non-linear patterns |

**WHY PCA for this exam?**
- ✅ Simple and fast
- ✅ Interpretable (variance explained)
- ✅ Works well with SVM/ANN
- ✅ Good baseline for comparison

---

### Practical Tips for This Task

#### Before PCA:
1. **Check feature correlations** → High correlation (>0.7) = PCA will help!
2. **Standardize data** → Essential (different scales)
3. **Visualize explained variance** → Decide how many PCs

#### During PCA:
1. **Try multiple n_components**: 2, 3, 5, 10, or 95% variance
2. **Check scree plot** → Find the elbow
3. **Inspect loadings** → Understand what PCs represent

#### After PCA:
1. **Retrain models** (SVM, ANN) on PCA data
2. **Compare metrics**: Accuracy, Precision, Recall, F1
3. **Compare training time**: PCA should be faster!
4. **Analyze results**:
   - Better performance? → Removed noise/collinearity
   - Worse performance? → Discarded important info
   - Same performance? → Features already optimal OR PCA just right

---

### Mathematical Summary

**Full PCA Pipeline**:

1. **Standardize**: $Z = \\frac{X - \\mu}{\\sigma}$
2. **Covariance**: $C = \\frac{1}{n-1} Z^T Z$
3. **Eigendecomposition**: $C = V \\Lambda V^T$
4. **Project**: $X_{\\text{PCA}} = Z \\cdot V_k$
5. **Reconstruct** (optional): $X_{\\text{approx}} = X_{\\text{PCA}} \\cdot V_k^T$

**Variance Preserved**:
$$
\\frac{\\sum_{i=1}^k \\lambda_i}{\\sum_{i=1}^m \\lambda_i} \\geq 0.95
$$

---

### Expected Findings (Exam)

**For Bank Marketing Dataset**:

**Hypothesis 1**: PCA helps (many correlated features)
- Result: Similar or better accuracy with fewer components
- Explanation: Removed redundant information, faster training

**Hypothesis 2**: PCA hurts (all features important)
- Result: Lower accuracy after PCA
- Explanation: Discarded variance contains class-discriminating info

**Your Task**: Run experiments and **EXPLAIN YOUR RESULTS**!

---

For practical usage guide, see **[README.md](./README.md)**
"""
        )

