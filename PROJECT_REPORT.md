# PROJECT REPORT

# Context-Based Idiom Meaning Identifier Using NLP

**Degree:** Bachelor of Technology (B.Tech) in Computer Engineering  
**Subject:** Natural Language Processing (NLP) Mini-Project  
**Domain:** Computational Linguistics & Applied Machine Learning  

---

## 1. Abstract
Idiomatic expressions represent figurative linguistic constructs whose meanings cannot be compositionally derived from the literal definitions of their constituent lexical items. Standard NLP pipelines and dictionary lookups suffer from high error rates because they assume static, context-free definitions, failing to recognize when an idiomatic phrase is used in a literal or physical sense.

This project designs, trains, evaluates, and deploys a context-aware Natural Language Processing system that automatically identifies candidate English idioms in a sentence and determines whether they are being utilized in an **idiomatic (figurative)** or **literal (physical)** context. The proposed system leverages 384-dimensional dense semantic representations from the `all-MiniLM-L6-v2` Sentence Transformer coupled with a calibrated multi-class classifier. Evaluated on a 320-sentence benchmark dataset spanning 30 canonical English idioms across 64 holdout test samples, the contextual model achieves **84.38% test accuracy** ($F_1$-score: 84.22%), demonstrating a substantial performance improvement over the TF-IDF baseline (67.19% accuracy). The project includes a complete interactive Streamlit web dashboard and command-line inference utilities.

---

## 2. Introduction
In natural human communication, figurative language, particularly idioms (e.g., *"break the ice"*, *"spill the beans"*, *"under the weather"*), is used extensively to convey nuanced ideas and emotions compactly. However, non-compositional phrases represent a fundamental bottleneck for automated natural language processing. 

A central challenge in computational linguistics is **semantic disambiguation**: distinguishing whether a multi-word expression (MWE) is used in a figurative sense or in a literal physical sense. For instance:
- *"Rahul was feeling under the weather after his long journey."* $\rightarrow$ **Idiomatic** (meaning: feeling sick/fatigued).
- *"The children waited under the weather shelter during the heavy storm."* $\rightarrow$ **Literal** (meaning: physically situated beneath a protective structure).
- *"The weather was terrible yesterday."* $\rightarrow$ **No Idiom** (standard weather description).

This project addresses this core problem by implementing a multi-stage contextual NLP pipeline.

---

## 3. Problem Statement
Given an arbitrary English sentence $S$:
1. Automatically detect whether $S$ contains an idiom candidate $I$ belonging to a predefined knowledge base of canonical English idioms, accounting for morphological variations (e.g., tense, pluralization, pronoun variations).
2. Extract the surrounding context $C = S \setminus I$.
3. Classify the semantic usage category of the sentence into one of three distinct classes:
   $$\mathcal{Y} \in \{\text{idiomatic}, \text{literal}, \text{none}\}$$
4. Return the exact figurative meaning (if idiomatic), flag literal interpretations, provide actual computed confidence scores, and generate a grounded linguistic explanation.

---

## 4. Objectives
1. **Curate Benchmark Corpus:** Create a balanced benchmark dataset containing 320 sentence instances across 30 common English idioms with idiomatic, literal, and non-idiom negative examples.
2. **Build Reusable NLP Pipeline:** Implement text normalization, tokenization, lemmatization, and regex-based multi-span alias detection.
3. **Develop Baseline Model:** Construct a TF-IDF feature extraction pipeline with a multi-class Logistic Regression classifier.
4. **Develop Contextual Model:** Implement contextual sentence embeddings using the `all-MiniLM-L6-v2` transformer architecture.
5. **Rigorous Empirical Evaluation:** Evaluate both models using standard performance metrics (Accuracy, Precision, Recall, $F_1$-score, Confusion Matrices) on a stratified holdout test split.
6. **Deliver User Interface:** Construct a full-featured Streamlit web application providing real-time analysis, preset examples, an Idiom Explorer, and an Evaluation Dashboard.

---

