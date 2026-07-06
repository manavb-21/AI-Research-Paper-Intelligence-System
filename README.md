# 🧠 AI Research Paper Intelligence System

An AI-powered research assistant that enables semantic search, intelligent information extraction, and AI-generated synthesis across **15,000+ Machine Learning research papers**.

Built using **FastAPI**, **FAISS**, **Sentence Transformers**, **KeyBERT**, **BERT-based Named Entity Recognition**, **BART-Large-CNN**, and **Streamlit**.

---

## 🚀 Features

- 🔍 **Semantic Search**
  - Dense vector retrieval using Sentence Transformers and FAISS
  - Finds semantically relevant papers instead of relying on keyword matching

- 📚 **Research Paper Intelligence**
  - Searches across 15,000+ Machine Learning papers from the Hugging Face ML-ArXiv dataset

- 🏷️ **Keyword Extraction**
  - Automatically extracts important research keywords using KeyBERT

- 🧠 **Named Entity Recognition (NER)**
  - Identifies important entities such as:
    - Frameworks
    - Organizations
    - Models
    - Technical terms

- ✨ **Generative AI Summarization**
  - Uses Facebook BART-Large-CNN to synthesize concise summaries from the retrieved papers

- ⚡ **REST API Backend**
  - Production-ready FastAPI backend exposing search endpoints

- 💻 **Interactive Web Interface**
  - Streamlit dashboard for intuitive research exploration

---

# 🏗 System Architecture

```text
                    User Query
                         │
                         ▼
                 Streamlit Frontend
                         │
                         ▼
                 FastAPI Backend API
                         │
                         ▼
                  engine.py (ML Engine)
                         │
      ┌──────────────────┼──────────────────┐
      │                  │                  │
      ▼                  ▼                  ▼
Sentence Transformer   FAISS Search     ML-ArXiv Dataset
(all-MiniLM-L6-v2)     Vector Index     (15K+ Papers)
                         │
                         ▼
                Top-K Relevant Papers
                         │
      ┌──────────────────┼──────────────────┐
      ▼                  ▼                  ▼
   KeyBERT            BERT NER        BART-Large-CNN
 Keywords          Named Entities      AI Summary
      │                  │                  │
      └──────────────────┼──────────────────┘
                         ▼
                  JSON API Response
```

---

# 📂 Project Structure

```text
AI-Research-Paper-Intelligence-System
│
├── data
│   ├── index
│   │   └── faiss.index
│   │
│   └── raw
│       └── paper_embeddings.npy
│
├── source code
│   ├── MB_CBSOT_SIP2.ipynb
│   └── mb_cbsot_sip2.py
│
├── src
│   ├── __init__.py
│   ├── api.py
│   └── engine.py
│
├── streamlit_app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Technology Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| Deep Learning | PyTorch |
| Transformers | Hugging Face Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | FAISS |
| Keyword Extraction | KeyBERT |
| Named Entity Recognition | dslim/bert-base-NER |
| Summarization | facebook/bart-large-cnn |
| Dataset | ML-ArXiv Papers (Hugging Face) |

---

# 📊 Dataset

**Source**

Hugging Face

**Dataset**

ML-ArXiv Papers

Contains over **117,000 Machine Learning research papers**.

This project currently indexes and searches the first **15,000 papers** for efficient local inference.

---

# 🔄 Workflow

1. User enters a research query.
2. Query is converted into a dense embedding using Sentence Transformers.
3. FAISS retrieves the Top-K semantically similar papers.
4. KeyBERT extracts important keywords.
5. BERT performs Named Entity Recognition.
6. BART generates a concise AI summary.
7. FastAPI returns structured JSON.
8. Streamlit displays the results.

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/<your-username>/AI-Research-Paper-Intelligence-System.git

cd AI-Research-Paper-Intelligence-System
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run FastAPI Backend

```bash
uvicorn src.api:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Run Streamlit

```bash
streamlit run streamlit_app.py
```

Frontend:

```
http://localhost:8501
```

---

# 📸 Demo

## Streamlit Dashboard

<img width="1913" height="992" alt="image" src="https://github.com/user-attachments/assets/08cf640f-2593-4ba9-9d8b-9936be835a3a" />

<img width="1155" height="848" alt="image" src="https://github.com/user-attachments/assets/5e264290-599b-449e-b228-942ce7000b99" />

---

## FastAPI Swagger API

<img width="1912" height="751" alt="image" src="https://github.com/user-attachments/assets/a738ba07-ede1-456e-94a1-e716267bfee3" />

---

# 📈 Future Improvements

- Hybrid Retrieval (Dense + BM25)
- Cross-Encoder Re-ranking
- PDF Upload & Analysis
- Citation-aware Response Generation
- Research Paper Recommendation Engine
- User Search History
- Docker Deployment
- Cloud Hosting

---

# 👨‍💻 Author

**Manav Bhatia**

B.Tech Computer Science Engineering (AI/ML)

Faculty of Technology, University of Delhi

---

# ⭐ Acknowledgements

- Hugging Face
- Facebook AI Research
- Sentence Transformers
- FAISS
- KeyBERT
- Streamlit
- FastAPI
