import json
import re
import uuid

from .models.chat import ToolCall


TOOL_PATTERN = re.compile(
    r"<tool_call>(.*?)</tool_call>",
    re.DOTALL,
)


def parse_tool_call(text: str) -> ToolCall | None:

    match = TOOL_PATTERN.search(text)

    if not match:
        return None

    try:

        payload = json.loads(match.group(1).strip())

        return ToolCall(
            id=f"call_{uuid.uuid4().hex[:24]}",
            function={
                "name": payload["name"],
                "arguments": json.dumps(
                    payload.get("arguments", {})
                ),
            },
        )

    except Exception:
        return None


def remove_tool_markup(text: str) -> str:

    return TOOL_PATTERN.sub("", text).strip()