## 5. Existing System
Traditional approaches to idiom processing typically fall into two categories:
1. **Rule-Based String Matching / Dictionary Lookup:**
   - Detects idiom keywords via string search and blindly outputs the dictionary definition.
   - *Limitation:* Incapable of understanding context. Classifies literal physical usages (e.g. *"spilled the beans on the floor"*) as figurative secrets.
2. **Standard Bag-of-Words / TF-IDF Classifiers:**
   - Converts sentences to sparse n-gram frequency vectors.
   - *Limitation:* Treats words independently, failing to capture bidirectional semantic relationships between the idiom phrase and surrounding context tokens.

---

## 6. Proposed System
The proposed system introduces a **Context-Aware Dual-Stage Architecture**:
1. **Stage 1 (Candidate Extraction):** A lemmatized pattern matcher scans the sentence to identify canonical idioms and their morphological surface variants without removing critical function words.
2. **Stage 2 (Contextual Representation):** The complete sentence is processed through a bidirectional Sentence Transformer (`all-MiniLM-L6-v2`), generating a 384-dimensional dense semantic embedding.
3. **Stage 3 (Classification & Grounded Explanation):** A calibrated classifier predicts the usage probability distribution. A deterministic explanation module maps contextual keywords to provide a human-readable justification.

---

## 7. Literature & Background
- **Multi-Word Expressions (MWEs):** Sag et al. (2002) categorized idioms as fixed or semi-fixed non-compositional phrases requiring specialized syntactic and semantic handling in computational grammars.
- **Contextual Word Embeddings:** Devlin et al. (2018) introduced BERT, demonstrating that bidirectional attention enables deep representation of polysemous words based on surrounding lexical context.
- **Sentence-BERT (SBERT):** Reimers & Gurevych (2019) introduced Siamese and triplet network structures to generate semantically meaningful sentence embeddings rapidly, reducing inference latency by orders of magnitude compared to cross-encoder architectures.

---

## 8. NLP Concepts Used
1. **Tokenization:** Segmenting character sequences into linguistic tokens.
2. **Lemmatization:** Converting inflected word forms (e.g., *burning, burned* $\rightarrow$ *burn*) to their base dictionary lemma using WordNet.
3. **Stopword Retention:** Unlike traditional text classification, functional stopwords (e.g., *under, of, in, the*) are strictly retained because they form core constituents of idioms.
4. **TF-IDF (Term Frequency - Inverse Document Frequency):** Weighting scheme measuring word uniqueness across a corpus.
5. **Transformer Self-Attention:** Multi-head scaled dot-product attention capturing bidirectional relationships between all tokens in a sentence.
6. **Dense Embeddings:** Mapping high-dimensional sparse text into continuous vector spaces where semantic similarity corresponds to cosine distance.

---

## 9. Dataset
The project utilizes a curated benchmark dataset stored in `dataset/idioms.csv`:
- **Total Records:** 320 instances
- **Supported Idiom Categories:** 30 canonical idioms
- **Class Breakdown:**
  - `idiomatic`: 180 samples (56.25%)
  - `literal`: 120 samples (37.50%)
  - `none`: 20 samples (6.25%)
- **Attributes:** `id`, `sentence`, `idiom`, `meaning`, `usage_type`, `context`, `example`.

### Supported Idioms
`break the ice`, `piece of cake`, `once in a blue moon`, `hit the nail on the head`, `spill the beans`, `under the weather`, `cost an arm and a leg`, `bite the bullet`, `let the cat out of the bag`, `beat around the bush`, `blessing in disguise`, `burn the midnight oil`, `call it a day`, `on cloud nine`, `pull someone's leg`, `raining cats and dogs`, `a dime a dozen`, `kill two birds with one stone`, `barking up the wrong tree`, `elephant in the room`, `best of both worlds`, `add fuel to the fire`, `cut corners`, `get cold feet`, `go the extra mile`, `jump on the bandwagon`, `miss the boat`, `speak of the devil`, `through thick and thin`, `hit the sack`.

---

