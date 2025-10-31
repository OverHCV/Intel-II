# Streamlit Documentation & Educational Content Patterns

## Two Types of Documentation

### 1. README.md - User Guide (External)

**Purpose**: Practical guide for using the interface effectively

**Location**: `ui/pages/{tab}/README.md`

**Content**:
- How to use the tab
- Step-by-step workflow
- Tips for achieving good results
- Common use cases
- Troubleshooting
- Best practices

**Example Structure**:

```markdown
# SVM Analysis - User Guide

## Quick Start

1. Load your dataset in the Config tab
2. Select a kernel (start with RBF)
3. Adjust parameters (C, gamma)
4. Click "Train SVM"
5. Review results in Model Performance tab

## Systematic Testing Approach

### Phase 1: Kernel Comparison
- Train with all 4 kernels using default parameters
- Identify which kernel works best
- Note results in experiment history

### Phase 2: Parameter Tuning
- Take best kernel from Phase 1
- Try different C values: [0.1, 1, 10, 100]
- Try different gamma values: ['scale', 0.01, 0.1, 1]
- Record best configuration

## Tips for Best Results

- Start with RBF kernel (works well for most problems)
- Use K-Fold CV for robust evaluation
- High C = risk of overfitting
- High gamma = complex boundary (may overfit)

## Troubleshooting

**Problem**: Low accuracy (<75%)
**Solutions**:
- Try different kernel
- Increase C or gamma
- Check for data quality issues

## For Exam/Presentation

Use the experiment history to show:
- "Trained N configurations..."
- "Best kernel: X with accuracy Y%"
- "RBF outperformed linear, suggesting..."
```

### 2. docs.py - Theory Component (In-App)

**Purpose**: Teach concepts while using the app

**Location**: `ui/pages/{tab}/docs.py`

**Content**:
- What is this technique?
- WHY does it work?
- Mathematical foundations
- When to use it
- How it solves the problem
- Concrete examples

**Pattern**:

```python
# ui/pages/svm/docs.py
import streamlit as st

def render_documentation():
    """Render expandable documentation section"""
    
    with st.expander("📚 Theory & Documentation", expanded=False):
        
        st.markdown("# Support Vector Machines (SVM)")
        
        # WHAT
        st.markdown("""
        ## What is SVM?
        
        Support Vector Machine is a supervised learning algorithm that finds
        the optimal hyperplane separating different classes.
        """)
        
        # WHY
        st.markdown("""
        ## Why Use SVM?
        
        **Problem**: Linear classifiers only work for linearly separable data.
        
        **Solution**: Map data to higher dimensional space where it becomes 
        linearly separable.
        
        **Example**: 2D circular pattern → 3D where it's linearly separable
        """)
        
        # HOW (with math)
        st.markdown(r"""
        ## The Kernel Trick
        
        Instead of computing $\phi(x)$ explicitly (expensive), we compute:
        
        $$k(x, y) = \phi(x)^T \phi(y)$$
        
        **Why this matters**: Saves computational cost while achieving same result.
        """)
        
        # WHEN
        st.markdown("""
        ## When to Use Different Kernels
        
        ### Linear Kernel
        - **Use when**: Data is linearly separable
        - **Example**: Well-separated classes in original space
        - **Pro**: Fast, interpretable
        - **Con**: Can't handle non-linear patterns
        
        ### RBF Kernel (Gaussian)
        - **Use when**: Unsure about data structure
        - **Example**: Most real-world problems
        - **Pro**: Flexible, works well generally
        - **Con**: Requires tuning gamma
        
        ### Polynomial Kernel
        - **Use when**: Data has polynomial relationships
        - **Example**: Interaction between features
        - **Pro**: Captures polynomial patterns
        - **Con**: Sensitive to degree parameter
        """)
        
        # Concrete Examples
        with st.expander("💡 Click to see example"):
            st.markdown("""
            **Example 1: Linear Separation**
            
            Data: Two clusters clearly separated by a line
            - Linear kernel: ✅ Works perfectly
            - RBF kernel: ✅ Also works (but overkill)
            - Result: Use linear (simpler is better)
            
            **Example 2: Circular Pattern**
            
            Data: One class in center, another surrounding it
            - Linear kernel: ❌ Can't separate (accuracy ~50%)
            - RBF kernel: ✅ Separates perfectly (accuracy ~95%)
            - Result: Use RBF (handles non-linearity)
            """)
        
        # Parameters Explained
        st.markdown("""
        ## Parameters Guide
        
        ### C (Regularization)
        
        **What it controls**: Trade-off between margin and errors
        
        - **Small C (0.1)**: Wide margin, more errors allowed
          - Pro: Better generalization, less overfitting
          - Con: May underfit if too small
        
        - **Large C (100)**: Narrow margin, fewer errors
          - Pro: Better training accuracy
          - Con: May overfit to training data
        
        **Rule of thumb**: Start with C=1, increase if underfitting
        
        ### Gamma
        
        **What it controls**: Influence radius of single sample
        
        - **Small gamma (0.001)**: Far points have influence
          - Result: Smooth, simple decision boundary
        
        - **Large gamma (1.0)**: Only nearby points matter
          - Result: Complex boundary, follows training data closely
          - Risk: Overfitting
        
        **Rule of thumb**: Use 'scale' (auto-calculated) first
        """)
        
        st.markdown("---")
        st.caption("💡 Experiment with different combinations in the interface above!")
```

## WHY Explanations Pattern

### Structure of Good Explanation

