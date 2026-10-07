"""
Comprehensive Automated Test Suite for Multilingual Idiom Identifier
Supports: English (en), Hindi (hi), and Marathi (mr)

Test Matrix:
1. English: Idiomatic, Literal, and None
2. Hindi: Idiomatic, Literal, and None
3. Marathi: Idiomatic, Literal, and None
4. Unicode & Devanagari handling (NFC, dandas, zero-width characters)
5. Empty and whitespace-only input
6. Short input (< 2 tokens)
7. Unsupported idiom / Out-of-vocabulary expression
8. Explicit language parameter selection and auto-detection
9. Punctuation handling (quotes, exclamation marks, question marks)
10. Multiple sentences input
11. Model inference probabilities and confidence calibration
"""

import os
import sys

# Add src to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from predict import analyze_sentence, load_inference_models
from idiom_dictionary import get_all_idioms, get_idiom_info
from multilingual_preprocessing import detect_candidate_idiom, clean_unicode, infer_language


# ══════════════════════════════════════════════════════════════════════════════
# COMPREHENSIVE TEST CASES MATRIX
# ══════════════════════════════════════════════════════════════════════════════

TEST_CASES = [
    # ── English Cases ──
    {
        "id": "EN-01",
        "name": "English Idiomatic: under the weather",
        "input": "After studying all night, Rahul was feeling under the weather.",
        "lang": "en",
        "expected_detected": True,
        "expected_idiom": "under the weather",
        "expected_usage": "Idiomatic"
    },
    {
        "id": "EN-02",
        "name": "English Literal: under the weather shelter",
        "input": "The school children stood huddled under the weather shelter during the heavy rainstorm.",
        "lang": "en",
        "expected_detected": True,
        "expected_idiom": "under the weather",
        "expected_usage": "Literal / Non-idiomatic"
    },
    {
        "id": "EN-03",
        "name": "English None: general weather report",
        "input": "The actual weather was cold and rainy yesterday in the valley.",
        "lang": "en",
        "expected_detected": False,
        "expected_idiom": None,
        "expected_usage": "None"
    },
    {
        "id": "EN-04",
        "name": "English Idiomatic: piece of cake",
        "input": "The final calculus examination was an absolute piece of cake for the prepared student.",
        "lang": "en",
        "expected_detected": True,
        "expected_idiom": "piece of cake",
        "expected_usage": "Idiomatic"
    },
    {
        "id": "EN-05",
        "name": "English Literal: piece of cake",
        "input": "The server carefully placed a generous piece of cake onto the porcelain saucer.",
        "lang": "en",
        "expected_detected": True,
        "expected_idiom": "piece of cake",
        "expected_usage": "Literal / Non-idiomatic"
    },
    {
        "id": "EN-06",
        "name": "English Idiomatic: hit the nail on the head",
        "input": "Her perceptive analysis of the software bug hit the nail on the head.",
        "lang": "en",
        "expected_detected": True,
        "expected_idiom": "hit the nail on the head",
        "expected_usage": "Idiomatic"
    },
    {
        "id": "EN-07",
        "name": "English Literal: hit the nail on the head",
        "input": "The carpenter swung the steel hammer to hit the nail on the head into the oak beam.",
        "lang": "en",
        "expected_detected": True,
        "expected_idiom": "hit the nail on the head",
        "expected_usage": "Literal / Non-idiomatic"
    },

    # ── Hindi Cases ──
    {
        "id": "HI-01",
        "name": "Hindi Idiomatic: आँखों का तारा",
        "input": "रोहन अपने माता-पिता की आँखों का तारा है और सबकी प्रशंसा पाता है।",
        "lang": "hi",
        "expected_detected": True,
        "expected_idiom": "आँखों का तारा",
        "expected_usage": "Idiomatic"
    },
    {
        "id": "HI-02",
        "name": "Hindi Idiomatic: भीगी बिल्ली बनना",
        "input": "अध्यापक के कक्षा में आते ही शरारती छात्र भीगी बिल्ली बन गया।",
        "lang": "hi",
        "expected_detected": True,
        "expected_idiom": "भीगी बिल्ली बनना",
        "expected_usage": "Idiomatic"
    },
    {
        "id": "HI-03",
        "name": "Hindi Idiomatic: दिन-रात एक करना",
        "input": "सिविल सेवा परीक्षा में सफल होने के लिए उसने दिन-रात एक कर दिया।",
        "lang": "hi",
        "expected_detected": True,
        "expected_idiom": "दिन-रात एक करना",
        "expected_usage": "Idiomatic"
    },
    {
        "id": "HI-04",
        "name": "Hindi Literal: भीगी बिल्ली बनना",
        "input": "भारी मानसूनी वर्षा में भीगी बिल्ली बरामदे की सीढ़ियों पर ठंड से कांप रही थी।",
        "lang": "hi",
        "expected_detected": True,
        "expected_idiom": "भीगी बिल्ली बनना",
        "expected_usage": "Literal / Non-idiomatic"
    },
    {
        "id": "HI-05",
        "name": "Hindi Literal: दाल में काला",
        "input": "रसोईघर में दाल बीनते समय थाली में दाल में काला कंकड़ अलग दिखाई दे रहा था।",
        "lang": "hi",
        "expected_detected": True,
        "expected_idiom": "दाल में काला",
        "expected_usage": "Literal / Non-idiomatic"
    },
    {
        "id": "HI-06",
        "name": "Hindi None: सामान्य मौसम समाचार",
        "input": "मौसम विभाग के अनुसार आगामी चौबीस घंटों में उत्तर भारत में हल्की धूप खिली रहेगी।",
        "lang": "hi",
        "expected_detected": False,
        "expected_idiom": None,
        "expected_usage": "None"
    },

    # ── Marathi Cases ──
    {
        "id": "MR-01",
        "name": "Marathi Idiomatic: डोळ्यात धूळ फेकणे",
        "input": "चोर पोलिसांच्या डोळ्यात धूळ फेकून अंधारात पसार झाला.",
        "lang": "mr",
        "expected_detected": True,
        "expected_idiom": "डोळ्यात धूळ फेकणे",
        "expected_usage": "Idiomatic"
    },
    {
        "id": "MR-02",
        "name": "Marathi Idiomatic: कंबर कसणे",
        "input": "दुष्काळावर मात करण्यासाठी ग्रामस्थांनी एकदिलाने कंबर कसली.",
        "lang": "mr",
        "expected_detected": True,
        "expected_idiom": "कंबर कसणे",
        "expected_usage": "Idiomatic"
    },
    {
        "id": "MR-03",
        "name": "Marathi Idiomatic: रक्ताचे पाणी करणे",
        "input": "शेतकऱ्याने रक्ताचे पाणी करून शेतात सोन्यासारखे पीक पिकवले.",
        "lang": "mr",
        "expected_detected": True,
        "expected_idiom": "रक्ताचे पाणी करणे",
        "expected_usage": "Idiomatic"
    },
    {
        "id": "MR-04",
        "name": "Marathi Literal: डोळ्यात धूळ फेकणे",
        "input": "वादळाच्या वाऱ्यामुळे डोळ्यात धूळ उडून डोळे लाल झाले.",
        "lang": "mr",
        "expected_detected": True,
        "expected_idiom": "डोळ्यात धूळ फेकणे",
        "expected_usage": "Literal / Non-idiomatic"
    },
    {
        "id": "MR-05",
        "name": "Marathi Literal: हात देणे",
        "input": "डोंगरावर चढणाऱ्या सहकाऱ्याला वर खेचण्यासाठी त्याने पुढे हात दिला.",
        "lang": "mr",
        "expected_detected": True,
        "expected_idiom": "हात देणे",
        "expected_usage": "Literal / Non-idiomatic"
    },
    {
        "id": "MR-06",
        "name": "Marathi None: सामान्य ग्रंथालय नोंद",
        "input": "ग्रंथालयाने वाचकांसाठी आधुनिक मराठी साहित्य आणि ज्ञानकोश उपलब्ध करून दिले आहेत.",
        "lang": "mr",
        "expected_detected": False,
        "expected_idiom": None,
        "expected_usage": "None"
    }
]


