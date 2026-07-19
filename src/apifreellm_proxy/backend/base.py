from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class ChatBackend(ABC):

    @abstractmethod
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
        """Return the assistant response as plain text."""
        raise NotImplementedError

    @abstractmethod
    async def stream_chat(
        self,
        *,
        prompt: str,
        model: str,
        temperature: float |None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
    ) -> AsyncIterator[str]:
        """Yield streamed text chunks from the backend."""
        raise NotImplementedError