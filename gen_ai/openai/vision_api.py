"""
Vision Language model API related functions
"""

from typing import Any, Dict, List, Optional, Tuple, Union

from gen_ai.openai.invoke_model import generate_chat_response
from gen_ai.openai.stream_model import generate_chat_response_streaming
from gen_ai.utils import validate_image_paths


def run_vision_request(
    prompt: Union[str, List[Dict[str, Any]]],
    image_paths: List[str],
    endpoint: str,
    model_name: str,
    api_key: str,
    timeout: int = 30,
    guided_json: Dict[str, Any] = None,
    stream: bool = False,
    return_error: bool = False,
    **kwargs
) -> Union[Optional[str], Tuple[Optional[str], Optional[Dict[str, Any]]]]:
    """
    Convenience function to send a vision request to the LLM API.

    Args:
        prompt: Text prompt or message to send with the images
        image_paths: List of paths to images to include in the request
        endpoint: Base API endpoint URL
        model_name: Name of the model to use
        api_key: API key for authentication
        timeout: Request timeout in seconds
        stream: If True, uses streaming mode for the request
        return_error: If True, returns both the result and error details
        **kwargs: Additional parameters to include in the request (temperature, max_tokens, top_p, etc.)

    Returns:
        If return_error is False: The generated text response or None if the request failed
        If return_error is True: A tuple of (result, error_details) where error_details is None if successful

    Raises:
        FileNotFoundError: If any of the provided image paths don't exist (unless return_error=True)
    """
    # Try to validate image paths early to avoid unnecessary processing
    try:
        image_paths = validate_image_paths(image_paths)
    except FileNotFoundError as e:
        if return_error:
            return None, {
                "error_type": "Image file not found",
                "message": str(e),
                "suggestion": "Check that all image paths exist and are valid files",
            }
        else:
            raise

    messages = (
        [{"role": "user", "content": prompt}] if isinstance(prompt, str) else prompt
    )

    # If streaming is enabled, use the streaming function
    if stream:
        return generate_chat_response_streaming(
            messages=messages,
            endpoint=endpoint,
            model_name=model_name,
            api_key=api_key,
            timeout=timeout,
            image_paths=image_paths,
            **kwargs
        )
    else:
        return generate_chat_response(
            messages=messages,
            endpoint=endpoint,
            model_name=model_name,
            api_key=api_key,
            timeout=timeout,
            guided_json=guided_json,
            return_error=return_error,
            image_paths=image_paths,
            **kwargs
        )
