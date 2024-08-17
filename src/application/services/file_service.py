import os
from typing import Annotated

from fastapi import Depends, UploadFile

from src.core.settings import Settings, get_settings
from src.domain.exceptions.file_service_exceptions import (
    FileDeleteException,
    FileSaveException,
)


class FileService:
    def __init__(
        self,
        settings: Annotated[Settings, Depends(get_settings)],
    ):
        self.base_path = settings.transcribe_base_path
        os.makedirs(self.base_path, exist_ok=True)

    async def save_file(
        self,
        file: UploadFile,
    ) -> str:
        if file.filename is None:
            raise FileSaveException("Filename cannot be None")

        file_path = os.path.join(self.base_path, file.filename)
        try:
            with open(file_path, "wb") as f:
                while content := await file.read(1024 * 1024):
                    f.write(content)
        except Exception as e:
            raise FileSaveException(f"Failed to save file: {str(e)}")
        return file_path

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
