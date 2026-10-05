"""
Baseline Model Training Script: TF-IDF + Logistic Regression

Pipeline:
1. Load dataset with stratified train/test split.
2. Normalize and preprocess text.
3. Extract n-gram TF-IDF features (unigrams + bigrams + trigrams).
4. Train a multi-class Logistic Regression classifier on usage_type ('idiomatic', 'literal', 'none').
5. Save the trained baseline model, TF-IDF vectorizer, and label encoder into models/.
"""

import os
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

from dataset_loader import get_train_test_split
from preprocessing import normalize_for_tokens


def train_baseline_pipeline(save_dir: str = None):
    if save_dir is None:
        save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
    os.makedirs(save_dir, exist_ok=True)

    print("=" * 60)
    print(" TRAINING BASELINE MODEL: TF-IDF + Logistic Regression")
    print("=" * 60)

    # 1. Load data
    X_train_raw, X_test_raw, y_train_raw, y_test_raw, _, _ = get_train_test_split()
    print(f"Loaded {len(X_train_raw)} training samples and {len(X_test_raw)} test samples.")

    # 2. Text normalization
    X_train_clean = [normalize_for_tokens(s) for s in X_train_raw]
    X_test_clean = [normalize_for_tokens(s) for s in X_test_raw]

    # 3. Encode labels
    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(y_train_raw)
    y_test = label_encoder.transform(y_test_raw)
    print(f"Classes: {list(label_encoder.classes_)}")

    # 4. TF-IDF Feature Extraction
    # Using sublinear tf scaling and ngram_range (1, 3) to capture multi-word idiom spans
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        min_df=1,
        sublinear_tf=True,
        norm='l2'
    )
    X_train_vec = vectorizer.fit_transform(X_train_clean)
    X_test_vec = vectorizer.transform(X_test_clean)
    print(f"TF-IDF feature vocabulary size: {X_train_vec.shape[1]} features")

    # 5. Logistic Regression Classifier
    baseline_clf = LogisticRegression(
        C=2.0,
        max_iter=1000,
        class_weight='balanced',
        random_state=42
    )
    baseline_clf.fit(X_train_vec, y_train)

    # 6. Evaluation on Train and Test sets
    y_pred_test = baseline_clf.predict(X_test_vec)
    test_acc = accuracy_score(y_test, y_pred_test)
    print(f"\nBaseline Test Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")
    print("\nClassification Report (Baseline on Test Set):")
    print(classification_report(y_test, y_pred_test, target_names=label_encoder.classes_))

    # 7. Save artifacts
    vectorizer_path = os.path.join(save_dir, "tfidf_vectorizer.pkl")
    model_path = os.path.join(save_dir, "baseline_model.pkl")
    le_path = os.path.join(save_dir, "label_encoder.pkl")

    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(baseline_clf, model_path)
    joblib.dump(label_encoder, le_path)

    print(f"Successfully saved TF-IDF vectorizer to: {vectorizer_path}")
    print(f"Successfully saved Baseline model to:    {model_path}")
    print(f"Successfully saved Label encoder to:     {le_path}")
    print("=" * 60)

    return {
        "model": baseline_clf,
        "vectorizer": vectorizer,
        "label_encoder": label_encoder,
        "accuracy": test_acc
    }


if __name__ == "__main__":
    train_baseline_pipeline()
