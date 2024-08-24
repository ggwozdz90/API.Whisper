from src.domain.services.whisper_service import WhisperService


class TranscribeService:
    def __init__(
        self,
        whisper_service: WhisperService,
    ):
        self.whisper_service = whisper_service

    async def transcribe(
        self,
        file_path: str,
    ) -> str:
        self.whisper_service.load_model()
        transcribed_text = self.whisper_service.transcribe(file_path)
        return transcribed_text
