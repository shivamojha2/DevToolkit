"""
Example script demonstrating how to use the OpenAIClient
"""

import json
import os
import sys
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from utils import print_response

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

from gen_ai.factory import create_client

BASE_ENDPOINT = os.getenv("BASE_ENDPOINT", "http://localhost:8000/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Llama-3.3-70B-Instruct")


class CodeReview(BaseModel):
    """Model for code review feedback"""

    overall_score: float = Field(
        ..., ge=0, le=10, description="Overall code quality score from 0-10"
    )
    strengths: List[str] = Field(..., description="List of code strengths")
    weaknesses: List[str] = Field(..., description="List of code weaknesses")
    suggestions: List[str] = Field(..., description="List of improvement suggestions")
    security_concerns: Optional[List[str]] = Field(
        None, description="List of security concerns if any"
    )


class ImageAnalysis(BaseModel):
    """Model for image analysis"""

    description: str = Field(..., description="Detailed description of the image")
    objects: List[str] = Field(..., description="List of objects in the image")
    colors: List[str] = Field(..., description="List of colors in the image")


def test_completions_api(client):
    """Test the basic completions API"""
    print("\n1. Testing Completions API")
    print("--------------------------")
    prompt = "Write a short poem about artificial intelligence."
    response = client.run_completions(prompt, max_tokens=100)
    print_response(response)


def test_chat_completions_api(client):
    """Test the chat completions API"""
    print("\n2. Testing Chat Completions API")
    print("------------------------------")
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What are the key benefits of modular code?"},
    ]
    response = client.run_chat_completions(messages, max_tokens=150)
    print_response(response)


def test_batch_completions_api(client):
    """Test the batch completions API"""
    print("\n3. Testing Batch Completions API")
    print("------------------------------")
    prompts = [
        "List 3 benefits of cloud computing.",
        "What is the capital of France?",
        "Provide a short definition of machine learning.",
    ]
    responses = client.run_completions_batch(prompts, max_tokens=100)
    for i, response in enumerate(responses):
        print(f"\nResponse {i+1}:")
        print_response(response)


def test_completions_streaming(client):
    """Test the completions API with streaming"""
    print("\n4. Testing Completions API with streaming")
    print("------------------------------")
    prompt = "Write a short poem about artificial intelligence."
    print("Streaming response token by token:")
    print("----------------------------------")

    response_stream = client.run_completions_stream(prompt, max_tokens=100)
    for token in response_stream:
        print(token, end="", flush=True)
    print()


def test_chat_completions_streaming(client):
    """Test the chat completions API with streaming"""
    print("\n5. Testing Chat Completions API with streaming")
    print("------------------------------")
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What are the key benefits of modular code?"},
    ]
    print("Streaming response token by token:")
    print("----------------------------------")

    response_stream = client.run_chat_completions_stream(messages, max_tokens=100)
    for token in response_stream:
        print(token, end="", flush=True)
    print()


def test_guided_json_completions(client):
    """Test the completions API with guided JSON output"""
    print("\n6. Testing Completions API with Guided JSON")
    print("------------------------------------------")

    # Example: Code Analysis
    print("\nExample: Code Analysis")
    print("----------------------")
    code_analysis_prompt = f"""
    Analyze the following code:
    
    class UserManager:
        def __init__(self):
            self.users = []
            
        def add_user(self, username, password):
            if username in self.users:
                return False
            self.users[username] = password
            return True
            
        def authenticate(self, username, password):
            return username in self.users and self.users[username] == password
    
    Provide your feedback in a structured JSON format only: {CodeReview.model_json_schema()}
    """

    response = client.run_completions(
        code_analysis_prompt, max_tokens=300, guided_json=CodeReview.model_json_schema()
    )
    print_response(response)


def test_guided_json_chat(client):
    """Test the chat completions API with guided JSON output"""
    print("\n7. Testing Chat Completions API with Guided JSON")
    print("----------------------------------------------")

    # Example: Code Review with Chat
    print("\nExample: Code Review with Chat")
    print("----------------------------")
    messages = [
        {
            "role": "system",
            "content": "You are an expert code reviewer. Provide feedback in a structured JSON format.",
        },
        {
            "role": "user",
            "content": f"""
        Review this code:
        
        def process_data(data):
            result = []
            for item in data:
                if item > 0:
                    result.append(item * 2)
            return result
        
        Provide your feedback in a structured JSON format only: {CodeReview.model_json_schema()}
        """,
        },
    ]

    response = client.run_chat_completions(
        messages, max_tokens=300, guided_json=CodeReview.model_json_schema()
    )
    print_response(response)


def test_vision_api(client):
    """Test the vision API"""
    print("\n8. Testing Vision API")
    print("----------------------")
    image_paths = ["examples/gen_ai/assets/test_image.jpg"]
    prompt = "Describe the image in detail."
    response = client.run_vision_request(prompt, image_paths, max_tokens=100)
    print_response(response)


def test_vision_streaming(client):
    """Test the vision API with streaming"""
    print("\n9. Testing Vision API with streaming")
    print("----------------------------------")
    image_paths = ["examples/gen_ai/assets/test_image.jpg"]
    prompt = "Describe the image in detail."
    response_stream = client.run_vision_request(
        prompt, image_paths, stream=True, max_tokens=100
    )
    for token in response_stream:
        print(token, end="", flush=True)
    print()


def test_vision_guided_json_chat(client):
    """Test the vision API with guided JSON output"""
    print("\n10. Testing Vision API with Guided JSON")
    print("-------------------------------------")
    image_paths = ["examples/gen_ai/assets/test_image.jpg"]

    # Convert Pydantic model schema to dict
    guided_json_schema = ImageAnalysis.model_json_schema()

    prompt = f"List out the objects and colors in the image & also describe the image. Provide your feedback in a structured JSON format only.{guided_json_schema}"
    messages = [
        {
            "role": "system",
            "content": "You are an expert at image analysis. Provide a detailed description of the image in a structured JSON format.",
        },
        {"role": "user", "content": prompt},
    ]

    response, error = client.run_vision_request(
        prompt=messages,
        image_paths=image_paths,
        guided_json=guided_json_schema,
        return_error=True,
    )
    print_response(response)


def setup_client():
    """Set up and return the OpenAI client"""
    # Try to load environment variables from .env file if dotenv is installed
    try:
        load_dotenv()
        print("Loaded environment from .env file")
    except ImportError:
        print("python-dotenv not installed. Using environment variables directly.")

    api_key = os.getenv("API_KEY")
    if not api_key:
        print("Error: API_KEY environment variable not set.")
        print(
            "Please create a .env file with your API key or set it in your environment."
        )
        sys.exit(1)

    # Create an OpenAI client using the factory
    return create_client(
        provider="openai",
        api_key=api_key,
        endpoint=BASE_ENDPOINT,
        model_name=MODEL_NAME,
    )


def main():
    """Main function to run all examples"""
    client = setup_client()

    # Run all examples
    # test_completions_api(client)
    # test_chat_completions_api(client)
    test_batch_completions_api(client)
    # test_completions_streaming(client)
    # test_chat_completions_streaming(client)
    # test_guided_json_completions(client)
    # test_guided_json_chat(client)

    # Vision API
    # test_vision_api(client)
    # test_vision_streaming(client)
    # test_vision_guided_json_chat(client)


if __name__ == "__main__":
    main()
