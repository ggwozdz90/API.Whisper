from typing import Any

import pytest
from pytest_mock import MockerFixture

from src.data.repositories.whisper_model_repository import WhisperModelRepository
from src.domain.exceptions.whisper_service_exceptions import (
    ModelLoadException,
    TranscriptionException,
)
from src.domain.services.whisper_service import WhisperService


@pytest.fixture
def mock_repository(mocker: MockerFixture) -> Any:
    return mocker.MagicMock(spec=WhisperModelRepository)


@pytest.fixture
def service(mock_repository: WhisperModelRepository) -> WhisperService:
    return WhisperService(whisper_repository=mock_repository)


def test_load_model_success(mocker: MockerFixture, mock_repository: Any, service: WhisperService) -> None:
    mock_model = mocker.patch("whisper.Whisper")()
    mock_repository.load_model.return_value = mock_model

    service.load_model()

    assert service.model is not None
    assert service.model == mock_model
    mock_repository.load_model.assert_called_once()


def test_load_model_failure(mock_repository: Any, service: WhisperService) -> None:
    mock_repository.load_model.side_effect = Exception("Load error")

    with pytest.raises(ModelLoadException) as excinfo:
        service.load_model()

    assert "Failed to load model" in str(excinfo.value)
    mock_repository.load_model.assert_called_once()


def test_transcribe_success(mocker: MockerFixture, service: WhisperService) -> None:
    mock_model = mocker.patch("whisper.Whisper")()
    service.model = mock_model
    mock_model.transcribe.return_value = {"text": "transcribed text"}

    result = service.transcribe("dummy_path")

    assert result == "transcribed text"
    mock_model.transcribe.assert_called_once_with("dummy_path", fp16=False)


def test_transcribe_model_not_loaded(service: WhisperService) -> None:
    service.model = None

    with pytest.raises(TranscriptionException) as excinfo:
        service.transcribe("dummy_path")

    assert "Model is not loaded" in str(excinfo.value)


def test_transcribe_invalid_result(mocker: MockerFixture, service: WhisperService) -> None:
    mock_model = mocker.patch("whisper.Whisper")()
    service.model = mock_model
    mock_model.transcribe.return_value = {"invalid_key": "no text"}

    with pytest.raises(TranscriptionException) as excinfo:
        service.transcribe("dummy_path")

    assert "Invalid transcription result" in str(excinfo.value)
    mock_model.transcribe.assert_called_once_with("dummy_path", fp16=False)


def test_transcribe_failure(mocker: MockerFixture, service: WhisperService) -> None:
    mock_model = mocker.patch("whisper.Whisper")()
    service.model = mock_model
    mock_model.transcribe.side_effect = Exception("Transcription error")

    with pytest.raises(TranscriptionException) as excinfo:
        service.transcribe("dummy_path")

    assert "Failed to transcribe file" in str(excinfo.value)
    mock_model.transcribe.assert_called_once_with("dummy_path", fp16=False)
