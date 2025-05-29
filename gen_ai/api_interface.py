"""
Abstract base class for LLM providers
"""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers
    """

    @abstractmethod
    def generate_chat_response(self, messages, **kwargs):
        """
        Generate a response in a chat/conversation context.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
                     representing the conversation history
            **kwargs: Additional provider-specific parameters

        Returns:
            Response from the language model in the conversation context
        """
        pass
