import os
from typing import Optional

import pytest

from src.domain.exceptions.file_service_exceptions import FileInvalidFilenameException
from src.domain.services.file_service import FileService


@pytest.fixture
def file_service() -> FileService:
    return FileService()


@pytest.fixture
def base_path() -> str:
    return "/safe/base/path"


def test_get_file_path_valid_filename(file_service: FileService, base_path: str) -> None:
    filename = "valid_filename.txt"
    expected_path = os.path.abspath(os.path.join(base_path, filename))

    result = file_service.get_file_path(base_path, filename)

    assert result == expected_path


def test_get_file_path_none_filename(file_service: FileService, base_path: str) -> None:
    filename: Optional[str] = None

    with pytest.raises(FileInvalidFilenameException) as excinfo:
        file_service.get_file_path(base_path, filename)

    assert str(excinfo.value) == "Filename cannot be None"


def test_get_file_path_invalid_filename(file_service: FileService, base_path: str) -> None:
    filename = "../../etc/passwd"

    with pytest.raises(FileInvalidFilenameException) as excinfo:
        file_service.get_file_path(base_path, filename)

    assert str(excinfo.value) == "Invalid file name"


def test_get_file_path_traversal_characters(file_service: FileService, base_path: str) -> None:
    filename = "valid_filename/../../invalid.txt"

    with pytest.raises(FileInvalidFilenameException) as excinfo:
        file_service.get_file_path(base_path, filename)

    assert str(excinfo.value) == "Invalid file name"


def test_get_file_path_outside_base_path(file_service: FileService, base_path: str) -> None:
    filename = "../outside_base.txt"

    with pytest.raises(FileInvalidFilenameException) as excinfo:
        file_service.get_file_path(base_path, filename)

    assert str(excinfo.value) == "Invalid file name"


def test_get_file_path_outside_base_path_absolute(file_service: FileService, base_path: str) -> None:
    filename = "/outside_base.txt"

    with pytest.raises(FileInvalidFilenameException) as excinfo:
        file_service.get_file_path(base_path, filename)

    assert str(excinfo.value) == "Invalid file name"
