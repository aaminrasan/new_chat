# Chatbot API

A structured chatbot API built with LangChain, ChatOllama (qwen3:8b), and LangGraph with MemorySaver checkpoint for conversation persistence.

## Project Structure

```
chatbot/
├── main.py                 # Entry point to run the FastAPI server
├── requirements.txt        # Python dependencies
├── README.md              # This documentation
└── src/
    ├── __init__.py
    ├── api/
    │   ├── __init__.py
    │   └── app.py         # FastAPI application with /chat endpoint
    ├── config/
    │   ├── __init__.py
    │   └── settings.py    # LLM & MemorySaver configuration
    ├── state/
    │   ├── __init__.py
    │   └── chat_state.py  # ChatState TypedDict schema
    ├── nodes/
    │   ├── __init__.py
    │   └── chat_node.py   # Single chat node implementation
    └── graphs/
        ├── __init__.py
        └── builder.py     # StateGraph builder with MemorySaver
```

## Prerequisites

1. **Install Ollama**: Download from [ollama.com](https://ollama.com)
2. **Pull the model**: 
   ```bash
   ollama pull qwen3:8b
   ```
3. **Start Ollama server** (if not running):
   ```bash
   ollama serve
   ```

## Installation

```bash
cd chatbot
pip install -r requirements.txt
```

## Running the API

```bash
python main.py
```

The API will start on `http://localhost:8000`

## API Endpoints

### POST /chat
Send a message with a thread_id to get an AI response.

**Request Body:**
```json
{
    "message": "Hello, how are you?",
    "thread_id": "user123"
}
```

**Response:**
```json
{
    "response": "I'm doing well, thank you for asking! How can I help you today?",
    "thread_id": "user123"
}
```

### GET /health
Check the API health status.

**Response:**
```json
{
    "status": "healthy"
}
```

### GET /
Get API information and available endpoints.

## Usage Examples

### Using curl

```bash
# Send a chat message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "thread_id": "user123"}'

# Check health
curl http://localhost:8000/health
```

### Using Python requests

```python
import requests

# Send a message
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "message": "What is LangGraph?",
        "thread_id": "user123"
    }
)
print(response.json())
```

### Using different thread_ids

Each unique `thread_id` maintains separate conversation history:

```python
# Conversation 1
requests.post("http://localhost:8000/chat", 
              json={"message": "Hi", "thread_id": "alice"})

# Conversation 2 (separate memory)
requests.post("http://localhost:8000/chat", 
              json={"message": "Hello", "thread_id": "bob"})
```

## How MemorySaver Works

The `MemorySaver` checkpoint in LangGraph persists conversation state per `thread_id`. When you send messages with the same `thread_id`, the bot remembers the entire conversation history. Different `thread_id` values create isolated conversation threads.

## Architecture

1. **Client** sends POST request with `message` and `thread_id`
2. **FastAPI** receives the request and creates initial state
3. **LangGraph** processes the message through the `chat_node`
4. **ChatOllama** (qwen3:8b) generates the response
5. **MemorySaver** stores the conversation state for the `thread_id`
6. **Response** is returned to the client

## Extending the Bot

To add more features:

- **Add tools**: Create tool nodes in `src/nodes/`
- **Conditional routing**: Add conditional edges in `src/graphs/builder.py`
- **Multiple nodes**: Add more nodes for specialized tasks
- **Custom checkpoints**: Replace MemorySaver with database-backed checkpoints
