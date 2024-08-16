from src.core.whisper_models import WhisperModel


def test_whisper_model_enum():
    assert WhisperModel.TINY.value == "tiny"
    assert WhisperModel.TINY_EN.value == "tiny.en"
    assert WhisperModel.BASE.value == "base"
    assert WhisperModel.BASE_EN.value == "base.en"
    assert WhisperModel.SMALL.value == "small"
    assert WhisperModel.SMALL_EN.value == "small.en"
    assert WhisperModel.MEDIUM.value == "medium"
    assert WhisperModel.MEDIUM_EN.value == "medium.en"
    assert WhisperModel.LARGE.value == "large"
