from sentence_transformers import SentenceTransformer
import faiss, numpy as np

def build_index(chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return model, index, embeddings

def retrieve(query, model, index, chunks, top_k=3):
    q_emb = model.encode([query])
    D, I = index.search(q_emb, top_k)
    return [chunks[i] for i in I[0]]
