from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from ai_assistant_platform.api.dependencies import get_chat_service
from main import app


def create_test_client() -> TestClient:
    """Creates a test client with mocked chat service dependency injection.

    Returns:
        TestClient: Configured FastAPI test client with dependency overrides.
    """
    chat_service = AsyncMock()
    chat_service.send.return_value = {
        "content": "O resultado é 30.",
        "metadata": {
            "math_result": 30,
        },
    }

    app.dependency_overrides[get_chat_service] = lambda: chat_service

    return TestClient(app)


def test_cors_allows_configured_origin() -> None:
    """Tests that OPTIONS preflight requests from allowed origins receive valid CORS headers."""
    client = create_test_client()

    try:
        response = client.options(
            "/chat",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            },
        )

        assert response.status_code == 200
        assert (
            response.headers["access-control-allow-origin"] == "http://localhost:3000"
        )
        assert response.headers["access-control-allow-credentials"] == "true"
    finally:
        app.dependency_overrides.clear()


def test_cors_rejects_unconfigured_origin() -> None:
    """Tests that OPTIONS preflight requests from unconfigured origins are rejected."""
    client = create_test_client()

    try:
        response = client.options(
            "/chat",
            headers={
                "Origin": "http://localhost:4000",
                "Access-Control-Request-Method": "POST",
            },
        )

        assert response.status_code == 400
        assert "access-control-allow-origin" not in response.headers
    finally:
        app.dependency_overrides.clear()


def test_post_chat_preserves_cors_behavior() -> None:
    """Tests that POST requests from permitted origins retain valid CORS headers."""
    client = create_test_client()

    try:
        response = client.post(
            "/chat",
            headers={
                "Origin": "http://localhost:3000",
            },
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
        assert (
            response.headers["access-control-allow-origin"] == "http://localhost:3000"
        )
        assert response.headers["access-control-allow-credentials"] == "true"
    finally:
        app.dependency_overrides.clear()
