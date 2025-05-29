"""
Factory for creating clients for different providers
"""

from typing import Optional

from gen_ai.bedrock.client import BedrockClient
from gen_ai.gemini.client import GeminiClient
from gen_ai.openai.azure_client import AzureOpenAIClient
from gen_ai.openai.client import OpenAIClient


def create_client(
    provider: str,
    api_key: str,
    model_name: str,
    endpoint: Optional[str] = None,
    region: Optional[str] = None,
    secret_key: Optional[str] = None,
    session_token: Optional[str] = None,
    deployment: Optional[str] = None,
    api_version: Optional[str] = None,
    **kwargs,
):
    """
    Create a client for a given provider

    Args:
        provider: The provider to use (e.g., "openai", "bedrock", "azure", "gemini")
        api_key: API key or AWS access key ID
        model_name: Name of the model to use
        endpoint: API endpoint URL (for OpenAI/Azure)
        region: AWS region (for Bedrock)
        secret_key: AWS secret access key (for Bedrock)
        session_token: AWS session token (for Bedrock)
        deployment: Azure OpenAI deployment name (for Azure)
        api_version: Azure OpenAI API version (for Azure)
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
    elif provider == "azure":
        if not deployment:
            raise ValueError("deployment is required for Azure OpenAI")
        return AzureOpenAIClient(
            api_key=api_key,
            endpoint=endpoint,
            model_name=model_name,
            deployment=deployment,
            api_version=api_version,
            **kwargs,
        )
    elif provider == "gemini":
        return GeminiClient(
            api_key=api_key,
            model_name=model_name,
            **kwargs,
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")
