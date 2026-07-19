from typing import Any, Literal

from pydantic import ConfigDict
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    model_config = ConfigDict(extra="allow")
    role: Literal["system","developer","user","assistant","tool"]

    content: str | list[Any] | None = None

    tool_calls: list["ToolCall"] | None = None

    tool_call_id: str | None = None

    name: str | None = None


class FunctionDefinition(BaseModel):
    model_config = ConfigDict(extra="allow")
    name: str
    description: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)


class Tool(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: Literal["function"] = "function"
    function: FunctionDefinition


class ChatCompletionRequest(BaseModel):
    model_config = ConfigDict(extra="allow")
    model: str
    messages: list[ChatMessage]

    temperature: float | None = None
    max_tokens: int | None = None
    stream: bool = False

    tools: list[Tool] | None = None
    tool_choice: Any | None = None


class FunctionCall(BaseModel):
    name: str
    arguments: str


class ToolCall(BaseModel):
    id: str
    type: Literal["function"] = "function"
    function: FunctionCall


class ChoiceMessage(BaseModel):
    model_config = ConfigDict(extra="allow")
    role: Literal["assistant"]
    content: str | None = None
    tool_calls: list[ToolCall] | None = None


class Choice(BaseModel):
    index: int
    message: ChoiceMessage
    finish_reason: str


class Usage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list[Choice]
    usage: Usage = Usage()


class ModelCard(BaseModel):
    id: str
    object: str = "model"
    owned_by: str = "apifreellm"


class ModelsResponse(BaseModel):
    object: str = "list"
    data: list[ModelCard]

ChatMessage.model_rebuild()