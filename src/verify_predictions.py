"""
Verification Script for Testing Benchmark Predictions and Context Awareness
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from predict import analyze_sentence

test_sentences = [
    # Specific Requested Cases
    ("Specific Case 1 (Idiomatic)", "Rahul was feeling under the weather."),
    ("Specific Case 2 (No Idiom)", "The weather was terrible yesterday."),
    ("Specific Case 3 (Literal)", "The child was sitting under the weather shelter."),
    ("Specific Case 4 (Idiomatic)", "The teacher said I had hit the nail on the head."),
    
    # Context-Aware Contrast Pairs (Testing genuine context usage)
    ("Contrast Pair 1A (Idiomatic)", "After the presentation, the teacher said I had hit the nail on the head."),
    ("Contrast Pair 1B (Literal)", "The carpenter swung the hammer to hit the nail on the head."),
    ("Contrast Pair 2A (Idiomatic)", "We planned a surprise party, but her brother spilled the beans."),
    ("Contrast Pair 2B (Literal)", "The toddler knocked over the pantry container and spilled the beans on the floor."),
    ("Contrast Pair 3A (Idiomatic)", "The final calculus exam turned out to be a piece of cake."),
    ("Contrast Pair 3B (Literal)", "She offered her guest a delicious sweet piece of cake.")
]

print("=" * 85)
print(" VERIFYING PREDICTIONS AND CONTEXT-AWARENESS")
print("=" * 85)

for label, sent in test_sentences:
    res = analyze_sentence(sent, model_type="contextual")
    print(f"\n[{label}]")
    print(f"  Sentence:    \"{sent}\"")
    print(f"  Expression:  {res.get('detected_expression')}")
    print(f"  Usage Class: {res.get('usage')}")
    print(f"  Confidence:  {res.get('confidence')}%")
    print(f"  Meaning:     {res.get('meaning')}")
    print(f"  Explanation: {res.get('explanation')}")
    print(f"  Probabilities: {res.get('probabilities')}")

print("\n" + "=" * 85)
