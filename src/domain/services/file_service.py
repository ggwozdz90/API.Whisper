import os
from typing import Optional

from fastapi import UploadFile

from src.domain.exceptions.file_service_exceptions import (
    FileDeleteException,
    FileInvalidFilenameException,
    FileSaveException,
)


class FileService:
    async def save_file(
        self,
        file_path: str,
        file: UploadFile,
    ) -> None:
        if file.filename is None:
            raise FileSaveException("Filename cannot be None")

        directory = os.path.dirname(file_path)
        os.makedirs(directory, exist_ok=True)

        try:
            with open(file_path, "wb") as f:
                while content := await file.read(1024 * 1024):
                    f.write(content)
        except Exception as e:
            raise FileSaveException(f"Failed to save file: {str(e)}")

    def delete_file(
        self,
        file_path: str,
    ) -> None:
        try:
            os.remove(file_path)
        except FileNotFoundError:
            raise FileDeleteException("File not found")
        except Exception as e:
            raise FileDeleteException(f"Failed to delete file: {str(e)}")

    def get_file_path(
        self,
        base_path: str,
        file_name: Optional[str],
    ) -> str:
        if file_name is None:
            raise FileInvalidFilenameException("Filename cannot be None")

        joined_path = os.path.join(base_path, file_name)
        normalized_path = os.path.normpath(joined_path)
        normalized_base_path = os.path.normpath(base_path)
        absolute_path = os.path.abspath(normalized_path)

        if not normalized_path.startswith(normalized_base_path):
            raise FileInvalidFilenameException("Invalid file name")

        return absolute_path
