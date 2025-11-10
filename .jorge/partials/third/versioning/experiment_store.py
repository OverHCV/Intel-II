"""
Experiment Store - Persistence layer for experiment tracking.

This module handles saving and loading experiments to/from disk, managing
the file system structure for organized experiment storage.

WHY: Experiments are valuable - losing them means losing insights and
     wasting computational time. Persistence enables learning from history.
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
import json
import pickle
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Base directory for all experiments
SANDBOX_DIR = Path(__file__).parent.parent / "sandbox"


def save_experiment(
    experiment_data: Dict[str, Any],
    algorithm_type: str,
    version_id: Optional[str] = None
) -> str:
    """
    Save experiment to disk with organized structure.
    
    WHY: Structured storage enables easy retrieval and comparison.
         Each experiment gets its own folder with metadata + artifacts.
    
    Structure:
        sandbox/{algorithm_type}/{version_id}/
            ├── metadata.json    - Timestamp, params, metrics
            ├── model.pkl        - Trained model object
            ├── predictions.npy  - Prediction arrays
            └── visualizations/  - Saved plots
    
    Args:
        experiment_data: Dictionary with model, metrics, predictions, etc.
        algorithm_type: "decision_tree", "hierarchical", or "kmeans"
        version_id: Optional custom ID (auto-generated if None)
        
    Returns:
        Version ID of saved experiment
    """
    if version_id is None:
        version_id = generate_version_id(algorithm_type)
    
    # Create experiment directory
    exp_dir = SANDBOX_DIR / algorithm_type / version_id
    exp_dir.mkdir(parents=True, exist_ok=True)
    
    # Save metadata as JSON
    metadata = {
        "version_id": version_id,
        "algorithm_type": algorithm_type,
        "timestamp": datetime.now().isoformat(),
        "parameters": experiment_data.get("parameters", {}),
        "metrics": experiment_data.get("metrics", {}),
        "dataset_info": experiment_data.get("dataset_info", {})
    }
    
    with open(exp_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    # Save model as pickle (if exists)
    if "model" in experiment_data:
        with open(exp_dir / "model.pkl", "wb") as f:
            pickle.dump(experiment_data["model"], f)
    
    # WIP: Save predictions and visualizations
    # WHY: Need to serialize numpy arrays and matplotlib figures
    
    logger.info(f"Saved experiment: {algorithm_type}/{version_id}")
    return version_id


def load_experiment(
    version_id: str,
    algorithm_type: str
) -> Dict[str, Any]:
    """
    Load experiment from disk.
    
    WHY: Enables reviewing past experiments, comparing results, and
         loading best models for deployment.
    
    Args:
        version_id: Experiment version ID
        algorithm_type: Algorithm type folder
        
    Returns:
        Dictionary with experiment data
    """
    exp_dir = SANDBOX_DIR / algorithm_type / version_id
    
    if not exp_dir.exists():
        raise FileNotFoundError(f"Experiment not found: {algorithm_type}/{version_id}")
    
    # Load metadata
    with open(exp_dir / "metadata.json", "r") as f:
        metadata = json.load(f)
    
    # Load model if exists
    model = None
    model_path = exp_dir / "model.pkl"
    if model_path.exists():
        with open(model_path, "rb") as f:
            model = pickle.load(f)
    
    experiment_data = {
        **metadata,
        "model": model,
        "predictions": "WIP: Load predictions.npy",
        "visualizations": "WIP: Load visualization paths"
    }
    
    logger.info(f"Loaded experiment: {algorithm_type}/{version_id}")
    return experiment_data


def list_experiments(
    algorithm_type: Optional[str] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    List all experiments, optionally filtered by algorithm type.
    
    WHY: Need to browse experiment history to find interesting runs
         or compare different approaches.
    
    Args:
        algorithm_type: Filter by algorithm (None = all)
        limit: Maximum number to return
        
    Returns:
        List of experiment metadata dictionaries
    """
    experiments = []
    
    # Determine which folders to scan
    if algorithm_type:
        folders = [SANDBOX_DIR / algorithm_type]
    else:
        folders = [
            SANDBOX_DIR / "decision_tree",
            SANDBOX_DIR / "hierarchical", 
            SANDBOX_DIR / "kmeans"
        ]
    
    for folder in folders:
        if not folder.exists():
            continue
            
        # Scan all version IDs in this algorithm folder
        for exp_dir in folder.iterdir():
            if not exp_dir.is_dir():
                continue
                
            metadata_path = exp_dir / "metadata.json"
            if metadata_path.exists():
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                    experiments.append(metadata)
    
    # Sort by timestamp (most recent first)
    experiments.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    if limit:
        experiments = experiments[:limit]
    
    logger.info(f"Found {len(experiments)} experiments")
    return experiments


def delete_experiment(
    version_id: str,
    algorithm_type: str
) -> bool:
    """
    Delete an experiment and all its artifacts.
    
    WHY: Clean up failed experiments or free disk space.
    
    Args:
        version_id: Experiment version ID
        algorithm_type: Algorithm type
        
    Returns:
        True if deleted successfully
    """
    import shutil
    
    exp_dir = SANDBOX_DIR / algorithm_type / version_id
    
    if not exp_dir.exists():
        logger.warning(f"Experiment not found: {algorithm_type}/{version_id}")
        return False
    
    shutil.rmtree(exp_dir)
    logger.info(f"Deleted experiment: {algorithm_type}/{version_id}")
    return True


def generate_version_id(algorithm_type: str) -> str:
    """
    Generate unique, sortable version ID.
    
    Format: YYYYMMDD_HHMMSS_{algorithm}_{hash}
    Example: 20251101_143022_decision_tree_a3f2d1
    
    WHY: Chronologically sortable + self-documenting + unique.
    
    Args:
        algorithm_type: Algorithm name
        
    Returns:
        Version ID string
    """
    import hashlib
    import random
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_hash = hashlib.md5(str(random.random()).encode()).hexdigest()[:6]
    
    version_id = f"{timestamp}_{algorithm_type}_{random_hash}"
    return version_id


# Module metadata
__version__ = "1.0.0"

