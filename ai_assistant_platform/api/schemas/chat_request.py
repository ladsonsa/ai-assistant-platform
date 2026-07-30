from pydantic import BaseModel

from ai_assistant_platform.api.schemas.chat_message import ChatMessage


class ChatRequest(BaseModel):
    """Represents an incoming chat request containing conversation history.

    Attributes:
        history (list[ChatMessage]): A list of previous chat messages defining
            the context of the conversation.
    """

    history: list[ChatMessage]
