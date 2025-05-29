"""
Google Gemini client implementation
"""

from typing import Any, Dict, List, Optional

import google.generativeai as genai

from gen_ai.api_interface import LLMProvider
from gen_ai.errors import APIError


class GeminiClient(LLMProvider):
    """
    Client for Google Gemini API
    """

    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-pro",
        **kwargs,
    ):
        """
        Initialize Gemini client

        Args:
            api_key: Google API key
            model_name: Name of the model to use (defaults to gemini-pro)
            **kwargs: Additional arguments to pass to Gemini client
        """
        self.model_name = model_name
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)
        except Exception as e:
            raise APIError(f"Error initializing Gemini client: {str(e)}")

    def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: float = 1.0,
        top_p: float = 1.0,
        **kwargs,
    ) -> Any:
        """
        Generate a response using Gemini

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            **kwargs: Additional arguments to pass to generate_content

        Returns:
            Response from Gemini API
        """
        try:
            # Convert OpenAI format messages to Gemini format
            gemini_messages = []
            for msg in messages:
                role = "model" if msg["role"] == "assistant" else msg["role"]
                gemini_messages.append({"role": role, "parts": [msg["content"]]})

            # Create generation config
            generation_config = {
                "temperature": temperature,
                "top_p": top_p,
            }
            if max_tokens:
                generation_config["max_output_tokens"] = max_tokens

            # Add any additional parameters
            generation_config.update(kwargs)

            # Create chat and get response
            chat = self.model.start_chat(history=gemini_messages[:-1])
            response = chat.send_message(
                gemini_messages[-1]["parts"][0],
                generation_config=generation_config
            )

            return response

        except Exception as e:
            raise APIError(f"Error calling Gemini API: {str(e)}")