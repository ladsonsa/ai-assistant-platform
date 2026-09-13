import json
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, field_validator

MAX_ROLE_LENGTH = 32
MAX_CONTENT_LENGTH = 8_000
MAX_METADATA_BYTES = 8_192


class ChatMessageSchema(BaseModel):
    """Represents an individual chat message within a conversation payload.

    Attributes:
        role (str): The role of the message sender.
        content (str): The textual body of the message.
        metadata (Optional[Dict[str, Any]]): Additional contextual key-value metadata
            associated with the message. Defaults to an empty dictionary.
    """

    role: str = Field(max_length=MAX_ROLE_LENGTH)
    content: str = Field(max_length=MAX_CONTENT_LENGTH)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def validate_metadata_size(
        cls,
        value: Optional[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:
        """Validate metadata size after UTF-8 JSON serialization."""
        serialized = json.dumps(value, ensure_ascii=False).encode("utf-8")

        if len(serialized) > MAX_METADATA_BYTES:
            raise ValueError(
                "metadata must not exceed 8192 bytes when serialized as UTF-8 JSON."
            )

        return value
