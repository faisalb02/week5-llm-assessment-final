Week 5 - LLM Application Assessment

Project Overview

This repository contains four tasks completed as part of the Week 5 LLM Application Assessment.

The project covers LLM API integration, streaming responses, token usage and cost estimation, retry handling, asynchronous programming, tools and memory, and a secure FastAPI backend.

---

Task 1 - SDK Calls, Streaming & Cost

Features

- Integrated LLM APIs using SDK clients
- Tested summarization, classification, and extraction
- Compared streaming and non-streaming responses
- Measured response time and time to first token
- Tracked token usage
- Estimated API costs

Technologies

- Python
- OpenAI SDK
- OpenRouter
- Python time module

---

Task 2 - Retries & Async

Features

- Implemented retry handling for API requests
- Handled API errors and rate limits
- Used asynchronous programming
- Compared sequential and concurrent execution
- Implemented async LLM requests

Technologies

- Python
- AsyncOpenAI
- asyncio
- OpenRouter API

---

Task 3 - Tools & Memory

Features

- Worked with LLM tools
- Implemented tool-related functionality
- Explored memory in LLM applications
- Practiced tool calling and model interactions

Technologies

- Python
- LLM API
- OpenRouter

---

Task 4 - Secure FastAPI Backend

Features

- Created chat sessions
- Sent messages to an AI assistant
- Retrieved session message history
- Implemented API key authentication
- Used Pydantic for request validation
- Added health check endpoint
- Implemented error handling
- Configured CORS
- Used dependency injection
- Tested API endpoints using Pytest
- Mocked LLM responses during testing

API Endpoints

Method| Endpoint| Description
POST| "/sessions"| Create a new session
POST| "/sessions/{session_id}/chat"| Send a chat message
GET| "/sessions/{session_id}/messages"| Retrieve session messages
GET| "/health"| Check API health

Technologies

- Python
- FastAPI
- Pydantic
- OpenAI SDK
- HTTPX
- Pytest

Run the Backend

python -m uvicorn app.main:app --reload

Open Swagger UI:

http://127.0.0.1:8000/docs

Run Tests

python -m pytest -v

Test Results

- 9 tests passed
- Code coverage: 95%

---

Overall Technologies

- Python
- OpenAI SDK
- OpenRouter API
- Asyncio
- FastAPI
- Pydantic
- Pytest
- HTTPX

Assessment Status

Task 1 - Completed

Task 2 - Completed

Task 3 - Completed

Task 4 - Completed

Overall Week 5 Assessment - Completed