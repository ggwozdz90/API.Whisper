from typing import Annotated

from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile, status

from ...application.exceptions.file_service_exceptions import (
    FileDeleteException,
    FileSaveException,
)
from ...application.services.file_service import FileService
from ...application.services.transcribe_service import TranscribeService
from ...core.headers import Headers
from ..dependencies.validate_token_dependency import validate_token
from ..dtos.transcribe_response_dto import TranscribeResponseDTO

router = APIRouter()


@router.post(
    "/transcribe/",
    tags=["whisper"],
    summary="Transcribe",
    response_description="Transcribe an audio file to text.",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(validate_token)],
)
async def transcribe(
    file_service: Annotated[FileService, Depends()],
    transcribe_service: Annotated[TranscribeService, Depends()],
    file: UploadFile = File(...),
    x_token: str = Header(..., alias=Headers.X_TOKEN_HEADER),
):
    file_path = None
    try:
        file_path = await save_file(file_service, file)
        transcribed_text = transcribe_file(transcribe_service, file_path)
        return TranscribeResponseDTO(text=transcribed_text)
    finally:
        if file_path:
            delete_file(file_service, file_path)


async def save_file(
    file_service: FileService,
    file: UploadFile,
) -> str:
    try:
        return await file_service.save_file(file)
    except FileSaveException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}",
        )


def transcribe_file(
    transcribe_service: TranscribeService,
    file_path: str,
) -> str:
    try:
        return transcribe_service.transcribe(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error transcribing file: {str(e)}",
        )


def delete_file(
    file_service: FileService,
    file_path: str,
):
    try:
        file_service.delete_file(file_path)
    except FileDeleteException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting file: {str(e)}",
        )
