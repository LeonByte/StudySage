"""
Async LLM response generation for better performance.
"""

import aiohttp
import asyncio
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
        conversation_context: str = "",
        max_tokens: int = 400,
    ) -> str:
        """
        Generate response with async HTTP for better performance.
        """
        # Prepare context (limit to 2 most relevant docs)
        top_docs = relevant_docs[:2]
        context = "\n\n".join([doc["content"][:300] for doc in top_docs])  # Limit doc length
        
        # Simple prompt with optional context
        if conversation_context and len(conversation_context) > 10:
            prompt = f"""You are StudySage, an AI tutor for machine learning topics.

Previous: {conversation_context}

Context: {context}

Question: {query}

Give a clear, educational answer based on the context. Be conversational and helpful."""
        else:
            prompt = f"""You are StudySage, an AI tutor for machine learning topics.

Context: {context}

Question: {query}

Give a clear, educational answer based on the context."""
        
        # Use async HTTP requests - CRITICAL FIX
        try:
            # Create timeout for reasonable response time
            timeout = aiohttp.ClientTimeout(total=30)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.7,
                    }
                }
                
                print(f"🤖 Generating response with {self.model}...")
                
                async with session.post(self.api_url, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        generated_text = result.get("response", "")
                        print(f"✅ Generated {len(generated_text)} characters")
                        return generated_text
                    else:
                        error_text = await response.text()
                        print(f"❌ Ollama API error {response.status}: {error_text}")
                        return "I'm having trouble generating a response right now. Please try again later."
                        
        except asyncio.TimeoutError:
            print(f"⏰ Ollama API timeout after 30 seconds")
            return "The response is taking too long. Please try a simpler question or try again later."
        except aiohttp.ClientError as e:
            print(f"🌐 Network error connecting to Ollama: {e}")
            return "I'm having trouble connecting to the AI model. Please try again later."
        except Exception as e:
            print(f"❌ Unexpected error generating response: {e}")
            return "I'm having trouble generating a response right now. Please try again later."
    
    def generate_off_topic_response(self) -> str:
        """
        Generate friendly response for off-topic queries.
        """
        return "I'm focused on AI and machine learning topics only 😊 Let's keep learning! Feel free to ask me anything about neural networks, deep learning, or other AI concepts."