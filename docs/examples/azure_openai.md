# Azure OpenAI Integration

This document describes how to use the Azure OpenAI integration in the DevToolkit.

## Setup

1. Create an Azure OpenAI resource in your Azure portal
2. Deploy a model in your Azure OpenAI resource
3. Get your API key and endpoint from the Azure portal
4. Set up the following environment variables:

   ```bash
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key
   AZURE_OPENAI_MODEL_NAME=gpt-4
   AZURE_OPENAI_DEPLOYMENT=your-deployment-name
   AZURE_OPENAI_API_VERSION=2024-02-15-preview  # Optional, defaults to 2024-02-15-preview
   ```

## Usage

You can use the Azure OpenAI client through the factory:

```python
from gen_ai.factory import create_client

# Create Azure OpenAI client
client = create_client(
    provider="azure",
    api_key="your-api-key",
    endpoint="https://your-resource.openai.azure.com/",
    model_name="gpt-4",
    deployment="your-deployment-name",
    api_version="2024-02-15-preview",  # Optional
)

# Run chat completion
response = client.run_chat_completions(
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
    frequency_penalty=0.0,
    presence_penalty=0.0,
)

# Get response
print(response.choices[0].message.content)
```

## Parameters

The Azure OpenAI client supports the following parameters:

- `api_key` (required): Your Azure OpenAI API key
- `endpoint` (required): Your Azure OpenAI endpoint URL
- `model_name` (required): The name of the model to use
- `deployment` (required): The name of your Azure OpenAI deployment
- `api_version` (optional): The API version to use (defaults to "2024-02-15-preview")

### Chat Completion Parameters

When calling `run_chat_completions`, you can use the following parameters:

- `messages` (required): List of message dictionaries with 'role' and 'content'
- `max_tokens` (optional): Maximum number of tokens to generate
- `temperature` (optional): Sampling temperature (default: 1.0)
- `top_p` (optional): Nucleus sampling parameter (default: 1.0)
- `frequency_penalty` (optional): Frequency penalty (default: 0.0)
- `presence_penalty` (optional): Presence penalty (default: 0.0)

## Example

See the complete example in `examples/azure_openai_example.py`.
