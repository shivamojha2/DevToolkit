"""
Abstract base class for LLM providers
"""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers
    """

    @abstractmethod
    def run_chat_completions(self, messages, **kwargs):
        pass
