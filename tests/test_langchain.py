from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    api_key="dummy",
    base_url="http://127.0.0.1:8000/v1",
    model="apifreellm",
)

response = llm.invoke("Tell me a joke.")

print(response.content)