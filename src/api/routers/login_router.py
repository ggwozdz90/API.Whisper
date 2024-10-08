from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.domain.services.auth_service import AuthService


class LoginRequestDTO(BaseModel):
    email: str


class LoginResponseDTO(BaseModel):
    token: str


router = APIRouter()


@router.post(
    "/login",
    tags=["auth"],
    summary="Login",
    response_description="Return a token to authenticate the user.",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponseDTO,
)
def login(
    request: LoginRequestDTO,
    auth_service: Annotated[AuthService, Depends()],
) -> LoginResponseDTO:
    token = auth_service.login(request.email)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return LoginResponseDTO(token=token)
