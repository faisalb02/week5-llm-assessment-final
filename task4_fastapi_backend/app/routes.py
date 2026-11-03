from fastapi import APIRouter, Depends, HTTPException
from openai import AsyncOpenAI

from app.auth import verify_api_key
from app.database import (
    create_session,
    get_session,
    save_message,
    get_messages,
)
from app.dependencies import get_llm_client
from app.models import MessageRequest


router = APIRouter()


@router.post("/sessions")
async def create_new_session(
    api_key: str = Depends(verify_api_key),
):
    session_id = create_session()

    return {
        "session_id": session_id,
        "message": "Session created successfully"
    }


@router.post("/sessions/{session_id}/chat")
async def chat(
    session_id: str,
    request: MessageRequest,
    api_key: str = Depends(verify_api_key),
    client: AsyncOpenAI = Depends(get_llm_client),
):
    session = get_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    save_message(
        session_id,
        "user",
        request.message
    )

    history = get_messages(session_id)

    try:
        response = await client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                },
                *history
            ]
        )

        answer = response.choices[0].message.content

        if not answer:
            answer = "No response from AI"

        save_message(
            session_id,
            "assistant",
            answer
        )

        return {
            "session_id": session_id,
            "message": request.message,
            "answer": answer
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="LLM service error"
        )


@router.get("/sessions/{session_id}/messages")
async def get_session_messages(
    session_id: str,
    api_key: str = Depends(verify_api_key),
):
    session = get_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    return {
        "session_id": session_id,
        "messages": get_messages(session_id)
    }