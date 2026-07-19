from collections.abc import AsyncIterator

from .base import ChatBackend
from ..client import client,ApiFreeLLMClient


class ApiFreeLLMBackend(ChatBackend):

    def __init__(self, client: ApiFreeLLMClient):
        self.client = client
    
    async def chat(
        self,
        *,
        prompt: str,
        model: str,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
    ) -> str:

        response = await self.client.chat(
            message=prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stop=stop,
        )

        return response.response

    async def stream_chat(
        self,
        *,
        prompt: str,
        model: str,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
    ) -> AsyncIterator[str]:

        raise NotImplementedError("Streaming is not implemented yet.")
    
backend = ApiFreeLLMBackend(client)