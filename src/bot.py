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
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# Initialize components
document_processor = None
retriever = None
generator = None

# Conversation memory
conversation_history = defaultdict(list)
CONTEXT_WINDOW_MINUTES = 5

def add_to_history(user_id: int, message: str, is_bot: bool = False):
    """Add message to conversation history."""
    now = datetime.now()
    conversation_history[user_id].append({
        'message': message[:200],
        'timestamp': now,
        'is_bot': is_bot
    })
    
    cutoff = now - timedelta(minutes=CONTEXT_WINDOW_MINUTES)
    recent_messages = [
        msg for msg in conversation_history[user_id]
        if msg['timestamp'] > cutoff
    ]
    conversation_history[user_id] = recent_messages[-3:]

def get_simple_context(user_id: int) -> str:
    """Get simple conversation context for the user."""
    if user_id not in conversation_history or len(conversation_history[user_id]) < 2:
        return ""
    
    last_messages = conversation_history[user_id][-2:]
    if len(last_messages) >= 2:
        last_user_msg = last_messages[-2]['message'] if not last_messages[-2]['is_bot'] else ""
        return last_user_msg[:100] if last_user_msg else ""
    
    return ""

# CREATE CLIENT FIRST
intents = discord.Intents.default()
intents.message_content = True

class StudySageBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        """Called when the bot is starting up."""
        global document_processor, retriever, generator
        
        print("📚 Initializing document processor...")
        document_processor = DocumentProcessor(
            knowledge_base_path=KNOWLEDGE_BASE_PATH,
            vector_db_path=VECTOR_DB_PATH,
            embedding_model_name=EMBEDDING_MODEL,
        )
        
        # Load or build vector database
        vector_db_result = document_processor.load_vector_db()
        
        if vector_db_result is None:
            print("❌ Failed to load or build vector database.")
            return
        
        index, documents = vector_db_result
        print(f"✅ Loaded {len(documents)} documents into vector database")
        
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

    async def on_ready(self):
        """Called when Discord bot is ready."""
        print(f"🤖 Logged in as {self.user} (ID: {self.user.id})")
        print(f"🏠 Bot is in {len(self.guilds)} guild(s)")
        for guild in self.guilds:
            print(f"  - {guild.name} (ID: {guild.id})")
        print("------")
        
        # FIXED: Copy global commands to guild, then sync
        print("🔄 Attempting to sync slash commands...")
        try:
            if DISCORD_GUILD_ID:
                guild = discord.Object(id=DISCORD_GUILD_ID)
                
                # Copy global commands to the guild
                self.tree.copy_global_to(guild=guild)
                print(f"📋 Copied global commands to guild {DISCORD_GUILD_ID}")
                
                # Now sync the guild
                synced = await self.tree.sync(guild=guild)
                print(f"✅ Synced {len(synced)} commands to guild {DISCORD_GUILD_ID}")
                
                # List synced commands
                for cmd in synced:
                    print(f"  - /{cmd.name}: {cmd.description}")
            else:
                # Sync globally
                synced = await self.tree.sync()
                print(f"✅ Synced {len(synced)} commands globally")
                
        except discord.HTTPException as e:
            print(f"❌ HTTP Error syncing commands: {e}")
        except discord.Forbidden as e:
            print(f"❌ Forbidden error: Bot lacks permissions")
        except Exception as e:
            print(f"❌ Unexpected error syncing commands: {e}")

    async def on_message(self, message):
        """Handle direct messages to bot with conversation context."""
        if message.author == self.user:
            return
        
        if not isinstance(message.channel, discord.DMChannel):
            return
        
        try:
            user_id = message.author.id
            question = message.content.strip()
            
            print(f"💬 DM from {message.author.name}: {question}")
            
            # Add user question to history
            add_to_history(user_id, question)
            
            # Get simple context
            simple_context = get_simple_context(user_id)
            
            # Check relevance
            if simple_context:
                is_relevant = retriever.is_query_relevant(question, simple_context)
            else:
                is_relevant = retriever.is_query_relevant(question)
            
            if not is_relevant:
                if any(word in question.lower() for word in ['why', 'how', 'explain', 'what', 'difference']):
                    response = "That's an interesting question! I focus on AI and machine learning topics though. Could you ask something about neural networks, deep learning, or other AI concepts? 😊"
                else:
                    response = generator.generate_off_topic_response()
            else:
                relevant_docs, _ = retriever.retrieve(question)
                
                async with message.channel.typing():
                    response = await generator.generate_response(question, relevant_docs, simple_context)
            
            # Add bot response to history
            add_to_history(user_id, response, is_bot=True)
            
            # Limit response length for Discord
            if len(response) > 2000:
                response = response[:1997] + "..."
            
            await message.channel.send(response)
            print(f"✅ Responded to DM successfully")
            
        except Exception as e:
            print(f"❌ Error in DM handler: {e}")
            await message.channel.send("Sorry, I encountered an error processing your message.")

