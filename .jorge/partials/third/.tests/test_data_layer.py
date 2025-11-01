"""
Test script for data layer.

Run this to verify all data layer modules work correctly.
"""

import sys
from pathlib import Path

from data import loader, validator, transformer, balancer


# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_loader():
    """Test data loading."""
    print("\n" + "="*60)
    print("TESTING LOADER")
    print("="*60)
    
    # Test loading Math dataset
    print("\n1. Loading Math dataset...")
    df_math = loader.load_dataset("math")
    print(f"✓ Math dataset: {df_math.shape}")
    print(f"  Columns: {list(df_math.columns[:5])}...")
    
    # Test loading Portuguese dataset
    print("\n2. Loading Portuguese dataset...")
    df_por = loader.load_dataset("portuguese")
    print(f"✓ Portuguese dataset: {df_por.shape}")
    
    # Test loading both
    print("\n3. Loading both datasets...")
    df_both = loader.load_dataset("both")
    print(f"✓ Both datasets: {df_both.shape}")
    print(f"  Math: {(df_both['dataset_source'] == 'math').sum()}")
    print(f"  Portuguese: {(df_both['dataset_source'] == 'portuguese').sum()}")
    
    return df_math, df_por


def test_validator(df_math, df_por):
    """Test data validation."""
    print("\n" + "="*60)
    print("TESTING VALIDATOR")
    print("="*60)
    
    # Test schema validation
    print("\n1. Validating schema...")
    result = validator.check_schema(df_math)
    print(f"✓ Schema validation: {result}")
    
    # Test missing values
    print("\n2. Checking missing values...")
    result = validator.check_missing(df_math, tolerance=0.05)
    print(f"✓ Missing value check: {result}")
    if result.warnings:
        print(f"  Warnings: {len(result.warnings)}")
    
    # Test ranges
    print("\n3. Checking value ranges...")
    result = validator.check_ranges(df_math)
    print(f"✓ Range validation: {result}")
    
    # Test cross-dataset validation
    print("\n4. Cross-dataset validation...")
    result = validator.validate_cross_dataset(df_math, df_por)
    print(f"✓ Cross-dataset: {result}")
    print(f"  Warnings: {len(result.warnings)}")
    if result.warnings:
        for w in result.warnings[:3]:
            print(f"    - {w}")


def test_transformer(df_math):
    """Test data transformation."""
    print("\n" + "="*60)
    print("TESTING TRANSFORMER")
    print("="*60)
    
    # Test binary target engineering
    print("\n1. Engineering binary target...")
    target = transformer.engineer_target(df_math, "binary")
    print(f"✓ Binary target: {target.value_counts().to_dict()}")
    
    # Test three-class target
    print("\n2. Engineering three-class target...")
    target = transformer.engineer_target(df_math, "three_class")
    print(f"✓ Three-class target: {target.value_counts().to_dict()}")
    
    # Test complete pipeline
    print("\n3. Complete preprocessing pipeline...")
    X, y, metadata = transformer.prepare_for_training(
        df_math,
        target_strategy="binary",
        remove_g1_g2=True,
        encode_method="label",
        scale_method="standard"
    )
    print(f"✓ Preprocessing complete:")
    print(f"  X shape: {X.shape}")
    print(f"  y shape: {y.shape}")
    print(f"  Classes: {metadata['class_distribution']['counts']}")
    print(f"  Imbalance ratio: {metadata['class_distribution']['imbalance_ratio']}")
    
    return X, y


def test_balancer(X, y):
    """Test class balancing."""
    print("\n" + "="*60)
    print("TESTING BALANCER")
    print("="*60)
    
    # Get imbalance metrics
    print("\n1. Calculating imbalance metrics...")
    metrics = balancer.get_imbalance_metrics(y)
    print(f"✓ Imbalance metrics:")
    print(f"  Ratio: {metrics['imbalance_ratio']:.2f}")
    print(f"  Severity: {metrics['imbalance_severity']}")
    print(f"  Class counts: {metrics['class_counts']}")
    
    # Get recommendation
    print("\n2. Getting balancing recommendation...")
    recommended = balancer.recommend_balancing_method(y)
    print(f"✓ Recommended method: {recommended}")
    
    # Apply SMOTE
    print("\n3. Applying SMOTE...")
    X_balanced, y_balanced = balancer.apply_smote(X, y, random_state=42)
    print(f"✓ SMOTE applied:")
    print(f"  Before: {len(y)} samples")
    print(f"  After: {len(y_balanced)} samples")
    print(f"  Class distribution: {dict(y_balanced.value_counts())}")
    
    # Compare distributions
    print("\n4. Comparing distributions...")
    comparison = balancer.compare_distributions(y, y_balanced)
    print(f"✓ Distribution comparison:")
    print(f"  Samples added: {comparison['change']['n_samples_added']}")
    print(f"  Ratio improvement: {comparison['change']['ratio_improvement']:.2f}")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("DATA LAYER TEST SUITE")
    print("="*60)
    
    try:
        # Test loader
        df_math, df_por = test_loader()
        
        # Test validator
        test_validator(df_math, df_por)
        
        # Test transformer
        X, y = test_transformer(df_math)
        
        # Test balancer
        test_balancer(X, y)
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

