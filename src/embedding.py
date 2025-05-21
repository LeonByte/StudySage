"""
Handles document loading, chunking, and embedding.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
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
        
        # Create markdown splitter with headers as metadata
        self.md_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "header1"),
                ("##", "header2"),
                ("###", "header3"),
            ]
        )
        
        # Create text splitter for further chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
        )
        
        # Ensure directories exist
        self.knowledge_base_path.mkdir(exist_ok=True, parents=True)
        self.vector_db_path.mkdir(exist_ok=True, parents=True)
    
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
            
            # Split document based on markdown headers
            md_header_splits = self.md_splitter.split_text(content)
            
            # Further split into smaller chunks
            for md_doc in md_header_splits:
                text = md_doc.page_content
                metadata = md_doc.metadata.copy()
                metadata["source"] = file_path.name
                
                chunks = self.text_splitter.split_text(text)
                
                for i, chunk in enumerate(chunks):
                    documents.append({
                        "content": chunk,
                        "metadata": {
                            **metadata,
                            "chunk_id": i,
                        }
                    })
        
        return documents

    def create_embeddings(self, documents: List[Dict]) -> List[List[float]]:
        """
        Create embeddings for document chunks.
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            List of document embeddings
        """
        texts = [doc["content"] for doc in documents]
        embeddings = self.embedding_model.encode(texts)
        return embeddings
    
    def build_vector_db(self) -> Optional[FAISS]:
        """
        Build and save vector database.
        
        Returns:
            The FAISS vector database
        """
        print("Loading documents...")
        documents = self.load_documents()
        
        if not documents:
            print("No documents found in knowledge base.")
            return None
        
        print(f"Loaded {len(documents)} document chunks.")
        
        print("Creating embeddings...")
        embeddings = self.create_embeddings(documents)
        
        print("Building vector database...")
        dimension = len(embeddings[0])
        vector_db = FAISS(dimension)
        
        # Add documents to vector database
        for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
            vector_db.add([embedding], [doc])
        
        print(f"Added {len(documents)} document chunks to vector database.")
        
        # Save vector database
        vector_db_path = self.vector_db_path / "faiss_index"
        vector_db.save(str(vector_db_path))
        print(f"Saved vector database to {vector_db_path}")
        
        return vector_db
    
    def load_vector_db(self) -> Optional[FAISS]:
        """
        Load vector database if it exists.
        
        Returns:
            The FAISS vector database, or None if it doesn't exist
        """
        vector_db_path = self.vector_db_path / "faiss_index"
        
        if vector_db_path.exists():
            print(f"Loading vector database from {vector_db_path}")
            return FAISS.load(str(vector_db_path))
        
        print("Vector database not found. Creating a new one...")
        return self.build_vector_db()