# ===========================
# Common Imports
# ===========================

# Core libraries
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from settings.options import ANNActivation, ANNSolver, HandleCategorical, SVMKernel

warnings.filterwarnings("ignore")

# Sklearn - Preprocessing
from time import time

# Additional utilities
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# Sklearn - Metrics
# Métricas y utilidades de sklearn (solo para métricas, no para evaluación)
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import (
    GridSearchCV,
    cross_val_predict,
    cross_val_score,
    train_test_split,
)

# Sklearn - Classifiers
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler

# Sklearn - Classifiers
from sklearn.svm import SVC
