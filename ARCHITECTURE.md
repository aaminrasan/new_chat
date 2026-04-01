# Chatbot Architecture

A chatbot built with LangChain, ChatOllama (Qwen3:8B), and LangGraph with MemorySaver checkpoint for state persistence.

## Architecture Overview

This chatbot uses:
- **LangChain**: For LLM integration and prompt management
- **ChatOllama**: To interact with the Qwen3:8B model via Ollama
- **LangGraph**: For building the conversational flow as a state graph
- **MemorySaver**: For checkpointing and maintaining conversation state

## Components

### 1. State Schema (`ChatState`)
Defines the structure of the conversation state:
- `messages`: List of conversation history
- `user_input`: Current user input
- `response`: Model's response

### 2. Chat Node (`chat_node`)
Single node that:
- Receives user input from the state
- Builds conversation context from message history
- Invokes the Qwen3:8B model via ChatOllama
- Returns updated state with response

### 3. Graph Structure
```
[Entry] → [chat node] → [END]
```

### 4. Memory Checkpoint
- Uses `MemorySaver` for in-memory state persistence
- Supports multi-turn conversations with thread IDs

## Prerequisites

1. Install Ollama: https://ollama.ai
2. Pull the Qwen3:8B model:
   ```bash
   ollama pull qwen3:8b
   ```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the chatbot:
```bash
python chatbot.py
```

Type your messages and use 'quit', 'exit', or 'bye' to end the conversation.

## File Structure

```
/workspace
├── chatbot.py          # Main chatbot implementation
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Future Enhancements

- Add multiple nodes for different conversation flows
- Implement conditional edges for routing
- Add persistent storage (PostgreSQL, Redis)
- Include tools/function calling capabilities
- Add streaming support for real-time responses
