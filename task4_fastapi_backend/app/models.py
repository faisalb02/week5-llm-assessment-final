from pydantic import BaseModel, Field


class MessageRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=2000
    )


class SessionResponse(BaseModel):
    session_id: str


class ChatResponse(BaseModel):
    session_id: str
    message: str
    answer: str


class MessageResponse(BaseModel):
    role: str
    content: str