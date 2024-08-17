from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from src.core.headers import Headers
from src.domain.services.auth_service import AuthService


async def validate_token(
    request: Request,
    auth_service: Annotated[AuthService, Depends()],
) -> None:
    token = request.headers.get(Headers.X_TOKEN_HEADER)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token_is_valid = auth_service.validate_token(token)
    if not token_is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
