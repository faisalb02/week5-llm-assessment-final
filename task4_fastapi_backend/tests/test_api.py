from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from fastapi import HTTPException

from app.main import app
from app.dependencies import get_llm_client
from app.database import database


API_HEADERS = {
    "x-api-key": "task4-secret-key"
}


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_session(client):
    response = client.post(
        "/sessions",
        headers=API_HEADERS
    )

    assert response.status_code == 200
    assert "session_id" in response.json()


def test_missing_api_key(client):
    response = client.post("/sessions")

    assert response.status_code == 401
    assert response.json()["error"] == "API key missing"


def test_invalid_api_key(client):
    response = client.post(
        "/sessions",
        headers={"x-api-key": "wrong-key"}
    )

    assert response.status_code == 403
    assert response.json()["error"] == "Invalid API key"


def test_chat_session_not_found(client):
    response = client.post(
        "/sessions/unknown/chat",
        headers=API_HEADERS,
        json={"message": "Hello"}
    )

    assert response.status_code == 404
    assert response.json()["error"] == "Session not found"


def test_message_too_long(client):
    response = client.post(
        "/sessions/unknown/chat",
        headers=API_HEADERS,
        json={"message": "a" * 2001}
    )

    assert response.status_code == 413


def test_empty_message(client):
    response = client.post(
        "/sessions/unknown/chat",
        headers=API_HEADERS,
        json={"message": ""}
    )

    assert response.status_code == 422


def test_get_messages(client):
    create_response = client.post(
        "/sessions",
        headers=API_HEADERS
    )

    session_id = create_response.json()["session_id"]

    response = client.get(
        f"/sessions/{session_id}/messages",
        headers=API_HEADERS
    )

    assert response.status_code == 200
    assert response.json()["messages"] == []


def test_get_messages_missing_session(client):
    response = client.get(
        "/sessions/unknown/messages",
        headers=API_HEADERS
    )

    assert response.status_code == 404
    assert response.json()["error"] == "Session not found"


def test_chat_success(client):
    mock_client = AsyncMock()

    fake_response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content="Hello from fake AI"
                )
            )
        ]
    )

    mock_client.chat.completions.create = AsyncMock(
        return_value=fake_response
    )

    app.dependency_overrides[get_llm_client] = (
        lambda: mock_client
    )

    create_response = client.post(
        "/sessions",
        headers=API_HEADERS
    )

    session_id = create_response.json()["session_id"]

    response = client.post(
        f"/sessions/{session_id}/chat",
        headers=API_HEADERS,
        json={"message": "Hello"}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "Hello from fake AI"


def test_llm_failure(client):
    mock_client = AsyncMock()

    mock_client.chat.completions.create = AsyncMock(
        side_effect=Exception("LLM unavailable")
    )

    app.dependency_overrides[get_llm_client] = (
        lambda: mock_client
    )

    create_response = client.post(
        "/sessions",
        headers=API_HEADERS
    )

    session_id = create_response.json()["session_id"]

    response = client.post(
        f"/sessions/{session_id}/chat",
        headers=API_HEADERS,
        json={"message": "Hello"}
    )

    assert response.status_code == 502
    assert response.json()["error"] == "LLM service error"