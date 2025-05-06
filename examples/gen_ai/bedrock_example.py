#!/usr/bin/env python3
"""
Example script demonstrating how to use the BedrockClient
"""

from gen_ai.factory import create_client

client = create_client(provider="bedrock", api_key="your_api_key")
