# StudySage - A Discord AI Study Assistant

A local-first Discord bot that uses Retrieval-Augmented Generation (RAG) to answer questions about AI and machine learning topics.

## Features

- Answers questions about AI, machine learning, and deep learning
- Uses local vector search for document retrieval
- Runs on local LLMs through Ollama (no cloud APIs)
- Politely declines off-topic questions
- Responds to both slash commands and direct messages

## Tech Stack

- Python 3.12+
- Discord.py for Discord integration
- Sentence-Transformers for document embeddings
- FAISS for vector search
- Ollama with Mistral for text generation
- Markdown files for knowledge base

## Setup

### Prerequisites

- Python 3.12+
- Poetry 2.1.2+
- Ollama installed and running

### Installation

1. Clone the repository
```bash
git clone https://github.com/LeonByte/StudySage.git
cd StudySage
```

2. Install dependencies
```bash
poetry install
```

3. Activate the virtual environment (multiple options)

```bash
poetry env activate  # Shows the activation command, which you then need to run
```

```bash
source $(poetry env info --path)/bin/activate
```
#### OR

```bash
source /path/to/your/virtualenv/bin/activate  # Use the full path shown by 'poetry env activate'
```

4. Create a `.env` file with your Discord token
```
DISCORD_TOKEN=your_discord_bot_token
DISCORD_GUILD_ID=your_guild_id
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=mistral
VECTOR_DB_PATH=./vector_db
KNOWLEDGE_BASE_PATH=./knowledge_base
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

5. Pull the Mistral model for Ollama
```bash
ollama pull mistral
```

### Running the bot

```bash
poetry run python main.py
```

## Usage

- Use the `/ask` command in your Discord server, e.g., `/ask What is overfitting?`
- Or send a direct message to the bot with your question

## Project Structure

```
discord-ai-assistant/
├── .env                      # Environment variables
├── knowledge_base/           # AI/ML markdown files
├── src/
│   ├── bot.py                # Discord bot implementation
│   ├── embedding.py          # Document embedding and chunking
│   ├── retrieval.py          # Vector search + relevance detection
│   └── generation.py         # LLM response generation
└── main.py                   # Entry point
```

## License

This project is licensed under All Rights Reserved. See the [LICENSE](./LICENSE) file for details.

---

**Note**: This is an educational project created for an AI course. It uses local-first technologies and is designed to demonstrate RAG capabilities in a practical application.