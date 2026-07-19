from apifreellm_proxy.openai.tool_calling import parse_tool_call

text = """
<tool_call>
{
    "name":"calculator",
    "arguments":{
        "a":5,
        "b":7
    }
}
</tool_call>
"""

tool = parse_tool_call(text)

print(tool)