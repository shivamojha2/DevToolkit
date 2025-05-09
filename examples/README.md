# DevToolkit Examples

This directory contains examples demonstrating how to use the DevToolkit generative AI interfaces.

## Prerequisites

Before running these examples, make sure you have:

1. Set up your API keys in environment variables or a `.env` file
2. Installed the required dependencies

For OpenAI examples, you'll need:

```
API_KEY=your_api_key_here
```

For Amazon Bedrock examples, you'll need:

```
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_REGION=your_region  # e.g., us-east-1
```

## Running Examples

### OpenAI Example

This example demonstrates how to use the OpenAI client for:

- Text completions
- Chat completions
- Batch completions

```bash
# From the project root directory
python examples/openai_example.py
```

### Amazon Bedrock Example

The shared example shows how to use Converse API to make calls to the text and vision capabilities of Bedrock models.

```bash
# From the project root directory
python examples/bedrock_example.py
```
