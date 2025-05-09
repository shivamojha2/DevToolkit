"""
Bedrock client implementation
"""

import boto3

from gen_ai.api_interface import LLMProvider
from gen_ai.bedrock.invoke_model import run_chat_completions
from gen_ai.bedrock.stream_model import run_chat_completions_streaming


class BedrockClient(LLMProvider):
    """
    Bedrock client implementation
    """

    def __init__(
        self, api_key, model_name, region, secret_key=None, session_token=None
    ):
        self.api_key = api_key
        self.secret_key = secret_key
        self.model_name = model_name
        self.region = region

        aws_config = {
            "region_name": region,
            "aws_access_key_id": api_key,
        }

        if secret_key:
            aws_config["aws_secret_access_key"] = secret_key

        if session_token:
            aws_config["aws_session_token"] = session_token

        # Create clients for both bedrock and bedrock-runtime services
        self.bedrock_client = boto3.client("bedrock", **aws_config)
        self.runtime_client = boto3.client("bedrock-runtime", **aws_config)

    def list_available_models(self):
        """
        List all available foundation models in Bedrock
        """
        try:
            response = self.bedrock_client.list_foundation_models()
            return response.get("modelSummaries", [])
        except Exception as e:
            print(f"Error listing models: {str(e)}")
            return []

    def run_chat_completions(self, messages, **kwargs):
        return run_chat_completions(
            self.runtime_client, messages, self.model_name, **kwargs
        )

    def run_chat_completions_streaming(self, messages, **kwargs):
        return run_chat_completions_streaming(
            self.runtime_client, messages, self.model_name, **kwargs
        )
