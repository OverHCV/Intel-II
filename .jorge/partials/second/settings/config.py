"""
Bank Marketing Dataset - Configuration File
=============================================
Centralized configuration for SVM, ANN, and PCA analysis
Based on the Bank Marketing dataset from UCI ML Repository
"""

from settings.feats import BankFeatures, BankTarget
from settings.options import ANNActivation, ANNSolver, HandleCategorical, SVMKernel

print("\nLibraries imported successfully")
print("=" * 50)


# ===========================
# Configuration Keys
# ===========================


class Keys:
    """Keys for accessing configuration dictionary"""

    # Dataset paths
    DATASET_PATH_FULL = "dataset_path_full"
    DATASET_PATH_SMALL = "dataset_path_small"
    DATASET_DELIMITER = "dataset_delimiter"
    DATASET_ENCODING = "dataset_encoding"

    # Feature selection
    NUMERICAL_FEATURES = "numerical_features"
    CATEGORICAL_FEATURES = "categorical_features"
    ALL_FEATURES = "all_features"
    TARGET_COLUMN = "target_column"

    # Data preprocessing
    SCALE_FEATURES = "scale_features"
    HANDLE_CATEGORICAL = "handle_categorical"

    # General ML parameters
    RANDOM_STATE = "random_state"
    TEST_SIZE = "test_size"
    CV_FOLDS = "cv_folds"

    # SVM configurations
    SVM_KERNELS = "svm_kernels"
    SVM_C_VALUES = "svm_c_values"
    SVM_GAMMA_VALUES = "svm_gamma_values"
    SVM_DEGREE_VALUES = "svm_degree_values"
    SVM_MAX_ITER = "svm_max_iter"

    # ANN configurations
    ANN_ARCHITECTURES = "ann_architectures"
    ANN_ACTIVATIONS = "ann_activations"
    ANN_SOLVERS = "ann_solvers"
    ANN_MAX_ITER = "ann_max_iter"
    ANN_LEARNING_RATE = "ann_learning_rate"
    ANN_ALPHA = "ann_alpha"

    # PCA configurations
    PCA_N_COMPONENTS_RANGE = "pca_n_components_range"
    PCA_VARIANCE_THRESHOLD = "pca_variance_threshold"

    # Visualization parameters
    FIGURE_SIZE_LARGE = "figure_size_large"
    FIGURE_SIZE_MEDIUM = "figure_size_medium"
    FIGURE_SIZE_SMALL = "figure_size_small"
    DPI = "dpi"
    STYLE = "style"
    COLOR_MAP = "color_map"
    GRID_ALPHA = "grid_alpha"

    # Output and reporting
    DECIMAL_PRECISION = "decimal_precision"
    RESULTS_DIR = "results_dir"
    VERBOSE = "verbose"


# ===========================
# Main Configuration
# ===========================

