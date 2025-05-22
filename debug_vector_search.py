"""
Debug the actual vector search and retrieval process.
"""

import os
from dotenv import load_dotenv
from src.embedding import DocumentProcessor
from src.retrieval import Retriever

# Load environment variables
load_dotenv()

# Initialize components
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./vector_db")
KNOWLEDGE_BASE_PATH = os.getenv("KNOWLEDGE_BASE_PATH", "./knowledge_base")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

print("Loading document processor...")
document_processor = DocumentProcessor(
    knowledge_base_path=KNOWLEDGE_BASE_PATH,
    vector_db_path=VECTOR_DB_PATH,
    embedding_model_name=EMBEDDING_MODEL,
)

print("Loading vector database...")
vector_db_result = document_processor.load_vector_db()

if vector_db_result is None:
    print("Failed to load vector database!")
    exit(1)

index, documents = vector_db_result
print(f"Loaded {len(documents)} documents")

# Initialize retriever
retriever = Retriever(
    index=index,
    documents=documents,
    embedding_model=document_processor.embedding_model,
)

# Test queries
test_queries = [
    "What is RAG",
    "What is Convolutional Neural Networks?",
    "What is supervised learning?"
]

print("\nTesting actual retrieval process:")
print("=" * 60)

for query in test_queries:
    print(f"\nQuery: '{query}'")
    
    # Test topic relevance
    is_relevant = retriever.is_query_relevant(query)
    print(f"  Topic relevance: {is_relevant}")
    
    # Test actual retrieval
    relevant_docs, retrieval_relevant = retriever.retrieve(query, top_k=5)
    print(f"  Retrieval relevant: {retrieval_relevant}")
    print(f"  Documents found: {len(relevant_docs)}")
    
    if relevant_docs:
        for i, doc in enumerate(relevant_docs):
            print(f"    Doc {i+1} (score: {doc.get('score', 'N/A'):.3f}):")
            print(f"      Source: {doc['metadata']['source']}")
            print(f"      Content preview: {doc['content'][:100]}...")
    else:
        print("    No documents found!")
        
        # Debug vector search specifically
        query_embedding = retriever.embedding_model.encode([query])
        import faiss
        faiss.normalize_L2(query_embedding)
        scores, indices = retriever.index.search(query_embedding, 5)
        
        print("    Raw vector search results:")
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx != -1:
                doc = documents[idx]
                print(f"      Result {i+1}: score={score:.3f}, source={doc['metadata']['source']}")
                print(f"        Content: {doc['content'][:80]}...")