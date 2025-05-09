"""
Streaming Converse API related functions for Bedrock models
"""

import logging
from typing import Any, Dict, Generator, List

import boto3
from botocore.exceptions import ClientError

from gen_ai.utils import format_messages_for_bedrock, validate_image_paths

# Set up logging
logger = logging.getLogger(__name__)


def run_chat_completions_streaming(
    client: boto3.client,
    messages: List[Dict[str, Any]],
    model_name: str,
    **kwargs,
) -> Generator[str, None, None]:
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

        response = client.converse_stream(
            modelId=model_name,
            messages=messages_copy,
            inferenceConfig=kwargs.get("inferenceConfig", {}),
        )
        response_stream = response.get("stream")

        try:
            for event in response_stream:
                if "contentBlockDelta" in event:
                    yield event["contentBlockDelta"]["delta"]["text"]
                # elif 'messageStop' in event:
                #     yield event['messageStop']['stopReason']
                # elif 'messageStart' in event:
                #     yield event['messageStart']['role']
                # elif 'metadata' in event:
                #     yield event['metadata']
        except Exception as e:
            logger.error(f"Error in streaming: {str(e)}")
            return None
    except ClientError as e:
        logger.error(f"Streaming request error: {e}")
        if hasattr(e, "response") and e.response:
            status_code = e.response.status_code
            error_text = e.response.text
            logger.error(f"Response status: {status_code}")
            logger.error(f"Response body: {error_text}")
    except Exception as e:
        logger.error(f"Unexpected error during streaming: {e}")
        raise ValueError(f"Failed to process streaming response: {e}")
