from apifreellm_proxy.openai.errors import NotSupportedError

from ...backend import backend
from ..prompt_builder import (
    build_prompt,
    normalize_responses_input,
)
from ..builders.responses import build_response
from ..models.responses import (
    ResponsesRequest,
    ResponsesResponse,
)


class ResponsesTranslator:
    """
    Translates OpenAI Responses API requests into backend calls.
    """

    # def __init__(self):
    #     self.backend = ApiFreeLLMBackend()

    async def create(
        self,
        request: ResponsesRequest,
    ) -> ResponsesResponse:
        
        if request.stream:
            raise NotSupportedError(
                "Streaming is not supported by the current backend."
            )

        messages = normalize_responses_input(
            request.input,
        )

        prompt = build_prompt(
            messages,
            request.tools,
        )

        text = await backend.chat(
            prompt=prompt,
            model=request.model,
        )

        return build_response(
            text=text,
            model=request.model,
        )


responses_translator = ResponsesTranslator()