"""
Data Loader - Pure file I/O operations.

Responsibilities:
- Load CSV files (Math, Portuguese datasets)
- Basic file validation (exists, readable)
- Return raw dataframes

NO transformations, NO preprocessing, NO algorithms.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Literal
import logging

logger = logging.getLogger(__name__)

# Constants
DATA_DIR = Path(__file__).parent / "source"
MATH_DATASET = "student-mat.csv"
PORTUGUESE_DATASET = "student-por.csv"

DatasetType = Literal["math", "portuguese", "both"]


def load_csv(filepath: Path) -> pd.DataFrame:
    """
    Load a single CSV file.
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        DataFrame with raw data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        pd.errors.EmptyDataError: If file is empty
        pd.errors.ParserError: If file is malformed
    """
    if not filepath.exists():
        msg = f"File not found: {filepath}"
        logger.error(msg)
        raise FileNotFoundError(msg)
    
    try:
        df = pd.read_csv(filepath, sep=";")
        logger.info(f"Loaded {len(df)} rows from {filepath.name}")
        return df
    except pd.errors.EmptyDataError as e:
        logger.error(f"Empty file: {filepath}")
        raise
    except pd.errors.ParserError as e:
        logger.error(f"Malformed CSV: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading {filepath}: {e}")
        raise


def load_dataset(
    dataset: DatasetType,
    data_dir: Optional[Path] = None
) -> pd.DataFrame:
    """
    Load a specific dataset by name.
    
    Args:
        dataset: Which dataset to load ('math', 'portuguese', 'both')
        data_dir: Optional custom data directory
        
    Returns:
        DataFrame with raw data
        
    Raises:
        ValueError: If dataset type is invalid
        FileNotFoundError: If dataset file doesn't exist
    """
    if data_dir is None:
        data_dir = DATA_DIR
    
    if dataset == "math":
        filepath = data_dir / MATH_DATASET
        df = load_csv(filepath)
        df["dataset_source"] = "math"
        return df
    
    elif dataset == "portuguese":
        filepath = data_dir / PORTUGUESE_DATASET
        df = load_csv(filepath)
        df["dataset_source"] = "portuguese"
        return df
    
    elif dataset == "both":
        df_math = load_dataset("math", data_dir)
        df_por = load_dataset("portuguese", data_dir)
        
        # Concatenate and add source identifier
        df_combined = pd.concat([df_math, df_por], ignore_index=True)
        logger.info(
            f"Combined datasets: {len(df_math)} math + {len(df_por)} portuguese "
            f"= {len(df_combined)} total"
        )
        return df_combined
    
    else:
        msg = f"Invalid dataset type: {dataset}. Must be 'math', 'portuguese', or 'both'"
        logger.error(msg)
        raise ValueError(msg)


def get_dataset_info(dataset: DatasetType) -> dict:
    """
    Get metadata about a dataset without loading it.
    
    Args:
        dataset: Which dataset to query
        
    Returns:
        Dictionary with metadata (path, size, exists)
    """
    if dataset == "math":
        filepath = DATA_DIR / MATH_DATASET
    elif dataset == "portuguese":
        filepath = DATA_DIR / PORTUGUESE_DATASET
    elif dataset == "both":
        return {
            "math": get_dataset_info("math"),
            "portuguese": get_dataset_info("portuguese")
        }
    else:
        raise ValueError(f"Invalid dataset type: {dataset}")
    
    info = {
        "path": str(filepath),
        "exists": filepath.exists(),
        "size_bytes": filepath.stat().st_size if filepath.exists() else None,
        "name": filepath.name
    }
    
    return info


def save_snapshot(
    df: pd.DataFrame,
    name: str,
    output_dir: Optional[Path] = None
) -> Path:
    """
    Save a dataframe snapshot for later use.
    
    Args:
        df: DataFrame to save
        name: Snapshot name (will be sanitized)
        output_dir: Optional custom output directory
        
    Returns:
        Path to saved snapshot
    """
    if output_dir is None:
        output_dir = DATA_DIR.parent.parent / "sandbox" / "snapshots"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Sanitize name
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
    filename = f"{safe_name}.csv"
    filepath = output_dir / filename
    
    try:
        df.to_csv(filepath, index=False)
        logger.info(f"Saved snapshot: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Failed to save snapshot {filepath}: {e}")
        raise


def load_snapshot(name: str, snapshot_dir: Optional[Path] = None) -> pd.DataFrame:
    """
    Load a previously saved snapshot.
    
    Args:
        name: Snapshot name
        snapshot_dir: Optional custom snapshot directory
        
    Returns:
        DataFrame with snapshot data
        
    Raises:
        FileNotFoundError: If snapshot doesn't exist
    """
    if snapshot_dir is None:
        snapshot_dir = DATA_DIR.parent.parent / "sandbox" / "snapshots"
    
    # Sanitize name
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
    filename = f"{safe_name}.csv"
    filepath = snapshot_dir / filename
    
    if not filepath.exists():
        raise FileNotFoundError(f"Snapshot not found: {filepath}")
    
    df = pd.read_csv(filepath)
    logger.info(f"Loaded snapshot: {filepath} ({len(df)} rows)")
    return df


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

