import os
import numpy as np
import pandas as pd
import faiss
import torch
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
from transformers import pipeline

DEVICE = 0 if torch.cuda.is_available() else -1

EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2', device='cuda' if DEVICE == 0 else 'cpu')
KEYWORD_MODEL = KeyBERT(model=EMBEDDING_MODEL)
NER_PIPELINE = pipeline('ner', model='dslim/bert-base-NER', aggregation_strategy='simple', device=DEVICE)
SUMMARIZATION_PIPELINE = pipeline('summarization', model='facebook/bart-large-cnn', device=DEVICE)

INDEX_PATH = 'data/index/faiss.index'

_dataframe = None
_faiss_index = None


def initialize_system():
    global _dataframe, _faiss_index

    dataset = load_dataset('CShorten/ML-ArXiv-Papers', split='train')
    df = dataset.to_pandas()
    df = df[['title', 'abstract']].dropna().reset_index(drop=True)
    df = df.iloc[:15000].reset_index(drop=True)
    df['combined_text'] = df['title'].astype(str) + '. ' + df['abstract'].astype(str)

    _dataframe = df

    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)

    if os.path.exists(INDEX_PATH):
        _faiss_index = faiss.read_index(INDEX_PATH)
    else:
        embeddings = EMBEDDING_MODEL.encode(
            df['combined_text'].tolist(),
            show_progress_bar=True,
            convert_to_numpy=True
        ).astype('float32')

        faiss.normalize_L2(embeddings)

        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(embeddings)

        faiss.write_index(index, INDEX_PATH)
        _faiss_index = index

    return _dataframe, _faiss_index


def extract_entities(text):
    raw_entities = NER_PIPELINE(text)
    entities = [(item['word'], item['entity_group']) for item in raw_entities]
    return entities


def process_query(query, k=3):
    global _dataframe, _faiss_index

    if _dataframe is None or _faiss_index is None:
        initialize_system()

    query_embedding = EMBEDDING_MODEL.encode([query], convert_to_numpy=True).astype('float32')
    faiss.normalize_L2(query_embedding)

    scores, indices = _faiss_index.search(query_embedding, k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue

        row = _dataframe.iloc[idx]
        title = row['title']
        abstract = row['abstract']

        keywords = KEYWORD_MODEL.extract_keywords(
            abstract,
            keyphrase_ngram_range=(1, 3),
            stop_words='english',
            top_n=5
        )
        entities = extract_entities(abstract)

        print(f'Title: {title}')
        print(f'Similarity Score: {float(score):.4f}')
        print(f'KeyBERT Keywords: {keywords}')
        print(f'NER Entities: {entities}')
        print('-' * 80)

        results.append({
            'title': title,
            'abstract': abstract,
            'score': float(score),
            'keywords': keywords,
            'entities': entities
        })

    top_abstracts = [r['abstract'] for r in results[:3]]
    context = ' '.join(top_abstracts)

    prompt = f'Synthesize a technical summary answering the query [{query}] using these references: [{context}]'

    max_input_chars = 4000
    if len(prompt) > max_input_chars:
        prompt = prompt[:max_input_chars]

    summary_output = SUMMARIZATION_PIPELINE(
        prompt,
        max_length=180,
        min_length=60,
        do_sample=False
    )

    final_summary = summary_output[0]['summary_text']
    return final_summary
