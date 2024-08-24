from typing import Optional

import whisper

from src.data.repositories.whisper_model_repository import WhisperModelRepository
from src.domain.exceptions.whisper_service_exceptions import (
    ModelLoadException,
    TranscriptionException,
)


class WhisperService:
    def __init__(
        self,
        whisper_repository: WhisperModelRepository,
    ):
        self.whisper_repository = whisper_repository

    model: Optional[whisper.Whisper] = None

    def load_model(self) -> None:
        if self.model is None:
            try:
                self.model = self.whisper_repository.load_model()
            except Exception as e:
                raise ModelLoadException(f"Failed to load model: {str(e)}")

    def transcribe(
        self,
        file_path: str,
    ) -> str:
        try:
            if self.model is None:
                raise TranscriptionException("Model is not loaded")

            result = self.model.transcribe(file_path, fp16=False)
            if not isinstance(result, dict) or "text" not in result:
                raise TranscriptionException("Invalid transcription result")

            return str(result["text"])
        except Exception as e:
            raise TranscriptionException(f"Failed to transcribe file: {str(e)}")
