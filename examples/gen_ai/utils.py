"""
Utility functions for the gen_ai examples
"""

import json


def print_response(response):
    """Print the response from the API in a formatted way"""
    if isinstance(response, dict):
        if "choices" in response:
            for choice in response["choices"]:
                if "text" in choice:
                    print(f"Response: {choice['text'].strip()}")
                elif "message" in choice:
                    print(f"Role: {choice['message']['role']}")
                    print(f"Content: {choice['message']['content'].strip()}")
        else:
            print(json.dumps(response, indent=2))
    else:
        print(response)
