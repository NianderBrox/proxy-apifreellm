from typing import Optional

import httpx

from .config import get_settings
from .openai.models.models import ApiFreeLLMRequest, ApiFreeLLMResponse
from .rate_limiter import RateLimiter
import asyncio
from collections.abc import AsyncIterator

import asyncio
from collections.abc import AsyncIterator

import httpx

from .config import get_settings
from .openai.errors import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    UnprocessableEntityError,
)
from .openai.models.models import ApiFreeLLMRequest, ApiFreeLLMResponse
from .rate_limiter import RateLimiter
from pydantic import ValidationError

class ApiFreeLLMClient:
    def __init__(self):
        settings = get_settings()

        self.endpoint = settings.endpoint
        self.api_key = settings.apifreellm_api_key
        self.timeout = settings.timeout
        self.rate_limiter = RateLimiter(settings.rate_limit_seconds)

        self.client = httpx.AsyncClient(
            timeout=self.timeout,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )

    async def _post(
        self,
        payload: ApiFreeLLMRequest,
    ) -> httpx.Response:

        try:
            return await self.client.post(
                self.endpoint,
                json=payload.model_dump(),
            )

        except httpx.ConnectTimeout as exc:
            raise APITimeoutError("Connection timed out.") from exc

        except httpx.ReadTimeout as exc:
            raise APITimeoutError("Request timed out.") from exc

        except httpx.ConnectError as exc:
            raise APIConnectionError(
                "Could not connect to ApiFreeLLM."
            ) from exc

    async def chat(
        self,
        *,
        message: str,
        model: str = "apifreellm",
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
    ) -> ApiFreeLLMResponse:

        payload = ApiFreeLLMRequest(
            message=message,
            model=model,
        )

        await self.rate_limiter.wait()

        response = await self._post(payload)

        if response.status_code == 429:
            print("Rate limited. Waiting before retrying...")
            await asyncio.sleep(21)

            response = await self._post(payload)

        self._raise_for_status(response)

        try:
            data = response.json()
            return ApiFreeLLMResponse.model_validate(data)

        except ValueError as exc:
            raise InternalServerError(
                "ApiFreeLLM returned invalid JSON."
            ) from exc
        
        except ValidationError as exc:
            raise InternalServerError(
                "ApiFreeLLM returned an invalid response."
            ) from exc

    async def stream_chat(
        self,
        *,
        message: str,
        model: str = "apifreellm",
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
    ) -> AsyncIterator[str]:

        raise NotImplementedError("Streaming is not implemented yet.")

    def _raise_for_status(self, response: httpx.Response) -> None:
        """
        Convert upstream HTTP errors into proxy exceptions.
        """

        status = response.status_code

        if status < 400:
            return

        message = response.text or "ApiFreeLLM returned an error."

        if status == 401:
            raise AuthenticationError(message)

        if status == 403:
            raise PermissionDeniedError(message)

        if status == 404:
            raise NotFoundError(message)

        if status == 409:
            raise ConflictError(message)

        if status == 422:
            raise UnprocessableEntityError(message)

        if status == 429:
            raise RateLimitError(
                message,
                headers={
                    "Retry-After": response.headers.get("Retry-After", "20"),
                },
            )

        raise InternalServerError(message)

    async def close(self):
        await self.client.aclose()


client = ApiFreeLLMClient()