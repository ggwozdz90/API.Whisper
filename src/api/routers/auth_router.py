from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ...application.services.auth_service import AuthService
from ..dtos.login_request_dto import LoginRequestDTO
from ..dtos.login_response_dto import LoginResponseDTO

router = APIRouter()


@router.post(
    "/login",
    tags=["auth"],
    summary="Login",
    response_description="Return a token to authenticate the user.",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponseDTO,
)
def loginLoginDto(
    request: LoginRequestDTO,
    auth_service: Annotated[AuthService, Depends()],
):
    token = auth_service.login(request.email)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return LoginResponseDTO(token=token)
