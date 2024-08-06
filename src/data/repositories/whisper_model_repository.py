from typing import Annotated

import whisper
from fastapi import Depends

from ...core.settings import Settings, get_settings


class WhisperModelRepository:
    def __init__(
        self,
        settings: Annotated[Settings, Depends(get_settings)],
    ):
        self.whisper_model_name = settings.whisper_model_name

    def load_model(self) -> whisper.Whisper:
        return whisper.load_model(self.whisper_model_name)
