"""Configuration settings for the chatbot."""

from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver

# LLM Configuration
LLM_MODEL = "qwen3:8b"
LLM_BASE_URL = "http://localhost:11434"

def get_llm():
    """Initialize and return the ChatOllama instance."""
    return ChatOllama(
        model=LLM_MODEL,
        base_url=LLM_BASE_URL,
        temperature=0.7,
    )

def get_memory_saver():
    """Initialize and return the MemorySaver checkpoint."""
    return MemorySaver()
