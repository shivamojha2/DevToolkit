"""
Azure OpenAI client implementation
"""

from typing import Any, Dict, List, Optional

from openai import AzureOpenAI

from gen_ai.api_interface import LLMProvider
from gen_ai.errors import APIError


class AzureOpenAIClient(LLMProvider):
    """
    Client for Azure OpenAI API
    """

    def __init__(
        self,
        api_key: str,
        endpoint: str,
        model_name: str,
        deployment: str,
        api_version: str = "2024-02-15-preview",
        **kwargs,
    ):
        """
        Initialize Azure OpenAI client

        Args:
            api_key: Azure OpenAI API key
            endpoint: Azure OpenAI endpoint URL
            model_name: Name of the model to use
            deployment: Name of the deployment
            api_version: API version to use
            **kwargs: Additional arguments to pass to AzureOpenAI client
        """
        self.model_name = model_name
        self.deployment = deployment
        self.client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=api_key,
            **kwargs,
        )

    def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: float = 1.0,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        **kwargs,
    ) -> Any:
        """
        Generate a chat response using Azure OpenAI

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            frequency_penalty: Frequency penalty
            presence_penalty: Presence penalty
            **kwargs: Additional arguments to pass to chat.completions.create

        Returns:
            Response from Azure OpenAI API
        """
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                model=self.deployment,
                **kwargs,
            )
            return response
        except Exception as e:
            raise APIError(f"Error calling Azure OpenAI API: {str(e)}") 