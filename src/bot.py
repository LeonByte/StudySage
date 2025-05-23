"""
Discord bot implementation for AI assistant with conversation context.
"""

import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timedelta

import discord
from discord import app_commands
from dotenv import load_dotenv

from src.embedding import DocumentProcessor
from src.generation import Generator
from src.retrieval import Retriever

# Load environment variables
load_dotenv()

# Get environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD_ID = int(os.getenv("DISCORD_GUILD_ID") or 0)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "mistral")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./vector_db")
KNOWLEDGE_BASE_PATH = os.getenv("KNOWLEDGE_BASE_PATH", "./knowledge_base")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Initialize Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Initialize components
document_processor = None
retriever = None
generator = None

# Conversation memory (simplified)
conversation_history = defaultdict(list)
CONTEXT_WINDOW_MINUTES = 5  # Reduced from 10

def add_to_history(user_id: int, message: str, is_bot: bool = False):
    """Add message to conversation history."""
    now = datetime.now()
    conversation_history[user_id].append({
        'message': message[:200],  # Limit message length
        'timestamp': now,
        'is_bot': is_bot
    })
    
    # Keep only last 3 messages and clean old ones
    cutoff = now - timedelta(minutes=CONTEXT_WINDOW_MINUTES)
    recent_messages = [
        msg for msg in conversation_history[user_id]
        if msg['timestamp'] > cutoff
    ]
    conversation_history[user_id] = recent_messages[-3:]  # Only keep last 3

def get_simple_context(user_id: int) -> str:
    """Get simple conversation context for the user."""
    if user_id not in conversation_history or len(conversation_history[user_id]) < 2:
        return ""
    
    # Only use the last user message for context
    last_messages = conversation_history[user_id][-2:]
    if len(last_messages) >= 2:
        last_user_msg = last_messages[-2]['message'] if not last_messages[-2]['is_bot'] else ""
        return last_user_msg[:100] if last_user_msg else ""  # Limit context
    
    return ""

@client.event
async def on_ready():
    """Called when Discord bot is ready."""
    global document_processor, retriever, generator
    
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")
    
    # Initialize document processor
    document_processor = DocumentProcessor(
        knowledge_base_path=KNOWLEDGE_BASE_PATH,
        vector_db_path=VECTOR_DB_PATH,
        embedding_model_name=EMBEDDING_MODEL,
    )
    
    # Load or build vector database
    vector_db_result = document_processor.load_vector_db()
    
    if vector_db_result is None:
        print("Failed to load or build vector database.")
        return
    
    index, documents = vector_db_result
    
    # Initialize retriever
    retriever = Retriever(
        index=index,
        documents=documents,
        embedding_model=document_processor.embedding_model,
    )
    
    # Initialize generator
    generator = Generator(
        base_url=OLLAMA_BASE_URL,
        model=LLM_MODEL,
    )
    
    # Sync commands with Discord
    try:
        guild = discord.Object(id=DISCORD_GUILD_ID) if DISCORD_GUILD_ID else None
        await tree.sync(guild=guild)
        print("Command tree synced.")
    except Exception as e:
        print(f"Error syncing command tree: {e}")

@tree.command(
    name="ask",
    description="Ask a question about AI or machine learning",
)
async def ask_command(interaction: discord.Interaction, question: str):
    """Ask command with light conversation context."""
    await interaction.response.defer()
    
    try:
        user_id = interaction.user.id
        
        # Add user question to history
        add_to_history(user_id, question)
        
        # Get simple context
        simple_context = get_simple_context(user_id)
        
        # Check relevance (with light context if available)
        if simple_context:
            # Try with context first
            is_relevant = retriever.is_query_relevant(question, simple_context)
        else:
            is_relevant = retriever.is_query_relevant(question)
        
        if not is_relevant:
            # Friendly off-topic response
            if any(word in question.lower() for word in ['why', 'how', 'explain', 'what', 'difference']):
                response = "That's an interesting question! I focus on AI and machine learning topics though. Could you ask something about neural networks, deep learning, or other AI concepts? 😊"
            else:
                response = generator.generate_off_topic_response()
        else:
            # Get relevant documents
            relevant_docs, _ = retriever.retrieve(question)
            
            # Generate response (simplified)
            response = await generator.generate_response(question, relevant_docs, simple_context)
        
        # Add bot response to history
        add_to_history(user_id, response, is_bot=True)
        
        # Limit response length for Discord
        if len(response) > 2000:
            response = response[:1997] + "..."
        
        await interaction.followup.send(response)
        
    except Exception as e:
        print(f"Error in ask command: {e}")
        await interaction.followup.send("Sorry, I encountered an error processing your question.")

@client.event
async def on_message(message):
    """
    Handle direct messages to bot with conversation context.
    """
    # Ignore messages from bot itself
    if message.author == client.user:
        return
    
    # Only respond to direct messages
    if not isinstance(message.channel, discord.DMChannel):
        return
    
    try:
        user_id = message.author.id
        question = message.content.strip()
        
        # Add user question to history
        add_to_history(user_id, question)
        
        # Get simple context
        simple_context = get_simple_context(user_id)
        
        # Check relevance (with light context if available)
        if simple_context:
            is_relevant = retriever.is_query_relevant(question, simple_context)
        else:
            is_relevant = retriever.is_query_relevant(question)
        
        if not is_relevant:
            # Friendly off-topic response
            if any(word in question.lower() for word in ['why', 'how', 'explain', 'what', 'difference']):
                response = "That's an interesting question! I focus on AI and machine learning topics though. Could you ask something about neural networks, deep learning, or other AI concepts? 😊"
            else:
                response = generator.generate_off_topic_response()
        else:
            # Get relevant documents and generate response
            relevant_docs, _ = retriever.retrieve(question)
            
            async with message.channel.typing():
                response = await generator.generate_response(question, relevant_docs, simple_context)
        
        # Add bot response to history
        add_to_history(user_id, response, is_bot=True)
        
        # Limit response length for Discord
        if len(response) > 2000:
            response = response[:1997] + "..."
        
        # Send response
        await message.channel.send(response)
        
    except Exception as e:
        print(f"Error in message handler: {e}")
        await message.channel.send("Sorry, I encountered an error processing your message.")

def main():
    """Main entry point."""
    if not DISCORD_TOKEN:
        print("Error: DISCORD_TOKEN not set in environment variables.")
        return
    
    print("Starting Discord bot...")
    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()