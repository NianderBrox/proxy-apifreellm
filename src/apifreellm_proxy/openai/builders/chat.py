import time
import uuid

from ..models.chat import (
    ChatCompletionResponse,
    Choice,
    ChoiceMessage,
    Usage,
)
from ..tool_calling import parse_tool_call, remove_tool_markup
from .utils import (
    generate_id,
    generate_timestamp,
)

def build_chat_response(
    text: str,
    model: str,
) -> ChatCompletionResponse:

    tool = parse_tool_call(text)

    if tool is not None:
        return ChatCompletionResponse(
            id=generate_id("chatcmpl"),
            created=generate_timestamp(),
            model=model,
            choices=[
                Choice(
                    index=0,
                    finish_reason="tool_calls",
                    message=ChoiceMessage(
                        role="assistant",
                        content=None,
                        tool_calls=[tool],
                    ),
                )
            ],
            usage=Usage(),
        )

    clean_text = remove_tool_markup(text).strip()

    return ChatCompletionResponse(
        id=generate_id("chatcmpl"),
        created=generate_timestamp(),
        model=model,
        choices=[
            Choice(
                index=0,
                finish_reason="stop",
                message=ChoiceMessage(
                    role="assistant",
                    content=clean_text or None,
                ),
            )
        ],
        usage=Usage(),
    )