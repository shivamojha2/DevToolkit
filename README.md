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
from devtoolkit.gen_ai.openai.invoke_model import run_completions

response = run_completions(
    query="your prompt here", 
    endpoint="http://localhost:8000/v1",
    model_name="Llama-3.3-70B-Instruct",
    api_key="",
) 
```

## Documentation

See the [docs](./docs) directory for detailed documentation on each module.
