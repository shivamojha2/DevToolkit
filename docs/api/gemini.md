# Google Gemini Integration

This document describes how to use the Google Gemini integration in the DevToolkit.

## Setup

1. Get your Google API key from Google Cloud Console
2. Set up the following environment variables:

   ```bash
   GOOGLE_API_KEY=your-api-key
   ```

## Usage

You can use the Gemini client through the factory:

```python
from gen_ai.factory import create_client

# Create Gemini client
client = create_client(
    provider="gemini",
    api_key="your-api-key",
    model_name="gemini-pro",  # Optional, defaults to gemini-pro
)

# Run chat completion
response = client.generate_chat_response(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "Hello!",
        }
    ],
    max_tokens=800,
    temperature=1.0,
    top_p=1.0,
)

# Get response
print(response.text)
```

## Parameters

The Gemini client supports the following parameters:

- `api_key` (required): Your Google API key
- `model_name` (optional): The name of the model to use (defaults to "gemini-pro")

### Chat Completion Parameters

When calling `generate_chat_response`, you can use the following parameters:

- `messages`: List of message dictionaries with 'role' and 'content'
- `max_tokens`: Maximum number of tokens to generate
- `temperature`: Sampling temperature (0.0 to 1.0)
- `top_p`: Nucleus sampling parameter (0.0 to 1.0)

### Available Models

- `gemini-pro`: The main Gemini Pro model for text generation
- `gemini-pro-vision`: The Gemini Pro Vision model for multimodal tasks (coming soon)

## Error Handling

The client uses the standard DevToolkit error handling system, raising `APIError` with detailed information when something goes wrong. 