import json
from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from ai_assistant_platform.api.dependencies import get_chat_service
from ai_assistant_platform.api.routers.chat import router
from ai_assistant_platform.services.chat_service import ChatService


def create_test_client(
    chat_service: ChatService | None = None,
) -> tuple[TestClient, MagicMock | None]:
    """Creates an isolated FastAPI test client with optional chat service injection.

    Args:
        chat_service (ChatService | None): Optional chat service to inject into the
            application dependency container.

    Returns:
        tuple[TestClient, MagicMock | None]: The test client and the mocked orchestrator
            when a chat service is provided.
    """
    app = FastAPI()
    app.include_router(router)

    orchestrator = None

    if chat_service is not None:
        orchestrator = chat_service._orchestrator
        app.dependency_overrides[get_chat_service] = lambda: chat_service

    return TestClient(app), orchestrator


def test_chat_preserves_metadata_in_response() -> None:
    """Tests that the chat endpoint preserves metadata in the response."""
    orchestrator = MagicMock()

    orchestrator_result = {
        "response": "O resultado é 30.",
        "metadata": {
            "math_result": 30,
            "expression": "20+10",
            "language": "pt",
        },
    }

    orchestrator.process_message.return_value = orchestrator_result

    chat_service = ChatService(
        orchestrator=orchestrator,
    )

    client, _ = create_test_client(
        chat_service=chat_service,
    )

    response = client.post(
        "/chat",
        json={
            "history": [
                {
                    "role": "user",
                    "content": "20 + 10",
                    "metadata": {},
                }
            ]
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["metadata"] == {
        "math_result": 30,
        "expression": "20+10",
        "language": "pt",
    }


def test_chat_preserves_metadata_in_conversation_history() -> None:
    """Tests that historical message metadata is preserved when sent to the orchestrator."""
    orchestrator = MagicMock()

    orchestrator_result = {
        "response": "O resultado é 15.",
        "metadata": {
            "math_result": 15,
            "expression": "30/2",
            "language": "pt",
        },
    }

    orchestrator.process_message.return_value = orchestrator_result

    chat_service = ChatService(
        orchestrator=orchestrator,
    )

    client, _ = create_test_client(
        chat_service=chat_service,
    )

    history = [
        {
            "role": "user",
            "content": "20 + 10",
            "metadata": {},
        },
        {
            "role": "assistant",
            "content": "O resultado é 30.",
            "metadata": {
                "math_result": 30,
                "expression": "20+10",
                "language": "pt",
            },
        },
        {
            "role": "user",
            "content": "agora divida por 2",
            "metadata": {},
        },
    ]

    response = client.post(
        "/chat",
        json={
            "history": history,
        },
    )

    assert response.status_code == 200

    call = orchestrator.process_message.call_args

    assert call.kwargs["user_message"] == "agora divida por 2"

    assert call.kwargs["conversation_history"] == [
        {
            "role": "user",
            "content": "20 + 10",
            "metadata": {},
        },
        {
            "role": "assistant",
            "content": "O resultado é 30.",
            "metadata": {
                "math_result": 30,
                "expression": "20+10",
                "language": "pt",
            },
        },
    ]


def test_chat_rejects_empty_history() -> None:
    """Tests that an empty conversation history is rejected with HTTP 400."""
    client, _ = create_test_client()

    response = client.post(
        "/chat",
        json={
            "history": [],
        },
    )

    assert response.status_code == 400


def test_chat_rejects_history_over_limit() -> None:
    """Tests that history with more than 100 messages returns HTTP 422."""
    client, _ = create_test_client()

    response = client.post(
        "/chat",
        json={
            "history": [
                {
                    "role": "user",
                    "content": "message",
                    "metadata": {},
                }
                for _ in range(101)
            ],
        },
    )

    assert response.status_code == 422


def test_chat_rejects_content_over_limit() -> None:
    """Tests that content longer than 8000 characters returns HTTP 422."""
    client, _ = create_test_client()

    response = client.post(
        "/chat",
        json={
            "history": [
                {
                    "role": "user",
                    "content": "a" * 8_001,
                    "metadata": {},
                }
            ],
        },
    )

    assert response.status_code == 422


def test_chat_rejects_role_over_limit() -> None:
    """Tests that role longer than 32 characters returns HTTP 422."""
    client, _ = create_test_client()

    response = client.post(
        "/chat",
        json={
            "history": [
                {
                    "role": "a" * 33,
                    "content": "message",
                    "metadata": {},
                }
            ],
        },
    )

    assert response.status_code == 422


def test_chat_rejects_metadata_over_limit() -> None:
    """Tests that metadata exceeding 8192 UTF-8 JSON bytes returns HTTP 422."""
    metadata = {"value": "a" * 8_180}

    assert len(json.dumps(metadata, ensure_ascii=False).encode("utf-8")) == 8_193

    client, _ = create_test_client()

    response = client.post(
        "/chat",
        json={
            "history": [
                {
                    "role": "user",
                    "content": "message",
                    "metadata": metadata,
                }
            ],
        },
    )

    assert response.status_code == 422
