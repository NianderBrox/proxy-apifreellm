from openai import OpenAI

client = OpenAI(
    api_key="dummy",
    base_url="http://127.0.0.1:8000/v1",
)

response = client.chat.completions.create(
    model="apifreellm",
    messages=[
        {
            "role": "user",
            "content": "Tell me a joke."
        }
    ]
)

print(response.choices[0].message.content)