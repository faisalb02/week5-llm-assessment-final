from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import router


app = FastAPI(
    title="Task 4 - Secure FastAPI Backend"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": str(exc.detail)
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):

    status_code = 422

    for error in exc.errors():
        if error["type"] == "string_too_long":
            status_code = 413
            break

    return JSONResponse(
        status_code=status_code,
        content={
            "error": "Request validation failed",
            "details": [
                {
                    "field": ".".join(
                        str(item) for item in error["loc"]
                    ),
                    "message": error["msg"]
                }
                for error in exc.errors()
            ]
        }
    )


app.include_router(router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }