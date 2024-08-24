import pytest
from pydantic import ValidationError
from pytest_mock import MockerFixture

from src.core.settings import Settings
from src.core.whisper_models import WhisperModel


def test_default_settings(mocker: MockerFixture) -> None:
    mocker.patch.dict(
        "os.environ",
        {
            "TRANSCRIBE_BASE_PATH": "files_to_transcribe",
            "WHISPER_MODEL_TYPE": "small.en",
            "HOST": "127.0.0.1",
            "REST_PORT": "8000",
        },
    )

    settings = Settings()

    assert settings.transcribe_base_path == "files_to_transcribe"
    assert settings.whisper_model_type == WhisperModel.SMALL_EN
    assert settings.host == "127.0.0.1"
    assert settings.rest_port == "8000"


def test_custom_settings(mocker: MockerFixture) -> None:
    mocker.patch.dict(
        "os.environ",
        {
            "TRANSCRIBE_BASE_PATH": "custom_path",
            "WHISPER_MODEL_TYPE": "large",
            "HOST": "192.168.1.1",
            "REST_PORT": "8080",
        },
    )

    settings = Settings()

    assert settings.transcribe_base_path == "custom_path"
    assert settings.whisper_model_type == WhisperModel.LARGE
    assert settings.host == "192.168.1.1"
    assert settings.rest_port == "8080"


def test_invalid_whisper_model_type(mocker: MockerFixture) -> None:
    mocker.patch.dict("os.environ", {"WHISPER_MODEL_TYPE": "INVALID_MODEL"})

    with pytest.raises(ValidationError) as excinfo:
        Settings()

    error_message = str(excinfo.value)
    assert "validation error for Settings" in error_message
    assert "INVALID_MODEL" in error_message
