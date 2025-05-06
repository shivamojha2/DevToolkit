"""
Utilities
"""

import base64
import logging
import os
from typing import List

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
