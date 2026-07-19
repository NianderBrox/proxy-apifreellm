import asyncio

from apifreellm_proxy.client import client


async def main():
    response = await client.chat(
        message="Say hello in one sentence."
    )
    print(response)

    await client.close()


asyncio.run(main())