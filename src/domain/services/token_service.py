import secrets
from typing import Annotated

from fastapi import Depends

from ...data.repositories.token_repository import TokenRepository


class TokenService:
    def __init__(
        self,
        token_repository: Annotated[TokenRepository, Depends()],
    ):
        self.token_repository = token_repository

    def create_token(
        self,
        email: str,
    ) -> str:
        token = secrets.token_urlsafe(32)
        self.token_repository.add(token)
        return token

    def validate_token(
        self,
        token: str,
    ) -> bool:
        return self.token_repository.is_valid(token)
