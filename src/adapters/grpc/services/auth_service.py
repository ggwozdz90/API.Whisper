import grpc

from adapters.grpc.pb import auth_pb2
from adapters.grpc.pb.auth_pb2_grpc import AuthServiceServicer


class AuthService(AuthServiceServicer):  # type: ignore
    def Login(
        self,
        request: auth_pb2.LoginRequest,
        context: grpc.ServicerContext,
    ) -> auth_pb2.LoginResponse:
        token = "dummy_token"  # nosec
        response = auth_pb2.LoginResponse(token=token)
        return response
