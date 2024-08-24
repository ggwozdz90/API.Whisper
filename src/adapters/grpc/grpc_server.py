from concurrent import futures

import grpc

from adapters.grpc.pb import auth_pb2_grpc, health_pb2_grpc, transcribe_pb2_grpc
from core.container import Container


def start_grpc_server(
    host: str,
    port: str,
    container: Container,
) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    health_pb2_grpc.add_HealthServiceServicer_to_server(container.health_grpc_service(), server)
    auth_pb2_grpc.add_AuthServiceServicer_to_server(container.auth_grpc_service(), server)
    transcribe_pb2_grpc.add_TranscribeServiceServicer_to_server(container.transcribe_grpc_service(), server)
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    server.wait_for_termination()
