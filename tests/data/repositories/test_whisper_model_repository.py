from typing import Any

import pytest
from pytest_mock import MockerFixture

from core.settings import Settings
from src.data.repositories.whisper_model_repository import WhisperModelRepository


@pytest.fixture
def settings(mocker: MockerFixture) -> Any:
    mock_settings = mocker.Mock(spec=Settings)
    mock_settings.whisper_model_type = mocker.Mock()
    mock_settings.whisper_model_type.value = "base"
    return mock_settings


@pytest.fixture
def whisper_model_repository(settings: Settings) -> WhisperModelRepository:
    return WhisperModelRepository(settings)


def test_load_model(
    whisper_model_repository: WhisperModelRepository,
    mocker: MockerFixture,
) -> None:
    mock_load_model = mocker.patch("whisper.load_model")
    mock_model = mocker.Mock()
    mock_load_model.return_value = mock_model

    model = whisper_model_repository.load_model()

    mock_load_model.assert_called_once_with("base")
    assert model == mock_model
