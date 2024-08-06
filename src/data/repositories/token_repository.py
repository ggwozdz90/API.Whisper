from threading import Lock
from typing import Set


class TokenRepository:
    _instance = None
    _lock = Lock()
    tokens: Set[str]

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(TokenRepository, cls).__new__(cls)
                    cls._instance.tokens = set()
        return cls._instance

    def add(
        self,
        token: str,
    ) -> None:
        self.tokens.add(token)

    def is_valid(
        self,
        token: str,
    ) -> bool:
        return token in self.tokens
