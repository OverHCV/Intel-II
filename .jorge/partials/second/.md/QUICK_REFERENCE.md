# Quick Reference Card 🚀

## Import in Any Notebook/File

```python
from config import *
```

## Load Data

```python
df = pd.read_csv(CONFIG[Keys.DATASET_PATH_SMALL], 
                 delimiter=CONFIG[Keys.DATASET_DELIMITER])
```

## Common Patterns

### Get Features and Target
```python
X = df[CONFIG[Keys.NUMERICAL_FEATURES]]  # Or ALL_FEATURES
y = df[CONFIG[Keys.TARGET_COLUMN]]
```

### Train/Test Split
```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=CONFIG[Keys.TEST_SIZE],
    random_state=CONFIG[Keys.RANDOM_STATE]
)
```

### Scale Features
```python
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

### Cross-Validation
```python
scores = cross_val_score(
    model, X, y, 
    cv=CONFIG[Keys.CV_FOLDS]
)
```

## Task 1: SVM

```python
for kernel in CONFIG[Keys.SVM_KERNELS]:
    svm = SVC(kernel=kernel, 
              random_state=CONFIG[Keys.RANDOM_STATE])
    svm.fit(X_train, y_train)
```

## Task 2: ANN

```python
for arch in CONFIG[Keys.ANN_ARCHITECTURES]:
    for act in CONFIG[Keys.ANN_ACTIVATIONS]:
        mlp = MLPClassifier(
            hidden_layer_sizes=arch,
            activation=act,
            max_iter=CONFIG[Keys.ANN_MAX_ITER],
            random_state=CONFIG[Keys.RANDOM_STATE]
        )
        mlp.fit(X_train, y_train)
```

## Task 3: PCA

```python
pca = PCA(n_components=10, 
          random_state=CONFIG[Keys.RANDOM_STATE])
X_pca = pca.fit_transform(X_scaled)
```

## Available in CONFIG

### Datasets
- `Keys.DATASET_PATH_SMALL` → "data/bank.csv"
- `Keys.DATASET_PATH_FULL` → "data/bank-full.csv"

### Features (16 total)
- `Keys.NUMERICAL_FEATURES` → [age, balance, day, duration, campaign, pdays, previous]
- `Keys.CATEGORICAL_FEATURES` → [job, marital, education, default, housing, loan, contact, month, poutcome]
- `Keys.TARGET_COLUMN` → "y"

### SVM (Task 1)
- `Keys.SVM_KERNELS` → ['linear', 'poly', 'rbf', 'sigmoid']
- `Keys.SVM_C_VALUES` → [0.01, 0.1, 1, 10, 100]
- `Keys.SVM_GAMMA_VALUES` → ['scale', 'auto', 0.001, 0.01, 0.1, 1]

### ANN (Task 2)
- `Keys.ANN_ARCHITECTURES` → 12 architectures: (10,), (20,), ..., (100,50,25)
- `Keys.ANN_ACTIVATIONS` → ['relu', 'tanh', 'logistic']
- `Keys.ANN_SOLVERS` → ['adam', 'sgd', 'lbfgs']

### PCA (Task 3)
- `Keys.PCA_N_COMPONENTS_RANGE` → [2, 3, 5, 10, 15, 20]

### General
- `Keys.RANDOM_STATE` → 42
- `Keys.CV_FOLDS` → 5
- `Keys.TEST_SIZE` → 0.2

## Run Commands

```powershell
# Test config
uv run python config.py

# Test main
uv run python main.py

# Jupyter
uv run jupyter notebook
```

## Feature Names via Classes

```python
BankFeatures.AGE          # "age"
BankFeatures.BALANCE      # "balance"
BankFeatures.DURATION     # "duration"
# ... etc

BankTarget.SUBSCRIBED     # "y"
```

---

**For full examples, see `CONFIG_USAGE.md`**

