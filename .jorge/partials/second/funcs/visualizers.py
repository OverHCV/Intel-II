"""
Visualization Functions for ML Analysis
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats
from settings.config import CONF, Keys
from sklearn.metrics import confusion_matrix


def plot_confusion_matrix(y_true, y_pred, labels=None, title="Confusion Matrix"):
    """
    Plot confusion matrix heatmap

    Args:
        y_true: True labels
        y_pred: Predicted labels
        labels: Class labels
        title: Plot title

    Returns:
        matplotlib Figure
    """
    cm = confusion_matrix(y_true, y_pred)

    fig, ax = plt.subplots(figsize=CONF[Keys.FIGURE_SIZE_SMALL])

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap=CONF[Keys.COLOR_MAP],
        xticklabels=labels if labels else ["Class 0", "Class 1"],
        yticklabels=labels if labels else ["Class 0", "Class 1"],
        ax=ax,
    )

    ax.set_title(title)
    ax.set_ylabel("True Label")
    ax.set_xlabel("Predicted Label")

    plt.tight_layout()
    return fig


def plot_metrics_bars(metrics: dict, title="Model Performance"):
    """
    Plot metrics as bar chart

    Args:
        metrics: Dictionary of metric_name: value
        title: Plot title

    Returns:
        matplotlib Figure
    """
    fig, ax = plt.subplots(figsize=CONF[Keys.FIGURE_SIZE_SMALL])

    metric_names = list(metrics.keys())
    metric_values = list(metrics.values())

    bars = ax.bar(
        metric_names,
        metric_values,
        color=plt.cm.viridis(np.linspace(0, 1, len(metric_names))),
    )

    ax.set_title(title)
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1)
    ax.grid(alpha=CONF[Keys.GRID_ALPHA], axis="y")

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height:.3f}",
            ha="center",
            va="bottom",
        )

    plt.tight_layout()
    return fig


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


def plot_learning_curve(train_scores, val_scores, param_range, param_name="Parameter"):
    """
    Plot learning curve showing train/validation scores vs parameter

    Args:
        train_scores: Training scores
        val_scores: Validation scores
        param_range: Parameter values
        param_name: Name of parameter being varied

    Returns:
        matplotlib Figure
    """
    fig, ax = plt.subplots(figsize=CONF[Keys.FIGURE_SIZE_SMALL])

    ax.plot(param_range, train_scores, marker="o", label="Training Score")
    ax.plot(param_range, val_scores, marker="s", label="Validation Score")

    ax.set_xlabel(param_name)
    ax.set_ylabel("Score")
    ax.set_title(f"Learning Curve - {param_name}")
    ax.legend()
    ax.grid(alpha=CONF[Keys.GRID_ALPHA])

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


def plot_correlation_heatmap(X, feature_names, title="Feature Correlation Matrix"):
    """
    Plot correlation heatmap between features

    Args:
        X: Feature matrix (numpy array or DataFrame)
        feature_names: List of feature names
        title: Plot title

    Returns:
        matplotlib Figure
    """
    import pandas as pd

    # Convert to DataFrame if needed
    if not isinstance(X, pd.DataFrame):
        df = pd.DataFrame(X, columns=feature_names)
    else:
        df = X

    # Calculate correlation matrix
    corr_matrix = df.corr()

    # Create figure
    fig, ax = plt.subplots(figsize=CONF[Keys.FIGURE_SIZE_MEDIUM])

    # Create mask for upper triangle (optional - shows only lower half)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)

    # Plot heatmap
    sns.heatmap(
        corr_matrix,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="RdBu_r",  # Diverging colormap: red=negative, blue=positive
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8, "label": "Correlation Coefficient"},
        ax=ax,
    )

    ax.set_title(title, fontsize=14, fontweight="bold", pad=20)

    plt.tight_layout()
    return fig


def plot_feature_distributions(
    X, feature_names, feature_indices=None, title_prefix="Distribution"
):
    """
    Plot distribution histograms with KDE overlay for multiple features

    Args:
        X: Feature matrix
        feature_names: List of all feature names
        feature_indices: List of indices to plot (default: first 4)
        title_prefix: Prefix for subplot titles

    Returns:
        matplotlib Figure
    """
    if feature_indices is None:
        # Select first 4 features by default
        feature_indices = list(range(min(4, len(feature_names))))

    n_features = len(feature_indices)
    fig, axes = plt.subplots(1, n_features, figsize=(5 * n_features, 4))

    # Handle single feature case
    if n_features == 1:
        axes = [axes]

    for idx, (ax, feat_idx) in enumerate(zip(axes, feature_indices)):
        data = X[:, feat_idx]
        feature_name = feature_names[feat_idx]

        # Histogram with KDE overlay
        ax.hist(
            data, bins=30, density=True, alpha=0.6, color="skyblue", edgecolor="black"
        )

        # KDE overlay
        kde_x = np.linspace(data.min(), data.max(), 100)
        kde = stats.gaussian_kde(data)
        ax.plot(kde_x, kde(kde_x), "r-", linewidth=2, label="KDE")

        # Normal distribution overlay for reference
        mu, sigma = data.mean(), data.std()
        normal_curve = stats.norm.pdf(kde_x, mu, sigma)
        ax.plot(kde_x, normal_curve, "g--", linewidth=2, label="Normal", alpha=0.7)

        # Styling
        ax.set_title(f"{feature_name}", fontsize=11, fontweight="bold")
        ax.set_xlabel("Value", fontsize=9)
        ax.set_ylabel("Density", fontsize=9)
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3, axis="y")

        # Add statistics text
        stats_text = f"μ={mu:.2f}\nσ={sigma:.2f}"
        ax.text(
            0.02,
            0.98,
            stats_text,
            transform=ax.transAxes,
            verticalalignment="top",
            fontsize=8,
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
        )

    plt.suptitle(f"{title_prefix} Analysis", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    return fig


def plot_feature_boxplots(X, feature_names, y=None, title="Feature Box Plots"):
    """
    Plot box plots for all features to show distribution and outliers

    Args:
        X: Feature matrix
        feature_names: List of feature names
        y: Target labels (optional, for color coding)
        title: Plot title

    Returns:
        matplotlib Figure
    """
    import pandas as pd

    # Convert to DataFrame
    if not isinstance(X, pd.DataFrame):
        df = pd.DataFrame(X, columns=feature_names)
    else:
        df = X

    n_features = len(feature_names)
    fig, ax = plt.subplots(figsize=(max(12, n_features * 1.5), 6))

    # Create box plot
    bp = ax.boxplot(
        [df[col] for col in feature_names],
        labels=feature_names,
        patch_artist=True,
        showmeans=True,
        meanprops=dict(marker="D", markerfacecolor="red", markersize=6),
    )

    # Color boxes with gradient
    colors = plt.cm.viridis(np.linspace(0, 1, n_features))
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)

    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_ylabel("Scaled Value", fontsize=11)
    ax.set_xlabel("Features", fontsize=11)
    ax.grid(alpha=0.3, axis="y")

    # Rotate x labels if too many
    if n_features > 5:
        plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    return fig


def plot_qq_plots(X, feature_names, feature_indices=None):
    """
    Plot Q-Q plots to test normality of features

    Args:
        X: Feature matrix
        feature_names: List of all feature names
        feature_indices: List of indices to plot (default: first 4)

    Returns:
        matplotlib Figure
    """
    if feature_indices is None:
        feature_indices = list(range(min(4, len(feature_names))))

    n_features = len(feature_indices)
    fig, axes = plt.subplots(1, n_features, figsize=(5 * n_features, 4))

    if n_features == 1:
        axes = [axes]

    for idx, (ax, feat_idx) in enumerate(zip(axes, feature_indices)):
        data = X[:, feat_idx]
        feature_name = feature_names[feat_idx]

        # Q-Q plot
        stats.probplot(data, dist="norm", plot=ax)
        ax.set_title(f"Q-Q: {feature_name}", fontsize=11, fontweight="bold")
        ax.grid(alpha=0.3)

        # Calculate and display Shapiro-Wilk test
        stat, p_value = stats.shapiro(
            data[: min(5000, len(data))]
        )  # Limit for performance
        normality = "Normal" if p_value > 0.05 else "Non-Normal"
        color = "green" if p_value > 0.05 else "red"

        ax.text(
            0.05,
            0.95,
            f"{normality}\np={p_value:.4f}",
            transform=ax.transAxes,
            verticalalignment="top",
            fontsize=9,
            bbox=dict(boxstyle="round", facecolor=color, alpha=0.3),
        )

    plt.suptitle("Normality Test (Q-Q Plots)", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    return fig


def plot_interactive_scatter_2d(
    X,
    y,
    feature_names,
    x_idx=0,
    y_idx=1,
    class_names=None,
    title="Feature Scatter Plot",
):
    """
    Plot 2D scatter plot with two selected features

    Args:
        X: Feature matrix
        y: Target labels
        feature_names: List of feature names
        x_idx: Index of feature for X axis
        y_idx: Index of feature for Y axis
        class_names: List of class names
        title: Plot title

    Returns:
        matplotlib Figure
    """
    fig, ax = plt.subplots(figsize=CONF[Keys.FIGURE_SIZE_SMALL])

    # Get unique classes
    unique_classes = np.unique(y)

    # Use class names if provided, otherwise use class numbers
    if class_names is None:
        class_names = [f"Class {int(c)}" for c in unique_classes]

    # Create scatter plot for each class
    colors = plt.cm.viridis(np.linspace(0, 1, len(unique_classes)))

    for idx, class_val in enumerate(unique_classes):
        mask = y == class_val
        ax.scatter(
            X[mask, x_idx],
            X[mask, y_idx],
            c=[colors[idx]],
            label=class_names[idx],
            alpha=0.6,
            s=50,
            edgecolors="k",
            linewidth=0.5,
        )

    ax.set_xlabel(feature_names[x_idx], fontsize=12)
    ax.set_ylabel(feature_names[y_idx], fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend(loc="best")
    ax.grid(alpha=CONF[Keys.GRID_ALPHA])

    plt.tight_layout()
    return fig


def plot_interactive_scatter_3d(
    X,
    y,
    feature_names,
    x_idx=0,
    y_idx=1,
    z_idx=2,
    class_names=None,
    title="3D Feature Scatter Plot",
):
    """
    Plot 3D scatter plot with three selected features using plotly

    Args:
        X: Feature matrix
        y: Target labels
        feature_names: List of feature names
        x_idx: Index of feature for X axis
        y_idx: Index of feature for Y axis
        z_idx: Index of feature for Z axis
        class_names: List of class names
        title: Plot title

    Returns:
        plotly Figure or None if plotly not available
    """
    try:
        import plotly.graph_objects as go

        # Get unique classes
        unique_classes = np.unique(y)

        # Use class names if provided
        if class_names is None:
            class_names = [f"Class {int(c)}" for c in unique_classes]

        # Create traces for each class
        traces = []
        colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

        for idx, class_val in enumerate(unique_classes):
            mask = y == class_val
            trace = go.Scatter3d(
                x=X[mask, x_idx],
                y=X[mask, y_idx],
                z=X[mask, z_idx],
                mode="markers",
                name=class_names[idx],
                marker=dict(
                    size=5,
                    color=colors[idx % len(colors)],
                    opacity=0.7,
                    line=dict(color="white", width=0.5),
                ),
            )
            traces.append(trace)

        # Create layout
        layout = go.Layout(
            title=title,
            scene=dict(
                xaxis_title=feature_names[x_idx],
                yaxis_title=feature_names[y_idx],
                zaxis_title=feature_names[z_idx],
            ),
            template="plotly_white",
            showlegend=True,
            legend=dict(x=0.7, y=0.9),
        )

        fig = go.Figure(data=traces, layout=layout)
        return fig

    except ImportError:
        print("Warning: plotly not available, falling back to 2D plot")
        return None
