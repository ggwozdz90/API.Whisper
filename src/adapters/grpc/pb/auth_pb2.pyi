"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class LoginRequest(google.protobuf.message.Message):
    """LoginRequest is the request message for logging in."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EMAIL_FIELD_NUMBER: builtins.int
    email: builtins.str
    """The email of the user."""
    def __init__(
        self,
        *,
        email: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["email", b"email"]) -> None: ...

global___LoginRequest = LoginRequest

@typing.final
class LoginResponse(google.protobuf.message.Message):
    """LoginResponse is the response message containing the authentication token."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TOKEN_FIELD_NUMBER: builtins.int
    token: builtins.str
    """The authentication token."""
    def __init__(
        self,
        *,
        token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["token", b"token"]) -> None: ...

global___LoginResponse = LoginResponse
