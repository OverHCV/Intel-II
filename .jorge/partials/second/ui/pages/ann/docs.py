"""
ANN Documentation Component
Theory and fundamentals - displayable in UI
"""

import streamlit as st


def render_ann_documentation():
    """
    Render expandable ANN theory documentation
    Theory extracted from course materials
    """
    with st.expander("📚 **Theory: Artificial Neural Networks**", expanded=False):
        st.markdown(
            """
### What is an Artificial Neural Network (ANN)?

An **Artificial Neural Network** extends the linear discriminant function by using **differentiable activation functions** instead of the sign function, enabling gradient descent optimization:

$$
d_i = \\text{activation}(\\boldsymbol{w}^T \\phi(\\boldsymbol{x}_i))
$$

Where:
- $\\boldsymbol{w}$ = weight vector
- $\\phi(\\cdot)$ = non-linear mapping function
- $\\text{activation}(\\cdot)$ = differentiable activation function

---

### Activation Functions

Neural networks use **differentiable activation functions** to enable backpropagation:

**1. Sigmoid (Logistic)**
$$
\\sigma(x) = \\frac{1}{1+e^{-x}}
$$
- Output range: (0, 1)
- Smooth, differentiable
- Can suffer from vanishing gradients

**2. Hyperbolic Tangent (tanh)**
$$
\\tanh(x) = \\frac{e^x - e^{-x}}{e^x + e^{-x}}
$$
- Output range: (-1, 1)
- Zero-centered (better than sigmoid)
- Derivative: $1 - \\tanh(x)^2$

**3. ReLU (Rectified Linear Unit)** - *Recommended*
$$
\\text{ReLU}(x) = \\max(0, x)
$$
- Most popular modern activation
- Fast computation
- Avoids vanishing gradient
- Can suffer from "dying ReLU" problem

---

### Neural Network Architecture

A **Multi-Layer Perceptron (MLP)** or **Feedforward Network** consists of:

**Layers:**
- **Input Layer**: Features from dataset
- **Hidden Layers**: 1 or more layers of neurons
- **Output Layer**: Class predictions

**Neuron Operation:**

For a neuron $k$ in the output layer:
$$
s_k = \\sigma_2\\left( \\boldsymbol{w}_{k,2}^T \\boldsymbol{d} \\right)
$$

Where $\\boldsymbol{d}$ is the output from the hidden layer:
$$
d_j = \\sigma_1\\left( \\boldsymbol{w}_{j,1}^T \\boldsymbol{x} \\right)
$$

**Architecture Notation:**
- `(10,)` = 1 hidden layer with 10 neurons
- `(20, 10)` = 2 hidden layers with 20 and 10 neurons
- `(50, 30, 10)` = 3 hidden layers

---

### Backpropagation Algorithm

**Training Process:**

1. **Forward Pass**: Propagate input through network
   - Calculate activations for all neurons
   - Compute output predictions

2. **Error Calculation**: Compare predictions with targets
   $$
   \\varepsilon = \\frac{1}{2}\\sum_k (s_k - y_k)^2
   $$

3. **Backward Pass**: Propagate errors backwards
   - Calculate gradients for all weights
   - Use chain rule for derivatives

4. **Weight Update**: Adjust weights using gradient descent
   $$
   \\boldsymbol{w}^{(\\tau+1)} = \\boldsymbol{w}^{(\\tau)} - \\alpha \\nabla \\varepsilon
   $$

**Key Insight**: Backpropagation efficiently computes gradients for all layers using the chain rule.

---

### MLPClassifier Parameters

**Architecture:**
- `hidden_layer_sizes`: Tuple defining network structure
  - Example: `(20, 10)` = 2 hidden layers
  - More layers = deeper network, more complex patterns
  - Too deep = overfitting, longer training

**Activation Function:**
- `'relu'`: **Recommended** - Fast, effective, standard choice
- `'tanh'`: Good for normalized data, zero-centered
- `'logistic'`: Sigmoid function, rarely used now

**Solver (Optimization Algorithm):**
- `'adam'`: **Recommended** - Adaptive learning rate, robust
- `'sgd'`: Stochastic Gradient Descent - simple, requires tuning
- `'lbfgs'`: Quasi-Newton method - good for small datasets

**Training Parameters:**
- `max_iter`: Maximum training iterations (default: 200)
  - Increase if model doesn't converge
  - 500-2000 is common range
- `alpha`: L2 regularization strength (default: 0.0001)
  - Higher = more regularization, simpler model
- `learning_rate`: Learning rate schedule
  - `'constant'`: Fixed rate
  - `'adaptive'`: Reduces if no improvement

---

### When to Use Different Solvers

**Use `adam` (default) when:**
- Large datasets (>1000 samples)
- General-purpose, works well in most cases
- You want adaptive learning rate

**Use `lbfgs` when:**
- Small to medium datasets (<1000 samples)
- You want faster convergence
- Memory is not a constraint

**Use `sgd` when:**
- Very large datasets
- Online learning (streaming data)
- You need fine control over learning rate

---

### Architecture Selection Tips

**Shallow Networks (1-2 layers):**
- Faster training
- Less prone to overfitting
- Good starting point
- Example: `(20,)` or `(50, 20)`

**Deep Networks (3+ layers):**
- Can learn complex patterns
- Requires more data
- Longer training time
- Risk of overfitting
- Example: `(100, 50, 20)`

**Rule of Thumb:**
1. Start with 1 hidden layer
2. Number of neurons ≈ 2/3 * (input + output)
3. If underfitting, add more neurons or layers
4. If overfitting, reduce complexity or add regularization

---

### Common Issues

**Convergence Warning:**
- Increase `max_iter` (try 1000-2000)
- Try different solver (`lbfgs` for small data)
- Scale/normalize features first

**Poor Performance:**
- Try different architectures
- Change activation function
- Adjust regularization (`alpha`)
- Ensure data is properly scaled

**Overfitting:**
- Reduce network size
- Increase regularization (`alpha`)
- Get more training data
- Use early stopping

---

For detailed usage guide, see **[README.md](./README.md)**
"""
        )

