# Batch Processing

The batch processing API allows you to efficiently process multiple prompts in parallel. This is useful for processing large datasets or handling multiple requests simultaneously.

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

# Process multiple prompts
prompts = [
    "List 3 benefits of cloud computing.",
    "What is the capital of France?",
    "Provide a short definition of machine learning."
]

responses = client.generate_batch_response(
    prompts=prompts,
    max_tokens=100
)

# Print results
for prompt, response in zip(prompts, responses):
    print(f"\nPrompt: {prompt}")
    print(f"Response: {response}")
```

## Parameters

### Required Parameters

- `prompts`: List of prompt texts to process

### Optional Parameters

- `max_tokens`: Maximum number of tokens to generate (default: 256)
- `temperature`: Controls randomness (0.0 to 1.0, default: 0)
- `top_p`: Controls diversity via nucleus sampling (default: 1.0)
- `timeout`: Request timeout in seconds (default: 60)
- `concurrent`: Whether to process requests concurrently (default: True)
- `max_concurrent`: Maximum number of concurrent requests (default: 5)
- `return_error`: Return error details along with the results

## Examples

### Basic Batch Processing

```python
prompts = [
    "Write a haiku about spring.",
    "Write a haiku about summer.",
    "Write a haiku about autumn.",
    "Write a haiku about winter."
]

responses = client.generate_batch_response(
    prompts=prompts,
    max_tokens=50,
    temperature=0.7
)
```

### Error Handling

```python
responses, errors = client.generate_batch_response(
    prompts=prompts,
    return_error=True
)

for i, (response, error) in enumerate(zip(responses, errors)):
    print(f"\nPrompt {i+1}:")
    if error:
        print(f"Error: {error['message']}")
        print(f"Suggestion: {error['suggestion']}")
    else:
        print(f"Response: {response}")
```

### Concurrent Processing

```python
# Process 10 prompts with max 3 concurrent requests
responses = client.generate_batch_response(
    prompts=prompts,
    concurrent=True,
    max_concurrent=3,
    max_tokens=100
)
```

## Next Steps

- Learn about [Text Completions](text-completions.md)
- Explore [Chat Completions](chat-completions.md)
- Check out the [OpenAI Examples](../examples/openai_examples.md)
