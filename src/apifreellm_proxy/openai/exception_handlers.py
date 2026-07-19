from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .errors import (
    OpenAIError,
    OpenAIErrorResponse,
    OpenAIProxyError,
)
from ..logger import logger


def error_response(
    *,
    status_code: int,
    message: str,
    error_type: str,
    param: str | None = None,
    code: str | None = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    """
    Build an OpenAI-compatible error response.
    """
    return JSONResponse(
        status_code=status_code,
        content=OpenAIErrorResponse(
            error=OpenAIError(
                message=message,
                type=error_type,
                param=param,
                code=code,
            )
        ).model_dump(exclude_none=True),
        headers=headers,
    )


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all global exception handlers.
    """

    @app.exception_handler(OpenAIProxyError)
    async def openai_proxy_error_handler(
        request: Request,
        exc: OpenAIProxyError,
    ):
        logger.warning("%s: %s", exc.error_type, exc.message)

        return error_response(
            status_code=exc.status_code,
            message=exc.message,
            error_type=exc.error_type,
            param=exc.param,
            code=exc.code,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        logger.warning("Validation error: %s", exc.errors())

        message = exc.errors()[0]["msg"] if exc.errors() else "Invalid request."

        return error_response(
            status_code=400,
            message=message,
            error_type="invalid_request_error",
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ):
        logger.warning(
            "HTTPException (%s): %s",
            exc.status_code,
            exc.detail,
        )

        error_type = {
            400: "invalid_request_error",
            401: "authentication_error",
            403: "permission_denied",
            404: "not_found_error",
            409: "conflict_error",
            422: "unprocessable_entity",
            429: "rate_limit_error",
        }.get(exc.status_code, "server_error")

        return error_response(
            status_code=exc.status_code,
            message=str(exc.detail),
            error_type=error_type,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ):
        logger.exception("Unhandled exception")

        return error_response(
            status_code=500,
            message="The server had an error while processing your request.",
            error_type="server_error",
        )