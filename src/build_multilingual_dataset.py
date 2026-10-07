"""
Master Script to Build the Multilingual Benchmark Dataset (5,400 samples)
Combines:
- 1,800 English samples
- 1,800 Hindi samples
- 1,800 Marathi samples
Total: 5,400 balanced, high-quality, 100% deduplicated samples.
"""

import os
import sys
import pandas as pd
import unicodedata

# Add src to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from idiom_dictionary import IDIOM_DICTIONARY, get_idiom_info
from dataset_generator_en import get_english_records
from dataset_generator_hi import get_hindi_records
from dataset_generator_mr import get_marathi_records


def build_multilingual_dataset_dataframe() -> pd.DataFrame:
    print("=" * 70)
    print(" GENERATING MULTILINGUAL IDIOMS BENCHMARK DATASET")
    print("=" * 70)

    en_records = get_english_records()
    print(f"Generated {len(en_records)} English records.")

    hi_records = get_hindi_records()
    print(f"Generated {len(hi_records)} Hindi records.")

    mr_records = get_marathi_records()
    print(f"Generated {len(mr_records)} Marathi records.")

    all_raw = en_records + hi_records + mr_records
    print(f"Combined total raw records: {len(all_raw)}")

    final_records = []
    seen_sentences = set()

    for idx, r in enumerate(all_raw, 1):
        sent = unicodedata.normalize("NFC", r["sentence"].strip())
        if sent in seen_sentences:
            raise ValueError(f"Cross-dataset duplicate detected at index {idx}: {sent}")
        seen_sentences.add(sent)

        idiom_name = r["idiom"]
        usage_type = r["usage_type"]
        context_desc = r["context"]
        lang = r["language"]

        # Lookup meaning and canonical example from dictionary
        if idiom_name != "none":
            meta = get_idiom_info(idiom_name, language=lang)
            if meta:
                meaning = meta.get("meaning", "Idiomatic figurative expression.")
                example = meta.get("example", "Not applicable")
                canonical_phrase = meta.get("phrase", idiom_name)
            else:
                meaning = "Figurative idiom meaning."
                example = "Not applicable"
                canonical_phrase = idiom_name
        else:
            meaning = "None / Standard non-idiomatic expression."
            example = "Not applicable"
            canonical_phrase = "none"

        final_records.append({
            "id": idx,
            "language": lang,
            "sentence": sent,
            "idiom": canonical_phrase,
            "meaning": meaning,
            "usage_type": usage_type,
            "context": context_desc,
            "example": example
        })

    df = pd.DataFrame(final_records)
    return df


def main():
    os.makedirs(DATASET_DIR, exist_ok=True)
    df = build_multilingual_dataset_dataframe()

    # Save to dataset/multilingual_idioms.csv
    multi_csv_path = os.path.join(DATASET_DIR, "multilingual_idioms.csv")
    df.to_csv(multi_csv_path, index=False, encoding="utf-8")
    print(f"\n[OK] Saved multilingual dataset to: {multi_csv_path}")

    # Also save to dataset/idioms.csv as primary source
    idioms_csv_path = os.path.join(DATASET_DIR, "idioms.csv")
    df.to_csv(idioms_csv_path, index=False, encoding="utf-8")
    print(f"[OK] Updated primary idioms dataset at: {idioms_csv_path}")

    print("\nDataset Summary Statistics:")
    print(f"Total Rows: {len(df)}")
    print("\nBreakdown by Language:")
    print(df['language'].value_counts())
    print("\nBreakdown by Usage Type:")
    print(df['usage_type'].value_counts())
    print("\nLanguage x Usage Type Matrix:")
    print(pd.crosstab(df['language'], df['usage_type']))
    print(f"\nTotal Unique Canonical Idioms: {df[df['idiom'] != 'none']['idiom'].nunique()}")
    print("=" * 70)


if __name__ == "__main__":
    main()
