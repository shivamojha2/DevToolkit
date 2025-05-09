# Client Factory

## Overview

The client factory provides a unified interface for creating clients for different LLM providers.

## Usage

```python
from gen_ai.factory import create_client

# Create OpenAI client
openai_client = create_client(
    provider="openai",
    api_key="your_openai_key",
    model_name="gpt-4",
    endpoint="https://api.openai.com/v1"
)

# Create Bedrock client
bedrock_client = create_client(
    provider="bedrock",
    api_key="your_aws_access_key",
    model_name="anthropic.claude-3-sonnet-20240229-v1:0",
    region="us-east-1",
    secret_key="your_aws_secret_key"
)
```

## Supported Providers

- OpenAI
- AWS Bedrock

## Common Parameters

- `provider`: The provider to use ("openai" or "bedrock")
- `api_key`: API key for authentication
- `model_name`: Name of the model to use
- `endpoint`: API endpoint URL (for OpenAI)
- `region`: AWS region (for Bedrock)
- `secret_key`: AWS secret access key (for Bedrock)
- `session_token`: AWS session token (for Bedrock)
