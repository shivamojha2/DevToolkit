# Chat Completions

The chat completions API allows you to interact with the model using a chat-like interface. This is useful for conversations, multi-turn interactions, and maintaining context.

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

# Chat with the model
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What are the key benefits of modular code?"}
]

response = client.run_chat_completions(
    messages=messages,
    max_tokens=150
)
print(response)
```

## Streaming

For real-time chat responses, use the streaming API:

```python
# Stream the response token by token
for token in client.run_chat_completions_stream(
    messages=messages,
    max_tokens=150
):
    print(token, end="", flush=True)
```

## Message Format

Messages are formatted as a list of dictionaries with the following structure:

```python
messages = [
    {
        "role": "system",  # System message to set behavior
        "content": "You are a helpful assistant."
    },
    {
        "role": "user",    # User message
        "content": "Hello!"
    },
    {
        "role": "assistant",  # Assistant's previous response
        "content": "Hi! How can I help you?"
    }
]
```

## Parameters

### Required Parameters

- `messages`: List of message dictionaries

### Optional Parameters

- `max_tokens`: Maximum number of tokens to generate (default: 256)
- `temperature`: Controls randomness (0.0 to 1.0, default: 0)
- `top_p`: Controls diversity via nucleus sampling (default: 1.0)
- `n`: Number of completions to generate (default: 1)
- `timeout`: Request timeout in seconds (default: 30)
- `guided_json`: JSON schema to enforce structured output
- `return_error`: Return error details along with the result

## Examples

### Basic Chat

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What are the key benefits of modular code?"}
]

response = client.run_chat_completions(
    messages=messages,
    max_tokens=150,
    temperature=0.7
)
```

### Multi-turn Conversation

```python
# First message
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is Python?"}
]
response = client.run_chat_completions(messages=messages)

# Add the response to the conversation
messages.append({"role": "assistant", "content": response})

# Follow-up question
messages.append({"role": "user", "content": "How does it compare to JavaScript?"})
response = client.run_chat_completions(messages=messages)
```

### Structured Output

```python
from pydantic import BaseModel, Field

class CodeReview(BaseModel):
    overall_score: float = Field(..., ge=0, le=10, description="Overall code quality score")
    strengths: list[str] = Field(..., description="List of code strengths")
    weaknesses: list[str] = Field(..., description="List of code weaknesses")
    suggestions: list[str] = Field(..., description="List of improvement suggestions")

messages = [
    {"role": "system", "content": "You are an expert code reviewer."},
    {"role": "user", "content": "Review this code: def hello(): print('Hello')"}
]

response = client.run_chat_completions(
    messages=messages,
    guided_json=CodeReview.model_json_schema(),
    max_tokens=300
)
```

## Next Steps

- Learn about [Text Completions](text-completions.md)
- Explore [Vision API](vision-api.md)
- Check out the [Examples](../examples/basic-usage.md)
