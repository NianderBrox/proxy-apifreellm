import asyncio

from apifreellm_proxy.openai.models.chat import ChatCompletionRequest
from apifreellm_proxy.openai.translators.chat import translator


async def main():

    request = ChatCompletionRequest(
        model="apifreellm",
        messages=[
            {
                "role": "system",
                "content": "You are helpful."
            },
            {
                "role": "user",
                "content": "Tell me a joke."
            }
        ]
    )

    response = await translator.chat(request)

    print(response.model_dump_json(indent=2))


asyncio.run(main())