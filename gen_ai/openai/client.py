"""
OpenAI client implementation
"""

from gen_ai.api_interface import LLMProvider
from gen_ai.openai.batch_api import run_completions_batch
from gen_ai.openai.invoke_model import run_chat_completions, run_completions
from gen_ai.openai.vision_api import run_vision_request


class OpenAIClient(LLMProvider):
    """
    OpenAI client implementation
    """

    def __init__(self, api_key, endpoint, model_name):
        self.api_key = api_key
        self.endpoint = endpoint
        self.model_name = model_name

    def run_completions(self, prompt, **kwargs):
        return run_completions(
            prompt, self.endpoint, self.model_name, self.api_key, **kwargs
        )

    def run_chat_completions(self, messages, **kwargs):
        return run_chat_completions(
            messages, self.endpoint, self.model_name, self.api_key, **kwargs
        )

    def run_completions_batch(self, prompts, **kwargs):
        return run_completions_batch(
            prompts, self.endpoint, self.model_name, self.api_key, **kwargs
        )

    def run_vision_request(self, prompt, image_paths, **kwargs):
        return run_vision_request(
            prompt, image_paths, self.endpoint, self.model_name, self.api_key, **kwargs
        )
