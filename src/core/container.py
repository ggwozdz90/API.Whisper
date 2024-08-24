from dependency_injector import containers, providers

from application.services.transcribe_service import TranscribeService
from core.settings import Settings
from data.repositories.token_repository import TokenRepository
from data.repositories.whisper_model_repository import WhisperModelRepository
from domain.services.auth_service import AuthService
from domain.services.file_service import FileService
from domain.services.whisper_service import WhisperService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    settings: Settings = providers.Singleton(Settings)
    token_repository: TokenRepository = providers.Singleton(TokenRepository)
    whisper_model_repository: WhisperModelRepository = providers.Singleton(
        WhisperModelRepository,
        settings=settings,
    )

    whisper_service: WhisperService = providers.Singleton(
        WhisperService,
        whisper_repository=whisper_model_repository,
    )
    auth_service: AuthService = providers.Factory(
        AuthService,
        token_repository=token_repository,
    )
    file_service: FileService = providers.Factory(FileService)

    transcribe_service: TranscribeService = providers.Factory(
        TranscribeService,
        whisper_service=whisper_service,
        file_service=file_service,
        settings=settings,
    )
