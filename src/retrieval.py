"""
Simplified retriever for vector search and relevance detection.
"""

from typing import Dict, List, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer, util


class Retriever:
    """
    Retrieve relevant document chunks based on query
    and determine if query is on-topic.
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
        
        Args:
            index: FAISS index
            documents: List of document dictionaries
            embedding_model: SentenceTransformer model
            similarity_threshold: Minimum similarity score to consider document relevant
        """
        self.index = index
        self.documents = documents
        self.embedding_model = embedding_model
        self.similarity_threshold = similarity_threshold
        
        # Define key AI/ML topics for relevance checking (moved to __init__)
        self.ai_ml_topics = [
            "machine learning", "artificial intelligence", "neural networks",
            "deep learning", "supervised learning", "unsupervised learning",
            "reinforcement learning", "natural language processing",
            "computer vision", "clustering", "classification", "regression",
            "overfitting", "underfitting", "backpropagation", "gradient descent",
            "loss function", "activation function", "training data",
            "testing data", "validation data", "feature extraction",
            "feature selection", "dimensionality reduction",
            "model evaluation", "hyperparameter tuning", "neural network",
            "algorithm", "data science", "model training", "prediction",
            "convolutional neural networks", "CNN", "RAG", "retrieval",
            "augmented generation", "vector database", "embedding",
            "transformer", "attention", "BERT", "GPT", "language model",
            "bias variance", "regularization", "cross validation",
            "confusion matrix", "precision", "recall", "F1 score"
        ]
    
    def is_query_relevant(self, query: str) -> bool:
        """
        Determine if query is relevant to knowledge base topics (AI/ML).
        
        Args:
            query: User's query
            
        Returns:
            True if query is relevant, False otherwise
        """
        # Define key AI/ML topics for relevance checking
        ai_ml_topics = [
            "machine learning", "artificial intelligence", "neural networks",
            "deep learning", "supervised learning", "unsupervised learning",
            "reinforcement learning", "natural language processing",
            "computer vision", "clustering", "classification", "regression",
            "overfitting", "underfitting", "backpropagation", "gradient descent",
            "loss function", "activation function", "training data",
            "testing data", "validation data", "feature extraction",
            "feature selection", "dimensionality reduction",
            "model evaluation", "hyperparameter tuning", "neural network",
            "algorithm", "data science", "model training", "prediction",
            "convolutional neural networks", "CNN", "RAG", "retrieval",
            "augmented generation", "vector database", "embedding"
        ]
        
        # Encode query and AI/ML topics
        query_embedding = self.embedding_model.encode([query])
        topics_embeddings = self.embedding_model.encode(ai_ml_topics)
        
        # Calculate cosine similarities
        similarities = util.cos_sim(query_embedding, topics_embeddings)
        
        # Get maximum similarity score
        max_similarity = similarities.max().item()
        
        # Return whether query is relevant based on threshold
        return max_similarity >= self.similarity_threshold
    
    def retrieve(self, query: str, top_k: int = 3) -> Tuple[List[Dict], bool]:
        """
        Retrieve most relevant document chunks for query.
        
        Args:
            query: User's query
            top_k: Number of top results to retrieve
            
        Returns:
            Tuple of (relevant_docs, is_relevant)
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
            if idx != -1 and score > 0.3:  # Basic relevance threshold
                doc = self.documents[idx].copy()
                doc["score"] = float(score)
                relevant_docs.append(doc)
        
        return relevant_docs, True