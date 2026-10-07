"""
Dataset Loader and Stratified Splitter Module
Handles loading the multilingual benchmark dataset (English + Hindi + Marathi),
performing scientific, reproducible stratified splits across Language x Class,
and preventing any data leakage between training, validation, and test sets.
"""

import os
import pandas as pd
from typing import Tuple, Optional
from sklearn.model_selection import train_test_split


def get_dataset_path() -> str:
    """
    Return path to multilingual_idioms.csv, falling back to idioms.csv.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    multi_path = os.path.join(base_dir, "dataset", "multilingual_idioms.csv")
    if os.path.exists(multi_path):
        return multi_path
    return os.path.join(base_dir, "dataset", "idioms.csv")


def load_dataset(csv_path: Optional[str] = None) -> pd.DataFrame:
    """
    Load the benchmark idioms dataset with clean string columns and UTF-8 encoding.
    """
    if csv_path is None:
        csv_path = get_dataset_path()

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Idioms dataset not found at expected path: {csv_path}")

    df = pd.read_csv(csv_path, encoding="utf-8", keep_default_na=False)

    # Ensure required string columns are stripped
    for col in ['sentence', 'idiom', 'meaning', 'usage_type', 'context', 'example', 'language']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df


def get_train_val_test_split(
    train_size: float = 0.70,
    val_size: float = 0.15,
    test_size: float = 0.15,
    random_state: int = 42,
    csv_path: Optional[str] = None
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Scientific, leak-free 3-way split (70% Train, 15% Validation, 15% Test).
    Stratified jointly on (language x usage_type) to guarantee perfectly balanced
    proportions across languages, classes, and sub-domains.

    Returns:
        df_train, df_val, df_test
    """
    assert abs((train_size + val_size + test_size) - 1.0) < 1e-5, "Split fractions must sum to 1.0"

    df = load_dataset(csv_path)

    # Stratification key: language + '_' + usage_type (9 distinct strata)
    strat_key = df['language'] + '_' + df['usage_type']

    # Step 1: Split train vs (val + test)
    val_test_fraction = val_size + test_size
    df_train, df_val_test = train_test_split(
        df,
        test_size=val_test_fraction,
        random_state=random_state,
        stratify=strat_key
    )

    # Step 2: Split val vs test equally
    strat_key_val_test = df_val_test['language'] + '_' + df_val_test['usage_type']
    val_ratio_in_remaining = val_size / val_test_fraction  # 0.15 / 0.30 = 0.50
    df_val, df_test = train_test_split(
        df_val_test,
        test_size=(1.0 - val_ratio_in_remaining),
        random_state=random_state,
        stratify=strat_key_val_test
    )

    return df_train, df_val, df_test


def get_train_test_split(
    test_size: float = 0.20,
    random_state: int = 42,
    csv_path: Optional[str] = None
):
    """
    Standard stratified train/test split preserved for backwards compatibility
    with existing training pipelines.

    Returns:
        X_train (pd.Series): Train sentences
        X_test (pd.Series): Test sentences
        y_train (pd.Series): Train usage labels ('idiomatic', 'literal', 'none')
        y_test (pd.Series): Test usage labels
        df_train (pd.DataFrame): Complete train dataframe
        df_test (pd.DataFrame): Complete test dataframe
    """
    df = load_dataset(csv_path)

    # Stratify by language and usage_type if language column exists
    if 'language' in df.columns:
        strat_key = df['language'] + '_' + df['usage_type']
    else:
        strat_key = df['usage_type']

    df_train, df_test = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=strat_key
    )

    X_train = df_train['sentence']
    y_train = df_train['usage_type']
    X_test = df_test['sentence']
    y_test = df_test['usage_type']

    return X_train, X_test, y_train, y_test, df_train, df_test


if __name__ == "__main__":
    df_tr, df_v, df_te = get_train_val_test_split()
    print("=" * 65)
    print(" MULTILINGUAL STRATIFIED 70/15/15 SPLIT VERIFICATION")
    print("=" * 65)
    total = len(df_tr) + len(df_v) + len(df_te)
    print(f"Total dataset:   {total}")
    print(f"Train split:     {len(df_tr)} ({len(df_tr)/total*100:.1f}%)")
    print(f"Val split:       {len(df_v)} ({len(df_v)/total*100:.1f}%)")
    print(f"Test split:      {len(df_te)} ({len(df_te)/total*100:.1f}%)")
    print("\nTrain Language x Class:")
    print(pd.crosstab(df_tr['language'], df_tr['usage_type']))
    print("\nTest Language x Class:")
    print(pd.crosstab(df_te['language'], df_te['usage_type']))
    print("=" * 65)
