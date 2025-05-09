"""
Utilities
"""

import base64
import logging
import os
from typing import Any, Dict, List

# Set up logging
logger = logging.getLogger(__name__)


def validate_image_paths(image_paths: List[str]) -> List[str]:
    """
    Validate that all image paths in the list exist.

    Args:
        image_paths: List of image file paths

    Returns:
        List of valid image file paths

    Raises:
        FileNotFoundError: If any of the image files do not exist
    """
    if not image_paths:
        return []

    missing_images = []
    for path in image_paths:
        if not os.path.exists(path):
            missing_images.append(path)
        elif not os.path.isfile(path):
            missing_images.append(path)

    if missing_images:
        error_msg = (
            f"The following image files were not found: {', '.join(missing_images)}"
        )
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    return image_paths


def encode_image(image_path: str) -> str:
    """
    Encode a local image file to base64 format.

    Args:
        image_path: Path to the image file

    Returns:
        Base64 encoded string of the image
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        logger.error(f"Error encoding image {image_path}: {e}")
        raise ValueError(f"Failed to encode image at {image_path}: {e}")


# gen_ai/utils/message_utils.py
def format_messages_for_bedrock(
    messages: List[Dict[str, Any]], image_paths: List[str] = None
) -> List[Dict[str, Any]]:
    """Format messages for Bedrock API, handling both text and image content."""
    messages_copy = [msg.copy() for msg in messages]

    if not image_paths:
        return messages_copy

    # Find or create user message
    last_user_idx = None
    for i in range(len(messages_copy) - 1, -1, -1):
        if messages_copy[i]["role"] == "user":
            last_user_idx = i
            break

    if last_user_idx is None:
        messages_copy.append({"role": "user", "content": [{"text": ""}]})
        last_user_idx = len(messages_copy) - 1

    # Ensure content is in the right format
    if isinstance(messages_copy[last_user_idx]["content"], str):
        messages_copy[last_user_idx]["content"] = [
            {"text": messages_copy[last_user_idx]["content"]}
        ]
    elif not isinstance(messages_copy[last_user_idx]["content"], list):
        messages_copy[last_user_idx]["content"] = [{"text": ""}]

    # Add images
    for image_path in image_paths:
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
            image_content = {
                "image": {"format": "jpeg", "source": {"bytes": image_bytes}}
            }
            messages_copy[last_user_idx]["content"].append(image_content)

    return messages_copy
