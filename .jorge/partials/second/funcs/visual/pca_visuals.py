"""
PCA-Specific Visualization Functions
"""

import matplotlib.pyplot as plt
import numpy as np
from settings.config import CONF, Keys


def plot_pca_variance(pca_object, title="PCA Explained Variance"):
    """
    Plot cumulative explained variance by PCA components

    Args:
        pca_object: Fitted PCA object
        title: Plot title

    Returns:
        matplotlib Figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=CONF[Keys.FIGURE_SIZE_MEDIUM])

    n_components = len(pca_object.explained_variance_ratio_)
    components = range(1, n_components + 1)

    # Individual variance
    ax1.bar(components, pca_object.explained_variance_ratio_)
    ax1.set_xlabel("Component")
    ax1.set_ylabel("Explained Variance Ratio")
    ax1.set_title("Individual Variance")
    ax1.grid(alpha=CONF[Keys.GRID_ALPHA], axis="y")

    # Cumulative variance
    cumulative_variance = np.cumsum(pca_object.explained_variance_ratio_)
    ax2.plot(components, cumulative_variance, marker="o")
    ax2.axhline(
        y=CONF[Keys.PCA_VARIANCE_THRESHOLD],
        color="r",
        linestyle="--",
        label=f"{CONF[Keys.PCA_VARIANCE_THRESHOLD]:.0%} threshold",
    )
    ax2.set_xlabel("Number of Components")
    ax2.set_ylabel("Cumulative Explained Variance")
    ax2.set_title("Cumulative Variance")
    ax2.legend()
    ax2.grid(alpha=CONF[Keys.GRID_ALPHA])

    plt.suptitle(title)
    plt.tight_layout()
    return fig


def plot_comparison(
    original_metrics: dict,
    pca_metrics: dict,
    title="Original vs PCA Comparison",
):
    """
    Plot side-by-side comparison of metrics before and after PCA

    Args:
        original_metrics: Metrics from original features
        pca_metrics: Metrics after PCA transformation
        title: Plot title

    Returns:
        matplotlib Figure
    """
    fig, ax = plt.subplots(figsize=CONF[Keys.FIGURE_SIZE_MEDIUM])

    metric_names = list(original_metrics.keys())
    original_values = list(original_metrics.values())
    pca_values = list(pca_metrics.values())

    x = np.arange(len(metric_names))
    width = 0.35

    ax.bar(x - width / 2, original_values, width, label="Original", alpha=0.8)
    ax.bar(x + width / 2, pca_values, width, label="PCA", alpha=0.8)

    ax.set_ylabel("Score")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(metric_names)
    ax.legend()
    ax.grid(alpha=CONF[Keys.GRID_ALPHA], axis="y")
    ax.set_ylim(0, 1)

    # Add value labels
    for i, v in enumerate(original_values):
        ax.text(i - width / 2, v, f"{v:.3f}", ha="center", va="bottom", fontsize=8)
    for i, v in enumerate(pca_values):
        ax.text(i + width / 2, v, f"{v:.3f}", ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    return fig


def plot_decision_boundary_2d(X, y, model, title="Decision Boundary"):
    """
    Plot 2D decision boundary (for PCA with 2 components)

    Args:
        X: Feature matrix (2D)
        y: Target labels
        model: Trained classifier
        title: Plot title

    Returns:
        matplotlib Figure
    """
    if X.shape[1] != 2:
        raise ValueError("X must have exactly 2 features for 2D plot")

    fig, ax = plt.subplots(figsize=CONF[Keys.FIGURE_SIZE_SMALL])

    # Create mesh
    h = 0.02  # Step size in mesh
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Predict on mesh
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # Plot decision boundary
    ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdYlBu)

    # Plot data points
    scatter = ax.scatter(
        X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdYlBu, edgecolors="k", s=50
    )

    ax.set_xlabel("First Component")
    ax.set_ylabel("Second Component")
    ax.set_title(title)
    plt.colorbar(scatter, ax=ax)

    plt.tight_layout()
    return fig

