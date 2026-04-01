"""
Chatbot Architecture using LangChain, ChatOllama (Qwen3:8B), and LangGraph
with MemorySaver checkpoint for state persistence.
"""

from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated, List
import operator


# Define the state schema
class ChatState(TypedDict):
    """State schema for the chatbot."""
    messages: Annotated[List[str], operator.add]
    user_input: str
    response: str


def chat_node(state: ChatState) -> ChatState:
    """
    Single node in the graph that handles chat interactions.
    
    Args:
        state: Current chat state containing messages and user input
        
    Returns:
        Updated state with the model's response
    """
    # Initialize the ChatOllama model with Qwen3:8B
    llm = ChatOllama(
        model="qwen3:8b",
        temperature=0.7,
    )
    
    # Get the user's input
    user_message = state["user_input"]
    
    # Build conversation history for context
    conversation_history = "\n".join(state["messages"])
    
    # Create the prompt
    if conversation_history:
        prompt = f"{conversation_history}\nUser: {user_message}"
    else:
        prompt = f"User: {user_message}"
    
    # Generate response
    response = llm.invoke(prompt)
    response_content = response.content if hasattr(response, 'content') else str(response)
    
    return {
        "messages": [f"User: {user_message}", f"Assistant: {response_content}"],
        "response": response_content
    }


def build_chatbot():
    """
    Build and configure the chatbot graph with MemorySaver checkpoint.
    
    Returns:
        Compiled graph ready for execution
    """
    # Create the state graph
    workflow = StateGraph(ChatState)
    
    # Add the chat node
    workflow.add_node("chat", chat_node)
    
    # Set the entry point
    workflow.set_entry_point("chat")
    
    # Add edge from chat to END (single node flow)
    workflow.add_edge("chat", END)
    
    # Initialize MemorySaver for checkpointing
    memory = MemorySaver()
    
    # Compile the graph with checkpointing
    app = workflow.compile(checkpointer=memory)
    
    return app


def run_chatbot():
    """
    Run the chatbot in interactive mode.
    """
    print("=" * 60)
    print("Chatbot initialized with Qwen3:8B (LangChain + LangGraph)")
    print("Type 'quit' or 'exit' to end the conversation")
    print("=" * 60)
    
    # Build the chatbot
    app = build_chatbot()
    
    # Configure thread ID for conversation memory
    config = {"configurable": {"thread_id": "1"}}
    
    # Initial state
    state = {
        "messages": [],
        "user_input": "",
        "response": ""
    }
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nAssistant: Goodbye! Have a great day!")
                break
            
            if not user_input:
                continue
            
            # Update state with user input
            state["user_input"] = user_input
            
            # Invoke the graph
            result = app.invoke(state, config=config)
            
            # Display response
            print(f"\nAssistant: {result['response']}")
            
            # Update messages history from result
            state["messages"] = result["messages"]
            
        except KeyboardInterrupt:
            print("\n\nAssistant: Conversation interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            break


if __name__ == "__main__":
    run_chatbot()
