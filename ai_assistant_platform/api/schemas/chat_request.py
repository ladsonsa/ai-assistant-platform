from typing import List

from pydantic import BaseModel, Field

from ai_assistant_platform.api.schemas.chat_message import ChatMessageSchema

MAX_HISTORY_LENGTH = 100


class ChatRequestSchema(BaseModel):
    """Represents the request payload for chat interactions.

    Attributes:
        history (List[ChatMessageSchema]): The sequence of chat messages representing
            the conversation history.
    """

    history: List[ChatMessageSchema] = Field(max_length=MAX_HISTORY_LENGTH)
