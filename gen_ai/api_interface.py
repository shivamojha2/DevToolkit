"""
Abstract base class for LLM providers
"""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers
    """

    @abstractmethod
    def run_completions(self, prompt, **kwargs):
        pass

    @abstractmethod
    def run_chat_completions(self, messages, **kwargs):
        pass

    @abstractmethod
    def run_vision_request(self, prompt, image_paths, **kwargs):
        pass

    @abstractmethod
    def run_completions_stream(self, prompt, **kwargs):
        pass

    @abstractmethod
    def run_chat_completions_stream(self, messages, **kwargs):
        pass