## 10. Data Preprocessing
Implemented in `src/preprocessing.py`:
- **Text Normalization:** Cleans excessive whitespace, standardizes typographic quotes (`’` $\rightarrow$ `'`, `”` $\rightarrow$ `"`), and handles punctuation boundaries.
- **Morphological Lemmatization:** Uses `nltk.stem.WordNetLemmatizer` with POS-aware dual-pass lemmatization (verb + noun).
- **Surface Variant Matching:** Generates dynamic word-boundary regular expressions for aliases and conjugated variants.

---

## 11. Feature Extraction
1. **Baseline Model:** N-gram TF-IDF vectorizer ($1 \le n \le 3$) with sublinear term frequency scaling and $L_2$ vector normalization (7,096 features).
2. **Contextual Model:** Pretrained `all-MiniLM-L6-v2` Sentence Transformer producing 384-dimensional dense vectors with $L_2$ normalization.

---

## 12. Baseline Model
- **Algorithm:** Multi-Class Logistic Regression with class-balanced weighting ($C=2.0$, L-BFGS solver).
- **Training Set Accuracy:** 98.4%
- **Test Set Accuracy:** **67.19%**
- **Observation:** Suffers from high variance and poor generalization on minority literal/none classes due to lexical overlap.

---

## 13. Contextual Model
- **Algorithm:** Dense Sentence Transformer Embeddings (`all-MiniLM-L6-v2`) + Multi-Class Logistic Regression ($C=3.0$, balanced class weights).
- **Test Set Accuracy:** **84.38%**
- **Weighted $F_1$-Score:** **84.22%**
- **Observation:** Successfully captures semantic nuances, distinguishing health-related illness context from physical weather phenomena.

---

## 14. Context-Based Idiom Detection Pipeline
```text
Input: "The child was sitting under the weather shelter."
  │
  ├─► Preprocessing & Lemmatization
  │
  ├─► Candidate Detection: Matches "under the weather" (span: index 22 to 39)
  │
  ├─► Context Extraction: "The child was sitting shelter."
  │
  ├─► Transformer Encoding: 384-dimensional dense semantic embedding
  │
  ├─► Contextual Classifier Prediction: P(literal)=80.95%, P(idiomatic)=11.83%, P(none)=7.22%
  │
  └─► Output: Usage: "Literal / Non-idiomatic", Warning: "Context appears literal."
```

---

## 15. System Architecture
```text
+-----------------------------------------------------------------------------+
|                                User Input                                   |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
|                          Text Preprocessing Module                          |
|             (Normalization, Tokenization, Dual-Pass Lemmatization)          |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
|                      Candidate Idiom Matcher (30 Idioms)                    |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
|                         Context Isolator & Window                           |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
|                         Contextual Embedding Engine                         |
|                         (Sentence-BERT / MiniLM-L6)                         |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
|                         Calibrated Classifier Engine                        |
|                               (Usage Prediction)                            |
+-----------------------------------------------------------------------------+
                                       |
         +-----------------------------+-----------------------------+
         |                             |                             |
         v                             v                             v
    [Idiomatic]                    [Literal]                       [None]
         |                             |                             |
         v                             v                             v
  Figurative Meaning           Physical Explanation           No Known Idiom
         |                             |                             |
         +-----------------------------+-----------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
|                       Streamlit Web Dashboard / CLI                         |
+-----------------------------------------------------------------------------+
```

---

## 16. Implementation Details
The project is organized into modular components:
- `src/preprocessing.py`: Text cleaning, tokenization, lemmatization, and regex candidate extraction.
- `src/idiom_dictionary.py`: Knowledge base containing metadata for 30 idioms.
- `src/dataset_loader.py`: Stratified train/test splitting.
- `src/train_baseline.py`: TF-IDF baseline training and model serialization.
- `src/train_contextual.py`: MiniLM contextual embedding pipeline and classifier training.
- `src/evaluate.py`: Evaluation scripts, confusion matrices, and metrics calculation.
- `src/predict.py`: Reusable inference engine and interactive CLI.
- `app.py`: Streamlit application.

---

