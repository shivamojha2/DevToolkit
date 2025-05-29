"""
OpenAI client implementation
"""

from gen_ai.api_interface import LLMProvider
from gen_ai.openai.batch_api import generate_batch_response
from gen_ai.openai.invoke_model import generate_chat_response, generate_response
from gen_ai.openai.stream_model import (generate_chat_response_streaming,
                                        generate_response_stream)
from gen_ai.openai.vision_api import run_vision_request


class OpenAIClient(LLMProvider):
    """
    OpenAI client implementation
    """

    def __init__(self, api_key, endpoint, model_name):
        self.api_key = api_key
        self.endpoint = endpoint
        self.model_name = model_name

    def generate_response(self, prompt, **kwargs):
        return generate_response(
            prompt, self.endpoint, self.model_name, self.api_key, **kwargs
        )

    def generate_chat_response(self, messages, **kwargs):
        return generate_chat_response(
            messages, self.endpoint, self.model_name, self.api_key, **kwargs
        )

    def generate_batch_response(self, prompts, **kwargs):
        return generate_batch_response(
            prompts, self.endpoint, self.model_name, self.api_key, **kwargs
        )

    def generate_response_stream(self, prompt, **kwargs):
        return generate_response_stream(
            prompt, self.endpoint, self.model_name, self.api_key, **kwargs
        )

    def generate_chat_response_streaming(self, messages, **kwargs):
        return generate_chat_response_streaming(
            messages, self.endpoint, self.model_name, self.api_key, **kwargs
        )

    def run_vision_request(self, prompt, image_paths, **kwargs):
        return run_vision_request(
            prompt, image_paths, self.endpoint, self.model_name, self.api_key, **kwargs
        )
