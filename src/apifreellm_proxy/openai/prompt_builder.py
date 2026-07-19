# from .openai_schema import ChatMessage, Tool


# def build_prompt(
#     messages: list[ChatMessage],
#     tools: list[Tool] | None = None,
# ) -> str:

#     parts: list[str] = []

#     for msg in messages:

#         if msg.role == "system":
#             parts.append(f"System:\n{msg.content}")

#         elif msg.role == "user":
#             parts.append(f"User:\n{msg.content}")

#         elif msg.role == "assistant":
#             parts.append(f"Assistant:\n{msg.content}")

#         elif msg.role == "tool":
#             parts.append(
#                 f"Tool Result ({msg.name}):\n{msg.content}"
#             )

#     if tools:

#         parts.append(
#             """
# You may use tools.

# When a tool is required,
# respond ONLY with valid JSON.

# Example:

# {
#   "tool": "calculator",
#   "arguments": {
#     "a": 5,
#     "b": 7
#   }
# }

# Do not include markdown.
# Do not explain.
# Return only JSON.
# """
#         )

#         for tool in tools:

#             parts.append(
#                 f"""
# Tool:
# Name: {tool.function.name}

# Description:
# {tool.function.description}

# Parameters:
# {tool.function.parameters}
# """
#             )

#     parts.append("Assistant:")

#     return "\n\n".join(parts)


import json
from typing import Any

from .models.chat import ChatMessage, Tool


def content_to_text(content: str | list[Any] | None) -> str:
    if content is None:
        return ""

    if isinstance(content, str):
        return content

    parts: list[str] = []

    for block in content:
        if isinstance(block, dict):
            if block.get("type") == "text":
                parts.append(block.get("text", ""))

    return "\n".join(parts)

from .models.chat import ChatMessage

def normalize_responses_input(
    input_data: str | list[Any],
) -> list[ChatMessage]:
    """
    Convert a Responses API input into ChatMessage objects.
    """

    if isinstance(input_data, str):
        return [
            ChatMessage(
                role="user",
                content=input_data,
            )
        ]

    messages: list[ChatMessage] = []

    for item in input_data:

        if isinstance(item, ChatMessage):
            messages.append(item)
            continue

        if not isinstance(item, dict):
            continue

        role = item.get("role", "user")

        content = item.get("content")

        if isinstance(content, str):
            messages.append(
                ChatMessage(
                    role=role,
                    content=content,
                )
            )
            continue

        if isinstance(content, list):

            text_parts: list[str] = []

            for block in content:

                if (
                    isinstance(block, dict)
                    and block.get("type") in ("input_text", "text")
                ):
                    text_parts.append(
                        block.get("text", "")
                    )

            messages.append(
                ChatMessage(
                    role=role,
                    content="\n".join(text_parts),
                )
            )

    return messages

def build_prompt(
    messages: list[ChatMessage],
    tools: list[Tool] | None = None,
) -> str:

    parts: list[str] = []

    has_tool_result = any(msg.role == "tool" for msg in messages)

    for msg in messages:

        if msg.role in ("system", "developer"):
            text = content_to_text(msg.content)

            if text:
                parts.append(f"{msg.role.capitalize()}:\n{text}")

        elif msg.role == "user":
            text = content_to_text(msg.content)

            if text:
                parts.append(f"User:\n{text}")

        elif msg.role == "assistant":

            text = content_to_text(msg.content)

            if text:
                parts.append(f"Assistant:\n{text}")

            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    parts.append(
                        "\n".join(
                            [
                                "Assistant:",
                                "<tool_call>",
                                "{",
                                f'"id": "{tool_call.id}",',
                                f'"name": "{tool_call.function.name}",',
                                f'"arguments": {tool_call.function.arguments}',
                                "}",
                                "</tool_call>",
                            ]
                        )
                    )

        elif msg.role == "tool":

            text = content_to_text(msg.content)

            parts.append(
                "\n".join(
                    [
                        "Tool Result:",
                        f"Tool Call ID: {msg.tool_call_id}",
                        "",
                        text,
                    ]
                )
            )

    # if tools:
    if tools:

        parts.append(
            "\n".join(
                [
                    "You may use tools.",
                    "",
                    "When a tool is required, respond EXACTLY like this:",
                    "",
                    "<tool_call>",
                    "{",
                    '  "name": "tool_name",',
                    '  "arguments": {',
                    '    "a": 5,',
                    '    "b": 7',
                    "  }",
                    "}",
                    "</tool_call>",
                    "",
                    "Do not use markdown.",
                    "Do not explain.",
                    "Do not output anything except the <tool_call> block.",
                ]
            )
        )

        for tool in tools:

            parts.append(
                "\n".join(
                    [
                        "Tool:",
                        f"Name: {tool.function.name}",
                        "",
                        "Description:",
                        tool.function.description or "",
                        "",
                        "Parameters:",
                        json.dumps(tool.function.parameters, indent=2),
                    ]
                )
            )

    if has_tool_result:
        parts.append(
            "\n".join(
                [
                    "You have already received one or more tool results.",
                    "",
                    "Use the available tool results whenever possible.",
                    "",
                    "Only call another tool if additional information is required to answer the user's request.",
                ]
            )
        )

    parts.append("Assistant:")

    return "\n\n".join(parts)