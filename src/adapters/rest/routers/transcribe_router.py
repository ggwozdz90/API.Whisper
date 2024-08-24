from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel

from core.container import Container
from src.adapters.rest.dependencies.validate_x_token_dependency import validate_token
from src.application.services.file_service import FileService
from src.application.services.transcribe_service import TranscribeService
from src.core.settings import Settings
from src.domain.exceptions.file_service_exceptions import (
    FileDeleteException,
    FileSaveException,
)
from src.domain.exceptions.whisper_service_exceptions import (
    ModelLoadException,
    TranscriptionException,
)


class TranscribeResponseDTO(BaseModel):
    text: str


router = APIRouter()


@router.post(
    "/transcribe/",
    tags=["transcribe"],
    summary="Transcribe",
    response_description="Transcribe an audio file to text.",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(validate_token)],
)
@inject
async def transcribe(
    file: UploadFile = File(...),
    transcribe_service: TranscribeService = Depends(Provide[Container.transcribe_service]),
    file_service: FileService = Depends(Provide[Container.file_service]),
    settings: Settings = Depends(Provide[Container.settings]),
) -> TranscribeResponseDTO:
    file_path = None
    try:
        file_path = file_service.get_file_path(settings.transcribe_base_path, file.filename)
        await file_service.save_file(file_path, file)
        transcribed_text = await transcribe_service.transcribe(file_path)
        return TranscribeResponseDTO(text=transcribed_text)
    except FileSaveException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}",
        )
    except FileDeleteException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting file: {str(e)}",
        )
    except ModelLoadException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading model: {str(e)}",
        )
    except TranscriptionException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error transcribing file: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error transcribing file: {str(e)}",
        )
    finally:
        if file_path:
            file_service.delete_file(file_path)
