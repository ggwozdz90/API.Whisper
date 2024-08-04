from typing import Annotated

from fastapi import Depends, HTTPException, Request

from ...application.services.auth_service import AuthService
from ...core.headers import Headers


async def validate_token(
    request: Request,
    auth_service: Annotated[AuthService, Depends()],
):
    token = request.headers.get(Headers.X_TOKEN_HEADER)
    if token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    token_is_valid = auth_service.validate_token(token)
    if not token_is_valid:
        raise HTTPException(status_code=401, detail="Unauthorized")
