from apifreellm_proxy.openai.models.chat import ChatMessage
from apifreellm_proxy.openai.prompt_builder import build_prompt

messages = [
    ChatMessage(
        role="system",
        content="You are a helpful assistant."
    ),
    ChatMessage(
        role="user",
        content="Who discovered gravity?"
    )
]

print(build_prompt(messages))