from src.core.headers import Headers


def test_headers() -> None:
    assert Headers.X_TOKEN_HEADER == "X-Token"
    assert Headers.X_PROCESS_TIME_HEADER == "X-Process-Time"
