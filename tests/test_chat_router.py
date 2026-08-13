from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from ai_assistant_platform.api.routers.chat import router


def create_test_client() -> TestClient:
    """Creates an isolated FastAPI test client initialized with the chat router.

    Returns:
        TestClient: An instance of TestClient bound to a newly instantiated FastAPI app.
    """
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_chat_preserves_metadata_in_response() -> None:
    """Tests that the chat endpoint preserves and returns metadata in the response.

    Verifies that metadata returned by the orchestrator (such as math execution details and
    language) is properly forwarded in the API response payload.
    """
    client = create_test_client()

    orchestrator_result = {
        "response": "O resultado é 30.",
        "metadata": {
            "math_result": 30,
            "expression": "20+10",
            "language": "pt",
        },
    }

    with patch(
        "ai_assistant_platform.api.routers.chat.orchestrator"
    ) as orchestrator:
        orchestrator.process_message.return_value = (
            orchestrator_result
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
    """Tests that metadata attached to historical messages is preserved during orchestrator calls.

    Verifies that multi-turn history retains metadata fields when passed down to the
    orchestrator's `process_message` method.
    """
    client = create_test_client()

    orchestrator_result = {
        "response": "O resultado é 15.",
        "metadata": {
            "math_result": 15,
            "expression": "30/2",
            "language": "pt",
        },
    }

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

    with patch(
        "ai_assistant_platform.api.routers.chat.orchestrator"
    ) as orchestrator:
        orchestrator.process_message.return_value = (
            orchestrator_result
        )

        response = client.post(
            "/chat",
            json={
                "history": history,
            },
        )

    assert response.status_code == 200

    call = orchestrator.process_message.call_args

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
    """Tests payload validation behavior when sending an empty conversation history list.

    Verifies that requests with an empty history list are rejected with an HTTP 400 status.
    """
    client = create_test_client()

    response = client.post(
        "/chat",
        json={
            "history": [],
        },
    )

    assert response.status_code == 400