from typing import Annotated

from fastapi import Depends, UploadFile

from src.domain.services.file_service import FileService
from src.domain.services.whisper_service import WhisperService


class TranscribeService:
    def __init__(
        self,
        whisper_service: Annotated[WhisperService, Depends()],
        file_service: Annotated[FileService, Depends()],
    ):
        self.whisper_service = whisper_service
        self.file_service = file_service

    async def transcribe(
        self,
        file: UploadFile,
    ) -> str:
        file_path = None
        try:
            file_path = await self.file_service.save_file(file)
            self.whisper_service.load_model()
            transcribed_text = self.whisper_service.transcribe(file_path)
            return transcribed_text
        finally:
            if file_path:
                self.file_service.delete_file(file_path)
