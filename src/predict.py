"""
Inference and Prediction Pipeline for Context-Based Idiom Identification

Provides the core `analyze_sentence()` function used by both the CLI
and the Streamlit UI, implementing the complete architecture:
Input -> Preprocessing -> Candidate Detection -> Context Extraction ->
Usage Classification -> Meaning Mapping -> Explanation Generation.
"""

import os
import re
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer

from idiom_dictionary import IDIOM_DICTIONARY, get_idiom_info
from preprocessing import clean_text, detect_candidate_idiom, normalize_for_tokens


# Global cache for models
_CACHED_RESOURCES = {}


def load_inference_models(models_dir: str = None):
    """
    Load and cache baseline, contextual, and label encoder models.
    """
    global _CACHED_RESOURCES
    if _CACHED_RESOURCES.get("loaded", False):
        return _CACHED_RESOURCES

    if models_dir is None:
        models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")

    # Label Encoder
    le_path = os.path.join(models_dir, "label_encoder.pkl")
    label_encoder = joblib.load(le_path)

    # Baseline Model + TF-IDF
    tfidf_path = os.path.join(models_dir, "tfidf_vectorizer.pkl")
    base_model_path = os.path.join(models_dir, "baseline_model.pkl")
    tfidf_vectorizer = joblib.load(tfidf_path)
    baseline_clf = joblib.load(base_model_path)

    # Contextual Model + Transformer
    ctx_model_path = os.path.join(models_dir, "contextual_model.pkl")
    ctx_bundle = joblib.load(ctx_model_path)
    contextual_clf = ctx_bundle["model"]
    emb_model_name = ctx_bundle.get("embedding_model_name", "all-MiniLM-L6-v2")
    transformer = SentenceTransformer(emb_model_name)

    _CACHED_RESOURCES = {
        "loaded": True,
        "label_encoder": label_encoder,
        "classes": list(label_encoder.classes_),
        "tfidf_vectorizer": tfidf_vectorizer,
        "baseline_model": baseline_clf,
        "contextual_model": contextual_clf,
        "transformer": transformer,
        "emb_model_name": emb_model_name
    }
    return _CACHED_RESOURCES


def generate_context_explanation(sentence: str, idiom_name: str, usage_type: str, idiom_meta: dict, context_text: str) -> str:
    """
    Generate a transparent, context-grounded explanation based on surrounding context
    tokens, domain keywords, and predicted usage type.
    """
    if not idiom_meta:
        return "No specific idiom pattern recognized in the sentence structure."

    lower_sentence = sentence.lower()
    words = set(re.findall(r'\b\w+\b', lower_sentence))

    if usage_type == "idiomatic":
        idiom_keywords = set(idiom_meta.get("idiomatic_keywords", []))
        matched_cues = words.intersection(idiom_keywords)
        
        category = idiom_meta.get("category", "General")
        if matched_cues:
            cues_str = ", ".join([f'"{w}"' for w in sorted(list(matched_cues))[:4]])
            return (
                f"The surrounding words such as {cues_str} provide semantic cues in the domain of "
                f"'{category}'. This strongly supports an idiomatic (figurative) interpretation of "
                f"\"{idiom_name}\" rather than a literal physical action."
            )
        else:
            return (
                f"The sentence context surrounding \"{idiom_name}\" relates to '{category}', "
                f"signaling that the expression is used figuratively to convey: \"{idiom_meta['meaning']}\"."
            )

    elif usage_type == "literal":
        literal_keywords = set(idiom_meta.get("literal_keywords", []))
        matched_literal_cues = words.intersection(literal_keywords)
        
        if matched_literal_cues:
            cues_str = ", ".join([f'"{w}"' for w in sorted(list(matched_literal_cues))[:4]])
            return (
                f"The presence of physical/concrete context words such as {cues_str} indicates that "
                f"the phrase \"{idiom_name}\" is being used in its literal, physical sense rather "
                f"than as a figurative expression."
            )
        else:
            return (
                f"The contextual structure indicates a concrete, physical, or non-figurative description. "
                f"Therefore, the model classifies the expression \"{idiom_name}\" as literal/non-idiomatic."
            )

    else:
        return "The sentence does not contain evidence of idiomatic or figurative usage."


