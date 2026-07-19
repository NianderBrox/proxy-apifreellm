from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


llm = ChatOpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="dummy",
    model="apifreellm",
)

llm = llm.bind_tools([add])

# response = llm.invoke("What is 12 + 30?")

# print(response)

response = llm.invoke("12 + 30")

print(response.tool_calls)

tool_result = add.invoke(response.tool_calls[0]["args"])

print(tool_result)