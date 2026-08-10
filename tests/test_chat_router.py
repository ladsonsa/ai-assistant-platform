from unittest.mock import patch
from fastapi import status
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_chat_endpoint_success() -> None:
    """Tests successful processing of a single-message chat request.

    Verifies that the `/chat` endpoint returns a HTTP 200 status code, correctly
    extracts the user message, forwards an empty preceding history to the orchestrator,
    and returns the expected response payload structure.
    """
    mock_orchestrator_response = {
        "content": "O resultado da operação é 42.",
        "metadata": {},
    }

    payload = {
        "history": [
            {"role": "user", "content": "Qual é a resposta?"}
        ]
    }

    with patch(
        "ai_assistant_platform.api.routers.chat.orchestrator.process_message",
        return_value=mock_orchestrator_response,
    ) as mock_process:
        response = client.post("/chat", json=payload)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["content"] == "O resultado da operação é 42."
        assert data["metadata"] == {}

        mock_process.assert_called_once_with(
            user_message="Qual é a resposta?",
            conversation_history=[],
        )


def test_chat_endpoint_multi_message_history() -> None:
    """Tests successful processing of a chat request with multi-turn history.

    Verifies that the endpoint correctly isolates the final user message from
    the preceding conversation turns when invoking the orchestrator.
    """
    mock_orchestrator_response = {
        "content": "Entendido! Como posso ajudar a seguir?",
        "metadata": {},
    }

    payload = {
        "history": [
            {"role": "user", "content": "Olá!"},
            {"role": "assistant", "content": "Olá, como posso ajudar?"},
            {"role": "user", "content": "Preciso de ajuda com código."},
        ]
    }

    with patch(
        "ai_assistant_platform.api.routers.chat.orchestrator.process_message",
        return_value=mock_orchestrator_response,
    ) as mock_process:
        response = client.post("/chat", json=payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["content"] == "Entendido! Como posso ajudar a seguir?"

        mock_process.assert_called_once_with(
            user_message="Preciso de ajuda com código.",
            conversation_history=[
                {"role": "user", "content": "Olá!"},
                {"role": "assistant", "content": "Olá, como posso ajudar?"},
            ],
        )


def test_chat_endpoint_empty_history_returns_bad_request() -> None:
    """Tests validation behavior when sending an empty message history payload.

    Verifies that the endpoint responds with HTTP 400 Bad Request and the 
    appropriate error detail message.
    """
    payload = {"history": []}

    response = client.post("/chat", json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "History cannot be empty"


def test_chat_endpoint_internal_server_error() -> None:
    """Tests exception handling when the orchestrator raises an unexpected error.

    Verifies that unhandled orchestrator exceptions are caught and transformed
    into an HTTP 500 Internal Server Error response.
    """
    payload = {
        "history": [
            {"role": "user", "content": "Erro proposital"}
        ]
    }

    with patch(
        "ai_assistant_platform.api.routers.chat.orchestrator.process_message",
        side_effect=Exception("Erro inesperado no modelo de IA"),
    ):
        response = client.post("/chat", json=payload)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json()["detail"] == "Erro inesperado no modelo de IA"