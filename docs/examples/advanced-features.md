# Advanced Features

This guide covers advanced features and techniques for using DevToolkit effectively.

## Structured Output

### Using Pydantic Models

```python
from pydantic import BaseModel, Field
from typing import List

class CodeReview(BaseModel):
    summary: str = Field(description="Brief summary of the code review")
    issues: List[str] = Field(description="List of issues found")
    suggestions: List[str] = Field(description="List of improvement suggestions")
    score: float = Field(description="Overall code quality score from 0 to 10")

# Generate structured output
response = client.run_chat_completions(
    messages=[
        {"role": "system", "content": "You are a code reviewer."},
        {"role": "user", "content": "Review this code: def add(a,b): return a+b"}
    ],
    guided_json=CodeReview
)

# Access structured data
review = CodeReview.parse_raw(response)
print(f"Score: {review.score}")
print(f"Issues: {review.issues}")
```

### Custom JSON Schema

```python
schema = {
    "type": "object",
    "properties": {
        "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "keywords": {"type": "array", "items": {"type": "string"}}
    }
}

response = client.run_completions(
    prompt="Analyze the sentiment of: 'I love this product!'",
    guided_json=schema
)
```

## Advanced Chat Features

### Function Calling

```python
from typing import List, Optional

def get_weather(location: str, unit: str = "celsius") -> str:
    # Implementation here
    return f"Weather in {location}: 20°{unit}"

def get_stock_price(symbol: str) -> float:
    # Implementation here
    return 150.25

# Define available functions
functions = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            }
        }
    },
    {
        "name": "get_stock_price",
        "description": "Get the current stock price",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string"}
            }
        }
    }
]

# Use function calling
response = client.run_chat_completions(
    messages=[{"role": "user", "content": "What's the weather in New York?"}],
    functions=functions
)
```

### Context Management

```python
class ConversationManager:
    def __init__(self, client, max_tokens=1000):
        self.client = client
        self.max_tokens = max_tokens
        self.messages = []
        self.token_count = 0

    def add_message(self, role: str, content: str):
        # Estimate tokens (rough approximation)
        estimated_tokens = len(content.split()) * 1.3
        
        # If adding this message would exceed the limit, remove oldest messages
        while self.token_count + estimated_tokens > self.max_tokens and self.messages:
            removed = self.messages.pop(0)
            self.token_count -= len(removed["content"].split()) * 1.3
        
        self.messages.append({"role": role, "content": content})
        self.token_count += estimated_tokens

    def get_response(self):
        response = self.client.run_chat_completions(
            messages=self.messages,
            max_tokens=150
        )
        self.add_message("assistant", response)
        return response

# Usage
manager = ConversationManager(client)
manager.add_message("system", "You are a helpful assistant.")
manager.add_message("user", "What is Python?")
response = manager.get_response()
```

## Advanced Vision Features

### Multi-Image Analysis

```python
# Analyze multiple images
image_paths = [
    "path/to/image1.jpg",
    "path/to/image2.jpg",
    "path/to/image3.jpg"
]

response = client.run_vision_request(
    prompt="Compare these images and identify common elements.",
    image_paths=image_paths,
    max_tokens=200
)
```

### Image Analysis with Structured Output

```python
class ImageAnalysis(BaseModel):
    objects: List[str] = Field(description="List of objects detected")
    colors: List[str] = Field(description="Main colors present")
    scene: str = Field(description="Description of the scene")
    confidence: float = Field(description="Confidence score of the analysis")

response = client.run_vision_request(
    prompt="Analyze this image in detail.",
    image_paths=["path/to/image.jpg"],
    guided_json=ImageAnalysis
)
```

## Advanced Batch Processing

### Concurrent Processing

```python
# Process multiple prompts concurrently
responses = client.run_completions_batch(
    prompts=[
        "Explain quantum computing",
        "Describe machine learning",
        "What is blockchain?"
    ],
    concurrent=True,
    max_concurrent=3,
    max_tokens=150
)
```

### Batch with Different Parameters

```python
# Process prompts with different parameters
requests = [
    {
        "prompt": "Short answer about Python",
        "max_tokens": 50,
        "temperature": 0.3
    },
    {
        "prompt": "Creative story about AI",
        "max_tokens": 200,
        "temperature": 0.8
    }
]

responses = client.run_completions_batch(
    prompts=[r["prompt"] for r in requests],
    max_tokens=[r["max_tokens"] for r in requests],
    temperature=[r["temperature"] for r in requests]
)
```

## Error Handling and Retries

### Custom Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def make_request_with_retry(client, prompt):
    try:
        return client.run_completions(
            prompt=prompt,
            max_tokens=100,
            return_error=True
        )
    except Exception as e:
        print(f"Attempt failed: {str(e)}")
        raise

# Usage
response, error = make_request_with_retry(client, "Hello")
```

### Error Recovery

```python
def process_with_recovery(client, prompt):
    try:
        response = client.run_completions(prompt=prompt)
        return response
    except Exception as e:
        if "rate_limit" in str(e).lower():
            # Wait and retry with exponential backoff
            time.sleep(5)
            return client.run_completions(prompt=prompt)
        elif "context_length" in str(e).lower():
            # Truncate prompt and retry
            truncated_prompt = prompt[:len(prompt)//2]
            return client.run_completions(prompt=truncated_prompt)
        else:
            raise
```

## Next Steps

- Review [Basic Usage](basic-usage.md) for fundamental examples
- Explore [API Documentation](../api/overview.md) for detailed API information
