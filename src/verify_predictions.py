"""
Verification Script for Testing Multilingual Predictions and Context Awareness
Covers: English, Hindi, and Marathi across Idiomatic, Literal, and Contrast Pairs.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from predict import analyze_sentence

test_sentences = [
    # ── English Cases ──
    ("EN-Idiomatic 1", "Rahul was feeling under the weather after studying all night.", "en"),
    ("EN-Literal 1", "The child was sitting under the weather shelter during the rain.", "en"),
    ("EN-Negative", "The actual weather was cold and rainy yesterday.", "en"),
    ("EN-Idiomatic 2", "The mathematics test was an absolute piece of cake.", "en"),
    ("EN-Literal 2", "She offered her guest a delicious sweet piece of cake.", "en"),
    ("EN-Contrast Pair 3A", "The teacher said I had hit the nail on the head.", "en"),
    ("EN-Contrast Pair 3B", "The carpenter swung the hammer to hit the nail on the head.", "en"),

    # ── Hindi Cases ──
    ("HI-Idiomatic 1", "रोहन अपने माता-पिता की आँखों का तारा है।", "hi"),
    ("HI-Idiomatic 2", "अध्यापक को देखते ही शरारती छात्र भीगी बिल्ली बन गया।", "hi"),
    ("HI-Literal 2", "भीषण मानसूनी वर्षा में भीगी बिल्ली बरामदे में कांप रही थी।", "hi"),
    ("HI-Idiomatic 3", "व्यापारिक सौदे में अधिकारियों की चुप्पी से लगा कि दाल में कुछ काला है।", "hi"),
    ("HI-Literal 3", "रसोईघर में दाल बीनते समय थाली में दाल में काला कंकड़ अलग दिखाई दे रहा था।", "hi"),
    ("HI-Negative", "मौसम विभाग के अनुसार आगामी चौबीस घंटों में हल्की वर्षा होगी।", "hi"),

    # ── Marathi Cases ──
    ("MR-Idiomatic 1", "चोर पोलिसांच्या डोळ्यात धूळ फेकून अंधारात पसार झाला.", "mr"),
    ("MR-Literal 1", "वादळाच्या वाऱ्यामुळे डोळ्यात धूळ उडून डोळे लाल झाले.", "mr"),
    ("MR-Idiomatic 2", "दुष्काळावर मात करण्यासाठी ग्रामस्थांनी एकदिलाने कंबर कसली.", "mr"),
    ("MR-Idiomatic 3", "शेतकऱ्याने रक्ताचे पाणी करून शेतात सोन्यासारखे पीक पिकवले.", "mr"),
    ("MR-Literal 3", "वैद्यकीय प्रयोगशाळेत रक्ताचे नमुने पाण्यात विरघळवून चाचणी केली.", "mr"),
    ("MR-Negative", "ग्रंथालयाने वाचकांसाठी आधुनिक मराठी साहित्य उपलब्ध करून दिले आहे.", "mr"),
]


def run_verification():
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

    print("=" * 85)
    print(" VERIFYING MULTILINGUAL PREDICTIONS & CONTEXT-AWARENESS (EN + HI + MR)")
    print("=" * 85)

    for label, sent, lang in test_sentences:
        res = analyze_sentence(sent, model_type="contextual", language=lang)
        print(f"\n[{label}] ({lang.upper()})")
        print(f"  Sentence:    \"{sent}\"")
        print(f"  Expression:  {res.get('detected_expression')}")
        print(f"  Usage Class: {res.get('usage')}")
        print(f"  Confidence:  {res.get('confidence')}%")
        print(f"  Meaning:     {res.get('meaning')}")
        print(f"  Explanation: {res.get('explanation')}")
        print(f"  Probabilities: {res.get('probabilities')}")

    print("\n" + "=" * 85)
    print(" MULTILINGUAL VERIFICATION COMPLETED")
    print("=" * 85)


if __name__ == "__main__":
    run_verification()
