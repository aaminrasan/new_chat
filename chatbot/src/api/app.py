"""FastAPI application for the chatbot API."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from typing import Optional

from src.graphs.builder import build_graph

app = FastAPI(
    title="Chatbot API",
    description="Chatbot API using LangChain, ChatOllama (qwen3:8b), and LangGraph with MemorySaver",
    version="1.0.0"
)

# Build the graph once at startup
graph_app = build_graph()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    thread_id: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    thread_id: str


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return the AI's response.
    
    Args:
        request: ChatRequest containing message and thread_id
        
    Returns:
        ChatResponse with the AI's response and thread_id
    """
    try:
        # Prepare the input state
        config = {
            "configurable": {
                "thread_id": request.thread_id
            }
        }
        
        # Create initial state with user message
        input_state = {
            "messages": [HumanMessage(content=request.message)],
            "thread_id": request.thread_id
        }
        
        # Invoke the graph
        result = graph_app.invoke(input_state, config=config)
        
        # Extract the last message (AI response)
        messages = result.get("messages", [])
        if not messages:
            raise HTTPException(status_code=500, detail="No response generated")
        
        # Get the last AI message
        ai_message = messages[-1]
        response_text = ai_message.content if hasattr(ai_message, 'content') else str(ai_message)
        
        return ChatResponse(
            response=response_text,
            thread_id=request.thread_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to the Chatbot API",
        "endpoints": {
            "POST /chat": "Send a message with thread_id to get a response",
            "GET /health": "Check API health status"
        }
    }
