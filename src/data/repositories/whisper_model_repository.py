import whisper

from src.core.whisper_models import WhisperModel


class WhisperModelRepository:
    def load_model(self) -> whisper.Whisper:
        return whisper.load_model(
            WhisperModel.SMALL_EN.value
        )  # TODO: Convert to start-up configuration
