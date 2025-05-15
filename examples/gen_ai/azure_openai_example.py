"""
Example usage of Azure OpenAI client
"""

import os
import sys
from dotenv import load_dotenv

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)
from gen_ai.factory import create_client

# Load environment variables
load_dotenv()

def main():
    # Azure OpenAI configuration
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    model_name = os.getenv("AZURE_OPENAI_MODEL_NAME")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

    # Create Azure OpenAI client
    client = create_client(
        provider="azure",
        api_key=api_key,
        endpoint=endpoint,
        model_name=model_name,
        deployment=deployment,
        api_version=api_version,
    )

    # Example chat completion
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "I am going to Paris, what should I see?",
        }
    ]

    # Run chat completion
    response = client.run_chat_completions(
        messages=messages,
        max_tokens=800,
        temperature=1.0,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    # Print response
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main() 