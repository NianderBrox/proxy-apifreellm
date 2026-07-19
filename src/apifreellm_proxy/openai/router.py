from fastapi import APIRouter

from ..config import get_settings
from .models.chat import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ModelCard,
    ModelsResponse,
)
from .translators.chat import translator
from .errors import NotSupportedError
from .models.responses import (
    ResponsesRequest,
    ResponsesResponse,
)
from .translators.responses import responses_translator


router = APIRouter(
    prefix="/v1",
    tags=["OpenAI"],
)


@router.get(
    "/models",
    response_model=ModelsResponse,
)
async def models():

    settings = get_settings()

    return ModelsResponse(
        data=[
            ModelCard(
                id=settings.model_name,
            )
        ]
    )


@router.post(
    "/chat/completions",
    response_model=ChatCompletionResponse,
)
async def chat(
    request: ChatCompletionRequest,
):
    # For Future Purpose
    # if request.stream:
    #     return await translator.stream_chat(request)

    return await translator.chat(request)


@router.post(
    "/responses",
    response_model=ResponsesResponse,
)
async def responses(
    request: ResponsesRequest,
):

    return await responses_translator.create(request)