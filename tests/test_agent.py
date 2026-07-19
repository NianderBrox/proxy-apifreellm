from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent


@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


llm = ChatOpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="dummy",
    model="apifreellm",
)

# agent = create_react_agent(
#     model=llm,
#     tools=[add],
# )

# result = agent.invoke(
#     {
#         "messages": [
#             ("user", "What is 12 + 30?")
#         ]
#     }
# )

response = llm.invoke("Explain mario")

print(response)