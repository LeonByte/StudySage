"""
Handles prompt construction and LLM response generation.
"""

import requests
from typing import Dict, List


class Generator:
    """
    Generate responses based on retrieved documents using local LLM.
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "mistral",
    ):
        """
        Initialize the generator.
        
        Args:
            base_url: Base URL for Ollama API
            model: Name of model to use
        """
        self.base_url = base_url
        self.model = model
        self.api_url = f"{self.base_url}/api/generate"
    
    async def generate_response(
        self,
        query: str,
        relevant_docs: List[Dict],
        max_tokens: int = 500,
    ) -> str:
        """
        Generate response based on query and relevant documents.
        
        Args:
            query: User's query
            relevant_docs: List of relevant document dictionaries
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response
        """
        # Prepare context from relevant documents
        context = "\n\n".join([doc["content"] for doc in relevant_docs])
        
        # Construct prompt
        prompt = f"""You are a helpful AI study assistant specialized in artificial intelligence and machine learning.
Use the following information to answer the question.

CONTEXT:
{context}

QUESTION:
{query}

INSTRUCTIONS:
- Answer based only on the provided context.
- If the context doesn't contain enough information, say so honestly.
- Keep your answer concise and to the point.
- Use Markdown formatting when helpful.
- Focus on being accurate and educational.

ANSWER:
"""
        
        # Call Ollama API with async aiohttp
        try:
            import aiohttp
            import asyncio
            
            timeout = aiohttp.ClientTimeout(total=60)  # 60 second timeout
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    self.api_url,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "num_predict": max_tokens,
                            "temperature": 0.7,
                        }
                    }
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["response"]
                    else:
                        print(f"Ollama API error: HTTP {response.status}")
                        return "I'm having trouble connecting to the language model. Please try again."
                        
        except asyncio.TimeoutError:
            print(f"Ollama API timeout after 60 seconds")
            return "The response is taking too long. Please try a simpler question or try again later."
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm having trouble generating a response right now. Please try again later."
    
    def generate_off_topic_response(self) -> str:
        """
        Generate friendly response for off-topic queries.
        
        Returns:
            Off-topic response
        """
        return "I'm focused on AI and machine learning topics only 😊 Let's keep learning! Feel free to ask me anything about neural networks, deep learning, or other AI concepts."