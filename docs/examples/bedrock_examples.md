# AWS Bedrock Examples

## Basic Chat

```python
from gen_ai.factory import create_client

client = create_client(
    provider="bedrock",
    api_key="your_aws_access_key",
    model_name="anthropic.claude-3-sonnet-20240229-v1:0",
    region="us-east-1",
    secret_key="your_aws_secret_key"
)

messages = [{"role": "user", "content": "Hello, how are you?"}]
response = client.run_chat_completions(messages)
print(response)
```

## Vision API

```python
messages = [{"role": "user", "content": "What's in this image?"}]
image_paths = ["path/to/image.jpg"]
response = client.run_chat_completions(messages, image_paths=image_paths)
print(response)
```

## Streaming

```python
messages = [{"role": "user", "content": "Tell me a story"}]
for chunk in client.run_chat_completions_streaming(messages):
    print(chunk, end="", flush=True)
```

```

Would you like me to:
1. Create any of these documentation files?
2. Add more specific examples?
3. Add more detailed API documentation for specific components?
