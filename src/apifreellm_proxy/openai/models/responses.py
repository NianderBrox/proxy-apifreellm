from typing import Any

from pydantic import BaseModel, ConfigDict

from .chat import Tool, Usage
class OutputFunctionCall(BaseModel):
    id: str

    type: str = "function_call"

    call_id: str

    name: str

    arguments: str

class ResponsesRequest(BaseModel):
    model: str

    input: str | list[Any]

    tools: list[Tool] | None = None

    stream: bool = False

    model_config = ConfigDict(extra="allow")

class OutputText(BaseModel):
    type: str = "output_text"

    text: str

class OutputMessage(BaseModel):
    id: str

    type: str = "message"

    role: str = "assistant"

    content: list[OutputText]

class ResponsesResponse(BaseModel):

    id: str

    object: str = "response"

    created_at: int

    model: str

    output: list[
                OutputMessage
                | OutputFunctionCall
            ]

    usage: Usage

    model_config = ConfigDict(extra="allow")