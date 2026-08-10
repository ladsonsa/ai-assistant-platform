from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ChatMessageSchema(BaseModel):
    """Represents an individual chat message within a conversation payload.

    Attributes:
        role (str): The role of the message sender (e.g., 'user', 'assistant', 'system').
        content (str): The textual body of the message.
        metadata (Optional[Dict[str, Any]]): Additional contextual key-value metadata 
            associated with the message. Defaults to an empty dictionary.
    """

    role: str
    content: str
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)