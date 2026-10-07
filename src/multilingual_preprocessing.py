"""
Multilingual Preprocessing and Candidate Idiom Detection Pipeline
Supports: English (en), Hindi (hi), and Marathi (mr)

Features:
- Unicode NFC normalization for Devanagari and Latin scripts
- Script detection (Latin vs Devanagari) and language heuristic detection
- Language-aware text cleaning and tokenization
- Devanagari-aware regex matching with flexible boundary and whitespace handling
- Lemmatization fallback for English (preserves Devanagari untouched)
- Surrounding context extraction
"""

import re
import unicodedata
import string
from typing import Dict, Any, Optional, List, Tuple

# Try importing NLTK lemmatizer for English
try:
    import nltk
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize
    _lemmatizer = None
except ImportError:
    _lemmatizer = None


def get_english_lemmatizer():
    global _lemmatizer
    if _lemmatizer is None:
        try:
            _lemmatizer = WordNetLemmatizer()
            _lemmatizer.lemmatize("testing")
        except Exception:
            try:
                nltk.download("wordnet", quiet=True)
                nltk.download("omw-1.4", quiet=True)
                _lemmatizer = WordNetLemmatizer()
            except Exception:
                _lemmatizer = None
    return _lemmatizer


def clean_unicode(text: str) -> str:
    """
    Standardize text with Unicode NFC normalization and clean typographic variants.
    """
    if not isinstance(text, str):
        return ""
    # NFC normalizes composed characters (vital for Hindi and Marathi matras)
    text = unicodedata.normalize("NFC", text.strip())
    # Normalize quotes
    text = re.sub(r'[\u2018\u2019\u201a\u201b`]', "'", text)
    text = re.sub(r'[\u201c\u201d\u201e\u201f"]', '"', text)
    # Normalize dashes and hyphens
    text = re.sub(r'[\u2013\u2014]', '-', text)
    # Clean zero-width non-breaking space (BOM)
    text = text.replace('\ufeff', '')
    # Collapse multiple whitespaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def detect_script(text: str) -> str:
    """
    Detect whether text is primarily Devanagari or Latin.
    Returns: 'devanagari' or 'latin'
    """
    cleaned = clean_unicode(text)
    devanagari_count = sum(1 for ch in cleaned if '\u0900' <= ch <= '\u097F')
    latin_count = sum(1 for ch in cleaned if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z'))
    
    if devanagari_count > latin_count:
        return "devanagari"
    return "latin"


# Distinctive grammatical markers for language disambiguation in Devanagari
_MARATHI_MARKERS = {
    "आहे", "नाही", "झाले", "झाला", "झाली", "करणे", "केले", "केला", "केली", "येणे", "घेणे", 
    "च्या", "ला", "चे", "मध्ये", "होते", "होता", "होती", "आहेत", "नाहीत", "द्या", "पाहिजे",
    "म्हणून", "पण", "असे", "आणि", "कसे", "कधी", "कुठे", "कोण", "त्याला", "तिला", "त्यांचे"
}

_HINDI_MARKERS = {
    "है", "नहीं", "हुआ", "हुआ", "हुई", "करना", "किया", "किए", "की", "आना", "लेना",
    "का", "को", "के", "में", "था", "थी", "थे", "हैं", "दो", "चाहिए",
    "इसलिए", "लेकिन", "और", "कैसे", "कब", "कहाँ", "कौन", "उसको", "उसकी", "उनका"
}


def infer_language(text: str, default: str = "en") -> str:
    """
    Infer language ('en', 'hi', 'mr') from text tokens and script.
    """
    script = detect_script(text)
    if script == "latin":
        return "en"
    
    # Devanagari text: check marker overlap
    tokens = set(tokenize_multilingual(text, language="hi"))
    mr_score = len(tokens.intersection(_MARATHI_MARKERS))
    hi_score = len(tokens.intersection(_HINDI_MARKERS))
    
    if mr_score > hi_score:
        return "mr"
    elif hi_score > mr_score:
        return "hi"
    return default if default in ("hi", "mr") else "hi"


def tokenize_multilingual(text: str, language: str = "en") -> List[str]:
    """
    Language-aware tokenization:
    - English: NLTK word_tokenize with regex fallback.
    - Hindi / Marathi: Devanagari-aware regex tokenization preserving matras and words.
    """
    cleaned = clean_unicode(text)
    if not cleaned:
        return []
    
    if language == "en":
        try:
            tokens = word_tokenize(cleaned)
        except Exception:
            tokens = re.findall(r"\b\w+(?:'\w+)?\b|[^\w\s]", cleaned)
        return tokens
    else:
        # Devanagari + word tokens
        tokens = re.findall(r'[\u0900-\u097F]+|[a-zA-Z0-9]+|[^\s\w]', cleaned)
        return tokens


def normalize_for_tokens(text: str, language: str = "en") -> str:
    """
    Normalize text for TF-IDF or token-based baseline models.
    Preserves Devanagari script integrity while stripping extraneous symbols.
    """
    cleaned = clean_unicode(text)
    if language == "en":
        cleaned = cleaned.lower()
        cleaned = re.sub(r"[^\w\s']", ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned
    else:
        # For Hindi and Marathi: strip Latin punctuation and Devanagari danda, keep Devanagari chars
        cleaned = re.sub(r'[।॥!?,.:;"\'\(\)\[\]\{\}\-_/\\@#\$%\^&\*~`+=\<\>]', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned


def lemmatize_english(text: str) -> str:
    """
    Lemmatize English tokens using WordNetLemmatizer.
    Only applied to English text.
    """
    lemmatizer = get_english_lemmatizer()
    tokens = tokenize_multilingual(text, language="en")
    if not lemmatizer:
        return " ".join(tokens).lower()
    
    lemmatized = []
    for token in tokens:
        lower_tok = token.lower()
        v_lem = lemmatizer.lemmatize(lower_tok, pos='v')
        n_lem = lemmatizer.lemmatize(v_lem, pos='n')
        lemmatized.append(n_lem)
    return " ".join(lemmatized)


def detect_candidate_idiom(
    sentence: str,
    idiom_dictionary: Dict[str, Any],
    language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Scan input sentence to identify any candidate idiom from the knowledge base.
    Works for English, Hindi, and Marathi with script-appropriate boundary matching.

    Parameters:
        sentence: Input text string
        idiom_dictionary: Dictionary of idioms with aliases and metadata
        language: 'en', 'hi', 'mr', or None (auto-detect)

    Returns dict with keys:
        - detected: bool
        - idiom: canonical phrase / key or None
        - matched_span: exact substring found in input
        - span_indices: (start_idx, end_idx)
        - context_text: sentence with idiom excised for context analysis
        - language: detected or specified language
    """
    if not sentence or not isinstance(sentence, str):
        return {
            "detected": False,
            "idiom": None,
            "matched_span": "",
            "span_indices": (-1, -1),
            "context_text": "",
            "language": language or "en"
        }

    raw_text = clean_unicode(sentence)
    
    # Auto-detect language if not provided
    if language is None or language == "auto":
        detected_lang = infer_language(raw_text)
    else:
        detected_lang = language.lower()

    lower_text = raw_text.lower() if detected_lang == "en" else raw_text
    
    best_match = None
    longest_len = 0

    # Filter dictionary candidates by language if language metadata exists
    filtered_items = []
    for key, info in idiom_dictionary.items():
        entry_lang = info.get("language")
        if entry_lang is None or entry_lang == detected_lang or language is None:
            filtered_items.append((key, info))

    # Priority 1: Exact alias match with language-appropriate boundary matching
    for canonical_name, info in filtered_items:
        aliases = info.get("aliases", [canonical_name])
        # Sort aliases by length descending
        for alias in sorted(aliases, key=len, reverse=True):
            clean_alias = clean_unicode(alias)
            if not clean_alias:
                continue

            if detected_lang == "en":
                escaped_alias = re.escape(clean_alias.lower())
                pattern = r'\b' + escaped_alias.replace(r'\ ', r'\s+') + r'\b'
                match = re.search(pattern, lower_text)
            else:
                # Devanagari word characters: letters and combining marks
                # Exclude punctuation such as danda (\u0964), double danda (\u0965), and abbreviation sign (\u0970)
                escaped_alias = re.escape(clean_alias)
                _dev_word = r'[\u0900-\u0963\u0971-\u097F\w]'
                pattern = r'(?<!' + _dev_word + r')' + escaped_alias.replace(r'\ ', r'\s+') + r'(?!' + _dev_word + r')'
                match = re.search(pattern, raw_text)

            if match:
                match_len = match.end() - match.start()
                if match_len > longest_len:
                    longest_len = match_len
                    start_idx, end_idx = match.span()
                    best_match = {
                        "detected": True,
                        "idiom": canonical_name,
                        "matched_span": raw_text[start_idx:end_idx],
                        "span_indices": (start_idx, end_idx),
                        "language": info.get("language", detected_lang)
                    }

    # Priority 2: Lemmatized match for English only if no direct alias matched
    if not best_match and detected_lang == "en":
        lemmatized_sentence = lemmatize_english(raw_text)
        for canonical_name, info in filtered_items:
            canonical_lem = lemmatize_english(canonical_name)
            escaped = re.escape(canonical_lem)
            pattern = r'\b' + escaped.replace(r'\ ', r'\s+') + r'\b'
            match = re.search(pattern, lemmatized_sentence)
            if match:
                best_match = {
                    "detected": True,
                    "idiom": canonical_name,
                    "matched_span": canonical_name,
                    "span_indices": (0, len(raw_text)),
                    "language": "en"
                }
                break

    if best_match:
        start_idx, end_idx = best_match["span_indices"]
        if 0 <= start_idx < end_idx <= len(raw_text):
            prefix = raw_text[:start_idx].strip()
            suffix = raw_text[end_idx:].strip()
            context_text = f"{prefix} {suffix}".strip()
        else:
            context_text = raw_text
        best_match["context_text"] = context_text
        return best_match

    return {
        "detected": False,
        "idiom": None,
        "matched_span": "",
        "span_indices": (-1, -1),
        "context_text": raw_text,
        "language": detected_lang
    }


def extract_context_features(sentence: str, idiom: str, language: str = "en") -> Dict[str, Any]:
    """
    Extract linguistic context features around the target idiom in the sentence.
    """
    cleaned = clean_unicode(sentence)
    tokens = tokenize_multilingual(cleaned, language=language)
    normalized = normalize_for_tokens(cleaned, language=language)
    
    return {
        "raw_sentence": cleaned,
        "language": language,
        "tokens": tokens,
        "token_count": len(tokens),
        "normalized": normalized,
        "target_idiom": idiom
    }
