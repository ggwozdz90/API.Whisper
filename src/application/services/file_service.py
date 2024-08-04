import os

from fastapi import UploadFile

from src.core.settings import Settings


class FileService:
    def __init__(self):
        self.base_path = (
            Settings.TRANSCRIBE_BASE_PATH
        )  # TODO: Convert to start-up configuration
        os.makedirs(self.base_path, exist_ok=True)

    async def save_file(
        self,
        file: UploadFile,
    ) -> str:
        file_path = os.path.join(self.base_path, file.filename)
        with open(file_path, "wb") as f:
            while content := await file.read(1024 * 1024):
                f.write(content)
        return file_path

    def delete_file(
        self,
        file_path: str,
    ) -> None:
        os.remove(file_path)
