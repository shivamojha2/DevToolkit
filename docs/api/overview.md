# API Overview

## Supported Providers

- OpenAI: Access to GPT models and other OpenAI services
- AWS Bedrock: Access to various foundation models including Claude, Llama, and others
- Azure OpenAI: Access to OpenAI models through Azure
- Google Gemini: Access to Google's Gemini Pro models

## Common Features

- Text completions
- Chat completions
- Streaming responses
- Vision API support
- Batch processing
- Error handling

## Provider-Specific Features

### OpenAI

- Custom endpoints support
- Guided JSON output
- Batch processing
- Vision API with base64 image encoding

### AWS Bedrock

- Multiple model support (Claude, Llama, etc.)
- Raw image bytes support
- AWS credential management
- Region-specific endpoints

### Azure OpenAI

- Azure-specific deployment support
- Custom API versions
- Azure credential management

### Google Gemini

- Simple API key authentication
- Support for Gemini Pro models
- Automatic message format conversion
- Temperature and top_p controls
