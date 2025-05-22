"""
Simplified document processor for AI/ML knowledge base.
No external dependencies beyond sentence-transformers and faiss.
"""

import os
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class DocumentProcessor:
    """
    Process documents from knowledge base, chunk them, and create embeddings.
    """
    
    def __init__(
        self,
        knowledge_base_path: str,
        vector_db_path: str,
        embedding_model_name: str = "all-MiniLM-L6-v2"
    ):
        """
        Initialize the document processor.
        
        Args:
            knowledge_base_path: Path to knowledge base directory
            vector_db_path: Path to store vector database
            embedding_model_name: Name of sentence-transformers model
        """
        self.knowledge_base_path = Path(knowledge_base_path)
        self.vector_db_path = Path(vector_db_path)
        self.embedding_model_name = embedding_model_name
        
        # Create embedding model
        print(f"Loading embedding model: {embedding_model_name}")
        self.embedding_model = SentenceTransformer(embedding_model_name)
        
        # Ensure directories exist
        self.knowledge_base_path.mkdir(exist_ok=True, parents=True)
        self.vector_db_path.mkdir(exist_ok=True, parents=True)
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Simple text chunking function.
        
        Args:
            text: Input text to chunk
            chunk_size: Size of each chunk
            overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks
    
    def load_documents(self) -> List[Dict]:
        """
        Load all markdown documents from knowledge base folder.
        
        Returns:
            List of document dictionaries with text and metadata
        """
        documents = []
        
        for file_path in self.knowledge_base_path.glob("*.md"):
            print(f"Processing file: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Simple chunking
            chunks = self.chunk_text(content)
            
            for i, chunk in enumerate(chunks):
                documents.append({
                    "content": chunk,
                    "metadata": {
                        "source": file_path.name,
                        "chunk_id": i,
                    }
                })
        
        return documents

    def create_embeddings(self, documents: List[Dict]) -> np.ndarray:
        """
        Create embeddings for document chunks.
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            Numpy array of document embeddings
        """
        texts = [doc["content"] for doc in documents]
        embeddings = self.embedding_model.encode(texts)
        return embeddings
    
    def build_vector_db(self) -> Optional[Tuple[faiss.IndexFlatIP, List[Dict]]]:
        """
        Build and save vector database.
        
        Returns:
            Tuple of (FAISS index, documents) or None if no documents
        """
        print("Loading documents...")
        documents = self.load_documents()
        
        if not documents:
            print("No documents found in knowledge base.")
            return None
        
        print(f"Loaded {len(documents)} document chunks.")
        
        print("Creating embeddings...")
        embeddings = self.create_embeddings(documents)
        
        print("Building FAISS index...")
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        index.add(embeddings)
        
        print(f"Added {len(documents)} document chunks to FAISS index.")
        
        # Save index and documents
        index_path = self.vector_db_path / "faiss_index.bin"
        docs_path = self.vector_db_path / "documents.pkl"
        
        faiss.write_index(index, str(index_path))
        with open(docs_path, 'wb') as f:
            pickle.dump(documents, f)
        
        print(f"Saved vector database to {self.vector_db_path}")
        
        return index, documents
    
    def load_vector_db(self) -> Optional[Tuple[faiss.IndexFlatIP, List[Dict]]]:
        """
        Load vector database if it exists.
        
        Returns:
            Tuple of (FAISS index, documents) or None if it doesn't exist
        """
        index_path = self.vector_db_path / "faiss_index.bin"
        docs_path = self.vector_db_path / "documents.pkl"
        
        if index_path.exists() and docs_path.exists():
            print(f"Loading vector database from {self.vector_db_path}")
            index = faiss.read_index(str(index_path))
            with open(docs_path, 'rb') as f:
                documents = pickle.load(f)
            return index, documents
        
        print("Vector database not found. Creating a new one...")
        return self.build_vector_db()