CONF = {
    # ===========================
    # Dataset Configuration
    # ===========================
    Keys.DATASET_PATH_FULL: "data/bank-full.csv",
    Keys.DATASET_PATH_SMALL: "data/bank.csv",
    Keys.DATASET_DELIMITER: ";",
    Keys.DATASET_ENCODING: "utf-8",
    # ===========================
    # Feature Selection
    # ===========================
    Keys.NUMERICAL_FEATURES: [
        BankFeatures.AGE,
        BankFeatures.BALANCE,
        BankFeatures.DAY,
        BankFeatures.DURATION,
        BankFeatures.CAMPAIGN,
        BankFeatures.PDAYS,
        BankFeatures.PREVIOUS,
    ],
    Keys.CATEGORICAL_FEATURES: [
        BankFeatures.JOB,
        BankFeatures.MARITAL,
        BankFeatures.EDUCATION,
        BankFeatures.DEFAULT,
        BankFeatures.HOUSING,
        BankFeatures.LOAN,
        BankFeatures.CONTACT,
        BankFeatures.MONTH,
        BankFeatures.POUTCOME,
    ],
    Keys.ALL_FEATURES: [
        BankFeatures.AGE,
        BankFeatures.JOB,
        BankFeatures.MARITAL,
        BankFeatures.EDUCATION,
        BankFeatures.DEFAULT,
        BankFeatures.BALANCE,
        BankFeatures.HOUSING,
        BankFeatures.LOAN,
        BankFeatures.CONTACT,
        BankFeatures.DAY,
        BankFeatures.MONTH,
        BankFeatures.DURATION,
        BankFeatures.CAMPAIGN,
        BankFeatures.PDAYS,
        BankFeatures.PREVIOUS,
        BankFeatures.POUTCOME,
    ],
    Keys.TARGET_COLUMN: BankTarget.SUBSCRIBED,
    # ===========================
    # Preprocessing Configuration
    # ===========================
    Keys.SCALE_FEATURES: True,
    Keys.HANDLE_CATEGORICAL: HandleCategorical.ONE_HOT,
    # ===========================
    # General ML Parameters
    # ===========================
    Keys.RANDOM_STATE: 72,
    Keys.TEST_SIZE: 0.2,
    Keys.CV_FOLDS: 5,
    # ===========================
    # SVM Configuration (Task 1)
    # ===========================
    Keys.SVM_KERNELS: [
        SVMKernel.LINEAR,
        SVMKernel.POLY,
        SVMKernel.RBF,
        SVMKernel.SIGMOID,
    ],
    Keys.SVM_C_VALUES: [0.01, 0.1, 1, 10, 100],
    Keys.SVM_GAMMA_VALUES: ["scale", "auto", 0.001, 0.01, 0.1, 1],
    Keys.SVM_DEGREE_VALUES: [2, 3, 4, 5],  # For polynomial kernel
    Keys.SVM_MAX_ITER: 10000,
    # ===========================
    # ANN Configuration (Task 2)
    # ===========================
    Keys.ANN_ARCHITECTURES: [
        (10,),
        (20,),
        (50,),
        (100,),
        (10, 10),
        (20, 20),
        (50, 50),
        (100, 50),
        (50, 25, 10),
        (100, 50, 25),
        (20, 20, 20),
        (50, 50, 50),
    ],
    Keys.ANN_ACTIVATIONS: [
        ANNActivation.RELU,
        ANNActivation.TANH,
        ANNActivation.LOGISTIC,
    ],
    Keys.ANN_SOLVERS: [
        ANNSolver.ADAM,
        ANNSolver.SGD,
        ANNSolver.LBFGS,
    ],
    Keys.ANN_MAX_ITER: 1000,
    Keys.ANN_LEARNING_RATE: "adaptive",
    Keys.ANN_ALPHA: 0.0001,  # L2 regularization parameter
    # ===========================
    # PCA Configuration (Task 3)
    # ===========================
    Keys.PCA_N_COMPONENTS_RANGE: [2, 3, 5, 10, 15, 20],
    Keys.PCA_VARIANCE_THRESHOLD: 0.95,  # Keep components explaining 95% variance
    # ===========================
    # Visualization Parameters
    # ===========================
    Keys.FIGURE_SIZE_LARGE: (15, 10),
    Keys.FIGURE_SIZE_MEDIUM: (12, 8),
    Keys.FIGURE_SIZE_SMALL: (8, 6),
    Keys.DPI: 100,
    Keys.STYLE: "seaborn-v0_8-darkgrid",
    Keys.COLOR_MAP: "viridis",
    Keys.GRID_ALPHA: 0.3,
    # ===========================
    # Output Configuration
    # ===========================
    Keys.DECIMAL_PRECISION: 4,
    Keys.RESULTS_DIR: "results",
    Keys.VERBOSE: True,
}


# ===========================
# Imports Section
# ===========================

print("=" * 50)
print("Bank Marketing Analysis - Configuration Loaded")
print("=" * 50)
print(f"Dataset (small): {CONF[Keys.DATASET_PATH_SMALL]}")
print(f"Dataset (full): {CONF[Keys.DATASET_PATH_FULL]}")
print(f"Numerical Features: {len(CONF[Keys.NUMERICAL_FEATURES])}")
print(f"Categorical Features: {len(CONF[Keys.CATEGORICAL_FEATURES])}")
print(f"Target: {CONF[Keys.TARGET_COLUMN]}")
print(f"CV Folds: {CONF[Keys.CV_FOLDS]}")
print(f"Random State: {CONF[Keys.RANDOM_STATE]}")
print()
print("SVM Configuration:")
print(f"  Kernels: {CONF[Keys.SVM_KERNELS]}")
print(f"  C values: {len(CONF[Keys.SVM_C_VALUES])} values")
print(f"  Gamma values: {len(CONF[Keys.SVM_GAMMA_VALUES])} values")
print()
print("ANN Configuration:")
print(f"  Architectures: {len(CONF[Keys.ANN_ARCHITECTURES])} configurations")
print(f"  Activations: {CONF[Keys.ANN_ACTIVATIONS]}")
print(f"  Solvers: {CONF[Keys.ANN_SOLVERS]}")
print()
print("PCA Configuration:")
print(f"  Component range: {CONF[Keys.PCA_N_COMPONENTS_RANGE]}")
print(f"  Variance threshold: {CONF[Keys.PCA_VARIANCE_THRESHOLD]}")
print("=" * 50)
