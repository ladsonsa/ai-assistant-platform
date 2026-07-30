from typing import Any

from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Represents an individual message within a chat session or conversation stream.

    Attributes:
        role: The entity or origin sending the message (e.g., 'user', 'assistant', 'system').
        content: The text or body content of the message.
        metadata: Optional dictionary containing additional contextual details or state key-value pairs.
    """

    role: str
    content: str
    metadata: dict[str, Any] | None = None
