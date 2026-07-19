from .utils import (
    generate_id,
    generate_timestamp,
)
from ..models.chat import Usage
from ..models.responses import (
    OutputFunctionCall,
    OutputMessage,
    OutputText,
    ResponsesResponse,
)
from ..tool_calling import (
    parse_tool_call,
    remove_tool_markup,
)


def build_response(
    *,
    text: str,
    model: str,
) -> ResponsesResponse:

    tool = parse_tool_call(text)

    if tool is not None:
        return ResponsesResponse(
            id=generate_id("resp"),
            created_at=generate_timestamp(),
            model=model,
            output=[
                OutputFunctionCall(
                    id=generate_id("fc"),
                    call_id=tool.id,
                    name=tool.function.name,
                    arguments=tool.function.arguments,
                )
            ],
            usage=Usage(),
        )

    clean_text = remove_tool_markup(text).strip()

    return ResponsesResponse(
        id=generate_id("resp"),
        created_at=generate_timestamp(),
        model=model,
        output=[
            OutputMessage(
                id=generate_id("msg"),
                content=[
                    OutputText(
                        text=clean_text or "",
                    )
                ],
            )
        ],
        usage=Usage(),
    )