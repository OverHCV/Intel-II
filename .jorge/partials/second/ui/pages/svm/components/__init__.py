"""
SVM Page Components
Modular components for the SVM interface
"""

from ui.pages.svm.components.best_model_saver import render_best_model_saver
from ui.pages.svm.components.model_config import render_model_configuration
from ui.pages.svm.components.visualizations import render_visualizations

__all__ = [
    "render_model_configuration",
    "render_visualizations",
    "render_best_model_saver",
]

