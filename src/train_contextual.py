"""
Contextual Model Training Script: Multilingual Sentence Transformer + Logistic Regression
Supports: English (en), Hindi (hi), and Marathi (mr)

Model: 'paraphrase-multilingual-MiniLM-L12-v2'
- Pretrained multilingual transformer architecture (XLM-RoBERTa / MiniLM)
- Documented native support for 50+ languages including English, Hindi, and Marathi
- Generates 384-dimensional dense contextual embeddings
- Captures deep cross-lingual semantic dependencies and figurative vs. literal context

Pipeline:
1. Load benchmark dataset with leak-free stratified split on (Language x Class).
2. Generate 384-dimensional dense contextual embeddings using 'paraphrase-multilingual-MiniLM-L12-v2'.
3. Train calibrated Logistic Regression classifier on sentence embeddings.
4. Evaluate performance on test set (Overall + Per-Language).
5. Save contextual model artifact bundle to models/contextual_model.pkl.
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, f1_score

# Add src to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
MODELS_DIR = os.path.join(BASE_DIR, "models")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from dataset_loader import get_train_val_test_split


DEFAULT_MULTILINGUAL_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"


def get_multilingual_embeddings(sentences, model_name=DEFAULT_MULTILINGUAL_MODEL, transformer_instance=None):
    """
    Encode a list of sentences into 384-dimensional dense contextual embeddings.
    """
    if transformer_instance is None:
        transformer_instance = SentenceTransformer(model_name)

    embeddings = transformer_instance.encode(
        list(sentences),
        batch_size=64,
        show_progress_bar=True,
        normalize_embeddings=True
    )
    return np.array(embeddings), transformer_instance


def train_contextual_pipeline(models_dir: str = None, model_name: str = DEFAULT_MULTILINGUAL_MODEL):
    if models_dir is None:
        models_dir = MODELS_DIR
    os.makedirs(models_dir, exist_ok=True)

    print("=" * 70)
    print(" TRAINING CONTEXTUAL MODEL: Multilingual Sentence Transformer + LogReg")
    print(f" Pretrained Transformer: {model_name}")
    print(" Supported Languages: English, Hindi, Marathi")
    print("=" * 70)

    # 1. Load data using leak-free 70/15/15 stratified split
    df_train, df_val, df_test = get_train_val_test_split(random_state=42)
    print(f"Loaded {len(df_train)} training samples and {len(df_test)} test samples.")
    print("Train language breakdown:", df_train['language'].value_counts().to_dict())
    print("Test language breakdown: ", df_test['language'].value_counts().to_dict())

    # 2. Label Encoding (align with baseline label encoder)
    le_path = os.path.join(models_dir, "label_encoder.pkl")
    if os.path.exists(le_path):
        label_encoder = joblib.load(le_path)
    else:
        from sklearn.preprocessing import LabelEncoder
        label_encoder = LabelEncoder()
        label_encoder.fit(df_train['usage_type'])
        joblib.dump(label_encoder, le_path)

    y_train = label_encoder.transform(df_train['usage_type'])
    y_test = label_encoder.transform(df_test['usage_type'])
    print(f"Target Classes: {list(label_encoder.classes_)}")

    # 3. Generate Multilingual Sentence Transformer Embeddings
    print("\nGenerating contextual embeddings for training sentences...")
    X_train_emb, transformer_model = get_multilingual_embeddings(
        df_train['sentence'],
        model_name=model_name
    )
    print(f"Train embeddings shape: {X_train_emb.shape} (Dimension = {X_train_emb.shape[1]})")

    print("\nGenerating contextual embeddings for test sentences...")
    X_test_emb, _ = get_multilingual_embeddings(
        df_test['sentence'],
        model_name=model_name,
        transformer_instance=transformer_model
    )
    print(f"Test embeddings shape: {X_test_emb.shape}")

    # 4. Train Classifier on Embeddings
    contextual_clf = LogisticRegression(
        C=3.0,
        max_iter=1000,
        class_weight='balanced',
        random_state=42
    )
    contextual_clf.fit(X_train_emb, y_train)

    # 5. Evaluate Performance
    y_pred_test = contextual_clf.predict(X_test_emb)
    test_acc = accuracy_score(y_test, y_pred_test)
    test_f1 = f1_score(y_test, y_pred_test, average='weighted')
    macro_f1 = f1_score(y_test, y_pred_test, average='macro')

    print(f"\nContextual Model Test Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")
    print(f"Contextual Model Weighted F1:   {test_f1:.4f}")
    print(f"Contextual Model Macro F1:      {macro_f1:.4f}")
    print("\nOverall Classification Report:")
    print(classification_report(y_test, y_pred_test, target_names=label_encoder.classes_, digits=4))

    # Per-Language Breakdown
    print("-" * 50)
    print("Per-Language Contextual Model Accuracy:")
    for lang in ['en', 'hi', 'mr']:
        mask = (df_test['language'] == lang).values
        if np.any(mask):
            acc_lang = accuracy_score(y_test[mask], y_pred_test[mask])
            f1_lang = f1_score(y_test[mask], y_pred_test[mask], average='weighted')
            lang_name = {"en": "English", "hi": "Hindi", "mr": "Marathi"}.get(lang, lang)
            print(f"  {lang_name} ({lang}): Accuracy = {acc_lang*100:.2f}%, F1 = {f1_lang:.4f} (N={np.sum(mask)})")
    print("-" * 50)

    # 6. Save Model Bundle
    bundle = {
        "model": contextual_clf,
        "embedding_model_name": model_name,
        "classes": label_encoder.classes_,
        "embedding_dimension": X_train_emb.shape[1],
        "languages": ["en", "hi", "mr"]
    }
    model_path = os.path.join(models_dir, "contextual_model.pkl")
    joblib.dump(bundle, model_path)
    print(f"[OK] Saved Contextual Model Bundle to: {model_path}")
    print("=" * 70)

    return {
        "model": contextual_clf,
        "embedding_model_name": model_name,
        "accuracy": test_acc,
        "f1": test_f1
    }


if __name__ == "__main__":
    train_contextual_pipeline()
