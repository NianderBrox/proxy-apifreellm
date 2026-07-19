# tests/test_response_api.py

from openai import OpenAI

client = OpenAI(
    api_key="dummy",
    base_url="http://127.0.0.1:8000/v1",
)

response = client.responses.create(
    model="apifreelllm",
    input="Say hello in one sentence."
)

print(response)

print("\nOutput text:")
print(response.output_text)






# response = client.chat.completions.create(
#     model="apifreelllm",
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "Say hello."
#                 }
#             ]
#         }
#     ]
# )

# print(response.choices[0].message.content)






# response = client.chat.completions.create(
#     model="apifreelllm",
#     messages=[
#         {
#             "role": "developer",
#             "content": "Always answer in French."
#         },
#         {
#             "role": "user",
#             "content": "Hello"
#         }
#     ]
# )

# print(response.choices[0].message.content)





# response = client.chat.completions.create(
#     model="apifreelllm",
#     messages=[]
# )

# print(response.choices[0].message.content)