"""
Debug script to test relevance detection thresholds.
"""

from sentence_transformers import SentenceTransformer, util

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# AI/ML topics for relevance checking
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
    "convolutional neural networks", "CNN", "RAG", "retrieval augmented generation"
]

# Test queries
test_queries = [
    "What is RAG",
    "What is Convolutional Neural Networks?",
    "What is supervised learning?",
    "Tell me a joke",
    "What's the weather?",
    "How do neural networks work?"
]

print("Testing relevance detection:")
print("=" * 50)

for query in test_queries:
    # Encode query and topics
    query_embedding = model.encode([query])
    topics_embeddings = model.encode(ai_ml_topics)
    
    # Calculate similarities
    similarities = util.cos_sim(query_embedding, topics_embeddings)
    max_similarity = similarities.max().item()
    
    # Test different thresholds
    relevant_06 = max_similarity >= 0.6
    relevant_05 = max_similarity >= 0.5
    relevant_04 = max_similarity >= 0.4
    relevant_03 = max_similarity >= 0.3
    
    print(f"Query: '{query}'")
    print(f"  Max similarity: {max_similarity:.3f}")
    print(f"  Relevant at 0.6: {relevant_06}")
    print(f"  Relevant at 0.5: {relevant_05}")
    print(f"  Relevant at 0.4: {relevant_04}")
    print(f"  Relevant at 0.3: {relevant_03}")
    print()