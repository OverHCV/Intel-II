"""
SVM Documentation - Theory and Learning Materials
Extracted from docs/5-SVM-Kernel.ipynb
"""

import streamlit as st


def render_svm_documentation():
    """Render expandable documentation about SVM and kernels"""
    with st.expander(
        "📚 **Theory & Docs** - More about SVMs and Kernels",
        expanded=False,
    ):
        st.markdown("""
        ### 🎯 Why Support Vector Machines?
        
        Support Vector Machines (SVMs) are powerful classifiers that find the **optimal separating hyperplane** 
        between classes by maximizing the margin between them.
        
        ---
        
        ### 🔄 The Non-Linear Problem
        
        **Linear classifiers only work when classes are linearly separable.** But what if data has complex patterns?
        
        **Solution**: Map data to a **higher-dimensional space** where it becomes linearly separable:
        """)

        st.latex(r"\phi: \mathbb{R}^n \rightarrow \mathbb{R}^m \text{ where } m > n")

        st.markdown("""
        **Example**: Circular data in 2D (not linearly separable) → Map to 3D using φ(x₁, x₂) = [x₁², x₂², x₁x₂] → Now linearly separable!
        
        **Problem**: High-dimensional mappings are computationally expensive.
        
        ---
        
        ### ✨ The Kernel Trick
        
        **Key insight**: We don't need to compute φ(x) explicitly!
        
        Instead, we use a **kernel function** that computes the dot product in the mapped space directly:
        """)

        st.latex(
            r"k(\boldsymbol{a}, \boldsymbol{b}) = \phi(\boldsymbol{a})^T \phi(\boldsymbol{b})"
        )

        st.markdown("""
        **Example**: Polynomial kernel k(a,b) = (aᵀb)² achieves the same result as explicitly mapping to polynomial space!
        
        **Benefits**:
        - ⚡ Computational efficiency (no explicit mapping)
        - 🎯 Works in infinite dimensions (RBF kernel)
        - 🛠️ Easy to swap kernels without changing algorithm
        
        ---
        
        ### 🔧 Common Kernels
        """)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **1. Linear Kernel**
            """)
            st.latex(
                r"k(\boldsymbol{x}, \boldsymbol{y}) = \boldsymbol{x}^T \boldsymbol{y}"
            )
            st.markdown("""
            - No mapping (original space)
            - **When to use**: Linearly separable data, high-dimensional data
            - **Pros**: Fast, no overfitting risk
            """)

            st.markdown("""
            **2. Polynomial Kernel**
            """)
            st.latex(
                r"k(\boldsymbol{x}, \boldsymbol{y}) = (\gamma \cdot \boldsymbol{x}^T \boldsymbol{y} + r)^d"
            )
            st.markdown("""
            - Maps to polynomial space of degree d
            - **When to use**: Data with polynomial relationships
            - **Warning**: High degree → overfitting risk
            """)

        with col2:
            st.markdown("""
            **3. RBF (Gaussian) Kernel** ⭐ Most Popular
            """)
            st.latex(
                r"k(\boldsymbol{x}, \boldsymbol{y}) = \exp\left(-\gamma \|\boldsymbol{x} - \boldsymbol{y}\|^2\right)"
            )
            st.markdown("""
            - Maps to infinite dimensional space!
            - **When to use**: Default choice, works for most problems
            - **Pros**: Very flexible, handles complex boundaries
            """)

            st.markdown("""
            **4. Sigmoid Kernel**
            """)
            st.latex(
                r"k(\boldsymbol{x}, \boldsymbol{y}) = \tanh(\gamma \cdot \boldsymbol{x}^T \boldsymbol{y} + r)"
            )
            st.markdown("""
            - Neural network-like behavior
            - **When to use**: Specific applications
            - **Note**: Not always positive definite
            """)

        st.markdown("""
        ---
        
        ### ⚙️ Parameter Guide
        """)

        st.markdown("""
        **C (Regularization Parameter)**
        - **Controls**: Trade-off between margin size and classification errors
        - **Small C** (< 1): Wide margin, tolerates errors → **prevents overfitting**
        - **Large C** (> 10): Narrow margin, fewer errors → **risk of overfitting**
        - **Recommendation**: Start with C=1, then try [0.1, 1, 10, 100]
        
        ---
        
        **γ (gamma) - Kernel Coefficient**
        - **Controls**: Influence of individual training samples
        - **Small γ**: Far points have influence → **smooth, simple boundary**
        - **Large γ**: Only nearby points matter → **complex boundary, overfitting risk**
        - **'scale'**: 1 / (n_features × variance) ← **Good default**
        - **'auto'**: 1 / n_features
        - **Recommendation**: Start with 'scale', then try [0.001, 0.01, 0.1, 1]
        
        ---
        
        **degree (d) - Polynomial Degree**
        - **Controls**: Complexity of polynomial mapping (poly kernel only)
        - **Typical range**: 2-5
        - **Higher degree**: More complex boundary, overfitting risk
        - **Recommendation**: Start with d=3, try [2, 3, 4]
        
        ---
        
        ### 📊 How SVMs Work Mathematically
        
        SVMs solve an optimization problem to find the best separating hyperplane:
        """)

        st.latex(r"""
        \begin{aligned}
        \text{minimize} \quad & \sum_{i=1}^N \lambda_i - \frac{1}{2}\sum_{i,j}^N \lambda_i \lambda_j y_i y_j \, k(\boldsymbol{x}_i, \boldsymbol{x}_j) \\
        \text{subject to} \quad & \sum_{i=1}^N y_i \lambda_i = 0 \\
        & 0 \leq \lambda_i \leq C
        \end{aligned}
        """)

        st.markdown("""
        Where:
        - λᵢ are Lagrange multipliers (one per training sample)
        - Samples with λᵢ > 0 are **support vectors** (define the decision boundary)
        - k(xᵢ, xⱼ) is the kernel function
        - C is the regularization parameter
        
        **Prediction** for a new sample **x**:
        """)

        st.latex(
            r"f(\boldsymbol{x}) = \text{sign}\left(\sum_{i=1}^N \lambda_i y_i \, k(\boldsymbol{x}_i, \boldsymbol{x}) + b\right)"
        )

        st.markdown("""
        ---
        
        ### 💡 Practical Tips for the Exam
        
        1. **Start with RBF kernel** - Works well for most problems
        2. **Try different C values**: [0.1, 1, 10, 100]
        3. **Try different γ values**: ['scale', 0.001, 0.01, 0.1, 1]
        4. **Use cross-validation** to avoid overfitting
        5. **Compare kernels systematically** - Track all experiments
        6. **Look for patterns**:
           - High CV variance → Overfitting (reduce C or γ)
           - Low train & test accuracy → Underfitting (increase C or γ)
        7. **Don't forget Linear kernel** - Sometimes simple is best!
        
        ---
        
        ### 📖 References
        - UCI Bank Marketing Dataset: Binary classification problem
        - Task: Test different kernels and parameters with cross-validation
        - Goal: Find best configuration and analyze WHY it works
        """)
