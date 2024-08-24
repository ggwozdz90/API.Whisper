import grpc

from adapters.grpc.pb import transcribe_pb2
from adapters.grpc.pb.transcribe_pb2_grpc import TranscribeServiceServicer
from application.services.file_service import FileService
from application.services.transcribe_service import TranscribeService
from core.settings import Settings
from domain.exceptions.file_service_exceptions import (
    FileDeleteException,
    FileSaveException,
)
from domain.exceptions.whisper_service_exceptions import (
    ModelLoadException,
    TranscriptionException,
)


class TranscribeGrpcService(TranscribeServiceServicer):  # type: ignore
    def __init__(
        self,
        transcribe_service: TranscribeService,
        file_service: FileService,
        settings: Settings,
    ):
        self.transcribe_service = transcribe_service
        self.file_service = file_service
        self.settings = settings

    async def Transcribe(
        self,
        request: transcribe_pb2.TranscribeRequest,
        context: grpc.ServicerContext,
    ) -> transcribe_pb2.TranscribeResponse:
        file_path = None
        try:
            file_path = self.file_service.get_file_path(self.settings.transcribe_base_path, request.filename)
            await self.file_service.save_bytes(file_path, request.file_content)
            transcribed_text = await self.transcribe_service.transcribe(file_path)
            return transcribe_pb2.TranscribeResponse(text=transcribed_text)
        except FileSaveException as e:
            context.abort(grpc.StatusCode.INTERNAL, f"Error saving file: {str(e)}")

        except FileDeleteException as e:
            context.abort(grpc.StatusCode.INTERNAL, f"Error deleting file: {str(e)}")

        except ModelLoadException as e:
            context.abort(grpc.StatusCode.INTERNAL, f"Error loading model: {str(e)}")

        except TranscriptionException as e:
            context.abort(grpc.StatusCode.INTERNAL, f"Error transcribing file: {str(e)}")

        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f"Error transcribing file: {str(e)}")
        finally:
            if file_path:
                self.file_service.delete_file(file_path)
