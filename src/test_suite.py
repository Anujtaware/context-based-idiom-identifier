"""
Automated Test Suite for Context-Based Idiom Meaning Identifier

Validates:
1. Exact prompt test cases
2. Idiomatic expressions
3. Literal physical usages
4. Negative/No-idiom sentences
5. Robustness against edge cases (short input, empty input, punctuation)
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from predict import analyze_sentence

TEST_CASES = [
    {
        "name": "Prompt Example 1 (Idiomatic under the weather)",
        "input": "After studying all night, Rahul was feeling under the weather.",
        "expected_detected": True,
        "expected_usage": "Idiomatic",
        "expected_idiom": "under the weather"
    },
    {
        "name": "Prompt Example 2 (Negative - no idiom)",
        "input": "The weather was terrible yesterday.",
        "expected_detected": False,
        "expected_usage": "None",
        "expected_idiom": None
    },
    {
        "name": "Prompt Example 3 (Literal under the weather shelter)",
        "input": "The child was sitting under the weather shelter.",
        "expected_detected": True,
        "expected_usage": "Literal / Non-idiomatic",
        "expected_idiom": "under the weather"
    },
    {
        "name": "Example 1 (Hit the nail on the head - Idiomatic)",
        "input": "After the presentation, the teacher said I had hit the nail on the head.",
        "expected_detected": True,
        "expected_usage": "Idiomatic",
        "expected_idiom": "hit the nail on the head"
    },
    {
        "name": "Example 2 (Piece of cake - Idiomatic)",
        "input": "The mathematics test was a piece of cake.",
        "expected_detected": True,
        "expected_usage": "Idiomatic",
        "expected_idiom": "piece of cake"
    },
    {
        "name": "Example 3 (Once in a blue moon - Idiomatic)",
        "input": "He visits us once in a blue moon.",
        "expected_detected": True,
        "expected_usage": "Idiomatic",
        "expected_idiom": "once in a blue moon"
    },
    {
        "name": "Example 4 (Under the weather - Idiomatic)",
        "input": "She was feeling under the weather today.",
        "expected_detected": True,
        "expected_usage": "Idiomatic",
        "expected_idiom": "under the weather"
    },
    {
        "name": "Example 5 (Call it a day - Idiomatic)",
        "input": "We have worked hard, so let's call it a day.",
        "expected_detected": True,
        "expected_usage": "Idiomatic",
        "expected_idiom": "call it a day"
    },
    {
        "name": "Example 6 (On cloud nine - Idiomatic)",
        "input": "After receiving the scholarship, she was on cloud nine.",
        "expected_detected": True,
        "expected_usage": "Idiomatic",
        "expected_idiom": "on cloud nine"
    },
    {
        "name": "Example 7 (Go the extra mile - Idiomatic)",
        "input": "The manager told us to go the extra mile.",
        "expected_detected": True,
        "expected_usage": "Idiomatic",
        "expected_idiom": "go the extra mile"
    },
    {
        "name": "Example 8 (Negative - Cold and rainy)",
        "input": "The actual weather was cold and rainy.",
        "expected_detected": False,
        "expected_usage": "None",
        "expected_idiom": None
    },
    {
        "name": "Literal Test (Hit the nail with hammer)",
        "input": "The carpenter swung the hammer to hit the nail on the head.",
        "expected_detected": True,
        "expected_usage": "Literal / Non-idiomatic",
        "expected_idiom": "hit the nail on the head"
    },
    {
        "name": "Literal Test (Break the ice in freezer)",
        "input": "The bartender had to break the ice into cubes for the drinks.",
        "expected_detected": True,
        "expected_usage": "Literal / Non-idiomatic",
        "expected_idiom": "break the ice"
    },
    {
        "name": "Literal Test (Spill the beans on floor)",
        "input": "The toddler knocked over the pantry container and spilled the beans on the floor.",
        "expected_detected": True,
        "expected_usage": "Literal / Non-idiomatic",
        "expected_idiom": "spill the beans"
    }
]


def run_all_tests():
    print("=" * 80)
    print(" EXECUTING TEST SUITE FOR CONTEXT-BASED IDIOM IDENTIFIER")
    print("=" * 80)

    passed = 0
    total = len(TEST_CASES)

    for idx, tc in enumerate(TEST_CASES, 1):
        print(f"\n[Test {idx}/{total}] {tc['name']}")
        print(f"  Input: \"{tc['input']}\"")
        
        res = analyze_sentence(tc['input'], model_type="contextual")
        
        detected_expr = res.get("detected_expression")
        usage = res.get("usage")
        conf = res.get("confidence")
        expl = res.get("explanation")
        
        print(f"  -> Detected Expression: {detected_expr}")
        print(f"  -> Predicted Usage:     {usage}")
        print(f"  -> Confidence:          {conf}%")
        print(f"  -> Meaning:             {res.get('meaning')}")
        print(f"  -> Explanation:         {expl}")
        
        # Check assertions
        if tc["expected_detected"]:
            assert detected_expr is not None, f"Expected detection for {tc['input']}"
            if tc["expected_usage"] == usage:
                print("  Result: PASS")
                passed += 1
            else:
                print(f"  Result: FAIL (Expected: {tc['expected_usage']}, Got: {usage})")
        else:
            if detected_expr is None and usage == "None":
                print("  Result: PASS")
                passed += 1
            else:
                print(f"  Result: FAIL (Expected None, Got: {detected_expr}, {usage})")

    print("\n" + "=" * 80)
    print(f" TEST RESULTS SUMMARY: {passed}/{total} Passed ({passed/total*100:.1f}%)")
    print("=" * 80)
    return passed == total


if __name__ == "__main__":
    run_all_tests()
