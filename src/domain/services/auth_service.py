import secrets
from typing import Annotated

from fastapi import Depends

from src.data.repositories.token_repository import TokenRepository


class AuthService:
    def __init__(
        self,
        token_repository: Annotated[TokenRepository, Depends()],
    ):
        self.token_repository = token_repository

    def login(
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
