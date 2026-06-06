import os
import re
import numpy as np
import json
import time
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

# Initialize Mistral Client for Embeddings
api_key = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=api_key) if api_key else None

def manual_chunk_text(text, chunk_size=500, overlap=50):
    """
    Splits text into chunks of approximately `chunk_size` characters,
    respecting sentence boundaries where possible.
    """
    # Split by simple sentence-ending punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            # Start new chunk with overlap (last N chars of previous)
            overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else ""
            current_chunk = overlap_text + sentence + " "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

class NativeVectorStore:
    def __init__(self):
        self.documents = [] # List of {"text": ..., "vector": ...}
        
    def add_texts(self, texts):
        if not client:
            raise ValueError("Mistral API Key not set")
            
        print(f"Generating embeddings for {len(texts)} chunks...")

        # Batch settings: allow override via env var MISTRAL_EMBED_BATCH_SIZE
        try:
            batch_size = int(os.getenv("MISTRAL_EMBED_BATCH_SIZE", "64"))
        except Exception:
            batch_size = 64

        def _call_embeddings(batch_inputs):
            # Simple retry/backoff for transient API errors
            max_retries = 3
            backoff = 1.0
            for attempt in range(1, max_retries + 1):
                try:
                    return client.embeddings.create(model="mistral-embed", inputs=batch_inputs)
                except Exception as e:
                    if attempt == max_retries:
                        raise
                    time.sleep(backoff)
                    backoff *= 2

        for start in range(0, len(texts), batch_size):
            end = start + batch_size
            batch = texts[start:end]
            print(f"Requesting embeddings for batch {start}-{end} (size={len(batch)})")
            resp = _call_embeddings(batch)

            # Append embeddings in order
            for i, text in enumerate(batch):
                vector = resp.data[i].embedding
                self.documents.append({
                    "text": text,
                    "vector": np.array(vector)
                })
            
    def similarity_search(self, query, k=3):
        if not client:
            raise ValueError("Mistral API Key not set")
            
        # Get query vector
        query_response = client.embeddings.create(
            model="mistral-embed",
            inputs=[query]
        )
        query_vec = np.array(query_response.data[0].embedding)
        
        scores = []
        for doc in self.documents:
            doc_vec = doc["vector"]
            # Cosine Similarity: (A . B) / (||A|| * ||B||)
            # Mistral embeddings are usually normalized, so just dot product suffices,
            # but we'll do full cosine to be safe.
            norm_q = np.linalg.norm(query_vec)
            norm_d = np.linalg.norm(doc_vec)
            
            if norm_q == 0 or norm_d == 0:
                score = 0
            else:
                score = np.dot(query_vec, doc_vec) / (norm_q * norm_d)
            
            scores.append((score, doc["text"]))
            
        # Sort by score descending
        scores.sort(key=lambda x: x[0], reverse=True)
        
        # Return top k texts
        return [text for score, text in scores[:k]]

# Global instance for simplicity in this MVP
native_db = NativeVectorStore()
