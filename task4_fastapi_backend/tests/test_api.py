from unittest.mock import AsyncMock

import pytest

from unittest.mock import AsyncMock

from app.database import sessions, messages


@pytest.fixture(autouse=True)
def clear_store():
    sessions.clear()
    messages.clear()


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_session(client):
    response = client.post(
        "/sessions",
        headers={"x-api-key": "task4-secret-key"}
    )

    assert response.status_code == 200
    assert "session_id" in response.json()


def test_missing_api_key(client):
    response = client.post("/sessions")

    assert response.status_code == 401


def test_invalid_api_key(client):
    response = client.post(
        "/sessions",
        headers={"x-api-key": "wrong-key"}
    )

    assert response.status_code == 403


def test_chat_session_not_found(client):
    response = client.post(
        "/sessions/unknown/chat",
        headers={"x-api-key": "task4-secret-key"},
        json={"message": "Hello"}
    )

    assert response.status_code == 404


def test_message_too_long(client):
    response = client.post(
        "/sessions/unknown/chat",
        headers={"x-api-key": "task4-secret-key"},
        json={"message": "a" * 2001}
    )

    assert response.status_code == 422


def test_get_messages(client):
    create_response = client.post(
        "/sessions",
        headers={"x-api-key": "task4-secret-key"}
    )

    session_id = create_response.json()["session_id"]

    response = client.get(
        f"/sessions/{session_id}/messages",
        headers={"x-api-key": "task4-secret-key"}
    )

    assert response.status_code == 200
    assert response.json()["messages"] == []


def test_get_messages_missing_session(client):
    response = client.get(
        "/sessions/unknown/messages",
        headers={"x-api-key": "task4-secret-key"}
    )

    assert response.status_code == 404

def test_chat_success(client, monkeypatch):
    from app.dependencies import get_llm_client

    mock_client = AsyncMock()

    mock_client.chat.completions.create.return_value = (
        type(
            "FakeResponse",
            (),
            {
                "choices": [
                    type(
                        "FakeChoice",
                        (),
                        {
                            "message": type(
                                "FakeMessage",
                                (),
                                {"content": "Hello from fake AI"}
                            )()
                        }
                    )()
                ]
            }
        )()
    )

    from app.main import app

    app.dependency_overrides[get_llm_client] = lambda: mock_client

    create_response = client.post(
        "/sessions",
        headers={"x-api-key": "task4-secret-key"}
    )

    session_id = create_response.json()["session_id"]

    response = client.post(
        f"/sessions/{session_id}/chat",
        headers={"x-api-key": "task4-secret-key"},
        json={"message": "Hello"}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "Hello from fake AI"

    app.dependency_overrides.clear()