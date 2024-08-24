import whisper

from core.settings import Settings


class WhisperModelRepository:
    def __init__(
        self,
        settings: Settings,
    ):
        self.whisper_model_type = settings.whisper_model_type

    def load_model(self) -> whisper.Whisper:
        return whisper.load_model(self.whisper_model_type.value)