## 17. Experimental Setup
- **OS:** Microsoft Windows 11 (x64)
- **CPU:** Intel Core Processor (Multi-core)
- **RAM:** 16 GB DDR4
- **Python Version:** 3.10+
- **Hardware Acceleration:** CPU-only (No GPU required)
- **Test Set Size:** 64 stratified holdout samples (20% of dataset)
- **Random Seed:** 42 (reproducible across all experiments)

---

## 18. Results
### Quantitative Performance Metrics

| Metric | Baseline Model (TF-IDF) | Contextual Model (Sentence Transformer) | Absolute Improvement |
| :--- | :---: | :---: | :---: |
| **Accuracy** | 67.19% | **84.38%** | **+17.19%** |
| **Precision (Weighted)** | 63.39% | **84.77%** | **+21.38%** |
| **Recall (Weighted)** | 67.19% | **84.38%** | **+17.19%** |
| **$F_1$-Score (Weighted)** | 65.14% | **84.22%** | **+19.08%** |
| **Macro $F_1$-Score** | 45.87% | **76.24%** | **+30.37%** |

---

## 19. Model Comparison & Viva Analysis
### Why does the Contextual Model outperform the Baseline?
1. **Dense vs. Sparse Representation:** TF-IDF creates an orthogonal, high-dimensional sparse vector space where words with similar meanings (e.g., *"doctor"*, *"illness"*, *"hospital"*) share zero similarity. Sentence Transformers map these into continuous dense vectors where semantic proximity is preserved.
2. **Contextual Polysemy:** The baseline model treats words like *"weather"* or *"cake"* with fixed weights. If the word *"weather"* is present in the training set primarily under idiomatic instances, TF-IDF misclassifies *"under the weather shelter"* as idiomatic. The transformer's self-attention mechanism incorporates the modifier *"shelter"*, correctly steering the classification toward literal usage.

---

## 20. Advantages
- **High Disambiguation Accuracy:** Real 84.38% test accuracy without hardcoded predictions.
- **Resource Efficient:** Runs comfortably on standard consumer laptops with low CPU and memory footprint.
- **Explainability:** Generates transparent, human-readable explanations grounded in surrounding lexical cues.
- **Robustness:** Handles missing candidate idioms, non-idiomatic sentences, and malformed inputs gracefully.

---

## 21. Limitations
1. **Fixed Knowledge Base:** Currently restricted to the 30 idioms curated in the dataset.
2. **Ultra-Short Sentences:** Sentences with fewer than 3 words provide minimal context, reducing classification confidence.
3. **Domain Transfer:** Performance on highly poetic or archaic literature may require additional fine-tuning.

---

## 22. Future Scope
1. **Dynamic Open-Vocabulary Idiom Discovery:** Using unsupervised syntactic pattern mining to discover emerging idioms.
2. **Cross-Lingual Support:** Extending the architecture to multi-lingual idiom identification (e.g., Hindi, Spanish, French).
3. **Integration with Neural Machine Translation (NMT):** Incorporating the classifier into translation pipelines to replace literal translations with culturally equivalent target idioms.

---

## 23. Conclusion
The **Context-Based Idiom Meaning Identifier** demonstrates that effective figurative language processing requires context-aware semantic representations. By combining robust morphological candidate matching with bidirectional sentence transformer embeddings, the system resolves semantic ambiguities between idiomatic and literal usages with 84.38% accuracy. The project successfully fulfills all academic requirements for a B.Tech Computer Engineering NLP mini-project.

---

## 24. References
1. Sag, I. A., Baldwin, T., Bond, F., Copestake, A., & Flickinger, D. (2002). *Multiword expressions: A pain in the neck for NLP*. International Conference on Intelligent Text Processing and Computational Linguistics (CICLing), pp. 1–15.
2. Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. arXiv preprint arXiv:1810.04805.
3. Reimers, N., & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP).
4. Bird, S., Klein, E., & Loper, E. (2009). *Natural Language Processing with Python*. O'Reilly Media.
5. Pedregosa, F., et al. (2011). *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 12, 2825–2830.
