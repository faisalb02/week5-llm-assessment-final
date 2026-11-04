import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import database


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def clear_store():
    database.sessions.clear()
    database.messages.clear()
    app.dependency_overrides.clear()

    yield

    app.dependency_overrides.clear()