from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel


class OpenAIError(BaseModel):
    """
    OpenAI-compatible error object.
    """

    message: str
    type: str
    param: str | None = None
    code: str | None = None


class OpenAIErrorResponse(BaseModel):
    """
    OpenAI-compatible error response.
    """

    error: OpenAIError


HTTP_ERROR_TYPES: dict[int, str] = {
    400: "invalid_request_error",
    401: "authentication_error",
    403: "permission_denied",
    404: "not_found_error",
    409: "conflict_error",
    422: "unprocessable_entity",
    429: "rate_limit_error",
}


class OpenAIProxyError(Exception):
    """
    Base class for all proxy exceptions.
    """

    status_code: ClassVar[int] = 500
    error_type: ClassVar[str] = "server_error"

    def __init__(
        self,
        message: str,
        *,
        param: str | None = None,
        code: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.param = param
        self.code = code
        self.headers = headers or {}


class InvalidRequestError(OpenAIProxyError):
    status_code: ClassVar[int] = 400
    error_type: ClassVar[str] = "invalid_request_error"


class AuthenticationError(OpenAIProxyError):
    status_code: ClassVar[int] = 401
    error_type: ClassVar[str] = "authentication_error"


class PermissionDeniedError(OpenAIProxyError):
    status_code: ClassVar[int] = 403
    error_type: ClassVar[str] = "permission_denied"


class NotFoundError(OpenAIProxyError):
    status_code: ClassVar[int] = 404
    error_type: ClassVar[str] = "not_found_error"


class ConflictError(OpenAIProxyError):
    status_code: ClassVar[int] = 409
    error_type: ClassVar[str] = "conflict_error"


class UnprocessableEntityError(OpenAIProxyError):
    status_code: ClassVar[int] = 422
    error_type: ClassVar[str] = "unprocessable_entity"


class RateLimitError(OpenAIProxyError):
    status_code: ClassVar[int] = 429
    error_type: ClassVar[str] = "rate_limit_error"


class APIConnectionError(OpenAIProxyError):
    status_code: ClassVar[int] = 502
    error_type: ClassVar[str] = "api_connection_error"


class APITimeoutError(OpenAIProxyError):
    status_code: ClassVar[int] = 504
    error_type: ClassVar[str] = "timeout_error"


class InternalServerError(OpenAIProxyError):
    status_code: ClassVar[int] = 500
    error_type: ClassVar[str] = "server_error"


class NotSupportedError(OpenAIProxyError):
    status_code: ClassVar[int] = 400
    error_type: ClassVar[str] = "invalid_request_error"


__all__ = [
    "OpenAIError",
    "OpenAIErrorResponse",
    "HTTP_ERROR_TYPES",
    "OpenAIProxyError",
    "InvalidRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "APIConnectionError",
    "APITimeoutError",
    "InternalServerError",
    "NotSupportedError",
]