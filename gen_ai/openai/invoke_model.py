"""
Module for interacting with LLM API endpoints, in Open AI Compatible API formats

Provides basic functionality to communicate with language models via completion endpoints.
Supports both text-only and image-based (multimodal) requests.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

import requests

from gen_ai.errors import APIError
from gen_ai.utils import encode_image

# Set up logging
logger = logging.getLogger(__name__)


def run_completions(
    query: str,
    endpoint: str,
    model_name: str,
    api_key: str,
    timeout: int = 30,
    guided_json: Dict[str, Any] = None,
    return_error: bool = False,
    **kwargs,
) -> Union[Optional[str], Tuple[Optional[str], Optional[Dict[str, Any]]]]:
    """
    Send a completion request to the LLM API.

    Args:
        query: The prompt text to send to the model
        endpoint: Base API endpoint URL (without the /completions part)
        model_name: Name of the model to use
        api_key: API key for authentication
        timeout: Request timeout in seconds
        guided_json: Optional JSON schema to enforce structured output format
        return_error: If True, returns both the result and error details
        **kwargs: Additional parameters to include in the request (temperature, max_tokens, top_p, etc.)

    Returns:
        If return_error is False: The generated text response or None if the request failed
        If return_error is True: A tuple of (result, error_details) where error_details is None if successful
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    error_details = None
    result = None

    try:
        completions_endpoint = f"{endpoint}/completions"

        # default parameters
        payload = {
            "model": model_name,
            "prompt": query,
            "max_tokens": 256,
            "temperature": 0,
            "n": 1,
        }

        # Add guided_json if specified
        if guided_json:
            payload["extra_body"] = {"guided_json": guided_json}

        # Add any additional parameters
        payload.update(kwargs)

        logger.info(f"Sending completion request to {completions_endpoint}")
        response = requests.post(
            completions_endpoint, headers=headers, json=payload, timeout=timeout
        )
        response.raise_for_status()

        result = response.json()["choices"][0]["text"]

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        if hasattr(e, "response") and e.response:
            status_code = e.response.status_code
            error_text = e.response.text
            logger.error(f"Response status: {status_code}")
            logger.error(f"Response body: {error_text}")

            # Create APIError but don't raise it, just capture details
            api_error = APIError(completions_endpoint, status_code, error_text)
            error_details = api_error.get_details()
            logger.error(f"API Error details: {error_details}")
        else:
            api_error = APIError(completions_endpoint, None, str(e))
            error_details = api_error.get_details()
            logger.error(f"Connection error details: {error_details}")

    except (KeyError, IndexError) as e:
        logger.error(f"Error parsing response: {e}")
        error_details = {
            "url": completions_endpoint,
            "method": "POST",
            "error_type": "Response parsing error",
            "message": str(e),
            "suggestion": "Check if the API response structure has changed",
        }

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        error_details = {
            "url": completions_endpoint,
            "method": "POST",
            "error_type": "Unexpected error",
            "message": str(e),
            "suggestion": "Check API documentation and request format",
        }

    if return_error:
        return result, error_details
    return result


def run_chat_completions(
    messages: List[Dict[str, Any]],
    endpoint: str,
    model_name: str,
    api_key: str,
    timeout: int = 30,
    guided_json: Dict[str, Any] = None,
    return_error: bool = False,
    image_paths: List[str] = None,
    **kwargs,
) -> Union[Optional[str], Tuple[Optional[str], Optional[Dict[str, Any]]]]:
    """
    Send a chat completion request to the LLM API.

    Args:
        messages: List of message dictionaries in the format [{"role": "user", "content": "Hello"}]
                 or with multimodal content: [{"role": "user", "content": [{"type": "text", "text": "Hello"},
                                                                         {"type": "image_url", ...}]}]
        endpoint: Base API endpoint URL (without the /chat/completions part)
        model_name: Name of the model to use
        api_key: API key for authentication
        timeout: Request timeout in seconds
        guided_json: Optional JSON schema to enforce structured output format
        return_error: If True, returns both the result and error details
        image_paths: Optional list of paths to images to attach to the last user message
        **kwargs: Additional parameters to include in the request (temperature, max_tokens, top_p, etc.)

    Returns:
        If return_error is False: The generated text response or None if the request failed
        If return_error is True: A tuple of (result, error_details) where error_details is None if successful
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    error_details = None
    result = None

    try:
        chat_endpoint = f"{endpoint}/chat/completions"

        # Make a deep copy of messages to avoid modifying the original
        messages_copy = []
        for msg in messages:
            messages_copy.append(msg.copy())

        # Add images to the last user message if provided
        if image_paths and len(image_paths) > 0:
            logger.info(f"Adding {len(image_paths)} images to chat request")

            # Find the last user message to attach images to
            last_user_idx = None
            for i in range(len(messages_copy) - 1, -1, -1):
                if messages_copy[i]["role"] == "user":
                    last_user_idx = i
                    break

            # If no user message found, create one
            if last_user_idx is None:
                user_message = {
                    "role": "user",
                    "content": [{"type": "text", "text": ""}],
                }
                messages_copy.append(user_message)
                last_user_idx = len(messages_copy) - 1

            # Convert the user message content to the multimodal format if it's a simple string
            if isinstance(messages_copy[last_user_idx]["content"], str):
                text_content = messages_copy[last_user_idx]["content"]
                messages_copy[last_user_idx]["content"] = [
                    {"type": "text", "text": text_content}
                ]

            # Ensure content is a list
            if not isinstance(messages_copy[last_user_idx]["content"], list):
                messages_copy[last_user_idx]["content"] = [{"type": "text", "text": ""}]

            # Add each image to the content list
            for image_path in image_paths:
                image_base64 = encode_image(image_path)
                image_content = {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                }
                messages_copy[last_user_idx]["content"].append(image_content)

        # default parameters
        payload = {
            "model": model_name,
            "messages": messages_copy,
            "max_tokens": 256,
            "temperature": 0,
            "n": 1,
        }

        # Add guided_json if specified
        if guided_json:
            payload["extra_body"] = {"guided_json": guided_json}

        # Add any additional parameters
        payload.update(kwargs)

        logger.info(f"Sending chat completion request to {chat_endpoint}")

        response = requests.post(
            chat_endpoint, headers=headers, json=payload, timeout=timeout
        )

        response.raise_for_status()

        result = response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        if hasattr(e, "response") and e.response:
            status_code = e.response.status_code
            error_text = e.response.text
            logger.error(f"Response status: {status_code}")
            logger.error(f"Response body: {error_text}")

            # Create APIError but don't raise it, just capture details
            api_error = APIError(chat_endpoint, status_code, error_text)
            error_details = api_error.get_details()
            logger.error(f"API Error details: {error_details}")
        else:
            api_error = APIError(chat_endpoint, None, str(e))
            error_details = api_error.get_details()
            logger.error(f"Connection error details: {error_details}")

    except (KeyError, IndexError) as e:
        logger.error(f"Error parsing response: {e}")
        error_details = {
            "url": chat_endpoint,
            "method": "POST",
            "error_type": "Response parsing error",
            "message": str(e),
            "suggestion": "Check if the API response structure has changed",
        }

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        error_details = {
            "url": chat_endpoint,
            "method": "POST",
            "error_type": "Unexpected error",
            "message": str(e),
            "suggestion": "Check API documentation and request format",
        }

    if return_error:
        return result, error_details
    return result
