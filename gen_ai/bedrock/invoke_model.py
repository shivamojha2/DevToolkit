"""
Module for interacting with AWS Bedrock API endpoints

Provides basic functionality to communicate with language models via Bedrock's converse API.
"""

import logging
from typing import Any, Dict, List

import boto3
from botocore.exceptions import ClientError

from gen_ai.errors import APIError
from gen_ai.utils import format_messages_for_bedrock, validate_image_paths

# Set up logging
logger = logging.getLogger(__name__)


def generate_chat_response(
    client: boto3.client,
    messages: List[Dict[str, Any]],
    model_name: str,
    **kwargs,
) -> Dict[str, Any]:
    """
    Run a chat completion request using the Converse API

    Args:
        client: boto3.client
        messages: List[Dict[str, Any]]
        model_name: str
        **kwargs: Dict[str, Any]
    """
    try:
        image_paths = kwargs.get("image_paths")
        if image_paths:
            validate_image_paths(image_paths)

        # Format messages for Bedrock
        messages_copy = format_messages_for_bedrock(messages, image_paths)

        response = client.converse(
            modelId=model_name,
            messages=messages_copy,
            inferenceConfig=kwargs.get("inferenceConfig", {}),
        )
        return response["output"]["message"]["content"][0]["text"]

    except Exception as e:
        if isinstance(e, ClientError):
            logger.error(f"Failed to process response: {e}")
            error_message = e.response.get("Error", {}).get("Message", str(e))
            raise APIError(f"API request failed: {error_message}")
        else:
            logger.error(f"Failed to process response: {e}")
            raise APIError(f"Failed to process response: {e}")
