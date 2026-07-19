from apifreellm_proxy.openai.builders.chat import build_chat_response

# resp = build_chat_response(
#     "Hello!",
#     "apifreellm"
# )

resp = build_chat_response("""
<tool_call>
{
"name":"calculator",
"arguments":{
"a":5,
"b":7
}
}
</tool_call>
""","apifreellm")

print(resp.model_dump_json(indent=2))