"""Chat node implementation."""

from langchain_core.messages import HumanMessage, AIMessage
from src.config.settings import get_llm
from src.state.chat_state import ChatState


def chat_node(state: ChatState) -> ChatState:
    """
    Process the user's message and generate a response.
    
    Args:
        state: Current chat state containing messages and thread_id
        
    Returns:
        Updated state with the AI's response added to messages
    """
    llm = get_llm()
    
    # Get the last message (user's input)
    messages = state["messages"]
    
    # Invoke the LLM with the conversation history
    response = llm.invoke(messages)
    
    # Return updated state with AI response
    return {
        "messages": [response],
        "thread_id": state["thread_id"]
    }
