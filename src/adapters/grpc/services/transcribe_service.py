import grpc

from adapters.grpc.pb import transcribe_pb2
from adapters.grpc.pb.transcribe_pb2_grpc import TranscribeServiceServicer


class TranscribeService(TranscribeServiceServicer):  # type: ignore
    def Transcribe(
        self,
        request: transcribe_pb2.TranscribeRequest,
        context: grpc.ServicerContext,
    ) -> transcribe_pb2.TranscribeResponse:
        transcribed_text = "dummy_transcription"
        response = transcribe_pb2.TranscribeResponse(text=transcribed_text)
        return response
