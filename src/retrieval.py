"""
Handles similarity search and determines query relevance.
"""

from typing import Dict, List, Tuple

from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer, util


class Retriever:
    """
    Retrieve relevant document chunks based on query
    and determine if query is on-topic.
    """
    
    def __init__(
        self,
        vector_db: FAISS,
        embedding_model: SentenceTransformer,
        similarity_threshold: float = 0.6,
    ):
        """
        Initialize the retriever.
        
        Args:
            vector_db: FAISS vector database
            embedding_model: SentenceTransformer model
            similarity_threshold: Minimum similarity score to consider document relevant
        """
        self.vector_db = vector_db
        self.embedding_model = embedding_model
        self.similarity_threshold = similarity_threshold
    
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
            "model evaluation", "hyperparameter tuning",
        ]
        
        # Encode query and AI/ML topics
        query_embedding = self.embedding_model.encode(query)
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
        query_embedding = self.embedding_model.encode(query)
        
        # Search for relevant document chunks
        search_results = self.vector_db.search_by_vector(
            embedding=query_embedding,
            k=top_k,
        )
        
        # Return search results and relevance flag
        return search_results, True