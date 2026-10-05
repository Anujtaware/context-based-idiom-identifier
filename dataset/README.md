# Idiom NLP Benchmark Dataset

## Overview
This benchmark dataset is curated specifically for the **Context-Based Idiom Meaning Identifier Using NLP** project. It contains labeled sentences for identifying whether a recognized idiom candidate is being used in an **idiomatic**, **literal**, or **none** context.

## Schema & Attributes
The dataset is stored in `dataset/idioms.csv` with the following columns:

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Unique identifier for each sample record. |
| `sentence` | String | Complete English input sentence containing the target phrase or context. |
| `idiom` | String | Canonical idiom expression or `none` if absent. |
| `meaning` | String | Figurative dictionary meaning of the idiom. |
| `usage_type` | Categorical | Usage classification: `idiomatic`, `literal`, or `none`. |
| `context` | String | Contextual domain / scenario description (e.g. academic, medical, carpentry). |
| `example` | String | Canonical usage example illustrating standard figurative use. |

## Dataset Statistics
- **Total Samples**: 320
- **Supported Target Idioms**: 30 canonical expressions
- **Class Distribution**:
  - `idiomatic`: 180 samples (56.25%)
  - `literal`: 120 samples (37.50%)
  - `none`: 20 samples (6.25%)

## Supported Idioms List
1. `break the ice`
2. `piece of cake`
3. `once in a blue moon`
4. `hit the nail on the head`
5. `spill the beans`
6. `under the weather`
7. `cost an arm and a leg`
8. `bite the bullet`
9. `let the cat out of the bag`
10. `beat around the bush`
11. `blessing in disguise`
12. `burn the midnight oil`
13. `call it a day`
14. `on cloud nine`
15. `pull someone's leg`
16. `raining cats and dogs`
17. `a dime a dozen`
18. `kill two birds with one stone`
19. `barking up the wrong tree`
20. `elephant in the room`
21. `best of both worlds`
22. `add fuel to the fire`
23. `cut corners`
24. `get cold feet`
25. `go the extra mile`
26. `jump on the bandwagon`
27. `miss the boat`
28. `speak of the devil`
29. `through thick and thin`
30. `hit the sack`

## Data Split Methodology
- **Stratified Split**: 80% Training (`train_set`), 20% Testing (`test_set`).
- **Reproducibility**: Fixed random seed (`random_state=42`) with stratification on `usage_type`.
- **Integrity**: Zero test leakage into training pipelines or feature transformers.
