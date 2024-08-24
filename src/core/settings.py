from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.whisper_models import WhisperModel


class Settings(BaseSettings):
    transcribe_base_path: str = "files_to_transcribe"
    whisper_model_type: WhisperModel = WhisperModel.SMALL_EN
    host: str = "127.0.0.1"
    rest_port: str = "8000"

    model_config = SettingsConfigDict(env_file=".env")

    @field_validator("whisper_model_type")
    def validate_whisper_model_type(
        cls,  # noqa
        value: str,
    ) -> WhisperModel:
        try:
            return WhisperModel(value)
        except ValueError:
            raise ValueError(f"Unsupported whisper model: {value}")
