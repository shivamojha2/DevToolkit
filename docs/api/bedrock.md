# AWS Bedrock Integration

## Overview

The AWS Bedrock integration provides a client for interacting with various foundation models available through AWS Bedrock.

## Client Setup

```python
from gen_ai.factory import create_client

client = create_client(
    provider="bedrock",
    api_key="your_aws_access_key",
    model_name="anthropic.claude-3-sonnet-20240229-v1:0",
    region="us-east-1",
    secret_key="your_aws_secret_key",
    session_token="optional_session_token"
)
```

## Available Methods

### Chat Completions

```python
messages = [{"role": "user", "content": "Hello, how are you?"}]
response = client.generate_chat_response(messages)
```

### Streaming Chat Completions

```python
for chunk in client.generate_chat_response_streaming(messages):
    print(chunk, end="", flush=True)
```

### Vision API

```python
messages = [{"role": "user", "content": "What's in this image?"}]
image_paths = ["path/to/image.jpg"]
response = client.generate_chat_response(messages, image_paths=image_paths)
```

## Message Format

- Text messages: `{"role": "user", "content": "message text"}`
- Multimodal messages: `{"role": "user", "content": [{"text": "message text"}, {"image": {...}}]}`

## Error Handling

The client handles common AWS errors and provides detailed error messages for debugging.
