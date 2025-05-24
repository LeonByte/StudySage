
# <img src="./assets/logo.svg" alt="StudySage Icon" width="100" height="100"> StudySage - AI-Powered Discord Study Assistant

  **A local-first Discord bot that uses Retrieval-Augmented Generation (RAG) to provide intelligent answers about AI and machine learning topics.**

  [![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
  [![Discord.py](https://img.shields.io/badge/discord.py-2.5+-blue.svg)](https://discordpy.readthedocs.io/)
  [![Version](https://img.shields.io/badge/version-v1.1.0-green.svg)](https://github.com/LeonByte/StudySage/releases)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Local-First](https://img.shields.io/badge/Local--First-Privacy--Focused-green.svg)](https://www.inkandswitch.com/local-first/)

## Overview

StudySage is an intelligent Discord bot designed to help students learn AI and machine learning concepts through interactive Q&A. Built with a focus on **privacy, performance, and pedagogical value**, it demonstrates practical implementation of modern RAG (Retrieval-Augmented Generation) techniques.

### Key Benefits

- **Privacy-First Architecture**: Runs entirely locally with no data sent to external APIs
- **Smart Context Awareness**: Understands conversation flow and follow-up questions  
- **Comprehensive Knowledge Base**: Covers 8 core AI/ML domains with detailed explanations
- **Real-Time Performance**: Fast responses powered by local vector search and LLMs
- **Educational Focus**: Perfect for students, researchers, and AI enthusiasts

## Features

### Core Functionality
- **Knowledge Base**: 8 comprehensive AI/ML topics with 17 document chunks
- **Vector Search**: FAISS-powered semantic similarity matching
- **Local LLM**: Mistral integration via Ollama (fully offline)
- **Conversational Interface**: Maintains context for natural follow-up questions
- **Smart Filtering**: Politely redirects off-topic queries to stay focused

### Technical Highlights
- **Complete RAG Pipeline**: End-to-end retrieval-augmented generation implementation
- **Async Architecture**: Non-blocking Discord interactions for optimal performance
- **Context Memory**: Tracks conversation history for better responses
- **Multi-Interface Support**: Both slash commands (`/ask`) and direct messages
- **Production Ready**: Error handling, timeouts, and graceful degradation

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Bot Framework** | Discord.py 2.5+ | Discord integration and command handling |
| **Embeddings** | Sentence-Transformers | Document and query vectorization |
| **Vector Database** | FAISS | Fast similarity search and retrieval |
| **Language Model** | Mistral (via Ollama) | Response generation and reasoning |
| **Knowledge Base** | Markdown files | Structured AI/ML educational content |
| **Environment** | Python 3.12+ & Poetry | Dependency management and execution |

## Quick Start

### Prerequisites

- **Python 3.12+** installed
- **Poetry 2.1.2+** for dependency management
- **Ollama** installed and running
- **Discord bot token** (from Discord Developer Portal)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/LeonByte/StudySage.git
   cd StudySage
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Activate the virtual environment (multiple options)**
   ```bash
   poetry env activate  # Shows the activation command, which you then need to run
   ```

   ```bash
   source $(poetry env info --path)/bin/activate
   ```

   ```bash
   source /path/to/your/virtualenv/bin/activate  # Alternately, use the full path shown by 'poetry env activate'
   ```

4. **Set up Ollama with Mistral**
   ```bash
   # Install Ollama (if not already installed)
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Pull the Mistral model
   ollama pull mistral
   
   # Verify Ollama is running
   ollama run mistral "Hello, world!"
   ```

5. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   DISCORD_GUILD_ID=your_guild_id_here
   OWNER_ID=your_discord_user_id_here
   OLLAMA_BASE_URL=http://localhost:11434
   LLM_MODEL=mistral
   VECTOR_DB_PATH=./vector_db
   KNOWLEDGE_BASE_PATH=./knowledge_base
   EMBEDDING_MODEL=all-MiniLM-L6-v2
   ```

6. **Run the bot**
   ```bash
   poetry run python main.py
   ```

### Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application and bot
3. Enable **Message Content Intent** in Bot settings
4. Copy the bot token to your `.env` file
5. **Get your Discord User ID**: Enable Developer Mode in Discord settings, right-click your username, and copy your ID for the `OWNER_ID` in `.env`
6. **Invite bot with correct permissions**: Use this URL format, replacing `YOUR_BOT_CLIENT_ID` with your Application ID:
   ```
   https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_CLIENT_ID&permissions=2147568640&scope=bot%20applications.commands
   ```
   **Important**: The `applications.commands` scope is required for slash commands to work.

## Usage Examples

### Slash Commands (Recommended)
```
/ask What is overfitting in machine learning?
/ask How do CNNs work in computer vision?
/ask Explain the difference between supervised and unsupervised learning
```

### Direct Messages
Simply DM the bot with your questions:
```
What is RAG?
How does backpropagation work?
What are the main challenges in NLP?
```

### Conversation Flow
```
Student: What is a neural network?
StudySage: [Detailed explanation of neural networks...]

Student: How do they learn?
StudySage: [Explains backpropagation with context from previous question...]
```

## Project Structure

```
StudySage/
├── README.md                           # Project documentation
├── LICENSE                             # MIT License
├── pyproject.toml                      # Poetry configuration
├── .env                                # Environment variables (create this)
├── assets/                             # Project assets
│   └── logo.svg                        # StudySage logo
├── knowledge_base/                     # AI/ML knowledge base (8 topics)
│   ├── introduction-to-ml.md           # ML fundamentals & learning types
│   ├── deep-learning-basics.md         # Neural networks & backpropagation  
│   ├── model-evaluation.md             # Metrics & validation strategies
│   ├── overfitting-and-regularization.md # Bias-variance & regularization
│   ├── natural-language-processing.md # NLP & transformer architectures
│   ├── computer-vision-basics.md       # CNNs & image processing
│   ├── ml-project-pipeline.md          # MLOps & deployment workflows
│   └── rag-and-llms.md                 # RAG systems & vector databases
├── src/                                # Source code
│   ├── bot.py                          # Discord bot & conversation logic
│   ├── embedding.py                    # Document processing & embeddings
│   ├── retrieval.py                    # Vector search & relevance detection
│   └── generation.py                   # LLM integration & response generation
├── vector_db/                          # Generated vector database (auto-created)
├── main.py                             # Application entry point
├── debug_relevance.py                  # Relevance threshold testing
└── debug_vector_search.py              # Vector search debugging
```

## RAG Architecture

StudySage implements a complete RAG (Retrieval-Augmented Generation) pipeline:

```
User Query → Relevance Check → Vector Search → Document Retrieval → LLM Generation → Response
     ↓              ↓               ↓               ↓                ↓              ↓
"What is CNN?" → AI/ML topic? → Find similar → Get CNN docs → Generate with → Detailed answer
                     ✅           embeddings     context        context       about CNNs
```

### Key Components

1. **Document Processing**: Markdown files are chunked into text segments and converted to vector embeddings
2. **Relevance Detection**: Query classification to ensure AI/ML focus and maintain topic boundaries
3. **Vector Retrieval**: Semantic search through knowledge base using FAISS for fast similarity matching
4. **Context Integration**: Combine retrieved documents with conversation history for coherent responses
5. **Response Generation**: Local LLM generates educational, contextual responses based on retrieved content

## Troubleshooting

### Slash Commands Not Appearing
- **Issue**: `/ask` command doesn't show up in Discord
- **Solution**: Ensure bot was invited with `applications.commands` scope and `Use Application Commands` permission
- **Debug**: Use `/sync` command (owner only) to force re-sync

### "Synced 0 commands" in Console  
- **Issue**: Bot shows "Synced 0 commands" but commands are defined
- **Solution**: This is fixed in v1.1.0+ with proper command tree handling

### Response Timeouts
- **Issue**: "The response is taking too long" error
- **Solution**: 
  - Ensure Ollama is running: `ollama list`
  - Check if Mistral model is pulled: `ollama pull mistral`
  - Restart Ollama service if needed

### Bot Keeps Disconnecting
- **Issue**: Connection drops and heartbeat warnings
- **Solution**: This is fixed in v1.1.0+ with async HTTP implementation

### Common Setup Issues
- **Missing Dependencies**: Run `poetry install` to ensure all packages are installed
- **Environment Variables**: Verify all required variables are set in `.env`
- **Ollama Connection**: Test with `curl http://localhost:11434/api/tags`

## Educational Value

This project demonstrates:

- **Modern RAG Implementation**: Complete pipeline from documents to responses
- **Vector Database Usage**: Practical application of semantic search with FAISS
- **Local LLM Integration**: Privacy-preserving AI without external API dependencies  
- **Conversation Design**: Context-aware chatbot development patterns
- **Production Patterns**: Error handling, async programming, and deployment considerations

## Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git switch -c feature/amazing-feature`
3. **Add your changes**: Focus on educational content or technical improvements
4. **Test thoroughly**: Ensure your changes work with the existing RAG pipeline
5. **Submit a pull request**: Include a clear description of your changes

### Contribution Ideas
- Add new AI/ML knowledge base topics
- Improve retrieval accuracy or response quality  
- Enhance user experience and conversation flow
- Add evaluation metrics and testing frameworks
- Optimize performance for larger knowledge bases

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **[Ollama](https://ollama.com/)** for local LLM hosting
- **[FAISS](https://github.com/facebookresearch/faiss)** for efficient vector search
- **[Sentence-Transformers](https://www.sbert.net/)** for semantic embeddings
- **[Discord.py](https://discordpy.readthedocs.io/)** for Discord integration
- **Open source community** for inspiration and tools

---

<div align="center">
  <sub>Built with ❤️ for AI education • <a href="#quick-start">Get Started</a> • <a href="https://github.com/LeonByte/StudySage/issues">Report Bug</a> • <a href="https://github.com/LeonByte/StudySage/issues">Request Feature</a></sub>
</div>