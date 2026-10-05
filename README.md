# Context-Based Idiom Meaning Identifier Using NLP

> **Academic Level:** B.Tech Computer Engineering Mini-Project / Viva Project  
> **Core Concept:** Context $\rightarrow$ Idiom Detection $\rightarrow$ Usage Classification $\rightarrow$ Meaning Mapping

---

## 1. Project Title
**Context-Based Idiom Meaning Identifier Using NLP**

---

## 2. Abstract
Idiomatic expressions represent figurative linguistic constructs whose semantic interpretations cannot be derived compositionally from their individual constituent words. Conventional NLP lookup systems naively map keywords to fixed dictionary definitions, leading to catastrophic misclassifications when phrases are utilized in literal contexts (e.g., *"sitting under the weather shelter"* vs. *"feeling under the weather"*). 

This project implements a complete, end-to-end, real machine learning and Natural Language Processing system that automatically identifies candidate English idioms from input sentences, extracts surrounding contextual cues, and classifies the usage context as **Idiomatic (Figurative)**, **Literal (Physical)**, or **None (No Idiom)**. Using deep bidirectional sentence embeddings from `all-MiniLM-L6-v2` paired with a calibrated classifier, the system achieves **84.38% test accuracy**, significantly outperforming a standard TF-IDF baseline (67.19%). The project features a full interactive Streamlit web dashboard, a CLI prediction interface, and a rich 30-idiom knowledge base.

---

## 3. Problem Statement
Given an arbitrary English sentence $S$:
1. Determine whether $S$ contains an idiom candidate $I$ from a knowledge base of common English idioms.
2. Formulate the surrounding context $C = S \setminus I$.
3. Classify whether $I$ in $S$ operates under an **Idiomatic** usage (figurative sense) or a **Literal** usage (concrete/physical sense).
4. Map the identified expression to its proper contextual meaning, calculate genuine confidence probabilities, and generate a transparent, grounded linguistic explanation.

---

## 4. Motivation
- **Linguistic Ambiguity in NLP:** Figurative language poses significant challenges for downstream NLP tasks such as Machine Translation, Sentiment Analysis, and Automated Text Summarization.
- **Failures of Keyword Matching:** Naive pattern matching fails to distinguish between *"spilled the beans"* (revealing a secret) and *"spilled the beans on the floor"* (dropping legumes).
- **Academic Relevance:** Provides undergraduate engineering students with a practical, explainable, and technically sound demonstration of context-aware NLP architectures using modern transformer embeddings without requiring heavy GPU infrastructure.

---

## 5. Objectives
1. Build a high-quality benchmark dataset of 320 annotated sentences covering 30 common English idioms with idiomatic, literal, and non-idiom negative examples.
2. Develop a clean, modular text preprocessing and candidate extraction pipeline preserving essential functional tokens.
3. Train a TF-IDF + Logistic Regression baseline classifier.
4. Implement a contextual classification pipeline using Sentence Transformers (`all-MiniLM-L6-v2`) embeddings.
5. Provide genuine evaluation metrics (Accuracy, Precision, Recall, F1-Score, Confusion Matrices) without fabricated numbers.
6. Build a modern Streamlit web user interface with interactive prediction, probability distribution analysis, an Idiom Explorer, and an Evaluation Dashboard.

---

## 6. Features
- 🔍 **Context-Aware Disambiguation:** Differentiates figurative vs. literal meanings using surrounding tokens.
- 📚 **30 Supported Canonical Idioms:** Full metadata including categories, canonical examples, context keywords, and historical origins.
- ⚡ **Lightweight CPU-Friendly Inference:** Uses 384-dimensional `all-MiniLM-L6-v2` embeddings (~22.7M parameters) for fast local CPU execution (<20ms per sentence).
- 📊 **Real Probabilistic Confidence:** Reports genuine class probability distributions.
- 💡 **Grounded Explanations:** Explains why specific context words support idiomatic or literal classification.
- 🖥️ **Interactive Web Application:** Built with Streamlit featuring real-time input analysis, preset examples, an Idiom Explorer, and live performance metrics.
- 💻 **Interactive CLI:** Terminal inference script for command-line demonstrations.

---

## 7. Technology Stack
- **Programming Language:** Python 3.10+
- **NLP & Embeddings:** NLTK, Sentence-Transformers (`all-MiniLM-L6-v2`), PyTorch
- **Machine Learning:** Scikit-Learn (Logistic Regression, TF-IDF Vectorizer, Stratified Split, Label Encoding)
- **Data Manipulation:** Pandas, NumPy
- **Model Serialization:** Joblib
- **Data Visualization:** Matplotlib, Seaborn
- **Web Interface:** Streamlit

---

## 8. NLP Techniques
- **Text Normalization:** Whitespace stripping, quotation normalization, lowercasing.
- **Tokenization & Lemmatization:** NLTK WordNetLemmatizer handling verb/noun inflection forms (e.g. *burning* $\rightarrow$ *burn*).
- **Stopword Policy:** Non-destructive token preservation (function words like *under, out, of, in* are retained as critical idiom components).
- **Surface Variant Regex Matching:** Multi-stage boundary regex matching supporting canonical expressions and inflected aliases.
- **Context Feature Extraction:** Window extraction isolating surrounding tokens from the detected idiom span.
- **Contextual Dense Embeddings:** 384-dimensional dense semantic vectors capturing bidirectional sentence semantics.

---

## 9. Dataset
The benchmark dataset is located at `dataset/idioms.csv`:
- **Total Samples:** 320 annotated sentences
- **Supported Idioms:** 30 canonical classes
- **Classes:**
  - `idiomatic`: 180 samples (56.25%)
  - `literal`: 120 samples (37.50%)
  - `none`: 20 samples (6.25%)
