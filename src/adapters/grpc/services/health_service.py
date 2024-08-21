import grpc

from adapters.grpc.pb import health_pb2
from adapters.grpc.pb.health_pb2_grpc import HealthServiceServicer


class HealthService(HealthServiceServicer):  # type: ignore
    def Check(
        self,
        request: health_pb2.HealthCheckRequest,
        context: grpc.ServicerContext,
    ) -> health_pb2.HealthCheckResponse:
        response = health_pb2.HealthCheckResponse(status="SERVING")
        return response
