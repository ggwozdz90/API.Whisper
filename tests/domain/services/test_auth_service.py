import hashlib
from typing import Any

import pytest
from pytest_mock import MockerFixture

from src.data.repositories.token_repository import TokenRepository
from src.domain.services.auth_service import AuthService


@pytest.fixture
def token_repository(mocker: MockerFixture) -> Any:
    return mocker.Mock(spec=TokenRepository)


@pytest.fixture
def auth_service(token_repository: TokenRepository) -> AuthService:
    return AuthService(token_repository)


def test_login(auth_service: AuthService, token_repository: Any, mocker: MockerFixture) -> None:
    email = "test@example.com"
    hashed_email = hashlib.sha256(email.encode()).hexdigest()
    token = "mocked_token"
    combined = f"{hashed_email}.{token}"

    mocker.patch("secrets.token_urlsafe", return_value=token)

    result = auth_service.login(email)

    token_repository.add.assert_called_once_with(combined)
    assert result == combined


def test_validate_token(auth_service: AuthService, token_repository: Any) -> None:
    token = "mocked_token"
    token_repository.is_valid.return_value = True

    result = auth_service.validate_token(token)

    token_repository.is_valid.assert_called_once_with(token)
    assert result is True
