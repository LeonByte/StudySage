"""
Discord bot implementation for AI assistant.
"""

import os
from pathlib import Path

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
    """
    Ask command handler.
    
    Args:
        interaction: Discord interaction
        question: User's question
    """
    # Defer response to show "thinking..." status
    await interaction.response.defer()
    
    try:
        # Check if question is relevant
        relevant_docs, is_relevant = retriever.retrieve(question)
        
        if not is_relevant:
            # Send off-topic response
            response = generator.generate_off_topic_response()
        else:
            # Generate response based on relevant documents
            response = await generator.generate_response(question, relevant_docs)
        
        # Limit response length for Discord
        if len(response) > 2000:
            response = response[:1997] + "..."
        
        # Send response as follow-up
        await interaction.followup.send(response)
        
    except Exception as e:
        print(f"Error in ask command: {e}")
        await interaction.followup.send("Sorry, I encountered an error processing your question.")

@client.event
async def on_message(message):
    """
    Handle direct messages to bot.
    
    Args:
        message: Discord message
    """
    # Ignore messages from bot itself
    if message.author == client.user:
        return
    
    # Only respond to direct messages
    if not isinstance(message.channel, discord.DMChannel):
        return
    
    try:
        # Process message content as question
        question = message.content.strip()
        
        # Check if question is relevant
        relevant_docs, is_relevant = retriever.retrieve(question)
        
        if not is_relevant:
            # Send off-topic response
            response = generator.generate_off_topic_response()
        else:
            # Generate response based on relevant documents
            async with message.channel.typing():
                response = await generator.generate_response(question, relevant_docs)
        
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