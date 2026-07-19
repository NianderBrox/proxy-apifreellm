from apifreellm_proxy.openai.errors import NotSupportedError
from ...backend import backend
from ..models.chat import ChatCompletionRequest, ChatCompletionResponse
from ..prompt_builder import build_prompt
from ..builders.chat import build_chat_response

class Translator:
    """
    Translates OpenAI Chat Completion requests into backend calls.
    """

    def _build_prompt(self, request: ChatCompletionRequest) -> str:
        return build_prompt(
            request.messages,
            request.tools,
        )

    # def __init__(self):
    #     self.backend = ApiFreeLLMBackend()

    async def chat(
        self,
        request: ChatCompletionRequest,
    ) -> ChatCompletionResponse:
        
        if request.stream:
            raise NotSupportedError(
                "Streaming is not supported by the current backend."
            )

        prompt = self._build_prompt(request)

        # print("=" * 80)
        # print("PROMPT")
        # print(prompt)
        # print("=" * 80)

        text = await backend.chat(
            prompt=prompt,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        return build_chat_response(
            text=text,
            model=request.model,
        )


translator = Translator()