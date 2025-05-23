"""
Optimized retriever for vector search and relevance detection.
"""

from typing import Dict, List, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer, util


class Retriever:
    """
    Retrieve relevant document chunks and determine query relevance.
    """
    
    def __init__(
        self,
        index: faiss.IndexFlatIP,
        documents: List[Dict],
        embedding_model: SentenceTransformer,
        similarity_threshold: float = 0.4,
    ):
        """
        Initialize the retriever.
        """
        self.index = index
        self.documents = documents
        self.embedding_model = embedding_model
        self.similarity_threshold = similarity_threshold
        
        # AI/ML topic keywords for relevance checking
        self.ai_ml_topics = [
            "machine learning", "artificial intelligence", "neural networks",
            "deep learning", "supervised learning", "unsupervised learning",
            "reinforcement learning", "natural language processing",
            "computer vision", "clustering", "classification", "regression",
            "overfitting", "underfitting", "backpropagation", "gradient descent",
            "CNN", "convolutional neural networks", "RAG", "retrieval",
            "transformer", "attention", "BERT", "GPT", "language model",
            "algorithm", "data science", "model training", "prediction"
        ]
    
    def is_query_relevant(self, query: str, conversation_context: str = "") -> bool:
        """
        Determine if query is relevant to AI/ML topics.
        """
        # Check for follow-up words with context
        follow_up_words = ['why', 'how', 'explain', 'difference', 'compare', 'what about']
        if any(word in query.lower() for word in follow_up_words) and conversation_context:
            # If conversation has AI/ML terms, allow follow-up
            ai_terms = ['neural', 'ai', 'machine learning', 'cnn', 'rag', 'model', 'algorithm']
            if any(term in conversation_context.lower() for term in ai_terms):
                return True
        
        # Standard relevance check
        query_embedding = self.embedding_model.encode([query])
        topics_embeddings = self.embedding_model.encode(self.ai_ml_topics)
        similarities = util.cos_sim(query_embedding, topics_embeddings)
        max_similarity = similarities.max().item()
        
        return max_similarity >= self.similarity_threshold
    
    def retrieve(self, query: str, top_k: int = 3) -> Tuple[List[Dict], bool]:
        """
        Retrieve most relevant document chunks for query.
        """
        # Check if query is relevant to AI/ML
        is_relevant = self.is_query_relevant(query)
        
        if not is_relevant:
            return [], False
        
        # Encode query
        query_embedding = self.embedding_model.encode([query])
        
        # Normalize for cosine similarity
        faiss.normalize_L2(query_embedding)
        
        # Search for relevant document chunks
        scores, indices = self.index.search(query_embedding, top_k)
        
        # Get relevant documents
        relevant_docs = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx != -1 and score > 0.2:  # Lower threshold for better results
                doc = self.documents[idx].copy()
                doc["score"] = float(score)
                relevant_docs.append(doc)
        
        return relevant_docs, True