from typing import Set


class TokenRepository:
    def __init__(self) -> None:
        self.tokens: Set[str] = set()

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
