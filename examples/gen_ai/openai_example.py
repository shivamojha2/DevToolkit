#!/usr/bin/env python3
"""
Example script demonstrating how to use the OpenAIClient
"""

import json
import os
import sys

from dotenv import load_dotenv

# Add the parent directory to sys.path to import the gen_ai package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gen_ai.factory import create_client

BASE_ENDPOINT = ("http://localhost:8000/v1",)
MODEL_NAME = "Llama-3.3-70B-Instruct"


# Define a simple print_response function since it's not in utils
def print_response(response):
    """Print the response from the API in a formatted way"""
    if isinstance(response, dict):
        if "choices" in response:
            for choice in response["choices"]:
                if "text" in choice:
                    print(f"Response: {choice['text'].strip()}")
                elif "message" in choice:
                    print(f"Role: {choice['message']['role']}")
                    print(f"Content: {choice['message']['content'].strip()}")
        else:
            print(json.dumps(response, indent=2))
    else:
        print(response)


def main():
    # Try to load environment variables from .env file if dotenv is installed
    try:
        load_dotenv()
        print("Loaded environment from .env file")
    except ImportError:
        print("python-dotenv not installed. Using environment variables directly.")

    # Get API key from environment variable
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("Error: API_KEY environment variable not set.")
        print(
            "Please create a .env file with your API key or set it in your environment."
        )
        sys.exit(1)

    # Create an OpenAI client using the factory
    client = create_client(
        provider="openai",
        api_key=api_key,
        endpoint=BASE_ENDPOINT,
        model_name=MODEL_NAME,
    )

    print("1. Testing Completions API")
    print("--------------------------")
    prompt = "Write a short poem about artificial intelligence."
    response = client.run_completions(prompt, max_tokens=100)
    print_response(response)

    print("\n2. Testing Chat Completions API")
    print("------------------------------")
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What are the key benefits of modular code?"},
    ]
    response = client.run_chat_completions(messages, max_tokens=150)
    print_response(response)

    print("\n3. Testing Batch Completions API")
    print("------------------------------")
    prompts = [
        "List 3 benefits of cloud computing.",
        "What is the capital of France?",
        "Provide a short definition of machine learning.",
    ]
    responses = client.run_completions_batch(prompts, max_tokens=50)
    for i, response in enumerate(responses):
        print(f"\nResponse {i+1}:")
        print_response(response)


if __name__ == "__main__":
    main()
