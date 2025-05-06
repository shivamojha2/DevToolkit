"""
Error handling
"""

from typing import Any, Dict


class APIError(Exception):
    """Exception raised for API request errors with detailed information for debugging."""

    # Common API error codes and their meanings
    ERROR_CODES = {
        400: "Bad Request - The request was malformed or contains invalid parameters",
        401: "Unauthorized - Authentication failed, check your API key",
        403: "Forbidden - You don't have permission to access this resource",
        404: "Not Found - The requested endpoint does not exist",
        429: "Too Many Requests - Rate limit exceeded, try again later",
        500: "Internal Server Error - Server error, try again later",
        502: "Bad Gateway - Gateway error, try again later",
        503: "Service Unavailable - Server temporarily unavailable, try again later",
        504: "Gateway Timeout - Request timed out, try again later",
    }

    def __init__(
        self, url: str, status_code: int = None, message: str = "", method: str = "POST"
    ) -> None:
        self.url = url
        self.status_code = status_code
        self.message = message
        self.method = method
        self.error_type = self._get_error_type()
        self.suggestion = self._get_suggestion()

        error_msg = f"API {self.method} request to '{self.url}' failed"
        if self.status_code:
            error_msg += f" with status code {self.status_code} ({self.error_type})"
        if self.message:
            error_msg += f": {self.message}"
        if self.suggestion:
            error_msg += f". {self.suggestion}"

        super().__init__(error_msg)

    def _get_error_type(self) -> str:
        """Map status code to a human-readable error type."""
        if not self.status_code:
            return "Unknown error"
        return self.ERROR_CODES.get(self.status_code, f"HTTP Error {self.status_code}")

    def _get_suggestion(self) -> str:
        """Provide troubleshooting suggestions based on status code."""
        if not self.status_code:
            return "Check your network connection and API endpoint URL"

        if self.status_code == 400:
            return "Check the request parameters and payload format"
        elif self.status_code in (401, 403):
            return "Verify your API key and permissions"
        elif self.status_code == 404:
            return "Verify the API endpoint URL"
        elif self.status_code == 429:
            return "Wait before sending more requests or implement rate limiting"
        elif self.status_code >= 500:
            return "Try again later or contact the API provider"
        return ""

    def get_details(self) -> Dict[str, Any]:
        """Return error details as a dictionary for logging or reporting."""
        return {
            "url": self.url,
            "method": self.method,
            "status_code": self.status_code,
            "error_type": self.error_type,
            "message": self.message,
            "suggestion": self.suggestion,
        }
