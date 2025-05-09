"""
Factory for creating clients for different providers
"""

from typing import Optional

from gen_ai.bedrock.client import BedrockClient
from gen_ai.openai.client import OpenAIClient


def create_client(
    provider: str,
    api_key: str,
    model_name: str,
    endpoint: Optional[str] = None,
    region: Optional[str] = None,
    secret_key: Optional[str] = None,
    session_token: Optional[str] = None,
    **kwargs,
):
    """
    Create a client for a given provider

    Args:
        provider: The provider to use (e.g., "openai", "bedrock")
        api_key: API key or AWS access key ID
        model_name: Name of the model to use
        endpoint: API endpoint URL (for OpenAI)
        region: AWS region (for Bedrock)
        secret_key: AWS secret access key (for Bedrock)
        session_token: AWS session token (for Bedrock)
        **kwargs: Additional provider-specific arguments
    """
    if provider == "openai":
        return OpenAIClient(
            api_key=api_key, endpoint=endpoint, model_name=model_name, **kwargs
        )
    elif provider == "bedrock":
        return BedrockClient(
            api_key=api_key,
            model_name=model_name,
            region=region,
            secret_key=secret_key,
            session_token=session_token,
            **kwargs,
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")
