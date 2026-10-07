"""
Inference and Prediction Pipeline for Multilingual Context-Based Idiom Identification
Supports: English, Hindi, and Marathi

Pipeline:
1. Input Validation & Language Detection
2. Multilingual Candidate Idiom Detection & Context Extraction
3. Usage Classification (Baseline TF-IDF or Multilingual Sentence Transformer)
4. Meaning Mapping & Grounded Linguistic Explanation Generation
"""

import os
import re
import joblib
import numpy as np
from typing import Dict, Any, Optional
from sentence_transformers import SentenceTransformer

from idiom_dictionary import IDIOM_DICTIONARY, get_idiom_info
from multilingual_preprocessing import (
    clean_unicode,
    detect_candidate_idiom,
    normalize_for_tokens,
    infer_language
)

# Global cache for inference models
_CACHED_RESOURCES = {}


def load_inference_models(models_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Load and cache baseline, contextual, and label encoder models.
    """
    global _CACHED_RESOURCES
    if _CACHED_RESOURCES.get("loaded", False):
        return _CACHED_RESOURCES

    if models_dir is None:
        models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")

    # 1. Label Encoder
    le_path = os.path.join(models_dir, "label_encoder.pkl")
    label_encoder = joblib.load(le_path)

    # 2. Baseline Model + TF-IDF Vectorizer
    tfidf_path = os.path.join(models_dir, "tfidf_vectorizer.pkl")
    base_model_path = os.path.join(models_dir, "baseline_model.pkl")
    tfidf_vectorizer = joblib.load(tfidf_path)
    baseline_clf = joblib.load(base_model_path)

    # 3. Contextual Model + Multilingual Transformer
    ctx_model_path = os.path.join(models_dir, "contextual_model.pkl")
    ctx_bundle = joblib.load(ctx_model_path)
    contextual_clf = ctx_bundle["model"]
    emb_model_name = ctx_bundle.get("embedding_model_name", "paraphrase-multilingual-MiniLM-L12-v2")
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


def generate_context_explanation(
    sentence: str,
    idiom_name: str,
    usage_type: str,
    idiom_meta: Optional[Dict[str, Any]],
    context_text: str,
    language: str = "en"
) -> str:
    """
    Generate transparent, context-grounded explanation based on surrounding context
    tokens, domain keywords, predicted usage type, and language.
    """
    if not idiom_meta:
        return "No specific idiom pattern recognized in the sentence structure."

    target_text = context_text if context_text else sentence
    lower_target = target_text.lower()
    words = set(re.findall(r'\b\w+\b', lower_target)) if language == "en" else set(re.findall(r'[\u0900-\u097F]+|\w+', target_text))
    category = idiom_meta.get("category", "General")
    meaning = idiom_meta.get("meaning", "")

    if usage_type == "idiomatic":
        idiom_keywords = set(idiom_meta.get("idiomatic_keywords", []))
        matched_cues = words.intersection(idiom_keywords)
        
        if language == "hi":
            if matched_cues:
                cues_str = ", ".join([f'"{w}"' for w in sorted(list(matched_cues))[:4]])
                return (
                    f"वाक्य के संदर्भ में {cues_str} जैसे शब्द '{category}' क्षेत्र के सांकेतिक संकेत प्रदान करते हैं। "
                    f"यह दृढ़ता से दर्शाता है कि \"{idiom_name}\" का प्रयोग भौतिक क्रिया के स्थान पर लाक्षणिक (मुहावरेदार) अर्थ: \"{meaning}\" में हुआ है।"
                )
            else:
                return (
                    f"\"{idiom_name}\" के आसपास का संदर्भ '{category}' से संबंधित है, जो संकेत करता है कि यह अभिव्यक्ति "
                    f"लाक्षणिक रूप से प्रयुक्त हुई है: \"{meaning}\"।"
                )
        elif language == "mr":
            if matched_cues:
                cues_str = ", ".join([f'"{w}"' for w in sorted(list(matched_cues))[:4]])
                return (
                    f"वाक्यातील {cues_str} यांसारखे संदर्भ शब्द '{category}' या क्षेत्रातील भाषिक संकेत दर्शवतात. "
                    f"यावरून स्पष्ट होते की \"{idiom_name}\" हा वाक्प्रचार प्रत्यक्ष कृतीऐवजी लाक्षणिक अर्थाने: \"{meaning}\" असा वापरला गेला आहे."
                )
            else:
                return (
                    f"\"{idiom_name}\" चा आजूबाजूचा संदर्भ '{category}' क्षेत्राशी संबंधित असून, "
                    f"तो लाक्षणिक अर्थाने: \"{meaning}\" असा व्यक्त होत आहे."
                )
        else:
            # English
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
                    f"signaling that the expression is used figuratively to convey: \"{meaning}\"."
                )

    elif usage_type == "literal":
        literal_keywords = set(idiom_meta.get("literal_keywords", []))
        matched_literal_cues = words.intersection(literal_keywords)

        if language == "hi":
            if matched_literal_cues:
                cues_str = ", ".join([f'"{w}"' for w in sorted(list(matched_literal_cues))[:4]])
                return (
                    f"वाक्य में {cues_str} जैसे भौतिक/ठोस शब्द इंगित करते हैं कि \"{idiom_name}\" "
                    f"का प्रयोग लाक्षणिक अर्थ में न होकर अपने प्रत्यक्ष भौतिक अर्थ में हुआ है।"
                )
            else:
                return (
                    f"वाक्य की संरचना ठोस, भौतिक अथवा गैर-लाक्षणिक विवरण दर्शाती है। इसलिए मॉडल ने "
                    f"\"{idiom_name}\" को प्रत्यक्ष/भौतिक (गैर-मुहावरेदार) वर्गीकृत किया है।"
                )
        elif language == "mr":
            if matched_literal_cues:
                cues_str = ", ".join([f'"{w}"' for w in sorted(list(matched_literal_cues))[:4]])
                return (
                    f"वाक्यात {cues_str} यांसारखे प्रत्यक्ष भौतिक शब्द आढळल्याने, \"{idiom_name}\" "
                    f"हा वाक्प्रचार नसून प्रत्यक्ष भौतिक अर्थाने वापरला गेला आहे."
                )
            else:
                return (
                    f"वाक्यातील संदर्भ प्रत्यक्ष भौतिक वर्णनाचा आहे. त्यामुळे मॉडेलने "
                    f"\"{idiom_name}\" चे वर्गीकरण अ-लाक्षणिक (प्रत्यक्ष अर्थ) असे केले आहे."
                )
        else:
            # English
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
        if language == "hi":
            return "वाक्य में किसी मुहावरेदार अथवा लाक्षणिक प्रयोग का कोई प्रमाण नहीं मिला।"
        elif language == "mr":
            return "वाक्यात कोणत्याही वाक्प्रचाराचा लाक्षणिक पुरावा आढळला नाही."
        return "The sentence does not contain evidence of idiomatic or figurative usage."


def analyze_sentence(
    sentence: str,
    model_type: str = "contextual",
    language: Optional[str] = None,
    models_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    Complete multilingual analysis pipeline:
    1. Input validation & script/language detection.
    2. Candidate idiom detection & context window isolation.
    3. Multilingual classification (Baseline or Contextual).
    4. Canonical meaning mapping & grounded explanation generation.
    """
    if not sentence or not isinstance(sentence, str) or len(sentence.strip()) == 0:
        return {
            "success": False,
            "error": "Input sentence is empty. Please enter a valid sentence.",
            "language": language or "en",
            "detected_expression": None,
            "usage": "None",
            "meaning": "N/A",
            "confidence": 0.0,
            "context": "",
            "explanation": "No input provided.",
            "example": "N/A",
            "category": "N/A",
            "probabilities": {},
            "warning": "Empty input"
        }

    cleaned = clean_unicode(sentence)
    if len(cleaned.split()) < 2:
        return {
            "success": False,
            "error": "Sentence is too short. Please provide a complete sentence with surrounding context.",
            "language": language or "en",
            "detected_expression": None,
            "usage": "None",
            "meaning": "N/A",
            "confidence": 0.0,
            "context": cleaned,
            "explanation": "Insufficient context for NLP classification.",
            "example": "N/A",
            "category": "N/A",
            "probabilities": {},
            "warning": "Short input"
        }

    # Language inference
    if language is None or language == "auto":
        target_lang = infer_language(cleaned)
    else:
        target_lang = language.lower()

    # Load inference models
    resources = load_inference_models(models_dir)
    classes = resources["classes"]

    # 1. Candidate Idiom Detection
    candidate = detect_candidate_idiom(cleaned, IDIOM_DICTIONARY, language=target_lang)
    has_candidate = candidate["detected"]
    idiom_key = candidate["idiom"]
    matched_span = candidate["matched_span"]
    context_text = candidate["context_text"]
    detected_lang = candidate.get("language", target_lang)

    # 2. Classification Inference
    if model_type.lower() == "baseline":
        clean_tok = normalize_for_tokens(cleaned, language=detected_lang)
        X_vec = resources["tfidf_vectorizer"].transform([clean_tok])
        probs = resources["baseline_model"].predict_proba(X_vec)[0].copy()
    else:
        # Contextual Sentence Transformer
        emb = resources["transformer"].encode([cleaned], show_progress_bar=False, normalize_embeddings=True)
        probs = resources["contextual_model"].predict_proba(emb)[0].copy()

    # Look up candidate metadata for grounded contextual disambiguation
    idiom_meta = get_idiom_info(idiom_key, language=detected_lang) if has_candidate else None

    if has_candidate and idiom_meta:
        # Surrounding context cues from excised context window
        ik = idiom_meta.get("idiomatic_keywords", [])
        lk = idiom_meta.get("literal_keywords", [])
        ctx_clean = context_text.lower() if detected_lang == "en" else context_text
        ctx_tokens = set(re.findall(r'[\u0900-\u097F]+|\w+', ctx_clean))

        idio_hits = [k for k in ik if any(k in tok or tok in k for tok in ctx_tokens)]
        lit_hits = [k for k in lk if any(k in tok or tok in k for tok in ctx_tokens)]

        idx_idio = list(classes).index("idiomatic")
        idx_lit = list(classes).index("literal")
        idx_none = list(classes).index("none")

        if len(idio_hits) > len(lit_hits):
            cue_diff = len(idio_hits) - len(lit_hits)
            cue_strength = min(0.45 * cue_diff, 0.85)
            probs[idx_idio] += cue_strength
            probs[idx_lit] = max(0.01, probs[idx_lit] * (1.0 - cue_strength))
            probs[idx_none] = max(0.001, probs[idx_none] * (1.0 - cue_strength))
            probs = probs / np.sum(probs)
        elif len(lit_hits) > len(idio_hits):
            cue_diff = len(lit_hits) - len(idio_hits)
            cue_strength = min(0.45 * cue_diff, 0.85)
            probs[idx_lit] += cue_strength
            probs[idx_idio] = max(0.01, probs[idx_idio] * (1.0 - cue_strength))
            probs[idx_none] = max(0.001, probs[idx_none] * (1.0 - cue_strength))
            probs = probs / np.sum(probs)

    prob_dict = {cls_name: float(probs[i]) for i, cls_name in enumerate(classes)}
    pred_class_idx = int(np.argmax(probs))
    pred_usage = classes[pred_class_idx]
    confidence = float(probs[pred_class_idx])

    # 3. Decision & Explanation Logic
    if not has_candidate:
        warning_msg = f"The input sentence in {detected_lang.upper()} does not match any idiom in the knowledge base."
        return {
            "success": True,
            "language": detected_lang,
            "detected_expression": None,
            "canonical_idiom": None,
            "usage": "None",
            "predicted_class": "none",
            "meaning": "No known idiom detected in the input sentence.",
            "confidence": round(confidence * 100, 2),
            "context": cleaned,
            "explanation": "The multilingual NLP pipeline scanned the sentence but found no matching candidate from the supported idioms registry.",
            "example": "Not applicable",
            "category": "None",
            "model_used": "Baseline (Multilingual TF-IDF)" if model_type.lower() == "baseline" else "Contextual (Multilingual MiniLM)",
            "probabilities": {k: round(v * 100, 2) for k, v in prob_dict.items()},
            "warning": warning_msg
        }

    # Candidate found
    idiom_meta = get_idiom_info(idiom_key, language=detected_lang)

    if pred_usage == "none":
        final_usage = "Literal / Non-idiomatic"
        meaning_text = f"Expression '{matched_span}' detected, but the context indicates non-idiomatic usage."
    elif pred_usage == "literal":
        final_usage = "Literal / Non-idiomatic"
        meaning_text = f"Expression '{matched_span}' detected, but the context indicates literal (physical) interpretation."
    else:
        final_usage = "Idiomatic"
        meaning_text = idiom_meta["meaning"] if idiom_meta else "Idiomatic figurative expression."

    explanation = generate_context_explanation(
        cleaned,
        idiom_key,
        pred_usage,
        idiom_meta,
        context_text,
        language=detected_lang
    )

    return {
        "success": True,
        "language": detected_lang,
        "detected_expression": matched_span if matched_span else idiom_key,
        "canonical_idiom": idiom_key,
        "usage": final_usage,
        "predicted_class": pred_usage,
        "meaning": meaning_text,
        "confidence": round(confidence * 100, 2),
        "context": f"...{context_text}..." if context_text else cleaned,
        "explanation": explanation,
        "example": idiom_meta.get("example", "Not applicable") if idiom_meta else "Not applicable",
        "category": idiom_meta.get("category", "General") if idiom_meta else "General",
        "model_used": "Baseline (Multilingual TF-IDF)" if model_type.lower() == "baseline" else "Contextual (Multilingual MiniLM)",
        "probabilities": {k: round(v * 100, 2) for k, v in prob_dict.items()},
        "warning": None
    }


def interactive_cli():
    print("=" * 70)
    print(" MULTILINGUAL CONTEXT-BASED IDIOM IDENTIFIER - CLI")
    print(" Supports: English (en), Hindi (hi), Marathi (mr)")
    print("=" * 70)
    print("Type your sentence and press Enter (or 'exit' to quit).\n")

    while True:
        try:
            sentence = input("\nEnter sentence: ").strip()
            if sentence.lower() in ["exit", "quit", "q"]:
                print("Exiting CLI. Goodbye!")
                break

            if not sentence:
                continue

            result = analyze_sentence(sentence, model_type="contextual")
            print("-" * 55)
            print(f"Language:            {result.get('language')}")
            print(f"Detected Idiom:      {result.get('detected_expression')}")
            print(f"Usage Class:         {result.get('usage')}")
            print(f"Confidence:          {result.get('confidence')}%")
            print(f"Meaning:             {result.get('meaning')}")
            print(f"Context:             {result.get('context')}")
            print(f"Explanation:         {result.get('explanation')}")
            print(f"Probabilities:       {result.get('probabilities')}")
            if result.get('warning'):
                print(f"Notice:              {result.get('warning')}")
            print("-" * 55)

        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            break


if __name__ == "__main__":
    interactive_cli()
