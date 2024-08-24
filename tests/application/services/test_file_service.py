import os
from typing import Optional

import pytest
from fastapi import UploadFile
from pytest_mock import MockerFixture

from src.application.services.file_service import FileService
from src.domain.exceptions.file_service_exceptions import (
    FileDeleteException,
    FileInvalidFilenameException,
    FileSaveException,
)


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


def test_delete_file_success(mocker: MockerFixture, file_service: FileService) -> None:
    mock_remove = mocker.patch("os.remove")

    file_service.delete_file("/fake/file.txt")

    mock_remove.assert_called_once_with("/fake/file.txt")


def test_delete_file_not_found(mocker: MockerFixture, file_service: FileService) -> None:
    mock_remove = mocker.patch("os.remove", side_effect=FileNotFoundError)

    with pytest.raises(FileDeleteException, match="File not found") as excinfo:
        file_service.delete_file("/fake/nonexistent.txt")

    mock_remove.assert_called_once_with("/fake/nonexistent.txt")
    assert str(excinfo.value) == "File not found"


def test_delete_file_other_exception(mocker: MockerFixture, file_service: FileService) -> None:
    mock_remove = mocker.patch("os.remove", side_effect=Exception("Some error"))

    with pytest.raises(FileDeleteException, match="Failed to delete file: Some error") as excinfo:
        file_service.delete_file("/fake/file.txt")

    mock_remove.assert_called_once_with("/fake/file.txt")
    assert str(excinfo.value) == "Failed to delete file: Some error"


@pytest.mark.asyncio
async def test_save_file_success(mocker: MockerFixture, file_service: FileService) -> None:
    mock_makedirs = mocker.patch("os.makedirs")
    mock_open = mocker.mock_open()
    mocker.patch("builtins.open", mock_open)

    mock_file = mocker.Mock(spec=UploadFile)
    mock_file.filename = "test.txt"
    mock_file.read = mocker.AsyncMock(side_effect=[b"data", b""])

    await file_service.save_file("/fake/path/test.txt", mock_file)

    mock_makedirs.assert_called_once_with("/fake/path", exist_ok=True)
    mock_open.assert_called_once_with("/fake/path/test.txt", "wb")
    mock_file.read.assert_awaited()


@pytest.mark.asyncio
async def test_save_file_no_filename(mocker: MockerFixture, file_service: FileService) -> None:
    mock_file = mocker.Mock(spec=UploadFile)
    mock_file.filename = None

    with pytest.raises(FileSaveException, match="Filename cannot be None") as excinfo:
        await file_service.save_file("/fake/path/test.txt", mock_file)

    assert str(excinfo.value) == "Filename cannot be None"


@pytest.mark.asyncio
async def test_save_file_exception(mocker: MockerFixture, file_service: FileService) -> None:
    mock_makedirs = mocker.patch("os.makedirs")
    mock_open = mocker.mock_open()
    mocker.patch("builtins.open", mock_open)

    mock_file = mocker.Mock(spec=UploadFile)
    mock_file.filename = "test.txt"
    mock_file.read = mocker.AsyncMock(side_effect=[b"data", b""])

    mock_open.side_effect = Exception("Some error")

    with pytest.raises(FileSaveException, match="Failed to save file: Some error") as excinfo:
        await file_service.save_file("/fake/path/test.txt", mock_file)

    mock_makedirs.assert_called_once_with("/fake/path", exist_ok=True)
    mock_open.assert_called_once_with("/fake/path/test.txt", "wb")
    mock_file.read.assert_not_awaited()
    assert str(excinfo.value) == "Failed to save file: Some error"


@pytest.mark.asyncio
async def test_save_bytes_success(mocker: MockerFixture, file_service: FileService) -> None:
    mock_makedirs = mocker.patch("os.makedirs")
    mock_open = mocker.mock_open()
    mocker.patch("builtins.open", mock_open)

    file_content = b"test content"

    file_service.save_bytes("/fake/path/test.txt", file_content)

    mock_makedirs.assert_called_once_with("/fake/path", exist_ok=True)
    mock_open.assert_called_once_with("/fake/path/test.txt", "wb")
    mock_open().write.assert_called_once_with(file_content)


@pytest.mark.asyncio
async def test_save_bytes_exception(mocker: MockerFixture, file_service: FileService) -> None:
    mock_makedirs = mocker.patch("os.makedirs")
    mock_open = mocker.mock_open()
    mocker.patch("builtins.open", mock_open)

    file_content = b"test content"

    mock_open.side_effect = Exception("Some error")

    with pytest.raises(FileSaveException, match="Failed to save file: Some error") as excinfo:
        file_service.save_bytes("/fake/path/test.txt", file_content)

    mock_makedirs.assert_called_once_with("/fake/path", exist_ok=True)
    mock_open.assert_called_once_with("/fake/path/test.txt", "wb")
    assert str(excinfo.value) == "Failed to save file: Some error"
