from typing import Any

import pytest
from pytest_mock import MockerFixture

from application.services.transcribe_service import TranscribeService
from src.domain.services.whisper_service import WhisperService


@pytest.fixture
def mock_whisper_service(mocker: MockerFixture) -> Any:
    mock_service = mocker.Mock(spec=WhisperService)
    mock_service.load_model.return_value = None
    return mock_service


@pytest.mark.asyncio
async def test_transcribe_success(mock_whisper_service: Any) -> None:
    mock_whisper_service.transcribe.return_value = "This is transcribed text"
    transcribe_service = TranscribeService(whisper_service=mock_whisper_service)

    transcribed_text = await transcribe_service.transcribe("path/to/file.wav")

    mock_whisper_service.load_model.assert_called_once()
    mock_whisper_service.transcribe.assert_called_once_with("path/to/file.wav")
    assert transcribed_text == "This is transcribed text"


@pytest.mark.asyncio
async def test_transcribe_whisper_service_error(mock_whisper_service: Any) -> None:
    mock_whisper_service.transcribe.side_effect = Exception("Whisper service error")
    transcribe_service = TranscribeService(whisper_service=mock_whisper_service)

    with pytest.raises(Exception) as excinfo:
        await transcribe_service.transcribe("path/to/file.wav")

    assert str(excinfo.value) == "Whisper service error"
