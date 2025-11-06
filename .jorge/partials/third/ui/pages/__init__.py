"""
UI Pages Package - All page render functions.

Each page follows the same pattern:
1. Display theory/explanation
2. Show controls
3. Execute logic
4. Display results with visualizations
"""

from .review import dataset_review
from .dtree import decision_tree
from . import hierarchical
from . import kmeans
from . import history

__all__ = ["dataset_review", "decision_tree", "hierarchical", "kmeans", "history"]

