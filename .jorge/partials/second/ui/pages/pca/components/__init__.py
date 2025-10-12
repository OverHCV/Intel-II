"""
PCA Page Components
Modular components for the PCA interface
"""

from ui.pages.pca.components.model_comparison import render_model_comparison
from ui.pages.pca.components.overall_analysis import render_overall_analysis
from ui.pages.pca.components.pca_transformer import render_pca_transformer
from ui.pages.pca.components.visualizations import render_pca_visualizations

__all__ = [
    "render_pca_visualizations",
    "render_pca_transformer",
    "render_model_comparison",
    "render_overall_analysis",
]

