# API Overview

DevToolkit provides a simple and consistent interface for interacting with LLM APIs. The library is designed to be easy to use while providing powerful features for various use cases.

## Core Components

### Client Factory

The main entry point for creating API clients:

```python
from gen_ai.factory import create_client

# Create an OpenAI-compatible client
client = create_client(
    provider="openai",
    api_key="your-api-key",
    endpoint="https://api.example.com/v1",
    model_name="gpt-3.5-turbo"
)
```

### Available Methods

1. **Text Completions**
   - `run_completions()`: Generate text from a prompt
   - `run_completions_stream()`: Stream text generation token by token

2. **Chat Completions**
   - `run_chat_completions()`: Chat with the model using messages
   - `run_chat_completions_stream()`: Stream chat responses

3. **Vision API**
   - `run_vision_request()`: Process images and generate text descriptions

4. **Batch Processing**
   - `run_completions_batch()`: Process multiple prompts efficiently

## Common Parameters

Most methods accept these common parameters:

- `timeout`: Request timeout in seconds (default: 30)
- `guided_json`: JSON schema to enforce structured output
- `return_error`: Return error details along with the result
- `max_tokens`: Maximum number of tokens to generate
- `temperature`: Controls randomness (0.0 to 1.0)
- `top_p`: Controls diversity via nucleus sampling
- `n`: Number of completions to generate

## Error Handling

The library provides comprehensive error handling:

```python
# Get error details with the response
response, error = client.run_completions(
    prompt="Hello",
    return_error=True
)

if error:
    print(f"Error: {error['message']}")
    print(f"Suggestion: {error['suggestion']}")
```

## Next Steps

- Learn about [Text Completions](text-completions.md)
- Explore [Chat Completions](chat-completions.md)
- Check out [Vision API](vision-api.md)
- See [Batch Processing](batch-processing.md)
- Try the [Examples](../examples/basic-usage.md)
