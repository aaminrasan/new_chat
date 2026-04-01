"""State definitions for the chatbot."""

from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
import operator


class ChatState(TypedDict):
    """State schema for the chatbot."""
    
    messages: Annotated[Sequence[BaseMessage], operator.add]
    thread_id: str
