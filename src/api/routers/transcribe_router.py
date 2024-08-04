from typing import Annotated

from fastapi import APIRouter, Depends, File, Header, UploadFile, status

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
    file_path = await file_service.save_file(file)
    transcribed_text = transcribe_service.transcribe(file_path)
    file_service.delete_file(file_path)
    return TranscribeResponseDTO(text=transcribed_text)
