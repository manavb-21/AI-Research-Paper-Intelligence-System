import os

import faiss
import torch
from datasets import load_dataset
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoModelForTokenClassification,
    AutoTokenizer,
)

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2', device=DEVICE.type)
KEYWORD_MODEL = KeyBERT(model=EMBEDDING_MODEL)

SUMMARIZER_TOKENIZER = AutoTokenizer.from_pretrained('facebook/bart-large-cnn')
SUMMARIZER_MODEL = AutoModelForSeq2SeqLM.from_pretrained('facebook/bart-large-cnn').to(DEVICE)
SUMMARIZER_MODEL.eval()

NER_TOKENIZER = AutoTokenizer.from_pretrained('dslim/bert-base-NER')
NER_MODEL = AutoModelForTokenClassification.from_pretrained('dslim/bert-base-NER').to(DEVICE)
NER_MODEL.eval()

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


def summarize_text(text, max_length=180, min_length=60):
    if not text or not text.strip():
        return ''

    inputs = SUMMARIZER_TOKENIZER(
        text,
        return_tensors='pt',
        max_length=1024,
        truncation=True,
    )
    inputs = {key: value.to(DEVICE) for key, value in inputs.items()}

    with torch.no_grad():
        summary_ids = SUMMARIZER_MODEL.generate(
            **inputs,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
        )

    return SUMMARIZER_TOKENIZER.decode(summary_ids[0], skip_special_tokens=True)


def extract_entities(text):
    if not text or not text.strip():
        return []

    inputs = NER_TOKENIZER(
        text,
        return_tensors='pt',
        return_offsets_mapping=True,
        truncation=True,
        max_length=512,
    )
    offset_mapping = inputs.pop('offset_mapping')[0].tolist()
    inputs = {key: value.to(DEVICE) for key, value in inputs.items()}

    with torch.no_grad():
        logits = NER_MODEL(**inputs).logits

    predictions = torch.argmax(logits, dim=-1)[0].cpu().tolist()
    id_to_label = NER_MODEL.config.id2label

    entities = []
    active_entity = None

    for prediction, offsets in zip(predictions, offset_mapping):
        start, end = offsets
        if start == end:
            continue

        label = id_to_label[prediction]
        if label == 'O':
            if active_entity is not None:
                entities.append(active_entity)
                active_entity = None
            continue

        prefix, entity_type = label.split('-', 1)

        if (
            prefix == 'B'
            or active_entity is None
            or active_entity['entity_group'] != entity_type
            or start > active_entity['end'] + 1
        ):
            if active_entity is not None:
                entities.append(active_entity)
            active_entity = {
                'start': start,
                'end': end,
                'entity_group': entity_type,
            }
        else:
            active_entity['end'] = end

    if active_entity is not None:
        entities.append(active_entity)

    return [
        (text[entity['start']:entity['end']], entity['entity_group'])
        for entity in entities
    ]


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

    final_summary = summarize_text(
        prompt,
        max_length=180,
        min_length=60,
    )
    return final_summary
