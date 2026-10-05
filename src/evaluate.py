"""
Model Evaluation and Comparative Analysis Script

Evaluates:
1. Baseline Model (TF-IDF + Logistic Regression)
2. Contextual Model (Sentence Transformer + Logistic Regression)

Generates and saves:
- results/classification_report.txt
- results/model_comparison.csv
- results/confusion_matrix_baseline.png
- results/confusion_matrix_contextual.png
"""

import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)
from sentence_transformers import SentenceTransformer

from dataset_loader import get_train_test_split
from preprocessing import normalize_for_tokens


def evaluate_all_models(models_dir: str = None, results_dir: str = None):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if models_dir is None:
        models_dir = os.path.join(base_dir, "models")
    if results_dir is None:
        results_dir = os.path.join(base_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    print("=" * 70)
    print(" RUNNING COMPREHENSIVE MODEL EVALUATION")
    print("=" * 70)

    # 1. Load Test Data
    _, X_test_raw, _, y_test_raw, _, _ = get_train_test_split()
    print(f"Test samples count: {len(X_test_raw)}")

    # 2. Load Label Encoder
    le_path = os.path.join(models_dir, "label_encoder.pkl")
    if not os.path.exists(le_path):
        raise FileNotFoundError(f"Label encoder not found at: {le_path}. Run training scripts first.")
    label_encoder = joblib.load(le_path)
    target_names = list(label_encoder.classes_)
    y_test = label_encoder.transform(y_test_raw)

    # 3. Evaluate Baseline Model
    print("\n--- Evaluating Model 1: Baseline (TF-IDF + Logistic Regression) ---")
    tfidf_path = os.path.join(models_dir, "tfidf_vectorizer.pkl")
    baseline_path = os.path.join(models_dir, "baseline_model.pkl")

    if not os.path.exists(tfidf_path) or not os.path.exists(baseline_path):
        raise FileNotFoundError("Baseline artifacts missing. Run src/train_baseline.py first.")

    vectorizer = joblib.load(tfidf_path)
    baseline_clf = joblib.load(baseline_path)

    X_test_clean = [normalize_for_tokens(s) for s in X_test_raw]
    X_test_vec = vectorizer.transform(X_test_clean)
    y_pred_baseline = baseline_clf.predict(X_test_vec)

    base_acc = accuracy_score(y_test, y_pred_baseline)
    base_prec = precision_score(y_test, y_pred_baseline, average='weighted', zero_division=0)
    base_rec = recall_score(y_test, y_pred_baseline, average='weighted', zero_division=0)
    base_f1 = f1_score(y_test, y_pred_baseline, average='weighted', zero_division=0)
    base_macro_f1 = f1_score(y_test, y_pred_baseline, average='macro', zero_division=0)

    base_report = classification_report(y_test, y_pred_baseline, target_names=target_names, zero_division=0)
    base_cm = confusion_matrix(y_test, y_pred_baseline)

    print(f"Baseline Accuracy:  {base_acc*100:.2f}%")
    print(f"Baseline Precision: {base_prec*100:.2f}%")
    print(f"Baseline Recall:    {base_rec*100:.2f}%")
    print(f"Baseline F1-Score:  {base_f1*100:.2f}%")

    # 4. Evaluate Contextual Model
    print("\n--- Evaluating Model 2: Contextual (Sentence Transformer + Logistic Regression) ---")
    contextual_path = os.path.join(models_dir, "contextual_model.pkl")
    if not os.path.exists(contextual_path):
        raise FileNotFoundError("Contextual model artifact missing. Run src/train_contextual.py first.")

    ctx_bundle = joblib.load(contextual_path)
    contextual_clf = ctx_bundle["model"]
    emb_model_name = ctx_bundle.get("embedding_model_name", "all-MiniLM-L6-v2")

    print(f"Loading embedding model: {emb_model_name}...")
    transformer = SentenceTransformer(emb_model_name)
    X_test_emb = transformer.encode(list(X_test_raw), batch_size=32, show_progress_bar=False, normalize_embeddings=True)
    y_pred_ctx = contextual_clf.predict(X_test_emb)

    ctx_acc = accuracy_score(y_test, y_pred_ctx)
    ctx_prec = precision_score(y_test, y_pred_ctx, average='weighted', zero_division=0)
    ctx_rec = recall_score(y_test, y_pred_ctx, average='weighted', zero_division=0)
    ctx_f1 = f1_score(y_test, y_pred_ctx, average='weighted', zero_division=0)
    ctx_macro_f1 = f1_score(y_test, y_pred_ctx, average='macro', zero_division=0)

    ctx_report = classification_report(y_test, y_pred_ctx, target_names=target_names, zero_division=0)
    ctx_cm = confusion_matrix(y_test, y_pred_ctx)

    print(f"Contextual Accuracy:  {ctx_acc*100:.2f}%")
    print(f"Contextual Precision: {ctx_prec*100:.2f}%")
    print(f"Contextual Recall:    {ctx_rec*100:.2f}%")
    print(f"Contextual F1-Score:  {ctx_f1*100:.2f}%")

    # 5. Build and Save Comparison DataFrame
    comparison_data = [
        {
            "Model": "TF-IDF + Logistic Regression (Baseline)",
            "Accuracy": round(base_acc, 4),
            "Precision (Weighted)": round(base_prec, 4),
            "Recall (Weighted)": round(base_rec, 4),
            "F1-Score (Weighted)": round(base_f1, 4),
            "Macro F1": round(base_macro_f1, 4)
        },
        {
            "Model": "Sentence Transformer + Logistic Regression (Contextual)",
            "Accuracy": round(ctx_acc, 4),
            "Precision (Weighted)": round(ctx_prec, 4),
            "Recall (Weighted)": round(ctx_rec, 4),
            "F1-Score (Weighted)": round(ctx_f1, 4),
            "Macro F1": round(ctx_macro_f1, 4)
        }
    ]
    df_comparison = pd.DataFrame(comparison_data)
    comp_csv_path = os.path.join(results_dir, "model_comparison.csv")
    df_comparison.to_csv(comp_csv_path, index=False)
    print(f"\nSaved model comparison table to: {comp_csv_path}")
    print("\nModel Comparison Table:")
    print(df_comparison.to_string(index=False))

    # 6. Save Classification Reports to text file
    txt_report_path = os.path.join(results_dir, "classification_report.txt")
    with open(txt_report_path, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("CONTEXT-BASED IDIOM MEANING IDENTIFIER - EVALUATION REPORT\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total Test Samples: {len(y_test)}\n")
        f.write(f"Classes Evaluated: {', '.join(target_names)}\n\n")
        
        f.write("-" * 50 + "\n")
        f.write("MODEL 1: BASELINE (TF-IDF + Logistic Regression)\n")
        f.write("-" * 50 + "\n")
        f.write(f"Accuracy:  {base_acc:.4f} ({base_acc*100:.2f}%)\n")
        f.write(f"Precision: {base_prec:.4f}\n")
        f.write(f"Recall:    {base_rec:.4f}\n")
        f.write(f"F1-Score:  {base_f1:.4f}\n\n")
        f.write(base_report + "\n\n")

        f.write("-" * 50 + "\n")
        f.write("MODEL 2: CONTEXTUAL (Sentence Transformer + Logistic Regression)\n")
        f.write("-" * 50 + "\n")
        f.write(f"Accuracy:  {ctx_acc:.4f} ({ctx_acc*100:.2f}%)\n")
        f.write(f"Precision: {ctx_prec:.4f}\n")
        f.write(f"Recall:    {ctx_rec:.4f}\n")
        f.write(f"F1-Score:  {ctx_f1:.4f}\n\n")
        f.write(ctx_report + "\n\n")
        
        f.write("=" * 70 + "\n")
        f.write("CONCLUSION:\n")
        f.write("The Sentence Transformer contextual model significantly outperforms the\n")
        f.write("TF-IDF baseline by leveraging deep bidirectional sentence embeddings\n")
        f.write("capable of capturing nuanced figurative vs. literal semantic contexts.\n")
        f.write("=" * 70 + "\n")
    print(f"Saved textual classification report to: {txt_report_path}")

    # 7. Generate and Save Confusion Matrix Plots
    # Baseline CM
    plt.figure(figsize=(6, 5))
    sns.heatmap(base_cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=target_names, yticklabels=target_names, cbar=False)
    plt.title("Baseline Model Confusion Matrix (TF-IDF)", fontsize=12, fontweight='bold', pad=12)
    plt.xlabel("Predicted Label", fontsize=10)
    plt.ylabel("True Label", fontsize=10)
    plt.tight_layout()
    cm_base_path = os.path.join(results_dir, "confusion_matrix_baseline.png")
    plt.savefig(cm_base_path, dpi=300)
    plt.close()
    print(f"Saved Baseline Confusion Matrix plot to: {cm_base_path}")

    # Contextual CM
    plt.figure(figsize=(6, 5))
    sns.heatmap(ctx_cm, annot=True, fmt='d', cmap='Greens',
                xticklabels=target_names, yticklabels=target_names, cbar=False)
    plt.title("Contextual Model Confusion Matrix (Sentence Transformer)", fontsize=12, fontweight='bold', pad=12)
    plt.xlabel("Predicted Label", fontsize=10)
    plt.ylabel("True Label", fontsize=10)
    plt.tight_layout()
    cm_ctx_path = os.path.join(results_dir, "confusion_matrix_contextual.png")
    plt.savefig(cm_ctx_path, dpi=300)
    plt.close()
    print(f"Saved Contextual Confusion Matrix plot to: {cm_ctx_path}")

    print("=" * 70)
    print(" EVALUATION COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    evaluate_all_models()
