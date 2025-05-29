# Text Completions

The text completions API allows you to generate text from a prompt. This is useful for tasks like text generation, summarization, and completion.

## Basic Usage

```python
from gen_ai.factory import create_client

# Create a client
client = create_client(
    provider="openai",
    api_key="your-api-key",
    endpoint="https://api.example.com/v1",
    model_name="gpt-3.5-turbo"
)

# Generate text
response = client.generate_response(
    prompt="Write a short poem about artificial intelligence.",
    max_tokens=100
)
print(response)
```

## Streaming

For real-time text generation, use the streaming API:

```python
# Stream the response token by token
for token in client.generate_response_stream(
    prompt="Write a short poem about artificial intelligence.",
    max_tokens=100
):
    print(token, end="", flush=True)
```

## Parameters

### Required Parameters

- `prompt`: The text prompt to generate from

### Optional Parameters

- `max_tokens`: Maximum number of tokens to generate (default: 256)
- `temperature`: Controls randomness (0.0 to 1.0, default: 0)
- `top_p`: Controls diversity via nucleus sampling (default: 1.0)
- `n`: Number of completions to generate (default: 1)
- `timeout`: Request timeout in seconds (default: 30)
- `guided_json`: JSON schema to enforce structured output
- `return_error`: Return error details along with the result

## Examples

### Basic Text Generation

```python
response = client.generate_response(
    prompt="Write a short poem about artificial intelligence.",
    max_tokens=100,
    temperature=0.7
)
```

### Structured Output

```python
from pydantic import BaseModel, Field

class Poem(BaseModel):
    title: str = Field(..., description="Title of the poem")
    content: str = Field(..., description="Content of the poem")
    theme: str = Field(..., description="Main theme of the poem")

response = client.generate_response(
    prompt="Write a short poem about artificial intelligence.",
    guided_json=Poem.model_json_schema(),
    max_tokens=200
)
```

### Error Handling

```python
response, error = client.generate_response(
    prompt="Write a short poem about artificial intelligence.",
    return_error=True
)

if error:
    print(f"Error: {error['message']}")
    print(f"Suggestion: {error['suggestion']}")
else:
    print(response)
```

## Next Steps

- Learn about [Chat Completions](chat-completions.md)
- Explore [Vision API](vision-api.md)
- Check out the [OpenAI Examples](../examples/openai_examples.md)
