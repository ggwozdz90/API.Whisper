from typing import Annotated

from fastapi import Depends

from ...domain.services.whisper_service import WhisperService


class TranscribeService:
    def __init__(
        self,
        whisper_service: Annotated[WhisperService, Depends()],
    ):
        self.whisper_service = whisper_service

    def transcribe(
        self,
        file_path: str,
    ) -> str:
        self.whisper_service.load_model()
        return self.whisper_service.transcribe(file_path)
