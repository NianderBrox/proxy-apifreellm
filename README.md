# ApiFreeLLM OpenAI-Compatible Proxy

> ⚠️ **This project is currently unmaintained.**
>
> It is shared for educational purposes and may not receive future updates. Feel free to fork and modify it for your own use.

An OpenAI-compatible proxy for **ApiFreeLLM** that allows OpenAI-based clients to work without any code changes.

The proxy translates OpenAI API requests into ApiFreeLLM requests and converts the responses back into OpenAI-compatible formats.

## Features

- OpenAI Chat Completions API
- OpenAI Responses API
- Tool Calling Support
- OpenAI-compatible Error Responses
- LangChain Compatible
- LangGraph Compatible
- OpenAI Python SDK Compatible
- Backend Abstraction
- Modular Architecture

---

# Installation

Clone the repository.

```bash
git clone https://github.com/NianderBrox/apifreelllm-proxy.git
cd apifreelllm-proxy
```

Install dependencies.

```bash
uv sync
```

or

```bash
pip install -e .
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
APIFREELLM_API_KEY=your_api_key_here

ENDPOINT=https://apifreellm.com/api/v1/chat

MODEL_NAME=apifreelllm

HOST=127.0.0.1
PORT=8000

TIMEOUT=120

RATE_LIMIT_SECONDS=20
```

---

# Running the Server

```bash
uv run uvicorn apifreelllm_proxy.app:app --host 127.0.0.1 --port 8000
```

Swagger UI will be available at

```
http://127.0.0.1:8000/docs
```

---

# Using with the OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(
    api_key="anything",
    base_url="http://127.0.0.1:8000/v1",
)

response = client.chat.completions.create(
    model="apifreelllm",
    messages=[
        {
            "role": "user",
            "content": "Hello!"
        }
    ],
)

print(response.choices[0].message.content)
```

---

# Responses API

```python
from openai import OpenAI

client = OpenAI(
    api_key="anything",
    base_url="http://127.0.0.1:8000/v1",
)

response = client.responses.create(
    model="apifreelllm",
    input="Hello!"
)

print(response.output_text)
```

---

# Supported Clients

- OpenAI Python SDK
- LangChain
- LangGraph
- OpenAI Agents SDK
- MCP Hosts
- LiteLLM
- OpenWebUI
- Continue.dev
- Cline
- Roo Code

---

# Limitations

- ApiFreeLLM does **not** support streaming.
- Therefore streaming endpoints are **not implemented**.
- Token usage statistics are currently placeholders.
- Multiple tool calls are not yet supported.

---

# Project Status

This repository is **unmaintained**.

It was created as a learning project demonstrating how to build an OpenAI-compatible provider over another LLM service.

Future improvements are unlikely unless contributed by the community.
