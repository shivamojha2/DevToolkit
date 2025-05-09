"""
Example script demonstrating how to use the BedrockClient
"""
import os
import sys

import dotenv
from utils import print_response

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)
from gen_ai.factory import create_client

dotenv.load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_NAME = os.getenv("MODEL_NAME", "us.anthropic.claude-3-7-sonnet-20250219-v1:0")

# AWS Credentials
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")


def setup_client():
    """Set up and return the OpenAI client"""
    if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY]):
        print("Error: AWS credentials not found in environment variables.")
        print(
            "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in your .env file or environment."
        )
        sys.exit(1)

    # Create an Bedrock client using the factory
    return create_client(
        provider="bedrock",
        api_key=AWS_ACCESS_KEY_ID,
        model_name=MODEL_NAME,
        region=AWS_REGION,
        secret_key=AWS_SECRET_ACCESS_KEY,
        session_token=AWS_SESSION_TOKEN,
    )


def test_chat_completions_api(client):
    """Test the chat completions API"""
    print("\n1. Testing Chat Completions API")
    print("------------------------------")
    messages = [{"role": "user", "content": "What is ambidexterity?"}]
    response = client.run_chat_completions(messages, inferenceConfig={"maxTokens": 100})
    print_response(response)


def test_chat_completions_streaming(client):
    """Test the chat completions streaming API"""
    print("\n2. Testing Chat Completions Streaming API")
    print("----------------------------------------")
    messages = [{"role": "user", "content": "What is ambidexterity?"}]
    response_stream = client.run_chat_completions_streaming(
        messages, inferenceConfig={"maxTokens": 100}
    )
    for token in response_stream:
        print(token, end="", flush=True)
    print()


def test_vision_api(client):
    """Test the vision API"""
    print("\n3. Testing Vision API")
    print("----------------------")
    image_paths = ["examples/gen_ai/assets/test_image.jpg"]
    messages = [{"role": "user", "content": "What is in this image?"}]
    response = client.run_chat_completions(messages, image_paths=image_paths)
    print_response(response)


def test_vision_api_streaming(client):
    """Test the vision API streaming"""
    print("\n4. Testing Vision API Streaming")
    print("--------------------------------")
    image_paths = ["examples/gen_ai/assets/test_image.jpg"]
    messages = [{"role": "user", "content": "What is in this image?"}]
    response_stream = client.run_chat_completions_streaming(
        messages, image_paths=image_paths
    )
    for token in response_stream:
        print(token, end="", flush=True)
    print()


def main():
    """Main function to run all examples"""
    client = setup_client()

    # print(client.list_available_models())
    # test_chat_completions_api(client)
    # test_chat_completions_streaming(client)
    test_vision_api(client)
    # test_vision_api_streaming(client)


if __name__ == "__main__":
    main()
