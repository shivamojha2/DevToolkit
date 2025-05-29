# OpenAI Examples

This guide provides examples of how to use DevToolkit with OpenAI-compatible APIs.

## Setup

First, create a client:

```python
from gen_ai.factory import create_client

# Create a client
client = create_client(
    provider="openai",
    api_key="your-api-key",
    endpoint="https://api.example.com/v1",
    model_name="gpt-3.5-turbo"
)
```

## Text Generation

### Basic Text Completion

```python
# Generate text from a prompt
response = client.generate_response(
    prompt="Write a short poem about artificial intelligence.",
    max_tokens=100
)
print(response)
```

### Streaming Text Generation

```python
# Stream the response token by token
for token in client.generate_response_stream(
    prompt="Write a short poem about artificial intelligence.",
    max_tokens=100
):
    print(token, end="", flush=True)
```

## Chat

### Basic Chat

```python
# Chat with the model
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What are the key benefits of modular code?"}
]

response = client.generate_chat_response(
    messages=messages,
    max_tokens=150
)
print(response)
```

### Multi-turn Conversation

```python
# First message
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is Python?"}
]
response = client.generate_chat_response(messages=messages)

# Add the response to the conversation
messages.append({"role": "assistant", "content": response})

# Follow-up question
messages.append({"role": "user", "content": "How does it compare to JavaScript?"})
response = client.generate_chat_response(messages=messages)
```

## Image Analysis

### Basic Image Description

```python
# Process an image
image_paths = ["path/to/image.jpg"]
prompt = "Describe the image in detail."

response = client.run_vision_request(
    prompt=prompt,
    image_paths=image_paths,
    max_tokens=150
)
print(response)
```

### Streaming Image Analysis

```python
# Stream the response token by token
for token in client.run_vision_request(
    prompt="Describe the image in detail.",
    image_paths=["path/to/image.jpg"],
    stream=True,
    max_tokens=150
):
    print(token, end="", flush=True)
```

## Batch Processing

### Process Multiple Prompts

```python
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

## Error Handling

### Basic Error Handling

```python
# Get error details with the response
response, error = client.generate_response(
    prompt="Hello",
    return_error=True
)

if error:
    print(f"Error: {error['message']}")
    print(f"Suggestion: {error['suggestion']}")
else:
    print(response)
```

### Batch Error Handling

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

## Next Steps

- Learn more about [Text Completions](../api/text-completions.md)
- Explore [Chat Completions](../api/chat-completions.md)
- Check out [Vision API](../api/vision-api.md)
- See [Batch Processing](../api/batch-processing.md)
- Try [Advanced Features](advanced-features.md)
