# Vision API

The Vision API allows you to process images and generate text descriptions or analysis. This is useful for tasks like image description, object detection, and visual analysis.

## Basic Usage

```python
from gen_ai.factory import create_client

# Create a client
client = create_client(
    provider="openai",
    api_key="your-api-key",
    endpoint="https://api.example.com/v1",
    model_name="gpt-4-vision-preview"
)

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

## Streaming

For real-time image analysis, use the streaming API:

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

## Parameters

### Required Parameters

- `prompt`: Text prompt or message to send with the images
- `image_paths`: List of paths to images to include in the request

### Optional Parameters

- `max_tokens`: Maximum number of tokens to generate (default: 256)
- `temperature`: Controls randomness (0.0 to 1.0, default: 0)
- `top_p`: Controls diversity via nucleus sampling (default: 1.0)
- `timeout`: Request timeout in seconds (default: 30)
- `guided_json`: JSON schema to enforce structured output
- `return_error`: Return error details along with the result
- `stream`: Whether to stream the response (default: False)

## Examples

### Basic Image Description

```python
response = client.run_vision_request(
    prompt="Describe the image in detail.",
    image_paths=["path/to/image.jpg"],
    max_tokens=150
)
```

### Structured Image Analysis

```python
from pydantic import BaseModel, Field

class ImageAnalysis(BaseModel):
    description: str = Field(..., description="Detailed description of the image")
    objects: list[str] = Field(..., description="List of objects in the image")
    colors: list[str] = Field(..., description="List of colors in the image")

response = client.run_vision_request(
    prompt="Analyze this image.",
    image_paths=["path/to/image.jpg"],
    guided_json=ImageAnalysis.model_json_schema(),
    max_tokens=300
)
```

### Chat with Images

```python
messages = [
    {
        "role": "system",
        "content": "You are an expert at image analysis."
    },
    {
        "role": "user",
        "content": "What's interesting about this image?"
    }
]

response = client.run_vision_request(
    prompt=messages,
    image_paths=["path/to/image.jpg"],
    max_tokens=200
)
```

## Next Steps

- Learn about [Text Completions](text-completions.md)
- Explore [Chat Completions](chat-completions.md)
- Check out the [OpenAI Examples](../examples/openai_examples.md)
