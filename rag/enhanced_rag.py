# enhanced_rag.py
from typing import List, Tuple
import numpy as np
from sentence_transformers import CrossEncoder, SentenceTransformer
import faiss

class EnhancedRAG:
    def __init__(self, base_embedder, cross_encoder_name='cross-encoder/ms-marco-MiniLM-L-6-v2'):
        self.base_embedder = base_embedder
        self.cross_encoder = CrossEncoder(cross_encoder_name)
        self.index = None
        self.documents = []

    def add_documents(self, documents: List[str]):
        """Add documents to the RAG system with metadata"""
        embeddings = self.base_embedder.encode(documents)
        embeddings = np.array(embeddings).astype('float32')
        if self.index is None:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.documents.extend(documents)

    def retrieve_and_rerank(self, query: str, k: int = 20, rerank_k: int = 5) -> List[Tuple[str, float]]:
        """Two-stage retrieval with initial semantic search and cross-encoder reranking"""
        # Initial retrieval
        query_embedding = self.base_embedder.encode([query])
        query_embedding = np.array(query_embedding).astype('float32')
        distances, indices = self.index.search(query_embedding, k)

        # Prepare candidates for reranking
        candidates = [(self.documents[idx], -dist) for idx, dist in zip(indices[0], distances[0])]

        # Rerank using cross-encoder
        rerank_pairs = [(query, doc[0]) for doc in candidates]
        rerank_scores = self.cross_encoder.predict(rerank_pairs)

        # Sort by cross-encoder scores and return top k
        reranked = [(doc[0], score) for doc, score in zip(candidates, rerank_scores)]
        reranked.sort(key=lambda x: x[1], reverse=True)

        return reranked[:rerank_k]