1. **State the Fact** (WHAT)
2. **Explain WHY it matters**
3. **Show Concrete Example**
4. **Demonstrate Problem → Solution**
5. **When to Use It**

### Example: Explaining PCA

```python
st.markdown("""
## What is PCA?

**WHAT**: Principal Component Analysis reduces dimensions by finding 
directions of maximum variance.

**WHY**: 
- High-dimensional data is hard to visualize and process
- Many features may be redundant (correlated)
- Fewer dimensions = faster training, less memory

**HOW IT WORKS**:

Imagine you have 100 features describing a person:
- height_cm
- height_inches  ← Redundant! (converts to cm)
- weight_kg
- weight_lbs     ← Redundant! (converts to kg)
- age_years
- age_months     ← Redundant! (converts to years)

PCA finds that these 6 features really only contain 3 pieces of information:
1. Height (combines height_cm and height_inches)
2. Weight (combines weight_kg and weight_lbs)
3. Age (combines age_years and age_months)

Result: 100 → 3 dimensions, no information lost!

**WHEN TO USE**:
- ✅ Features are correlated (correlation > 0.7)
- ✅ Have too many features (> 50)
- ✅ Want to visualize high-dimensional data
- ✅ Model training is too slow

**WHEN NOT TO USE**:
- ❌ Features are already independent
- ❌ Need to interpret which features matter (PCA creates new features)
- ❌ Only have a few features (<10)
""")
```

## LaTeX Math Integration

### Pattern: Inline Math

```python
st.markdown(r"""
The kernel function $k(x, y) = \phi(x)^T \phi(y)$ computes 
the dot product in the transformed space without explicit mapping.
""")
```

### Pattern: Block Math

```python
st.markdown(r"""
## Polynomial Kernel

The polynomial kernel is defined as:

$$k(x, y) = (\gamma \cdot x^T y + r)^d$$

Where:
- $\gamma$ is the kernel coefficient
- $r$ is the independent term
- $d$ is the degree
""")
```

### Pattern: Multi-Line Equations

```python
st.markdown(r"""
## Backpropagation Algorithm

Forward pass:

$$
\begin{align}
z^{[1]} &= W^{[1]} x + b^{[1]} \\
a^{[1]} &= \sigma(z^{[1]}) \\
z^{[2]} &= W^{[2]} a^{[1]} + b^{[2]} \\
a^{[2]} &= \sigma(z^{[2]})
\end{align}
$$

Backward pass:

$$
\begin{align}
\frac{\partial L}{\partial W^{[2]}} &= \frac{\partial L}{\partial a^{[2]}} \cdot \frac{\partial a^{[2]}}{\partial z^{[2]}} \cdot \frac{\partial z^{[2]}}{\partial W^{[2]}} \\
\frac{\partial L}{\partial W^{[1]}} &= \frac{\partial L}{\partial a^{[2]}} \cdot \frac{\partial a^{[2]}}{\partial z^{[2]}} \cdot \frac{\partial z^{[2]}}{\partial a^{[1]}} \cdot \frac{\partial a^{[1]}}{\partial W^{[1]}}
\end{align}
$$
""")
```

## Expandable Examples Pattern

```python
with st.expander("💡 Click to see example with actual numbers"):
    st.markdown("""
    ### Example: 3x3 Covariance Matrix
    
    Given features: [Age, Income, Debt]
    
    ```
    Covariance Matrix:
    [[ 25.0   150.0   50.0]
     [150.0  1000.0  300.0]
     [ 50.0   300.0  100.0]]
    ```
    
    **Interpretation**:
    - Age variance: 25 (moderate spread)
    - Income variance: 1000 (high spread - people earn very differently)
    - Income-Debt covariance: 300 (positive - higher income = higher debt)
    
    PCA will find:
    - PC1: Mostly captures Income (highest variance)
    - PC2: Captures Age with some Income
    - PC3: Captures remaining Debt variations
    """)
```

## Code Example Pattern

```python
with st.expander("🔧 Show Code Example"):
    st.code("""
# Train SVM with RBF kernel
from sklearn.svm import SVC

model = SVC(
    kernel='rbf',
    C=10.0,
    gamma='scale',
    random_state=42
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Calculate metrics
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
    """, language="python")
```

## Visual Intuition Pattern

```python
st.markdown("""
## Visual Intuition

### Before PCA (3D space):
```
      z
      ↑
      |  ●    ●
      | ●  ●●
      |●●●
      |________→ y
     / ●
    /
   ↙ x
```

Data varies mostly along one diagonal direction.

### After PCA (2D space):
```
   PC2 ↑
       |
       | ●
       |  ●●
       |   ●●●
       |________→ PC1
```

PC1 captures the main direction of variation.
PC2 captures remaining variation.
(Z-axis information preserved in these two components!)
""")
```

## Key Takeaways

1. **Two Documentation Types**:
   - README.md = Practical user guide (external)
   - docs.py = Theory component (in-app, expandable)

2. **WHY Explanations**:
   - State fact → Explain WHY → Show example → Demonstrate

3. **Concrete Examples**:
   - Use actual numbers
   - Show problems → solutions
   - Real-world analogies

4. **LaTeX Math**:
   - Inline: `$equation$`
   - Block: `$$equation$$`
   - Always use raw string: `r"""`

5. **Expandable Sections**:
   - Hide detailed examples
   - Show code snippets
   - Prevent overwhelming beginners

6. **Educational Tone**:
   - Teach concepts, don't just describe
   - Connect theory to interface
   - Help users succeed

