import os
import pandas as pd
import numpy as np

def test_dataset_existence_and_shape():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "bps_e_commerce_tax_compliance.csv")
    assert os.path.exists(data_path), "Dataset BPS CSV file does not exist"
    
    df = pd.read_csv(data_path)
    assert df.shape == (5000, 12), f"Expected shape (5000, 12), got {df.shape}"
    assert "target_non_compliance" in df.columns, "Target column missing"
    assert df["target_non_compliance"].isnull().sum() == 0, "Missing values in target"

def test_reproducibility_seed():
    from src.generate_data import generate_benchmark_tax_dataset
    df1 = generate_benchmark_tax_dataset(n_samples=500, seed=42)
    df2 = generate_benchmark_tax_dataset(n_samples=500, seed=42)
    
    pd.testing.assert_frame_equal(df1, df2), "Dataset generation is not deterministic with seed=42"