def analyze_sentence(sentence: str, model_type: str = "contextual", models_dir: str = None) -> dict:
    """
    Complete analysis pipeline:
    1. Validate input text.
    2. Detect candidate idiom and extract context window.
    3. Run classification (Baseline or Contextual) to determine usage type ('idiomatic', 'literal', 'none').
    4. Retrieve canonical meaning and generate explanation.
    """
    if not sentence or not isinstance(sentence, str) or len(sentence.strip()) == 0:
        return {
            "success": False,
            "error": "Input sentence is empty. Please enter a valid English sentence.",
            "detected_expression": None,
            "usage": "None",
            "meaning": "N/A",
            "confidence": 0.0,
            "context": "",
            "explanation": "No input provided.",
            "example": "N/A",
            "category": "N/A",
            "probabilities": {}
        }

    cleaned = clean_text(sentence)
    if len(cleaned.split()) < 2:
        return {
            "success": False,
            "error": "Sentence is too short. Please provide a complete sentence with surrounding context.",
            "detected_expression": None,
            "usage": "None",
            "meaning": "N/A",
            "confidence": 0.0,
            "context": cleaned,
            "explanation": "Insufficient context for NLP classification.",
            "example": "N/A",
            "category": "N/A",
            "probabilities": {}
        }

    # Load models
    resources = load_inference_models(models_dir)
    classes = resources["classes"]

    # 1. Candidate Detection
    candidate = detect_candidate_idiom(cleaned, IDIOM_DICTIONARY)
    has_candidate = candidate["detected"]
    idiom_key = candidate["idiom"]
    matched_span = candidate["matched_span"]
    context_text = candidate["context_text"]

    # 2. Classification on sentence
    if model_type.lower() == "baseline":
        clean_tok = normalize_for_tokens(cleaned)
        X_vec = resources["tfidf_vectorizer"].transform([clean_tok])
        probs = resources["baseline_model"].predict_proba(X_vec)[0]
    else:
        # Contextual model
        emb = resources["transformer"].encode([cleaned], show_progress_bar=False, normalize_embeddings=True)
        probs = resources["contextual_model"].predict_proba(emb)[0]

    prob_dict = {cls_name: float(probs[i]) for i, cls_name in enumerate(classes)}
    pred_class_idx = int(np.argmax(probs))
    pred_usage = classes[pred_class_idx]
    confidence = float(probs[pred_class_idx])

    # 3. Decision Logic: Combine Candidate Match and Model Prediction
    if not has_candidate:
        # If no candidate idiom is detected in knowledge base
        return {
            "success": True,
            "detected_expression": None,
            "usage": "None",
            "meaning": "No known idiom detected in the input sentence.",
            "confidence": round(confidence * 100, 2),
            "context": cleaned,
            "explanation": "The NLP pipeline scanned the sentence but found no known idiom pattern from the supported knowledge base.",
            "example": "N/A",
            "category": "None",
            "model_used": "Baseline (TF-IDF)" if model_type.lower() == "baseline" else "Contextual (Sentence Transformer)",
            "probabilities": {k: round(v * 100, 2) for k, v in prob_dict.items()}
        }

    # Candidate was found
    idiom_meta = get_idiom_info(idiom_key)
    
    # If classifier predicted 'none' despite candidate, check if candidate was ambiguous or fallback to literal
    if pred_usage == "none":
        final_usage = "Literal / Non-idiomatic"
        meaning_text = f"Expression '{matched_span}' detected, but the context indicates non-idiomatic usage."
    elif pred_usage == "literal":
        final_usage = "Literal / Non-idiomatic"
        meaning_text = f"Expression '{matched_span}' detected, but the context appears literal (physical interpretation)."
    else:
        final_usage = "Idiomatic"
        meaning_text = idiom_meta["meaning"] if idiom_meta else "Idiomatic figurative expression."

    explanation = generate_context_explanation(cleaned, idiom_key, pred_usage, idiom_meta, context_text)

    return {
        "success": True,
        "detected_expression": matched_span if matched_span else idiom_key,
        "canonical_idiom": idiom_key,
        "usage": final_usage,
        "predicted_class": pred_usage,
        "meaning": meaning_text,
        "confidence": round(confidence * 100, 2),
        "context": f"...{context_text}..." if context_text else cleaned,
        "explanation": explanation,
        "example": idiom_meta.get("example", "N/A") if idiom_meta else "N/A",
        "category": idiom_meta.get("category", "General") if idiom_meta else "General",
        "model_used": "Baseline (TF-IDF)" if model_type.lower() == "baseline" else "Contextual (Sentence Transformer)",
        "probabilities": {k: round(v * 100, 2) for k, v in prob_dict.items()}
    }


def interactive_cli():
    print("=" * 65)
    print(" CONTEXT-BASED IDIOM MEANING IDENTIFIER - CLI")
    print("=" * 65)
    print("Type your sentence and press Enter (or type 'exit' / 'quit' to stop).\n")

    while True:
        try:
            sentence = input("\nEnter sentence: ").strip()
            if sentence.lower() in ["exit", "quit", "q"]:
                print("Exiting CLI. Goodbye!")
                break

            if not sentence:
                continue

            result = analyze_sentence(sentence, model_type="contextual")
            
            print("-" * 50)
            if not result.get("detected_expression"):
                print("Detected Expression: No known idiom detected.")
                print(f"Confidence:          {result.get('confidence', 0)}%")
                print(f"Explanation:         {result.get('explanation')}")
            else:
                print(f"Detected Idiom:      {result.get('detected_expression')}")
                print(f"Usage:               {result.get('usage')}")
                print(f"Meaning:             {result.get('meaning')}")
                print(f"Confidence:          {result.get('confidence')}%")
                print(f"Context:             {result.get('context')}")
                print(f"Explanation:         {result.get('explanation')}")
                print(f"Example:             {result.get('example')}")
            print("-" * 50)

        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            break


if __name__ == "__main__":
    interactive_cli()
