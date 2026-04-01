"""Graph builder for the chatbot."""

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from src.state.chat_state import ChatState
from src.nodes.chat_node import chat_node
from src.config.settings import get_memory_saver


def build_graph() -> StateGraph:
    """
    Build and compile the state graph with MemorySaver checkpoint.
    
    Returns:
        Compiled StateGraph ready to process messages
    """
    # Create the state graph
    workflow = StateGraph(ChatState)
    
    # Add the chat node
    workflow.add_node("chat_node", chat_node)
    
    # Set the entry point
    workflow.set_entry_point("chat_node")
    
    # Add edge from chat_node to END
    workflow.add_edge("chat_node", END)
    
    # Get memory saver checkpoint
    memory = get_memory_saver()
    
    # Compile the graph with memory
    app = workflow.compile(checkpointer=memory)
    
    return app
