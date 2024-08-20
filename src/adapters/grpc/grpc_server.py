from concurrent import futures

import grpc

from adapters.grpc.pb import health_pb2_grpc
from adapters.grpc.services.health_service import HealthService


def start_grpc_server(host: str, port: str) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    health_pb2_grpc.add_HealthServiceServicer_to_server(HealthService(), server)
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    server.wait_for_termination()
