# Configuration Usage Guide

## Overview
The `config.py` file centralizes all parameters, constants, and imports for the Bank Marketing analysis project.

## Quick Start

In any notebook or Python file, simply import everything from config:

```python
from config import *
```

This gives you access to:
- `CONFIG` dictionary with all parameters
- `Keys` class for accessing configuration values
- `BankFeatures` class for feature column names
- `BankTarget` class for target column name
- All necessary libraries (numpy, pandas, sklearn, etc.)

## Usage Examples

### 1. Loading Data

```python
from config import *

# Load the dataset
df = pd.read_csv(
    CONFIG[Keys.DATASET_PATH_SMALL],
    delimiter=CONFIG[Keys.DATASET_DELIMITER],
    encoding=CONFIG[Keys.DATASET_ENCODING]
)

# Access features
numerical_features = CONFIG[Keys.NUMERICAL_FEATURES]
target = CONFIG[Keys.TARGET_COLUMN]

# Separate features and target
X = df[CONFIG[Keys.ALL_FEATURES]]
y = df[CONFIG[Keys.TARGET_COLUMN]]
```

### 2. SVM Experiments (Task 1)

```python
from config import *

# Get SVM parameters from config
kernels = CONFIG[Keys.SVM_KERNELS]  # ['linear', 'poly', 'rbf', 'sigmoid']
C_values = CONFIG[Keys.SVM_C_VALUES]  # [0.01, 0.1, 1, 10, 100]
gamma_values = CONFIG[Keys.SVM_GAMMA_VALUES]

# Train SVM with different kernels
for kernel in kernels:
    svm = SVC(
        kernel=kernel,
        C=1.0,
        gamma='scale',
        max_iter=CONFIG[Keys.SVM_MAX_ITER],
        random_state=CONFIG[Keys.RANDOM_STATE]
    )
    # Cross-validation
    scores = cross_val_score(svm, X_scaled, y, cv=CONFIG[Keys.CV_FOLDS])
    print(f"{kernel} kernel - Accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")
```

### 3. ANN Experiments (Task 2)

```python
from config import *

# Get ANN parameters from config
architectures = CONFIG[Keys.ANN_ARCHITECTURES]  # [(10,), (20,), (50,), ...]
activations = CONFIG[Keys.ANN_ACTIVATIONS]  # ['relu', 'tanh', 'logistic']
solvers = CONFIG[Keys.ANN_SOLVERS]  # ['adam', 'sgd', 'lbfgs']

# Train ANN with different architectures
for architecture in architectures:
    for activation in activations:
        mlp = MLPClassifier(
            hidden_layer_sizes=architecture,
            activation=activation,
            solver='adam',
            max_iter=CONFIG[Keys.ANN_MAX_ITER],
            random_state=CONFIG[Keys.RANDOM_STATE],
            learning_rate=CONFIG[Keys.ANN_LEARNING_RATE]
        )
        # Cross-validation
        scores = cross_val_score(mlp, X_scaled, y, cv=CONFIG[Keys.CV_FOLDS])
        print(f"Architecture {architecture}, {activation} - Accuracy: {scores.mean():.4f}")
```

### 4. PCA Analysis (Task 3)

```python
from config import *

# Get PCA parameters from config
pca_components = CONFIG[Keys.PCA_N_COMPONENTS_RANGE]  # [2, 3, 5, 10, 15, 20]
variance_threshold = CONFIG[Keys.PCA_VARIANCE_THRESHOLD]  # 0.95

# Apply PCA
for n_components in pca_components:
    pca = PCA(n_components=n_components, random_state=CONFIG[Keys.RANDOM_STATE])
    X_pca = pca.fit_transform(X_scaled)
    
    # Re-train best models with PCA-transformed data
    # ... your code here ...
```

### 5. Visualization

```python
from config import *

# Use configured visualization parameters
plt.figure(figsize=CONFIG[Keys.FIGURE_SIZE_LARGE], dpi=CONFIG[Keys.DPI])
plt.grid(alpha=CONFIG[Keys.GRID_ALPHA])

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap=CONFIG[Keys.COLOR_MAP])
plt.title('Confusion Matrix')
plt.show()
```

## Configuration Structure

### Dataset Paths
- `Keys.DATASET_PATH_SMALL`: "data/bank.csv" (4,521 samples)
- `Keys.DATASET_PATH_FULL`: "data/bank-full.csv" (45,211 samples)

### Features
- `Keys.NUMERICAL_FEATURES`: 7 numerical columns (age, balance, day, duration, campaign, pdays, previous)
- `Keys.CATEGORICAL_FEATURES`: 9 categorical columns (job, marital, education, etc.)
- `Keys.ALL_FEATURES`: All 16 input features
- `Keys.TARGET_COLUMN`: "y" (yes/no subscription)

### SVM Parameters
- `Keys.SVM_KERNELS`: 4 kernel types
- `Keys.SVM_C_VALUES`: 5 regularization values
- `Keys.SVM_GAMMA_VALUES`: 6 gamma values
- `Keys.SVM_DEGREE_VALUES`: 4 polynomial degrees

### ANN Parameters
- `Keys.ANN_ARCHITECTURES`: 12 different architectures
- `Keys.ANN_ACTIVATIONS`: 3 activation functions
- `Keys.ANN_SOLVERS`: 3 optimization algorithms

### Cross-Validation
- `Keys.CV_FOLDS`: 5 folds (adjustable)
- `Keys.RANDOM_STATE`: 42 (for reproducibility)
- `Keys.TEST_SIZE`: 0.2 (20% test split)

## Best Practices

1. **Always use config values** instead of hardcoding parameters
2. **Reference feature names** through `BankFeatures` class
3. **Use consistent random state** from config for reproducibility
4. **Follow visualization parameters** for consistent plots
5. **Access paths** through config keys (makes switching between small/full dataset easy)

## Extending the Configuration

To add new parameters:

1. Add a key to the `Keys` class:
```python
class Keys:
    MY_NEW_PARAMETER = "my_new_parameter"
```

2. Add the value to the `CONFIG` dictionary:
```python
CONFIG = {
    # ... existing config ...
    Keys.MY_NEW_PARAMETER: "my_value",
}
```

3. Use it in your code:
```python
value = CONFIG[Keys.MY_NEW_PARAMETER]
```

## Notes

- The config file automatically loads all necessary imports
- Warning messages are suppressed by default
- Configuration summary is printed when config.py is imported
- All numerical features should be scaled before training
- Categorical features need encoding (OneHot recommended)

