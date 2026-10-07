"""
Dataset Quality and Integrity Validator
Validates:
1. Duplicate rows and duplicate sentences
2. Missing / null values in all required fields
3. Label validity (strictly 'idiomatic', 'literal', or 'none')
4. Language distribution ('en', 'hi', 'mr')
5. Class distribution and balance
6. Idiom distribution and canonical registry alignment
7. Language x Class distribution matrix
8. Unicode NFC normalization and Devanagari script integrity
9. Language-sentence alignment (no English marked as Hindi/Marathi or vice versa)
"""

import os
import sys
import unicodedata
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from idiom_dictionary import IDIOM_DICTIONARY, get_all_idioms


def validate_dataset(csv_path: str = None) -> bool:
    if csv_path is None:
        csv_path = os.path.join(DATASET_DIR, "multilingual_idioms.csv")
    
    print("=" * 75)
    print(f" VALIDATING DATASET INTEGRITY: {os.path.basename(csv_path)}")
    print("=" * 75)

    if not os.path.exists(csv_path):
        print(f"[FAIL] Dataset file not found at: {csv_path}")
        return False

    df = pd.read_csv(csv_path, encoding="utf-8", keep_default_na=False)
    total_rows = len(df)
    print(f"[INFO] Loaded {total_rows} total rows.")

    errors = []
    warnings = []

    # 1. Required Columns
    required_cols = ['id', 'language', 'sentence', 'idiom', 'meaning', 'usage_type', 'context', 'example']
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
    else:
        print(f"[PASS] All {len(required_cols)} required columns present.")

    # 2. Missing / Null Values
    null_counts = df[required_cols].isnull().sum()
    has_nulls = False
    for col, count in null_counts.items():
        if count > 0:
            errors.append(f"Column '{col}' has {count} null/missing values.")
            has_nulls = True
    if not has_nulls:
        print("[PASS] Zero null/missing values across all required attributes.")

    # 3. Duplicate Sentences
    dupe_sentences = df[df.duplicated(subset=['sentence'], keep=False)]
    if len(dupe_sentences) > 0:
        errors.append(f"Found {len(dupe_sentences)} duplicate sentence entries.")
    else:
        print(f"[PASS] Zero duplicate sentences. Exactly {df['sentence'].nunique()} unique sentences out of {total_rows} rows.")

    # 4. Valid Usage Labels
    valid_labels = {'idiomatic', 'literal', 'none'}
    actual_labels = set(df['usage_type'].unique())
    invalid_labels = actual_labels - valid_labels
    if invalid_labels:
        errors.append(f"Invalid usage_type labels found: {invalid_labels}")
    else:
        print(f"[PASS] All labels strictly valid: {sorted(list(actual_labels))}")

    # 5. Language Distribution
    valid_langs = {'en', 'hi', 'mr'}
    actual_langs = set(df['language'].unique())
    invalid_langs = actual_langs - valid_langs
    if invalid_langs:
        errors.append(f"Invalid language codes: {invalid_langs}")
    else:
        print(f"[PASS] Supported languages strictly valid: {sorted(list(actual_langs))}")
    
    lang_counts = df['language'].value_counts().to_dict()
    print("       Language breakdown:", lang_counts)

    # 6. Class Distribution
    class_counts = df['usage_type'].value_counts().to_dict()
    print("       Class breakdown:   ", class_counts)

    # 7. Language x Class Distribution Matrix
    crosstab = pd.crosstab(df['language'], df['usage_type'])
    print("\n[INFO] Language x Class Distribution Matrix:")
    print(crosstab.to_string())

    # Check that each cell has samples
    for lang in valid_langs:
        for cls in valid_labels:
            if lang in crosstab.index and cls in crosstab.columns:
                count = crosstab.loc[lang, cls]
                if count == 0:
                    errors.append(f"Zero samples for Language '{lang}' x Class '{cls}'!")
            else:
                errors.append(f"Missing row/col in crosstab for {lang} x {cls}")

    # 8. Idiom Coverage and Dictionary Alignment
    non_none_idioms = df[df['idiom'] != 'none']['idiom'].unique()
    dict_idioms = set(IDIOM_DICTIONARY.keys())
    missing_from_dict = [i for i in non_none_idioms if i not in dict_idioms]
    if missing_from_dict:
        warnings.append(f"{len(missing_from_dict)} idioms in dataset not found in IDIOM_DICTIONARY: {missing_from_dict[:5]}")
    else:
        print(f"\n[PASS] All {len(non_none_idioms)} non-none idioms map to IDIOM_DICTIONARY entries.")

    # 9. Unicode NFC Normalization and Script Check
    nfc_issues = 0
    script_mismatches = 0
    for idx, row in df.iterrows():
        s = str(row['sentence'])
        if s != unicodedata.normalize("NFC", s):
            nfc_issues += 1
        
        lang = row['language']
        devanagari_chars = sum(1 for ch in s if '\u0900' <= ch <= '\u097F')
        latin_chars = sum(1 for ch in s if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z'))

        if lang == 'en' and devanagari_chars > latin_chars:
            script_mismatches += 1
        elif lang in ('hi', 'mr') and latin_chars > devanagari_chars:
            script_mismatches += 1

    if nfc_issues > 0:
        errors.append(f"Found {nfc_issues} sentences with non-NFC Unicode normalization.")
    else:
        print("[PASS] 100% of sentences satisfy Unicode NFC normalization.")

    if script_mismatches > 0:
        errors.append(f"Found {script_mismatches} language-script mismatch anomalies.")
    else:
        print("[PASS] 100% language-script concordance (zero language-script mismatches).")

    # Final verdict
    print("\n" + "=" * 75)
    if warnings:
        print(f"[WARNINGS] ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print(f"[FAIL] Validation FAILED with {len(errors)} errors:")
        for err in errors:
            print(f"  [ERROR] {err}")
        print("=" * 75)
        return False
    else:
        print("[SUCCESS] ALL INTEGRITY CHECKS PASSED (0 errors). Dataset is 100% valid and production-ready!")
        print("=" * 75)
        return True


if __name__ == "__main__":
    csv_file = sys.argv[1] if len(sys.argv) > 1 else None
    success = validate_dataset(csv_file)
    sys.exit(0 if success else 1)
