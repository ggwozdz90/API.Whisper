from pydantic import BaseModel


class TranscribeResponseDTO(BaseModel):
    text: str
