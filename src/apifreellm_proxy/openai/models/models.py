from pydantic import BaseModel


class ApiFreeLLMRequest(BaseModel):
    message: str
    model: str = "apifreellm"


class ApiFreeLLMResponse(BaseModel):
    success: bool
    response: str