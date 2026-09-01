import os
import pandas as pd
import numpy as np

def test_dataset_existence_and_shape():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "tax_compliance_synthetic_data.csv")
    assert os.path.exists(data_path), "Dataset CSV file does not exist"
    
    df = pd.read_csv(data_path)
    assert df.shape == (5000, 12), f"Expected shape (5000, 12), got {df.shape}"
    assert "target_non_compliance" in df.columns, "Target column missing"
    assert df["target_non_compliance"].isnull().sum() == 0, "Missing values in target"

def test_reproducibility_seed():
    from src.generate_data import generate_true_latent_benchmark
    df1 = generate_true_latent_benchmark(n_samples=500, seed=42)
    df2 = generate_true_latent_benchmark(n_samples=500, seed=42)
    
    pd.testing.assert_frame_equal(df1, df2), "Dataset generation is not deterministic with seed=42"
