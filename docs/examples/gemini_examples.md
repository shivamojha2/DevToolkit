# Google Gemini Integration Examples

This document provides examples of how to use the Google Gemini integration in the DevToolkit.

## Setup

1. Get your Google API key from Google Cloud Console
2. Set up the following environment variables:

   ```bash
   GOOGLE_API_KEY=your-api-key
   ```

## Basic Usage

Here's a basic example using the Gemini client through the factory:

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
    temperature=0.7,
    top_p=1.0,
)

# Get response
print(response.text)
```

## Best Practices

1. **API Key Security**: Never hardcode your API key. Use environment variables or secure secret management.
2. **Temperature Control**: 
   - Use lower temperature (0.1-0.3) for factual/analytical tasks
   - Use higher temperature (0.7-0.9) for creative tasks
3. **Error Handling**: Always implement proper error handling to manage API limits and potential failures
4. **Message History**: Keep track of conversation history for context-aware responses
5. **Resource Management**: Close or clean up resources when done with the client

## Complete Example

See the complete example in `examples/gemini_example.py`. 