- **Data Split:** Stratified 80% Train (256 samples) and 20% Test (64 samples) with `random_state=42`.

---

## 10. System Architecture
```text
User Input Sentence
       │
       ▼
Text Preprocessing & Normalization
       │
       ▼
Candidate Idiom Detection (Aliases & Lemmatization)
       │
       ▼
Context Extraction (Surrounding Words)
       │
       ▼
Contextual Classifier (Sentence Transformer + Classifier)
       │
 ┌─────┴─────────────────────┬─────────────────────┐
 │                           │                     │
 ▼                           ▼                     ▼
[Idiomatic]              [Literal]              [None]
 │                           │                     │
 ▼                           ▼                     ▼
Figurative Meaning      Literal Warning     No Idiom Detected
 │                           │                     │
 └───────────────────────────┼─────────────────────┘
                             │
                             ▼
               Confidence Score + Grounded Explanation
```

---

## 11. Baseline Methodology
- **Pipeline:** Raw Sentence $\rightarrow$ Token Normalization $\rightarrow$ Sublinear TF-IDF (1-to-3 n-grams) $\rightarrow$ Balanced Multi-class Logistic Regression.
- **Limitation:** TF-IDF relies on bag-of-words frequencies and lacks deep semantic comprehension of surrounding context. For example, the presence of the word *"weather"* biases TF-IDF toward literal interpretation regardless of figurative phrases.

---

## 12. Contextual Methodology
- **Pipeline:** Complete Sentence $\rightarrow$ Pretrained `all-MiniLM-L6-v2` Transformer $\rightarrow$ 384-dimensional dense contextual vector $\rightarrow$ Calibrated Logistic Regression Classifier.
- **Advantage:** Self-attention mechanisms model complex dependencies between surrounding context words (e.g., *"studying"*, *"exam"*, *"fever"*, *"hospital"*) and the target phrase, accurately distinguishing figurative health expressions from physical weather structures.

---

## 13. Model Training
Run training from the project root:
```bash
# 1. Train Baseline Model (TF-IDF + Logistic Regression)
python src/train_baseline.py

# 2. Train Contextual Model (Sentence Transformer + Logistic Regression)
python src/train_contextual.py
```

---

## 14. Evaluation
Run evaluation to generate metrics, reports, and confusion matrices:
```bash
python src/evaluate.py
```

---

## 15. Results
Actual evaluated metrics on the 64-sample holdout test set:

| Model | Accuracy | Precision (Weighted) | Recall (Weighted) | F1-Score (Weighted) | Macro F1 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **TF-IDF + Logistic Regression (Baseline)** | 67.19% | 63.39% | 67.19% | 65.14% | 45.87% |
| **Sentence Transformer + Logistic Regression (Contextual)** | **84.38%** | **84.77%** | **84.38%** | **84.22%** | **76.24%** |

- **Confusion Matrices:** Saved in `results/confusion_matrix_baseline.png` and `results/confusion_matrix_contextual.png`.
- **Classification Report:** Saved in `results/classification_report.txt`.

---

## 16. Installation
Clone the repository and install required packages:
```bash
cd context-based-idiom-identifier
pip install -r requirements.txt
```

Download necessary NLTK corpora:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('wordnet'); nltk.download('omw-1.4'); nltk.download('stopwords')"
```

---

## 17. How to Run

### Run Streamlit Web Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### Run Interactive CLI Prediction
```bash
python src/predict.py
```

### Run Automated Test Suite
```bash
python src/test_suite.py
```

---

## 18. Sample Inputs & Outputs

### Test Case 1: Idiomatic Expression
- **Input:** *"After studying all night, Rahul was feeling under the weather."*
- **Detected Expression:** `under the weather`
- **Usage:** `Idiomatic`
- **Meaning:** *Feeling slightly ill, unwell, indisposed, or fatigued.*
- **Confidence:** `78.52%`
- **Explanation:** The surrounding words such as "studying" provide semantic cues in the domain of 'Health & State', supporting an idiomatic interpretation.

### Test Case 2: Literal Expression
- **Input:** *"The child was sitting under the weather shelter."*
- **Detected Expression:** `under the weather`
- **Usage:** `Literal / Non-idiomatic`
- **Meaning:** *Expression 'under the weather' detected, but the context appears literal (physical interpretation).*
- **Confidence:** `80.95%`
- **Explanation:** The presence of physical context words such as "shelter" indicates literal, non-idiomatic usage.

### Test Case 3: No Idiom
- **Input:** *"The weather was terrible yesterday."*
- **Detected Expression:** *None*
- **Usage:** `None`
- **Meaning:** *No known idiom detected in the input sentence.*
- **Confidence:** `53.91%`

---

## 19. Limitations
1. **Vocabulary Coverage:** Supports the 30 idioms curated in the knowledge base; idioms outside this dictionary require dataset expansion.
2. **Ambiguous Inputs:** Extremely brief inputs (e.g., 2-word inputs) lacking contextual tokens may have lower classification confidence.
3. **Prototype Scope:** Designed as an academic NLP system rather than a universal open-domain figurative language parser.

---

## 20. Future Scope
- Expansion to multi-lingual idiom disambiguation (e.g., Hindi, Spanish idioms).
- Few-shot prompt fine-tuning on larger LLMs (e.g. LLaMA-3 / Mistral).
- Integration with real-time translation pipelines to replace naive literal translations with culturally equivalent target language idioms.

---

## 21. Conclusion
The project successfully addresses figurative language disambiguation by combining candidate pattern extraction with bidirectional sentence transformer embeddings. Demonstrating an accuracy improvement from 67.19% (Baseline) to 84.38% (Contextual), the system highlights the paramount role of surrounding semantic context in understanding human language.
