import grpc

from adapters.grpc.pb import auth_pb2
from adapters.grpc.pb.auth_pb2_grpc import AuthServiceServicer
from domain.services.auth_service import AuthService


class AuthGrpcService(AuthServiceServicer):  # type: ignore
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def Login(
        self,
        request: auth_pb2.LoginRequest,
        context: grpc.ServicerContext,
    ) -> auth_pb2.LoginResponse:
        try:
            token = self.auth_service.login(request.email)
            if not token:
                context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid credentials")
            return auth_pb2.LoginResponse(token=token)
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