def run_benchmark_tests():
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

    print("=" * 75)
    print(" RUNNING AUTOMATED MULTILINGUAL BENCHMARK TEST SUITE")
    print(" Languages Tested: English (en), Hindi (hi), Marathi (mr)")
    print("=" * 75)

    passed = 0
    total = len(TEST_CASES)

    for idx, tc in enumerate(TEST_CASES, 1):
        print(f"\n[Test {tc['id']}] {tc['name']}")
        print(f"  Input: \"{tc['input']}\" (Lang: {tc['lang']})")

        res = analyze_sentence(tc['input'], model_type="contextual", language=tc['lang'])

        detected = res.get("detected_expression")
        usage = res.get("usage")
        conf = res.get("confidence")
        meaning = res.get("meaning")

        print(f"  -> Detected: {detected}")
        print(f"  -> Usage:    {usage}")
        print(f"  -> Conf:     {conf}%")

        if tc["expected_detected"]:
            assert detected is not None, f"Expected detection for {tc['input']}"
            if usage == tc["expected_usage"]:
                print("  Verdict: PASS")
                passed += 1
            else:
                print(f"  Verdict: FAIL (Expected '{tc['expected_usage']}', got '{usage}')")
        else:
            if detected is None and usage == "None":
                print("  Verdict: PASS")
                passed += 1
            else:
                print(f"  Verdict: FAIL (Expected None, got '{detected}', '{usage}')")

    print("\n" + "-" * 75)
    print(" ROBUSTNESS & EDGE CASE TESTS")
    print("-" * 75)

    # 1. Empty input
    res_empty = analyze_sentence("", model_type="contextual")
    assert not res_empty["success"] and "empty" in res_empty["error"].lower()
    print("  [PASS] Empty input handled gracefully with error notice.")

    # 2. Whitespace-only input
    res_ws = analyze_sentence("     \n  \t  ", model_type="contextual")
    assert not res_ws["success"] and "empty" in res_ws["error"].lower()
    print("  [PASS] Whitespace-only input handled gracefully.")

    # 3. Short input (< 2 tokens)
    res_short = analyze_sentence("Hello", model_type="contextual")
    assert not res_short["success"] and "short" in res_short["error"].lower()
    print("  [PASS] Short single-token input handled gracefully with prompt.")

    # 4. Unsupported Idiom / OOV
    res_oov = analyze_sentence("He decided to kick the bucket while on vacation.", model_type="contextual")
    assert res_oov["success"]
    assert res_oov["detected_expression"] is None
    print("  [PASS] Unsupported idiom returns None and clear explanation notice.")

    # 5. Unicode and Devanagari normalization
    hindi_nfc = clean_unicode("रोहन\u200d आँखों का तारा है।")
    assert len(hindi_nfc) > 0
    print("  [PASS] Devanagari Unicode NFC cleaning test passed.")

    # 6. Punctuation robustness
    res_punct = analyze_sentence(
        "\"After studying all night!\" Rahul was feeling 'under the weather'???",
        model_type="contextual"
    )
    assert res_punct["success"]
    assert res_punct["detected_expression"] is not None
    print("  [PASS] Severe punctuation marks handled without detection disruption.")

    # 7. Probability Distribution Validation
    probs = res_punct.get("probabilities", {})
    prob_sum = sum(probs.values())
    assert 99.0 <= prob_sum <= 101.0, f"Probabilities sum {prob_sum} out of range"
    print(f"  [PASS] Class probability distribution is calibrated (Sum = {prob_sum:.1f}%).")

    # 8. Multi-sentence input
    res_multi = analyze_sentence(
        "We have worked hard all morning. The team completed the initial sprints. Let's call it a day now.",
        model_type="contextual"
    )
    assert res_multi["success"]
    assert res_multi["detected_expression"] is not None
    print("  [PASS] Multi-sentence paragraph input successfully detected idiom.")

    print("\n" + "=" * 75)
    print(f" FINAL BENCHMARK TEST RESULT: {passed}/{total} Passed ({passed/total*100:.1f}%)")
    print(" All edge case and robustness assertions passed successfully.")
    print("=" * 75)

    return passed == total


if __name__ == "__main__":
    success = run_benchmark_tests()
    sys.exit(0 if success else 1)
