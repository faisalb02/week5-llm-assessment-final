import pytest
import httpx


from unittest.mock import AsyncMock, patch

from openai import RateLimitError

from task2_retries_async.retry import ask_model


def create_rate_limit_error():

    request = httpx.Request(
        "POST",
        "https://openrouter.ai/api/v1/chat/completions"
    )

    response = httpx.Response(
        429,
        request=request
    )

    return RateLimitError(
        "Rate limit",
        response=response,
        body=None
    )


def create_fake_response():

    fake_message = type(
        "FakeMessage",
        (),
        {"content": "Fake AI response"}
    )()

    fake_choice = type(
        "FakeChoice",
        (),
        {"message": fake_message}
    )()

    fake_response = type(
        "FakeResponse",
        (),
        {"choices": [fake_choice]}
    )()

    return fake_response


@pytest.mark.asyncio
async def test_retry_success():

    fake_response = create_fake_response()

    mock_create = AsyncMock(
        side_effect=[
            create_rate_limit_error(),
            create_rate_limit_error(),
            fake_response
        ]
    )

    with patch(
        "task2_retries_async.retry.client.chat.completions.create",
        new=mock_create
    ):

        result = await ask_model("What is Python?")

    assert result == "Fake AI response"

    assert mock_create.call_count == 3