# AI Research Paper Intelligence System

An advanced Natural Language Processing pipeline designed to semantically search, retrieve, summarize, and extract critical entities from a massive corpus of machine learning research papers.

## Features
* **Semantic Search:** Utilizes `all-MiniLM-L6-v2` and FAISS for ultra-fast, dense vector retrieval.
* **Abstract Summarization:** Leverages `facebook/bart-large-cnn` to distill complex research into concise summaries.
* **Keyword Extraction:** Uses KeyBERT to extract prominent N-grams and candidate phrases.
* **Entity Recognition (NER):** Extracts domain-specific entities (Frameworks, Models, Organizations).

## Tech Stack
* Python 3
* Hugging Face Transformers
* FAISS (Facebook AI Similarity Search)
* Sentence-Transformers
* KeyBERT & Pandas

## Installation

```bash
git clone <your-repo-url>
cd ai-research-intelligence
pip install -r requirements.txt
