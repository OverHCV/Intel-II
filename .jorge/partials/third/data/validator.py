"""
Data Validator - Data quality checks and cross-dataset validation.

Responsibilities:
- Check schema (expected columns exist)
- Check for missing values
- Check data ranges and types
- Validate cross-dataset compatibility (Math vs Portuguese)

NO transformations, NO preprocessing, NO algorithms.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

# Expected schema for Student Performance dataset
EXPECTED_COLUMNS = [
    "school", "sex", "age", "address", "famsize", "Pstatus",
    "Medu", "Fedu", "Mjob", "Fjob", "reason", "guardian",
    "traveltime", "studytime", "failures", "schoolsup", "famsup",
    "paid", "activities", "nursery", "higher", "internet", "romantic",
    "famrel", "freetime", "goout", "Dalc", "Walc", "health",
    "absences", "G1", "G2", "G3"
]

NUMERIC_COLUMNS = [
    "age", "Medu", "Fedu", "traveltime", "studytime", "failures",
    "famrel", "freetime", "goout", "Dalc", "Walc", "health",
    "absences", "G1", "G2", "G3"
]

CATEGORICAL_COLUMNS = [
    "school", "sex", "address", "famsize", "Pstatus", "Mjob", "Fjob",
    "reason", "guardian", "schoolsup", "famsup", "paid", "activities",
    "nursery", "higher", "internet", "romantic"
]


class ValidationResult:
    """Container for validation results."""
    
    def __init__(self, is_valid: bool, errors: List[str], warnings: List[str] = None):
        self.is_valid = is_valid
        self.errors = errors
        self.warnings = warnings or []
    
    def __bool__(self) -> bool:
        return self.is_valid
    
    def __repr__(self) -> str:
        status = "VALID" if self.is_valid else "INVALID"
        return f"ValidationResult({status}, {len(self.errors)} errors, {len(self.warnings)} warnings)"


def check_schema(
    df: pd.DataFrame,
    required_columns: Optional[List[str]] = None
) -> ValidationResult:
    """
    Check if dataframe has required columns.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names (defaults to EXPECTED_COLUMNS)
        
    Returns:
        ValidationResult with errors if columns are missing
    """
    if required_columns is None:
        required_columns = EXPECTED_COLUMNS
    
    missing_cols = set(required_columns) - set(df.columns)
    extra_cols = set(df.columns) - set(required_columns) - {"dataset_source"}
    
    errors = []
    warnings = []
    
    if missing_cols:
        errors.append(f"Missing required columns: {sorted(missing_cols)}")
    
    if extra_cols:
        warnings.append(f"Extra columns found: {sorted(extra_cols)}")
    
    is_valid = len(errors) == 0
    
    if is_valid:
        logger.info(f"Schema validation passed: {len(df.columns)} columns")
    else:
        logger.error(f"Schema validation failed: {errors}")
    
    return ValidationResult(is_valid, errors, warnings)


def check_missing(
    df: pd.DataFrame,
    tolerance: float = 0.0
) -> ValidationResult:
    """
    Check for missing values in dataframe.
    
    Args:
        df: DataFrame to validate
        tolerance: Maximum acceptable fraction of missing values (0.0 = no missing allowed)
        
    Returns:
        ValidationResult with errors if too many missing values
    """
    missing_counts = df.isnull().sum()
    total_rows = len(df)
    
    errors = []
    warnings = []
    
    for col, count in missing_counts.items():
        if count > 0:
            fraction = count / total_rows
            msg = f"{col}: {count}/{total_rows} ({fraction:.1%}) missing"
            
            if fraction > tolerance:
                errors.append(msg)
            else:
                warnings.append(msg)
    
    is_valid = len(errors) == 0
    
    if is_valid:
        total_missing = missing_counts.sum()
        logger.info(f"Missing value check passed: {total_missing} total missing values")
    else:
        logger.error(f"Missing value check failed: {errors}")
    
    return ValidationResult(is_valid, errors, warnings)


def check_ranges(
    df: pd.DataFrame,
    constraints: Optional[Dict[str, Tuple[float, float]]] = None
) -> ValidationResult:
    """
    Check if numeric columns are within expected ranges.
    
    Args:
        df: DataFrame to validate
        constraints: Dict mapping column names to (min, max) tuples
        
    Returns:
        ValidationResult with errors if values out of range
    """
    if constraints is None:
        # Default constraints for Student Performance dataset
        constraints = {
            "age": (15, 22),
            "Medu": (0, 4),
            "Fedu": (0, 4),
            "traveltime": (1, 4),
            "studytime": (1, 4),
            "failures": (0, 4),
            "famrel": (1, 5),
            "freetime": (1, 5),
            "goout": (1, 5),
            "Dalc": (1, 5),
            "Walc": (1, 5),
            "health": (1, 5),
            "absences": (0, 93),  # Observed max
            "G1": (0, 20),
            "G2": (0, 20),
            "G3": (0, 20)
        }
    
    errors = []
    warnings = []
    
    for col, (min_val, max_val) in constraints.items():
        if col not in df.columns:
            continue
        
        below_min = (df[col] < min_val).sum()
        above_max = (df[col] > max_val).sum()
        
        if below_min > 0:
            errors.append(f"{col}: {below_min} values below {min_val}")
        
        if above_max > 0:
            errors.append(f"{col}: {above_max} values above {max_val}")
    
    is_valid = len(errors) == 0
    
    if is_valid:
        logger.info(f"Range validation passed for {len(constraints)} columns")
    else:
        logger.error(f"Range validation failed: {errors}")
    
    return ValidationResult(is_valid, errors, warnings)


def validate_cross_dataset(
    df_train: pd.DataFrame,
    df_test: pd.DataFrame
) -> ValidationResult:
    """
    Validate compatibility between train and test datasets.
    
    Checks:
    - Same columns (order doesn't matter)
    - Same data types
    - Compatible categorical values
    - Similar numeric ranges
    
    Args:
        df_train: Training dataset
        df_test: Test dataset
        
    Returns:
        ValidationResult with compatibility report
    """
    errors = []
    warnings = []
    
    # Check columns
    train_cols = set(df_train.columns) - {"dataset_source"}
    test_cols = set(df_test.columns) - {"dataset_source"}
    
    missing_in_test = train_cols - test_cols
    missing_in_train = test_cols - train_cols
    
    if missing_in_test:
        errors.append(f"Test dataset missing columns: {sorted(missing_in_test)}")
    
    if missing_in_train:
        warnings.append(f"Train dataset missing columns: {sorted(missing_in_train)}")
    
    # Check data types for common columns
    common_cols = train_cols & test_cols
    
    for col in common_cols:
        if df_train[col].dtype != df_test[col].dtype:
            warnings.append(
                f"{col}: dtype mismatch (train={df_train[col].dtype}, test={df_test[col].dtype})"
            )
    
    # Check categorical value compatibility
    for col in CATEGORICAL_COLUMNS:
        if col not in common_cols:
            continue
        
        train_values = set(df_train[col].dropna().unique())
        test_values = set(df_test[col].dropna().unique())
        
        new_in_test = test_values - train_values
        if new_in_test:
            warnings.append(
                f"{col}: test has unseen values: {sorted(new_in_test)}"
            )
    
    # Check numeric range compatibility
    for col in NUMERIC_COLUMNS:
        if col not in common_cols:
            continue
        
        train_min, train_max = df_train[col].min(), df_train[col].max()
        test_min, test_max = df_test[col].min(), df_test[col].max()
        
        if test_min < train_min or test_max > train_max:
            warnings.append(
                f"{col}: test range [{test_min}, {test_max}] outside train range [{train_min}, {train_max}]"
            )
    
    is_valid = len(errors) == 0
    
    if is_valid:
        logger.info(
            f"Cross-dataset validation passed: {len(common_cols)} common columns, "
            f"{len(warnings)} warnings"
        )
    else:
        logger.error(f"Cross-dataset validation failed: {errors}")
    
    return ValidationResult(is_valid, errors, warnings)


def get_data_summary(df: pd.DataFrame) -> Dict:
    """
    Get summary statistics for a dataframe.
    
    Args:
        df: DataFrame to summarize
        
    Returns:
        Dictionary with summary statistics
    """
    summary = {
        "n_rows": len(df),
        "n_columns": len(df.columns),
        "missing_total": df.isnull().sum().sum(),
        "missing_by_column": df.isnull().sum().to_dict(),
        "numeric_columns": [],
        "categorical_columns": [],
        "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024 ** 2)
    }
    
    for col in df.columns:
        if df[col].dtype in [np.int64, np.float64]:
            summary["numeric_columns"].append({
                "name": col,
                "min": float(df[col].min()),
                "max": float(df[col].max()),
                "mean": float(df[col].mean()),
                "std": float(df[col].std())
            })
        else:
            summary["categorical_columns"].append({
                "name": col,
                "n_unique": int(df[col].nunique()),
                "top_values": df[col].value_counts().head(5).to_dict()
            })
    
    return summary


