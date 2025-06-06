# DevToolkit

A collection of reusable utility functions and tools to streamline development workflows across projects.

## Overview

This repo containes scripts that are modular, tested, and easily integrable into any project.

## Categories

- **Gen AI** - Utilities for working with generative language and vision models
- **Data** - Tools for data processing, transformation, and analysis
- **System** - Utilities for system automation and management

## Usage

Each utility module is designed to be imported independently:

```python
# Example: Using LLM API utilities
from devtoolkit.gen_ai.openai.invoke_model import generate_response

response = generate_response(
    query="your prompt here", 
    endpoint="http://localhost:8000/v1",
    model_name="Llama-3.3-70B-Instruct",
    api_key="",
) 
```

## Documentation

The full documentation is available at: [https://shivamojha2.github.io/DevToolkit/](https://shivamojha2.github.io/DevToolkit/)

## Roadmap

- Add async completion functionality (highly recommended and a best practice to use asynchronous operations in a service environment to ensure scalability, responsiveness, and efficient resource utilization)
- Add function calling
- Add vector databases
