"""
Experiment Persistence Module
Handles saving and loading experiment history to/from JSON files
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


def get_cache_dir() -> Path:
    """
    Get the cache directory path, creating it if it doesn't exist

    Returns:
        Path to .cache directory
    """
    cache_dir = Path(__file__).parent.parent / ".cache"
    cache_dir.mkdir(exist_ok=True)
    return cache_dir


def get_experiments_file_path(experiment_type: str = "svm") -> Path:
    """
    Get the path to the experiments JSON file

    Args:
        experiment_type: Type of experiment (svm, ann, pca)

    Returns:
        Path to experiments file
    """
    cache_dir = get_cache_dir()
    return cache_dir / f"{experiment_type}_experiments.json"


def save_experiments_to_file(
    experiments: List[Dict[str, Any]], experiment_type: str = "svm"
) -> bool:
    """
    Save experiments list to JSON file

    Args:
        experiments: List of experiment dictionaries
        experiment_type: Type of experiment (svm, ann, pca)

    Returns:
        True if successful, False otherwise
    """
    try:
        file_path = get_experiments_file_path(experiment_type)

        # Add metadata
        data = {
            "saved_at": datetime.now().isoformat(),
            "experiment_type": experiment_type,
            "count": len(experiments),
            "experiments": experiments,
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"Error saving experiments: {e}")
        return False


def load_experiments_from_file(experiment_type: str = "svm") -> List[Dict[str, Any]]:
    """
    Load experiments list from JSON file

    Args:
        experiment_type: Type of experiment (svm, ann, pca)

    Returns:
        List of experiment dictionaries, empty list if file doesn't exist or error
    """
    try:
        file_path = get_experiments_file_path(experiment_type)

        if not file_path.exists():
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Extract experiments array from metadata wrapper
        if isinstance(data, dict) and "experiments" in data:
            return data["experiments"]
        elif isinstance(data, list):
            # Backward compatibility: old format was just a list
            return data
        else:
            print(f"Warning: Unexpected data format in {file_path}")
            return []

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Error loading experiments: {e}")
        return []


def clear_experiments_file(experiment_type: str = "svm") -> bool:
    """
    Clear the experiments file (delete it)

    Args:
        experiment_type: Type of experiment (svm, ann, pca)

    Returns:
        True if successful or file didn't exist, False on error
    """
    try:
        file_path = get_experiments_file_path(experiment_type)

        if file_path.exists():
            file_path.unlink()

        return True
    except Exception as e:
        print(f"Error clearing experiments file: {e}")
        return False


def get_experiment_stats(experiments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate statistics about experiments

    Args:
        experiments: List of experiment dictionaries

    Returns:
        Dictionary with statistics (count, best accuracy, avg time, etc.)
    """
    if not experiments:
        return {
            "count": 0,
            "best_accuracy": None,
            "best_experiment_id": None,
            "avg_training_time": None,
        }

    # Find accuracy metric (could be "Accuracy" or "CV Accuracy")
    accuracies = []
    for exp in experiments:
        metrics = exp.get("metrics", {})
        acc = metrics.get("Accuracy") or metrics.get("CV Accuracy")
        if acc is not None:
            accuracies.append((exp["id"], acc))

    best_id, best_acc = (
        max(accuracies, key=lambda x: x[1]) if accuracies else (None, None)
    )

    training_times = [exp.get("training_time", 0) for exp in experiments]
    avg_time = sum(training_times) / len(training_times) if training_times else None

    return {
        "count": len(experiments),
        "best_accuracy": best_acc,
        "best_experiment_id": best_id,
        "avg_training_time": avg_time,
        "total_training_time": sum(training_times),
    }


def export_experiments_to_csv(
    experiments: List[Dict[str, Any]], output_path: str
) -> bool:
    """
    Export experiments to CSV file (bonus feature)

    Args:
        experiments: List of experiment dictionaries
        output_path: Path to output CSV file

    Returns:
        True if successful, False otherwise
    """
    try:
        import pandas as pd

        # Flatten the nested structure for CSV
        flattened = []
        for exp in experiments:
            row = {
                "id": exp["id"],
                "kernel": exp.get("kernel", ""),
                "C": exp.get("C", ""),
                "gamma": exp.get("gamma", ""),
                "degree": exp.get("degree", ""),
                "cv_strategy": exp.get("cv_strategy", ""),
                "training_time": exp.get("training_time", ""),
            }

            # Add metrics
            for metric_name, metric_value in exp.get("metrics", {}).items():
                row[metric_name] = metric_value

            flattened.append(row)

        df = pd.DataFrame(flattened)
        df.to_csv(output_path, index=False)

        return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False
