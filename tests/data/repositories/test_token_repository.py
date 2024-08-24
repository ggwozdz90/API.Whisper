from src.data.repositories.token_repository import TokenRepository


def test_add_token() -> None:
    repo = TokenRepository()
    token = "test_token"

    repo.add(token)

    assert token in repo.tokens


def test_is_valid_token() -> None:
    repo = TokenRepository()
    token = "test_token"

    repo.add(token)

    assert repo.is_valid(token) is True
    assert repo.is_valid("invalid_token") is False


def test_add_duplicate_token() -> None:
    repo = TokenRepository()
    token = "test_token"

    repo.add(token)
    repo.add(token)

    assert len(repo.tokens) == 1


def test_is_valid_empty_repository() -> None:
    repo = TokenRepository()

    assert repo.is_valid("any_token") is False
