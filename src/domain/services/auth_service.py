import hashlib
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
        hashed_email = hashlib.sha256(email.encode()).hexdigest()
        token = secrets.token_urlsafe(32)
        combined = f"{hashed_email}.{token}"
        self.token_repository.add(combined)
        return combined

    def validate_token(
        self,
        token: str,
    ) -> bool:
        return self.token_repository.is_valid(token)
