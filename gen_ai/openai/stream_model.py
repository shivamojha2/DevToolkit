"""
Streaming API related functions, using completions endpoint
"""

import json
import logging
from typing import Any, Dict, Generator, List

import requests

from gen_ai.errors import APIError
from gen_ai.utils import encode_image, validate_image_paths

# Set up logging
logger = logging.getLogger(__name__)


def generate_response_stream(
    query: str,
    endpoint: str,
    model_name: str,
    api_key: str,
    timeout: int = 30,
    **kwargs,
) -> Generator[str, None, None]:
    """
    Send a streaming completion request to the LLM API.

    Args:
        query: The prompt text to send to the model
        endpoint: Base API endpoint URL (without the /completions part)
        model_name: Name of the model to use
        api_key: API key for authentication
        timeout: Request timeout in seconds
        **kwargs: Additional parameters to include in the request
        (temperature, max_tokens, top_p, etc.)

    Returns:
        A generator that yields text chunks as they are generated

    Raises:
        APIError: If the API request fails
        ValueError: If the response parsing fails
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    completions_endpoint = f"{endpoint}/completions"

    # default parameters with stream=True
    payload = {
        "model": model_name,
        "prompt": query,
        "max_tokens": 256,
        "temperature": 0,
        "n": 1,
        "stream": True,
    }

    # Always ensure stream is True regardless of user settings
    payload["stream"] = True

    # Add any additional parameters
    payload.update(kwargs)

    logger.info(f"Sending streaming completion request to {completions_endpoint}")

    try:
        with requests.post(
            completions_endpoint,
            headers=headers,
            json=payload,
            timeout=timeout,
            stream=True,
        ) as response:
            response.raise_for_status()

            for line in response.iter_lines():
                if not line:
                    continue

                # Skip the "data: " prefix
                if line.startswith(b"data: "):
                    line = line[6:]  # Skip "data: " prefix

                # Handle the "[DONE]" marker
                if line.strip() == b"[DONE]":
                    break

                try:
                    # Parse the JSON response chunk
                    chunk = json.loads(line)

                    # Skip empty chunks
                    if not chunk or "choices" not in chunk or not chunk["choices"]:
                        continue

                    # Extract the text content
                    delta = chunk["choices"][0].get("text", "")
                    if delta:
                        yield delta
                except json.JSONDecodeError as e:
                    logger.warning(f"Error decoding JSON chunk: {e}, chunk: {line}")
                    continue

    except requests.exceptions.RequestException as e:
        logger.error(f"Streaming request error: {e}")
        if hasattr(e, "response") and e.response:
            status_code = e.response.status_code
            error_text = e.response.text
            logger.error(f"Response status: {status_code}")
            logger.error(f"Response body: {error_text}")

            # Create and raise APIError with details
            api_error = APIError(completions_endpoint, status_code, error_text)
            raise api_error
        else:
            # Network error, no response
            api_error = APIError(completions_endpoint, None, str(e))
            raise api_error
    except Exception as e:
        logger.error(f"Unexpected error during streaming: {e}")
        raise ValueError(f"Failed to process streaming response: {e}")


def generate_chat_response_streaming(
    messages: List[Dict[str, Any]],
    endpoint: str,
    model_name: str,
    api_key: str,
    timeout: int = 30,
    image_paths: List[str] = None,
    **kwargs,
) -> Generator[str, None, None]:
    """
    Send a streaming chat completion request to the LLM API.

    Args:
        messages: List of message dictionaries in the format [{"role": "user", "content": "Hello"}]
                 or with multimodal content: [{"role": "user", "content": [{"type": "text", "text": "Hello"},
                                                                         {"type": "image_url", ...}]}]
        endpoint: Base API endpoint URL (without the /chat/completions part)
        model_name: Name of the model to use
        api_key: API key for authentication
        timeout: Request timeout in seconds
        image_paths: Optional list of paths to images to attach to the last user message
        **kwargs: Additional parameters to include in the request
        (temperature, max_tokens, top_p, etc.)
    Returns:
        A generator that yields text chunks as they are generated

    Raises:
        APIError: If the API request fails
        ValueError: If the response parsing fails
        FileNotFoundError: If any of the provided image paths don't exist
    """
    import json

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    chat_endpoint = f"{endpoint}/chat/completions"

    # Make a deep copy of messages to avoid modifying the original
    messages_copy = []
    for msg in messages:
        messages_copy.append(msg.copy())

    # Add images to the last user message if provided
    if image_paths and len(image_paths) > 0:
        try:
            # Validate image paths first
            image_paths = validate_image_paths(image_paths)

            logger.info(f"Adding {len(image_paths)} images to streaming chat request")

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
        except FileNotFoundError as e:
            # Re-raise with original error message
            logger.error(f"Image file error: {e}")
            raise

    # default parameters with stream=True
    payload = {
        "model": model_name,
        "messages": messages_copy,
        "max_tokens": 256,
        "temperature": 0,
        "n": 1,
        "stream": True,
    }

    # Always ensure stream is True regardless of user settings
    payload["stream"] = True

    # Add any additional parameters
    payload.update(kwargs)

    logger.info(f"Sending streaming chat completion request to {chat_endpoint}")

    try:
        with requests.post(
            chat_endpoint, headers=headers, json=payload, timeout=timeout, stream=True
        ) as response:
            response.raise_for_status()

            for line in response.iter_lines():
                if not line:
                    continue

                # Skip the "data: " prefix
                if line.startswith(b"data: "):
                    line = line[6:]  # Skip "data: " prefix

                # Handle the "[DONE]" marker
                if line.strip() == b"[DONE]":
                    break

                try:
                    # Parse the JSON response chunk
                    chunk = json.loads(line)

                    # Skip empty chunks
                    if not chunk or "choices" not in chunk or not chunk["choices"]:
                        continue

                    # OpenAI format uses 'delta' in streaming responses
                    if "delta" in chunk["choices"][0]:
                        delta = chunk["choices"][0]["delta"].get("content", "")
                        if delta:
                            yield delta
                    else:
                        # Some API implementations might use different formats
                        content = (
                            chunk["choices"][0].get("message", {}).get("content", "")
                        )
                        if content:
                            yield content
                except json.JSONDecodeError as e:
                    logger.warning(f"Error decoding JSON chunk: {e}, chunk: {line}")
                    continue

    except requests.exceptions.RequestException as e:
        logger.error(f"Streaming request error: {e}")
        if hasattr(e, "response") and e.response:
            status_code = e.response.status_code
            error_text = e.response.text
            logger.error(f"Response status: {status_code}")
            logger.error(f"Response body: {error_text}")

            # Create and raise APIError with details
            api_error = APIError(chat_endpoint, status_code, error_text)
            raise api_error
        else:
            # Network error, no response
            api_error = APIError(chat_endpoint, None, str(e))
            raise api_error
    except FileNotFoundError:
        # Re-raise any image path errors
        raise
    except Exception as e:
        logger.error(f"Unexpected error during streaming: {e}")
        raise ValueError(f"Failed to process streaming response: {e}")


def stream_to_console(generator: Generator[str, None, None], end: str = ""):
    """
    Stream response chunks to console, useful for CLI applications or notebooks.

    Args:
        generator: The generator from run_*_stream functions
        end: String appended after each chunk, defaults to empty string for seamless display
    """
    import sys

    try:
        for chunk in generator:
            print(chunk, end=end, flush=True)
        print()  # Add a newline at the end
    except KeyboardInterrupt:
        print("\nGeneration interrupted by user.")
    except Exception as e:
        print(f"\nError during streaming: {e}")
