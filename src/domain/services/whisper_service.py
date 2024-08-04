from threading import Lock
from typing import Annotated

from fastapi import Depends

from ...data.repositories.whisper_model_repository import WhisperModelRepository


class WhisperService:
    _instance = None
    _lock = Lock()
    whisper_repository: WhisperModelRepository

    def __new__(
        cls,
        whisper_repository: Annotated[WhisperModelRepository, Depends()],
    ):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(WhisperService, cls).__new__(cls)
                    cls._instance.whisper_repository = whisper_repository
                    cls._instance.model = None
        return cls._instance

    def load_model(self):
        if self.model is None:
            self.model = self.whisper_repository.load_model()

    def transcribe(
        self,
        file_path: str,
    ) -> str:
        result = self.model.transcribe(file_path, fp16=False)
        return result["text"]
