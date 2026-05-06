import faiss
import numpy as np
import pickle
import os

from src.rag.embedder import embed_texts, embed_query
from src.rag.chunker import chunk_text

INDEX_FILE = "vectorstore/faiss_index.bin"
TEXTS_FILE = "vectorstore/texts.pkl"


def build_index(df):
    print("Building FAISS index...")

    # LIMIT DATA FOR SPEED
    df = df.head(1000)

    texts = []

    for _, row in df.iterrows():
        content = f"{row['title']} {row['genres']} {row.get('description','')}"
        chunks = chunk_text(content)
        texts.extend(chunks)

    embeddings = embed_texts(texts)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    os.makedirs("vectorstore", exist_ok=True)
    faiss.write_index(index, INDEX_FILE)

    with open(TEXTS_FILE, "wb") as f:
        pickle.dump(texts, f)

    print("FAISS ready")
    return index, texts


def load_index():
    if os.path.exists(INDEX_FILE) and os.path.exists(TEXTS_FILE):
        index = faiss.read_index(INDEX_FILE)

        with open(TEXTS_FILE, "rb") as f:
            texts = pickle.load(f)

        print("FAISS loaded")
        return index, texts

    return None, None


def retrieve(index, texts, query, k=5):
    query_vec = embed_query(query)

    distances, indices = index.search(np.array([query_vec]), k)

    return [texts[i] for i in indices[0]]