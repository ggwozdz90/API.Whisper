from typing import Annotated, Optional

from fastapi import Depends

from ...domain.services.token_service import TokenService
from ...domain.services.user_service import UserService


class AuthService:
    def __init__(
        self,
        user_service: Annotated[UserService, Depends()],
        token_service: Annotated[TokenService, Depends()],
    ):
        self.user_service = user_service
        self.token_service = token_service

    def login(
        self,
        email: str,
    ) -> Optional[str]:
        success = self.user_service.authenticate(email)
        if success:
            token = self.token_service.create_token(email)
            return token
        return None

    def validate_token(
        self,
        token: str,
    ) -> bool:
        return self.token_service.validate_token(token)
