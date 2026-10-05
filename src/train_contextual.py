"""
Contextual Model Training Script: Sentence Transformer Embeddings + Logistic Regression Classifier

Pipeline:
1. Load dataset with stratified train/test split.
2. Generate 384-dimensional dense contextual embeddings for the complete sentences using
   the lightweight, high-performance 'all-MiniLM-L6-v2' pretrained transformer model.
3. Train a multi-class Logistic Regression classifier with class balancing on the contextual embeddings.
4. Evaluate performance on the test set.
5. Save the trained contextual classifier artifact to models/contextual_model.pkl.
"""

import os
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

from dataset_loader import get_train_test_split


DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def get_sentence_embeddings(sentences, model_name=DEFAULT_EMBEDDING_MODEL, transformer_instance=None):
    """
    Encode a list of sentences into dense contextual embeddings.
    """
    if transformer_instance is None:
        transformer_instance = SentenceTransformer(model_name)
    
    embeddings = transformer_instance.encode(
        list(sentences),
        batch_size=32,
        show_progress_bar=False,
        normalize_embeddings=True
    )
    return np.array(embeddings), transformer_instance


def train_contextual_pipeline(save_dir: str = None, model_name: str = DEFAULT_EMBEDDING_MODEL):
    if save_dir is None:
        save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
    os.makedirs(save_dir, exist_ok=True)

    print("=" * 60)
    print(" TRAINING CONTEXTUAL MODEL: Sentence Transformer + Logistic Regression")
    print(f" Pretrained Transformer: {model_name}")
    print("=" * 60)

    # 1. Load data
    X_train_raw, X_test_raw, y_train_raw, y_test_raw, _, _ = get_train_test_split()
    print(f"Loaded {len(X_train_raw)} training samples and {len(X_test_raw)} test samples.")

    # 2. Load label encoder from models if available or create new
    le_path = os.path.join(save_dir, "label_encoder.pkl")
    if os.path.exists(le_path):
        label_encoder = joblib.load(le_path)
    else:
        from sklearn.preprocessing import LabelEncoder
        label_encoder = LabelEncoder()
        label_encoder.fit(y_train_raw)
        joblib.dump(label_encoder, le_path)

    y_train = label_encoder.transform(y_train_raw)
    y_test = label_encoder.transform(y_test_raw)

    # 3. Generate contextual embeddings
    print("Generating contextual embeddings for training sentences...")
    X_train_emb, transformer_model = get_sentence_embeddings(X_train_raw, model_name=model_name)
    print(f"Generated train embeddings shape: {X_train_emb.shape}")

    print("Generating contextual embeddings for test sentences...")
    X_test_emb, _ = get_sentence_embeddings(X_test_raw, transformer_instance=transformer_model)
    print(f"Generated test embeddings shape: {X_test_emb.shape}")

    # 4. Train classifier on contextual embeddings
    contextual_clf = LogisticRegression(
        C=3.0,
        max_iter=1000,
        class_weight='balanced',
        random_state=42
    )
    contextual_clf.fit(X_train_emb, y_train)

    # 5. Evaluate on Test Set
    y_pred_test = contextual_clf.predict(X_test_emb)
    test_acc = accuracy_score(y_test, y_pred_test)
    print(f"\nContextual Model Test Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")
    print("\nClassification Report (Contextual Model on Test Set):")
    print(classification_report(y_test, y_pred_test, target_names=label_encoder.classes_))

    # 6. Save model bundle
    bundle = {
        "model": contextual_clf,
        "embedding_model_name": model_name,
        "classes": label_encoder.classes_
    }
    model_path = os.path.join(save_dir, "contextual_model.pkl")
    joblib.dump(bundle, model_path)
    print(f"Successfully saved Contextual Model bundle to: {model_path}")
    print("=" * 60)

    return {
        "model": contextual_clf,
        "transformer_model": transformer_model,
        "accuracy": test_acc
    }


if __name__ == "__main__":
    train_contextual_pipeline()
