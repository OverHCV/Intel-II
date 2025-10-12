"""
ANN Documentation Component
Theory and fundamentals - displayable in UI
"""

import streamlit as st


def render_ann_documentation():
    """
    Render expandable ANN theory documentation with WHY explanations
    """
    with st.expander("📚 **Theory: Artificial Neural Networks**", expanded=False):
        st.markdown(
            """
### What is an Artificial Neural Network (ANN)?

**The Problem**: We want to classify data, but simple linear models (like a line) can't handle complex patterns.

**The Solution**: Use multiple layers of "neurons" that learn to transform data into something linearly separable.

#### From Linear to Neural

**Start with a linear model**:
$$
d_i = \\text{sign}(\\boldsymbol{w}^T \\boldsymbol{x}_i)
$$

**Problem with sign()**: It's not differentiable (can't calculate gradient), so we can't use gradient descent to train it.

**Neural Network solution**:
$$
d_i = \\text{activation}(\\boldsymbol{w}^T \\phi(\\boldsymbol{x}_i))
$$

<details>
<summary><b>🔍 Click to see concrete example</b></summary>

**Example with 3 input features**:

Given a sample: $\\boldsymbol{x}_i = [2.5, 1.8, 3.1]$ (e.g., age, income, loan amount)

Weights: $\\boldsymbol{w} = [0.5, -0.3, 0.8]$

**Why these dimensions?**  
✓ Weight vector has **3 values** = **same as features**  
✓ **Why?** Each weight multiplies one feature (to give it importance)  
✓ Positive weights (0.5, 0.8) → feature increases output  
✓ Negative weights (-0.3) → feature decreases output

**Calculate**:
1. $\\boldsymbol{w}^T \\boldsymbol{x}_i = 0.5(2.5) + (-0.3)(1.8) + 0.8(3.1) = 1.25 - 0.54 + 2.48 = 3.19$
2. $\\text{activation}(3.19) = \\text{sigmoid}(3.19) = 0.96$ ≈ "yes" (close to 1)

**The magic**: Different weights = different importance to each feature!

</details>

**Key insight**: 
- $\\phi(\\cdot)$ transforms input (done automatically by hidden layers)
- $\\text{activation}(\\cdot)$ is differentiable → we can train with gradient descent!

---

### Activation Functions: The "Decision Makers"

**WHY do we need activation functions?**

Without activation, stacking layers = still just a linear model!  
**Example**: $f(f(x)) = W_2(W_1x) = (W_2W_1)x = W_{total}x$ ← Still linear!

**With activation**: $f_2(\\text{activation}(f_1(x)))$ ← Now non-linear! Can learn complex patterns!

#### 1. Sigmoid (Logistic)

$$
\\sigma(x) = \\frac{1}{1+e^{-x}}
$$

**WHY use it?**  
✓ Output: (0, 1) → Can interpret as probability  
✓ Smooth curve → Differentiable everywhere

**WHY NOT use it?** (Rarely used now)  
✗ Vanishing gradient: For large |x|, derivative ≈ 0 → Training stops!  
✗ Not zero-centered → Makes training harder

<details>
<summary><b>🔍 Example: Vanishing Gradient Problem</b></summary>

**Input values**: x = -10, -1, 0, 1, 10

**Sigmoid outputs**:
- $\\sigma(-10) = 0.000045$ ← Almost 0
- $\\sigma(-1) = 0.27$
- $\\sigma(0) = 0.5$
- $\\sigma(1) = 0.73$
- $\\sigma(10) = 0.999955$ ← Almost 1

**Derivatives** (gradient):
- At x = -10: derivative ≈ 0.00004 ← **Training stops here!**
- At x = 0: derivative = 0.25 ← Good for learning
- At x = 10: derivative ≈ 0.00004 ← **Training stops here too!**

**The problem**: In deep networks, gradients multiply. Small gradients (0.00004) become tiny (0.00004³ = 0.000000000064)!

**Result**: Early layers don't learn → Bad performance

</details>

---

#### 2. Hyperbolic Tangent (tanh)

$$
\\tanh(x) = \\frac{e^x - e^{-x}}{e^x + e^{-x}}
$$

**WHY use it?**  
✓ Output: (-1, 1) → Zero-centered! Better than sigmoid  
✓ Stronger gradients than sigmoid in middle range  
✓ Derivative: $1 - \\tanh(x)^2$ ← Easy to compute

**WHY NOT use it?**  
✗ Still suffers from vanishing gradient for large |x|  
✗ More expensive to compute than ReLU

**When to use**: Data is normalized around 0, or you need outputs between -1 and 1

<details>
<summary><b>🔍 Example: Why Zero-Centered Matters</b></summary>

**Scenario**: Training a weight $w$ with gradient descent

**With Sigmoid** (outputs 0-1):
- All activations are positive
- Gradient: $\\frac{\\partial L}{\\partial w} = \\text{activation} \\cdot \\text{error}$
- If activation always positive → gradients all same sign
- **Result**: Weight updates zigzag → slow convergence!

**With Tanh** (outputs -1 to 1):
- Activations can be negative or positive
- Gradients can point in any direction
- **Result**: More direct path to optimum → faster training!

</details>

---

#### 3. ReLU (Rectified Linear Unit) ⭐ **RECOMMENDED**

$$
\\text{ReLU}(x) = \\max(0, x) = \\begin{cases} x & \\text{if } x > 0 \\\\ 0 & \\text{if } x \\leq 0 \\end{cases}
$$

**WHY is this the BEST for most cases?**  
✓ **No vanishing gradient** for x > 0 (derivative = 1!)  
✓ **Super fast** to compute (just a comparison)  
✓ **Sparsity**: Many neurons output 0 → More efficient  
✓ **Empirically works better** than sigmoid/tanh in deep networks

**WHY NOT use it?**  
✗ "Dying ReLU": If neuron outputs 0, gradient = 0 → Never recovers  
✗ Not zero-centered (but less problematic than sigmoid)

<details>
<summary><b>🔍 Example: ReLU vs Sigmoid in Deep Network</b></summary>

**5-layer network, input x = 2**:

**With Sigmoid**:
1. Layer 1: $\\sigma(2 \\cdot 0.5) = \\sigma(1) = 0.73$
2. Layer 2: $\\sigma(0.73 \\cdot 0.5) = 0.59$
3. Layer 3: $\\sigma(0.59 \\cdot 0.5) = 0.57$
4. Layer 4: $\\sigma(0.57 \\cdot 0.5) = 0.57$
5. Layer 5: $\\sigma(0.57 \\cdot 0.5) = 0.57$

**Gradient** (backprop):
- Layer 5 → 4: 0.25
- Layer 4 → 3: 0.25 × 0.24 = 0.06
- Layer 3 → 2: 0.06 × 0.24 = 0.014
- Layer 2 → 1: 0.014 × 0.25 = 0.0035 ← **Almost vanished!**

**With ReLU**:
1. Layer 1: $\\max(0, 2 \\cdot 0.5) = 1$
2. Layer 2: $\\max(0, 1 \\cdot 0.5) = 0.5$
3. Layer 3: $\\max(0, 0.5 \\cdot 0.5) = 0.25$
4. Layer 4: $\\max(0, 0.25 \\cdot 0.5) = 0.125$
5. Layer 5: $\\max(0, 0.125 \\cdot 0.5) = 0.0625$

**Gradient** (backprop):
- All layers: 1 × 1 × 1 × 1 = 1 ← **No vanishing!**

**Result**: ReLU trains MUCH faster in deep networks!

</details>

**Bottom line**: Use **ReLU** unless you have a specific reason not to!

---

### Neural Network Architecture: Building Blocks

**WHY use multiple layers?**

Single layer = Can only draw straight lines/planes to separate classes  
Multiple layers = Can approximate ANY function! (Universal approximation theorem)

#### The Structure

```
Input Layer → Hidden Layer(s) → Output Layer
   [x₁]         [h₁]              [y₁]
   [x₂]    →    [h₂]         →    [y₂]
   [x₃]         [h₃]
```

**Each neuron computes**:
$$
\\text{output} = \\text{activation}\\left(\\sum_{i} w_i \\cdot \\text{input}_i + b\\right)
$$

<details>
<summary><b>🔍 Complete Example: 3-input, 2-hidden, 1-output network</b></summary>

**Problem**: Classify if customer will buy (yes/no)

**Input**: $\\boldsymbol{x} = [2.5, 1.8, 3.1]$ (age/10, income/10k, credit score/100)

**Hidden layer** (2 neurons):

Neuron 1:
- Weights: $\\boldsymbol{w_1} = [0.5, -0.3, 0.8]$, bias $b_1 = 0.1$
- Calculation: $0.5(2.5) - 0.3(1.8) + 0.8(3.1) + 0.1 = 3.29$
- Activation: $h_1 = \\text{ReLU}(3.29) = 3.29$

Neuron 2:
- Weights: $\\boldsymbol{w_2} = [-0.2, 0.9, 0.1]$, bias $b_2 = -0.5$
- Calculation: $-0.2(2.5) + 0.9(1.8) + 0.1(3.1) - 0.5 = 0.83$
- Activation: $h_2 = \\text{ReLU}(0.83) = 0.83$

**Output layer** (1 neuron):
- Weights: $\\boldsymbol{w_{out}} = [0.7, 0.4]$, bias $b_{out} = -0.2$
- Calculation: $0.7(3.29) + 0.4(0.83) - 0.2 = 2.43$
- Activation: $y = \\sigma(2.43) = 0.92$

**Prediction**: 0.92 > 0.5 → **YES**, customer will buy!

**WHY this works**:
- Hidden neurons extract features (neuron 1: "high value customer", neuron 2: "good credit")
- Output combines these features to make final decision

</details>

#### Architecture Notation

- `(10,)` = 1 hidden layer, 10 neurons
- `(20, 10)` = 2 hidden layers (20 neurons, then 10 neurons)
- `(50, 30, 10)` = 3 hidden layers (50 → 30 → 10)

**WHY the size matters**:

**Too small** (e.g., `(5,)`):
- Cannot learn complex patterns
- Underfitting → Poor accuracy

**Just right** (e.g., `(20, 10)`):
- Learns patterns without memorizing
- Good generalization

**Too large** (e.g., `(200, 100, 50)`):
- Memorizes training data
- Overfitting → Poor on new data

---

### Backpropagation: How Neural Networks Learn

**The Goal**: Adjust weights to minimize error

**The Method**: Gradient descent with chain rule (calculus!)

#### Forward Pass: Make Prediction

1. Input goes through each layer
2. Calculate activations
3. Get output prediction
4. Compare with true label → Calculate error

#### Error Function (Loss)

$$
\\varepsilon = \\frac{1}{2}\\sum_k (\\text{prediction}_k - \\text{true}_k)^2
$$

**WHY squared error?**  
✓ Always positive (error can't cancel out)  
✓ Differentiable (smooth gradient)  
✓ Penalizes large errors more (squared term)

<details>
<summary><b>🔍 Example: Why Squared Error Makes Sense</b></summary>

**Two predictions**:

Model A errors: [0.1, 0.1, 0.1, 0.1] → Average = 0.1
- Squared error: $0.1^2 + 0.1^2 + 0.1^2 + 0.1^2 = 0.04$

Model B errors: [0.0, 0.0, 0.0, 0.4] → Average = 0.1 (same!)
- Squared error: $0.0^2 + 0.0^2 + 0.0^2 + 0.4^2 = 0.16$

**Result**: Model A is better! Squared error captures this (0.04 < 0.16)

**WHY**: We prefer consistent small errors over occasional large errors

</details>

#### Backward Pass: Update Weights

1. Start at output layer
2. Calculate how much each weight contributed to error (gradient)
3. Propagate error backwards through network
4. Update weights: $w_{new} = w_{old} - \\alpha \\cdot \\text{gradient}$

**WHY it's called "backpropagation"**: Error propagates BACKWARDS from output to input!

**The Math** (for one layer):

For output layer:
$$
\\frac{\\partial \\varepsilon}{\\partial w} = (\\text{prediction} - \\text{true}) \\cdot (1 - \\text{activation}^2) \\cdot \\text{input}
$$

**Translation**:
- $(\\text{prediction} - \\text{true})$ = How wrong we were
- $(1 - \\text{activation}^2)$ = How sensitive activation is (derivative of tanh)
- $\\text{input}$ = What value was fed to this weight

**WHY multiply these?** Chain rule from calculus! Each term is one link in the computation chain.

---

### MLPClassifier: Putting It All Together

**MLP** = Multi-Layer Perceptron = Feedforward Neural Network

**Parameters you control**:

#### hidden_layer_sizes

**What**: Architecture of hidden layers

**Examples**:
- `(10,)` = 1 layer, 10 neurons
- `(20, 10)` = 2 layers, 20 then 10 neurons
- `(50, 30, 10)` = 3 layers, 50 → 30 → 10 neurons

**WHY it matters**:
- More layers = Can learn more complex patterns
- BUT: More layers = Longer training, risk of overfitting
- **Rule of thumb**: Start with 1-2 layers

<details>
<summary><b>🔍 How many parameters?</b></summary>

**Example**: 3 inputs, (5, 3) hidden, 2 outputs

**Layer 1** (input → hidden 1):
- Weights: 3 inputs × 5 neurons = 15
- Biases: 5 neurons = 5
- **Total: 20 parameters**

**Layer 2** (hidden 1 → hidden 2):
- Weights: 5 × 3 = 15
- Biases: 3 = 3
- **Total: 18 parameters**

**Layer 3** (hidden 2 → output):
- Weights: 3 × 2 = 6
- Biases: 2 = 2
- **Total: 8 parameters**

**Grand total: 20 + 18 + 8 = 46 parameters to learn!**

**WHY this matters**: More parameters = need more training data

</details>

#### activation

**What**: Function used in hidden layers

**Choices**:
- `'relu'` ⭐ **RECOMMENDED** - Fast, avoids vanishing gradient
- `'tanh'` - Good for normalized data
- `'logistic'` - Rarely used (sigmoid, vanishing gradient)

**WHY ReLU is default**: Works best in practice, fastest to compute

#### solver

**What**: Algorithm to update weights

**Choices**:
- `'adam'` ⭐ **RECOMMENDED** - Adaptive learning rate, robust
- `'sgd'` - Simple, requires tuning
- `'lbfgs'` - Good for small datasets, uses more memory

**WHY they differ**:

**adam**: Adjusts learning rate per-parameter → Faster convergence  
**sgd**: Fixed learning rate → Need to tune carefully  
**lbfgs**: Uses second-order information → More accurate but expensive

<details>
<summary><b>🔍 Example: adam vs sgd</b></summary>

**Training scenario**: 100 iterations

**sgd with learning_rate=0.01**:
- Iterations 1-50: Loss decreases steadily
- Iterations 51-100: Loss barely changes (learning rate too small now!)
- **Final loss: 0.15**

**sgd with learning_rate=0.1**:
- Iterations 1-10: Loss decreases fast
- Iterations 11-100: Loss bouncing around (learning rate too big!)
- **Final loss: 0.12**

**adam** (adapts automatically):
- Iterations 1-20: Fast decrease (large steps)
- Iterations 21-100: Slow decrease (small steps near optimum)
- **Final loss: 0.08** ← **Best!**

**WHY adam wins**: Automatically adjusts learning rate based on gradients!

</details>

#### max_iter

**What**: Maximum training iterations

**Why it matters**: Network needs time to learn!

**Typical values**:
- 100-500: Quick experiments
- 500-1000: Standard training
- 1000-2000: If you see "ConvergenceWarning"

**WHY increase it**: If model hasn't converged, give it more time!

---

### Practical Tips

#### When to use different solvers

**Use `adam` when**:
- Large datasets (>1000 samples) ✅
- You want it to "just work" ✅
- Default choice for most problems ✅

**WHY**: Adapts learning rate automatically, robust to hyperparameter choices

**Use `lbfgs` when**:
- Small datasets (<1000 samples) ✅
- You have enough memory ✅
- You want faster convergence ✅

**WHY**: Uses more sophisticated optimization (quasi-Newton method)

**Use `sgd` when**:
- Very large datasets (online learning) ✅
- You need fine control over learning ✅
- You're an expert tuning hyperparameters ✅

**WHY**: Simple, memory-efficient, but requires careful tuning

#### Architecture selection

**Start simple**: `(20,)` or `(50,)`

**If underfitting** (poor accuracy):
→ Increase size: `(20,)` → `(50,)` → `(100,)`  
→ Add depth: `(50,)` → `(50, 30)` → `(50, 30, 10)`

**If overfitting** (great on training, poor on test):
→ Decrease size: `(100,)` → `(50,)` → `(20,)`  
→ Reduce depth: `(50, 30, 10)` → `(50, 30)` → `(50,)`

**WHY this strategy**: Find the "sweet spot" between too simple and too complex!

---

For practical usage guide, see **[README.md](./README.md)**
"""
        )
