from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from .llm_client import client, MODEL
from .usage import (
    count_tokens,
    check_token_limit,
    log_usage,
    get_today_usage,
    encoding,
)


app = FastAPI(
    title="Week 5 LLM Assessment - Task 1"
)


class ChatRequest(BaseModel):
    prompt: str


@app.post("/chat/stream")
def chat_stream(request: ChatRequest):

    messages = [
        {
            "role": "user",
            "content": request.prompt
        }
    ]

    try:
        input_tokens = check_token_limit(messages)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    def generate():

        output_text = ""

        try:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                stream=True
            )

            for chunk in stream:

                content = chunk.choices[0].delta.content

                if content:

                    output_text += content

                    yield f"data: {content}\n\n"

            output_tokens = len(
                encoding.encode(output_text)
            )

            log_usage(
                input_tokens,
                output_tokens
            )

        except Exception as error:

            yield f"data: Error: {str(error)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@app.get("/usage")
def usage():

    return get_today_usage()