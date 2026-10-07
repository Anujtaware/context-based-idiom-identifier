"""
Baseline Model Training Script: Language-Aware TF-IDF + Logistic Regression
Supports: English, Hindi, Marathi (Multilingual 5,400 dataset)

Pipeline:
1. Load benchmark dataset with leak-free stratified split on (Language x Class).
2. Apply language-aware text normalization (Latin + Devanagari Unicode preservation).
3. Extract unigram + bigram + trigram TF-IDF features across multilingual vocabulary.
4. Train multi-class Logistic Regression with class balancing.
5. Save trained baseline artifacts (baseline_model.pkl, tfidf_vectorizer.pkl, label_encoder.pkl).
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, f1_score

# Add src to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
MODELS_DIR = os.path.join(BASE_DIR, "models")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from dataset_loader import get_train_val_test_split
from multilingual_preprocessing import normalize_for_tokens


def train_baseline_pipeline(models_dir: str = None):
    if models_dir is None:
        models_dir = MODELS_DIR
    os.makedirs(models_dir, exist_ok=True)

    print("=" * 70)
    print(" TRAINING BASELINE MODEL: Multilingual TF-IDF + Logistic Regression")
    print("=" * 70)

    # 1. Load data using leak-free 70/15/15 stratified split
    df_train, df_val, df_test = get_train_val_test_split(random_state=42)
    print(f"Loaded {len(df_train)} training samples and {len(df_test)} test samples.")
    print("Train language breakdown:", df_train['language'].value_counts().to_dict())
    print("Test language breakdown: ", df_test['language'].value_counts().to_dict())

    # 2. Language-aware text normalization
    X_train_clean = [
        normalize_for_tokens(row['sentence'], language=row.get('language', 'en'))
        for _, row in df_train.iterrows()
    ]
    X_test_clean = [
        normalize_for_tokens(row['sentence'], language=row.get('language', 'en'))
        for _, row in df_test.iterrows()
    ]

    # 3. Label Encoding
    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(df_train['usage_type'])
    y_test = label_encoder.transform(df_test['usage_type'])
    print(f"Target Classes: {list(label_encoder.classes_)}")

    # 4. Multilingual TF-IDF Vectorizer
    # Unicode word pattern (?u)\b\w+\b natively captures English and Devanagari words
    vectorizer = TfidfVectorizer(
        token_pattern=r'(?u)\b\w+\b',
        ngram_range=(1, 3),
        min_df=2,
        sublinear_tf=True,
        norm='l2'
    )
    X_train_vec = vectorizer.fit_transform(X_train_clean)
    X_test_vec = vectorizer.transform(X_test_clean)
    print(f"Multilingual TF-IDF vocabulary size: {X_train_vec.shape[1]} features")

    # 5. Logistic Regression Classifier
    baseline_clf = LogisticRegression(
        C=2.5,
        max_iter=1000,
        class_weight='balanced',
        random_state=42
    )
    baseline_clf.fit(X_train_vec, y_train)

    # 6. Evaluation
    y_pred_test = baseline_clf.predict(X_test_vec)
    test_acc = accuracy_score(y_test, y_pred_test)
    test_f1 = f1_score(y_test, y_pred_test, average='weighted')
    macro_f1 = f1_score(y_test, y_pred_test, average='macro')

    print(f"\nBaseline Test Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")
    print(f"Baseline Weighted F1:   {test_f1:.4f}")
    print(f"Baseline Macro F1:      {macro_f1:.4f}")
    print("\nOverall Classification Report:")
    print(classification_report(y_test, y_pred_test, target_names=label_encoder.classes_, digits=4))

    # Per-language breakdown
    print("-" * 50)
    print("Per-Language Baseline Accuracy:")
    for lang in ['en', 'hi', 'mr']:
        mask = (df_test['language'] == lang).values
        if np.any(mask):
            acc_lang = accuracy_score(y_test[mask], y_pred_test[mask])
            f1_lang = f1_score(y_test[mask], y_pred_test[mask], average='weighted')
            lang_name = {"en": "English", "hi": "Hindi", "mr": "Marathi"}.get(lang, lang)
            print(f"  {lang_name} ({lang}): Accuracy = {acc_lang*100:.2f}%, F1 = {f1_lang:.4f} (N={np.sum(mask)})")
    print("-" * 50)

    # 7. Save artifacts
    vectorizer_path = os.path.join(models_dir, "tfidf_vectorizer.pkl")
    model_path = os.path.join(models_dir, "baseline_model.pkl")
    le_path = os.path.join(models_dir, "label_encoder.pkl")

    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(baseline_clf, model_path)
    joblib.dump(label_encoder, le_path)

    print(f"[OK] Saved TF-IDF vectorizer to: {vectorizer_path}")
    print(f"[OK] Saved Baseline model to:    {model_path}")
    print(f"[OK] Saved Label encoder to:     {le_path}")
    print("=" * 70)

    return {
        "model": baseline_clf,
        "vectorizer": vectorizer,
        "label_encoder": label_encoder,
        "accuracy": test_acc
    }


if __name__ == "__main__":
    train_baseline_pipeline()
