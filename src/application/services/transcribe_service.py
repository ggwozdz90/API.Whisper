from typing import Annotated

from fastapi import Depends, UploadFile

from core.settings import Settings, get_settings
from src.domain.services.file_service import FileService
from src.domain.services.whisper_service import WhisperService


class TranscribeService:
    def __init__(
        self,
        whisper_service: Annotated[WhisperService, Depends()],
        file_service: Annotated[FileService, Depends()],
        settings: Annotated[Settings, Depends(get_settings)],
    ):
        self.whisper_service = whisper_service
        self.file_service = file_service
        self.transcribe_base_path = settings.transcribe_base_path

    async def transcribe(
        self,
        file: UploadFile,
    ) -> str:
        file_path = None
        try:
            file_path = self.file_service.get_file_path(self.transcribe_base_path, file.filename)
            await self.file_service.save_file(file_path, file)
            self.whisper_service.load_model()
            transcribed_text = self.whisper_service.transcribe(file_path)
            return transcribed_text
        finally:
            if file_path:
                self.file_service.delete_file(file_path)
