from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from src.core.headers import Headers
from src.domain.services.auth_service import AuthService


async def validate_token(
    auth_service: Annotated[AuthService, Depends()],
    x_token: str = Header(..., alias=Headers.X_TOKEN_HEADER),
) -> None:
    token_is_valid = auth_service.validate_token(x_token)
    if not token_is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
