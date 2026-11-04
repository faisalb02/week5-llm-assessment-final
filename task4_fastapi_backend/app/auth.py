import secrets

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from app.dependencies import get_settings


api_key_header = APIKeyHeader(
    name="x-api-key",
    auto_error=False
)


def verify_api_key(
    api_key: str = Depends(api_key_header),
    config=Depends(get_settings)
):
    if api_key is None:
        raise HTTPException(
            status_code=401,
            detail="API key missing"
        )

    if not secrets.compare_digest(
        api_key,
        config.API_KEY
    ):
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )

    return api_key