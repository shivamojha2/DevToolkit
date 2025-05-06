"""
Factory for creating clients for different providers
"""

from gen_ai.openai.client import OpenAIClient


def create_client(provider, api_key, endpoint=None, model_name=None):
    """
    Create a client for a given provider
    """
    if provider == "openai":
        return OpenAIClient(api_key, endpoint, model_name)
    # elif provider == "bedrock":
    #     return BedrockClient(api_key, endpoint, model_name)
    else:
        raise ValueError(f"Unknown provider: {provider}")
