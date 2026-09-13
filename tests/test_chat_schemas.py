"""Tests for chat schema validation, boundaries, and payload limits."""

import json
from typing import Any

import pytest
from pydantic import ValidationError

from ai_assistant_platform.api.schemas.chat_message import (
    ChatMessageSchema,
)
from ai_assistant_platform.api.schemas.chat_request import (
    ChatRequestSchema,
)


def create_message(
    role: str = "user",
    content: str = "message",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Helper function to build a chat message dictionary with default or custom values.

    Args:
        role: Message role string. Defaults to "user".
        content: Text content of the message. Defaults to "message".
        metadata: Optional metadata dictionary. Defaults to an empty dict.

    Returns:
        dict[str, Any]: Formatted dictionary representation of a chat message.
    """
    return {
        "role": role,
        "content": content,
        "metadata": {} if metadata is None else metadata,
    }


def create_metadata_with_size(size: int) -> dict[str, str]:
    """Helper function to create a metadata dictionary with an exact JSON serialized byte size.

    Args:
        size: Target payload size in bytes when UTF-8 encoded.

    Returns:
        dict[str, str]: Dictionary containing a padded string value matching target size.
    """
    empty_metadata = {"value": ""}
    overhead = len(json.dumps(empty_metadata, ensure_ascii=False).encode("utf-8"))

    return {"value": "a" * (size - overhead)}


@pytest.mark.parametrize(
    "field,value",
    [
        ("role", "a" * 32),
        ("content", "a" * 8_000),
    ],
)
def test_message_accepts_exact_string_limits(field: str, value: str) -> None:
    """Tests that ChatMessageSchema accepts string fields at their maximum allowed character length."""
    message = create_message()
    message[field] = value

    ChatMessageSchema(**message)


@pytest.mark.parametrize(
    "field,value",
    [
        ("role", "a" * 33),
        ("content", "a" * 8_001),
    ],
)
def test_message_rejects_string_limits_exceeded(
    field: str,
    value: str,
) -> None:
    """Tests that ChatMessageSchema raises ValidationError when string fields exceed character limits."""
    message = create_message()
    message[field] = value

    with pytest.raises(ValidationError):
        ChatMessageSchema(**message)


def test_message_accepts_metadata_exact_byte_limit() -> None:
    """Tests that ChatMessageSchema accepts metadata within the maximum byte limit (8192 bytes)."""
    metadata = create_metadata_with_size(8_192)

    serialized_size = len(json.dumps(metadata, ensure_ascii=False).encode("utf-8"))

    assert serialized_size == 8_192

    ChatMessageSchema(**create_message(metadata=metadata))


def test_message_rejects_metadata_byte_limit_exceeded() -> None:
    """Tests that ChatMessageSchema raises ValidationError when metadata exceeds the byte limit."""
    metadata = create_metadata_with_size(8_193)

    serialized_size = len(json.dumps(metadata, ensure_ascii=False).encode("utf-8"))

    assert serialized_size == 8_193

    with pytest.raises(ValidationError):
        ChatMessageSchema(**create_message(metadata=metadata))


def test_request_accepts_exact_history_limit() -> None:
    """Tests that ChatRequestSchema accepts history lists up to the maximum count (100 messages)."""
    history = [create_message() for _ in range(100)]

    ChatRequestSchema(history=history)


def test_request_rejects_history_limit_exceeded() -> None:
    """Tests that ChatRequestSchema raises ValidationError when history length exceeds 100 messages."""
    history = [create_message() for _ in range(101)]

    with pytest.raises(ValidationError):
        ChatRequestSchema(history=history)


def test_request_accepts_empty_history() -> None:
    """Tests that ChatRequestSchema allows an empty history list."""
    ChatRequestSchema(history=[])
