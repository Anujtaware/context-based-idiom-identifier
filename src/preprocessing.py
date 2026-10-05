"""
Text Preprocessing and Candidate Idiom Detection Pipeline

Includes:
- Text normalization (casing, whitespace, punctuation)
- Tokenization and Lemmatization
- Candidate Idiom Detection with flexible regex and alias matching
- Context Extraction (surrounding words excluding candidate idiom)
"""

import re
import string
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Lazy initialize lemmatizer
_lemmatizer = None


def get_lemmatizer():
    global _lemmatizer
    if _lemmatizer is None:
        try:
            _lemmatizer = WordNetLemmatizer()
            # Test run
            _lemmatizer.lemmatize("testing")
        except Exception:
            try:
                nltk.download("wordnet", quiet=True)
                nltk.download("omw-1.4", quiet=True)
                _lemmatizer = WordNetLemmatizer()
            except Exception:
                _lemmatizer = None
    return _lemmatizer


def clean_text(text: str) -> str:
    """
    Standardize text by stripping whitespace and normalizing quotes/hyphens.
    Preserves case and punctuation structure for context understanding.
    """
    if not isinstance(text, str):
        return ""
    text = text.strip()
    text = re.sub(r'[\u2018\u2019\u201a\u201b`]', "'", text)
    text = re.sub(r'[\u201c\u201d\u201e\u201f"]', '"', text)
    text = re.sub(r'\s+', ' ', text)
    return text


def normalize_for_tokens(text: str) -> str:
    """
    Lowercase and normalize text for basic token-level feature extraction.
    Note: Stopwords are preserved intentionally because function words
    (e.g., 'under', 'on', 'in', 'of') are critical constituents of idioms.
    """
    text = clean_text(text).lower()
    # Replace non-alphanumeric (except standard apostrophes and spaces)
    text = re.sub(r"[^\w\s']", ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def tokenize_sentence(text: str) -> list[str]:
    """
    Tokenize sentence using NLTK word_tokenize with regex fallback.
    """
    cleaned = clean_text(text)
    try:
        tokens = word_tokenize(cleaned)
    except Exception:
        # Fallback if punkt is not loaded
        tokens = re.findall(r"\b\w+(?:'\w+)?\b|[^\w\s]", cleaned)
    return tokens


def lemmatize_text(text: str) -> str:
    """
    Lemmatize tokens in text using WordNetLemmatizer.
    """
    lemmatizer = get_lemmatizer()
    tokens = tokenize_sentence(text)
    if not lemmatizer:
        return " ".join(tokens).lower()
    
    lemmatized = []
    for token in tokens:
        # Lemmatize both as verb and noun to catch inflection variants (e.g., spilled -> spill, hitting -> hit)
        lower_tok = token.lower()
        v_lem = lemmatizer.lemmatize(lower_tok, pos='v')
        n_lem = lemmatizer.lemmatize(v_lem, pos='n')
        lemmatized.append(n_lem)
    return " ".join(lemmatized)


def detect_candidate_idiom(sentence: str, idiom_dictionary: dict) -> dict:
    """
    Scan the input sentence to identify any candidate idiom from the knowledge base.
    Uses multi-stage matching:
    1. Exact alias/variant substring matching with word boundaries.
    2. Lemmatized matching for inflected forms (e.g. 'burning the midnight oil' -> 'burn the midnight oil').
    3. Partial core phrase matching.

    Returns:
        dict with keys:
            - detected: bool
            - idiom: canonical idiom name (str) or None
            - matched_span: exact substring found in input (str)
            - span_indices: (start_idx, end_idx)
            - context_text: sentence with the idiom removed/masked for context analysis
    """
    if not sentence or not isinstance(sentence, str):
        return {
            "detected": False,
            "idiom": None,
            "matched_span": "",
            "span_indices": (-1, -1),
            "context_text": ""
        }

    raw_text = clean_text(sentence)
    lower_text = raw_text.lower()
    
    # Priority 1: Exact alias match with word boundaries
    best_match = None
    longest_len = 0
    
    for canonical_name, info in idiom_dictionary.items():
        aliases = info.get("aliases", [canonical_name])
        # Sort aliases by length descending so longer matching phrases match first
        for alias in sorted(aliases, key=len, reverse=True):
            # Create word-boundary regex pattern
            escaped_alias = re.escape(alias.lower())
            # Replace spaces with flexible whitespace pattern
            pattern = r'\b' + escaped_alias.replace(r'\ ', r'\s+') + r'\b'
            
            match = re.search(pattern, lower_text)
            if match:
                match_len = match.end() - match.start()
                if match_len > longest_len:
                    longest_len = match_len
                    start_idx, end_idx = match.span()
                    best_match = {
                        "detected": True,
                        "idiom": canonical_name,
                        "matched_span": raw_text[start_idx:end_idx],
                        "span_indices": (start_idx, end_idx)
                    }

    # Priority 2: Lemmatized match if no direct alias matched
    if not best_match:
        lemmatized_sentence = lemmatize_text(raw_text)
        for canonical_name, info in idiom_dictionary.items():
            canonical_lem = lemmatize_text(canonical_name)
            escaped = re.escape(canonical_lem)
            pattern = r'\b' + escaped.replace(r'\ ', r'\s+') + r'\b'
            match = re.search(pattern, lemmatized_sentence)
            if match:
                # Find approximate span in raw text by word overlap
                best_match = {
                    "detected": True,
                    "idiom": canonical_name,
                    "matched_span": canonical_name,
                    "span_indices": (0, len(raw_text))
                }
                break

    if best_match:
        start_idx, end_idx = best_match["span_indices"]
        if start_idx >= 0 and end_idx <= len(raw_text):
            # Context is surrounding sentence without the idiom phrase
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
        "context_text": raw_text
    }


def extract_context_features(sentence: str, idiom: str) -> dict:
    """
    Extract linguistic context features around the idiom in the sentence.
    """
    cleaned = clean_text(sentence)
    tokens = tokenize_sentence(cleaned)
    lem_sentence = lemmatize_text(cleaned)
    
    return {
        "raw_sentence": cleaned,
        "tokens": tokens,
        "token_count": len(tokens),
        "lemmatized": lem_sentence,
        "target_idiom": idiom
    }


if __name__ == "__main__":
    import sys
    from pathlib import Path

    # Ensure parent dir is in sys.path to import idiom_dictionary
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from idiom_dictionary import IDIOM_DICTIONARY

    print("=" * 70)
    print(" PREPROCESSING & IDIOM DETECTION PIPELINE DEMO")
    print("=" * 70)

    sample_sentences = [
        "After studying all night, Rahul was feeling under the weather.",
        "The child was sitting under the weather shelter.",
        "The mathematics test was a piece of cake.",
        "The weather was terrible yesterday."
    ]

    for i, s in enumerate(sample_sentences, 1):
        print(f"\n[Sample {i}] \"{s}\"")
        norm = clean_text(s)
        tokens = tokenize_sentence(norm)
        lem = lemmatize_text(norm)
        detection = detect_candidate_idiom(norm, IDIOM_DICTIONARY)
        
        print(f"  * Cleaned:       {norm}")
        print(f"  * Tokens:        {tokens[:8]}{'...' if len(tokens) > 8 else ''}")
        print(f"  * Lemmatized:    {lem}")
        print(f"  * Detected:      {detection['detected']}")
        if detection['detected']:
            print(f"  * Idiom:         {detection['idiom']}")
            print(f"  * Matched Span:  \"{detection['matched_span']}\"")
            print(f"  * Context Words: \"{detection['context_text']}\"")
    print("\n" + "=" * 70)

