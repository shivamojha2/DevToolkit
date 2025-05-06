"""
Vision Language model API related functions
"""

from typing import Any, Dict, List, Optional, Tuple, Union

from gen_ai.openai.invoke_model import run_chat_completions
from gen_ai.utils import validate_image_paths


def run_vision_request(
    prompt: str,
    image_paths: List[str],
    endpoint: str,
    model_name: str,
    api_key: str,
    api_type: str = "chat",
    timeout: int = 30,
    generation_params: Dict[str, Any] = None,
    return_error: bool = False,
    **kwargs,
) -> Union[Optional[str], Tuple[Optional[str], Optional[Dict[str, Any]]]]:
    """
    Convenience function to send a vision request to the LLM API.

    Args:
        prompt: Text prompt to send with the images
        image_paths: List of paths to images to include in the request
        endpoint: Base API endpoint URL
        model_name: Name of the model to use
        api_key: API key for authentication
        api_type: API type to use, either "chat" or "completions"
        timeout: Request timeout in seconds
        generation_params: Optional dictionary with model generation parameters
                          (temperature, max_tokens, top_p, etc.)
        return_error: If True, returns both the result and error details
        **kwargs: Additional parameters to include in the request

    Returns:
        If return_error is False: The generated text response or None if the request failed
        If return_error is True: A tuple (result, error_details)

    Raises:
        FileNotFoundError: If any of the provided image paths don't exist (unless return_error=True)
        ValueError: If api_type is not "chat" or "completions"
    """
    # Validate API type
    if api_type not in ["chat"]:
        error_msg = f"Invalid api_type: {api_type}. Must be 'chat'."
        if return_error:
            return None, {
                "error_type": "Invalid parameter",
                "message": error_msg,
                "suggestion": "Use 'chat' for api_type",
            }
        else:
            raise ValueError(error_msg)

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

    if api_type == "chat":
        messages = [{"role": "user", "content": prompt}]
        return run_chat_completions(
            messages=messages,
            endpoint=endpoint,
            model_name=model_name,
            api_key=api_key,
            timeout=timeout,
            generation_params=generation_params,
            return_error=return_error,
            image_paths=image_paths,
            **kwargs,
        )
