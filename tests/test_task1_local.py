from task1_sdk_streaming_cost.usage import (
    count_tokens,
    calculate_cost,
)


def test_count_tokens():

    messages = [
        {
            "role": "user",
            "content": "Hello Faisal"
        }
    ]

    result = count_tokens(messages)

    assert result > 0

    print("Token count:", result)


def test_calculate_cost():

    cost = calculate_cost(
        input_tokens=1000,
        output_tokens=500
    )

    assert cost >= 0

    print("Calculated cost:", cost)


def test_empty_messages():

    result = count_tokens([])

    assert result == 0

    print("Empty messages:", result)