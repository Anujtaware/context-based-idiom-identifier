"""
Dataset Loader and Splitter Module

Handles loading the benchmark idioms dataset, performing reproducible
stratified train-test splits, and providing access to feature and label arrays.
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def get_dataset_path() -> str:
    """Return absolute path to dataset/idioms.csv relative to this module."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "dataset", "idioms.csv")


def load_dataset(csv_path: str = None) -> pd.DataFrame:
    """
    Load the idiom dataset from CSV.
    """
    if csv_path is None:
        csv_path = get_dataset_path()
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Idioms dataset not found at expected path: {csv_path}")
    
    df = pd.read_csv(csv_path)
    # Ensure all string columns are clean
    for col in ['sentence', 'idiom', 'meaning', 'usage_type', 'context', 'example']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    return df


def get_train_test_split(
    test_size: float = 0.20,
    random_state: int = 42,
    csv_path: str = None
):
    """
    Split the idioms dataset into train and test sets using stratified sampling
    on the `usage_type` column to ensure balanced representation.

    Returns:
        X_train (pd.Series): Train sentences
        X_test (pd.Series): Test sentences
        y_train (pd.Series): Train usage labels ('idiomatic', 'literal', 'none')
        y_test (pd.Series): Test usage labels
        df_train (pd.DataFrame): Complete train dataframe
        df_test (pd.DataFrame): Complete test dataframe
    """
    df = load_dataset(csv_path)
    
    # Stratified split based on usage_type
    df_train, df_test = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=df['usage_type']
    )
    
    X_train = df_train['sentence']
    y_train = df_train['usage_type']
    X_test = df_test['sentence']
    y_test = df_test['usage_type']
    
    return X_train, X_test, y_train, y_test, df_train, df_test


if __name__ == "__main__":
    X_train, X_test, y_train, y_test, df_train, df_test = get_train_test_split()
    print("Dataset successfully loaded and split:")
    print(f"Total samples: {len(df_train) + len(df_test)}")
    print(f"Train samples: {len(X_train)} ({len(X_train)/(len(df_train)+len(df_test)):.1%})")
    print(f"Test samples:  {len(X_test)} ({len(X_test)/(len(df_train)+len(df_test)):.1%})")
    print("\nTrain class distribution:\n", y_train.value_counts())
    print("\nTest class distribution:\n", y_test.value_counts())
