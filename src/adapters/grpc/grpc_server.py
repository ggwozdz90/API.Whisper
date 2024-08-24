from concurrent import futures

import grpc

from adapters.grpc.pb import auth_pb2_grpc, health_pb2_grpc, transcribe_pb2_grpc
from adapters.grpc.services.auth_service import AuthService
from adapters.grpc.services.health_service import HealthService
from adapters.grpc.services.transcribe_service import TranscribeService


def start_grpc_server(
    host: str,
    port: str,
) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    health_pb2_grpc.add_HealthServiceServicer_to_server(HealthService(), server)
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    transcribe_pb2_grpc.add_TranscribeServiceServicer_to_server(TranscribeService(), server)
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    server.wait_for_termination()