# Create the client instance
client = StudySageBot(intents=intents)

# Define commands as GLOBAL commands
@client.tree.command(
    name="ask",
    description="Ask a question about AI or machine learning"
)
@app_commands.describe(question="Your AI/ML question")
async def ask_command(interaction: discord.Interaction, question: str):
    """Ask command with conversation context."""
    print(f"📝 /ask command from {interaction.user.name}: {question}")
    
    await interaction.response.defer()
    
    try:
        user_id = interaction.user.id
        
        # Add user question to history
        add_to_history(user_id, question)
        
        # Get simple context
        simple_context = get_simple_context(user_id)
        
        # Check relevance
        if simple_context:
            is_relevant = retriever.is_query_relevant(question, simple_context)
        else:
            is_relevant = retriever.is_query_relevant(question)
        
        if not is_relevant:
            if any(word in question.lower() for word in ['why', 'how', 'explain', 'what', 'difference']):
                response = "That's an interesting question! I focus on AI and machine learning topics though. Could you ask something about neural networks, deep learning, or other AI concepts? 😊"
            else:
                response = generator.generate_off_topic_response()
        else:
            # Get relevant documents
            relevant_docs, _ = retriever.retrieve(question)
            print(f"📚 Found {len(relevant_docs)} relevant documents")
            
            # Generate response
            response = await generator.generate_response(question, relevant_docs, simple_context)
        
        # Add bot response to history
        add_to_history(user_id, response, is_bot=True)
        
        # Limit response length for Discord
        if len(response) > 2000:
            response = response[:1997] + "..."
        
        await interaction.followup.send(response)
        print(f"✅ Responded to /ask command successfully")
        
    except Exception as e:
        print(f"❌ Error in ask command: {e}")
        try:
            await interaction.followup.send("Sorry, I encountered an error processing your question. Please try again.")
        except:
            print("Failed to send error message")

@client.tree.command(
    name="sync",
    description="Force sync slash commands (owner only)"
)
async def sync_command(interaction: discord.Interaction):
    """Force sync commands - for debugging."""
    
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ Only the bot owner can use this command.", ephemeral=True)
        return
        
    await interaction.response.defer(ephemeral=True)
    
    try:
        print(f"🔄 Manual sync requested by {interaction.user.name}")
        
        if DISCORD_GUILD_ID:
            guild = discord.Object(id=DISCORD_GUILD_ID)
            client.tree.copy_global_to(guild=guild)
            synced = await client.tree.sync(guild=guild)
            message = f"✅ Synced {len(synced)} commands to this guild."
        else:
            synced = await client.tree.sync()
            message = f"✅ Synced {len(synced)} commands globally (may take up to 1 hour)."
            
        await interaction.followup.send(message, ephemeral=True)
        print(f"✅ Manual sync completed: {len(synced)} commands")
        
    except Exception as e:
        error_msg = f"❌ Failed to sync: {str(e)}"
        await interaction.followup.send(error_msg, ephemeral=True)
        print(f"❌ Manual sync failed: {e}")

@client.tree.command(
    name="status",
    description="Check bot status and configuration"
)
async def status_command(interaction: discord.Interaction):
    """Show bot status information."""
    await interaction.response.defer(ephemeral=True)
    
    try:
        # Get basic stats
        guild_count = len(client.guilds)
        doc_count = len(retriever.documents) if retriever else 0
        
        status_msg = f"""**🤖 StudySage Status**
        
**Bot Info:**
• Connected to {guild_count} server(s)
• Knowledge base: {doc_count} document chunks
• Model: {LLM_MODEL}
• Embedding model: {EMBEDDING_MODEL}

**Commands:**
• `/ask` - Ask AI/ML questions
• `/status` - Show this status
• `/sync` - Force command sync (owner only)

**Bot ID:** `{client.user.id}`
**Guild ID:** `{DISCORD_GUILD_ID if DISCORD_GUILD_ID else 'Global'}`
"""
        
        await interaction.followup.send(status_msg, ephemeral=True)
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error getting status: {e}", ephemeral=True)

def main():
    """Main entry point."""
    if not DISCORD_TOKEN:
        print("❌ Error: DISCORD_TOKEN not set in environment variables.")
        return
    
    if not OWNER_ID:
        print("⚠️ Warning: OWNER_ID not set. /sync command will be disabled.")
    
    print("🚀 Starting StudySage Discord bot...")
    print(f"🏠 Guild ID: {DISCORD_GUILD_ID if DISCORD_GUILD_ID else 'Global sync'}")
    print(f"👤 Owner ID: {OWNER_ID if OWNER_ID else 'Not set'}")
    
    try:
        client.run(DISCORD_TOKEN)
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")