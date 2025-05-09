"""
Batch API related functions, using completions endpoint
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from gen_ai.openai.invoke_model import run_completions

# Set up logging
logger = logging.getLogger(__name__)


def run_completions_batch(
    queries: List[str],
    endpoint: str,
    model_name: str,
    api_key: str,
    timeout: int = 60,  # Increased default timeout for batch processing
    return_error: bool = False,
    concurrent: bool = True,
    max_concurrent: int = 5,
    **kwargs,
) -> Union[
    List[Optional[str]], Tuple[List[Optional[str]], List[Optional[Dict[str, Any]]]]
]:
    """
    Send a batch of completion requests to the LLM API.

    Args:
        queries: List of prompt texts to send to the model
        endpoint: Base API endpoint URL (without the /completions part)
        model_name: Name of the model to use
        api_key: API key for authentication
        timeout: Request timeout in seconds
        return_error: If True, returns both the results and error details
        concurrent: If True, process requests concurrently using ThreadPoolExecutor
        max_concurrent: Maximum number of concurrent requests (only used if concurrent=True)
        **kwargs: Additional parameters to include in the request (temperature, max_tokens, top_p, etc.)

    Returns:
        If return_error is False: List of generated text responses (None for failed requests)
        If return_error is True: Tuple of (results, error_details) where error_details contains
                                error information for each failed request

    Example:
        >>> queries = ["Describe a sunset", "What is machine learning?"]
        >>> results = run_completions_batch(queries, endpoint, model_name, api_key)
        >>> for query, result in zip(queries, results):
        >>>     print(f"Query: {query}")
        >>>     print(f"Result: {result}")
    """
    import concurrent.futures

    # Validate inputs
    if not queries:
        if return_error:
            return [], []
        return []

    # Initialize results and errors lists
    results = [None] * len(queries)
    errors = [None] * len(queries)

    # Function to process a single query
    def process_single_query(idx: int):
        query = queries[idx]

        result, error = run_completions(
            query=query,
            endpoint=endpoint,
            model_name=model_name,
            api_key=api_key,
            timeout=timeout,
            return_error=True,
            **kwargs,
        )

        return idx, result, error

    if concurrent and len(queries) > 1:
        # Process queries concurrently
        logger.info(
            f"Processing {len(queries)} queries concurrently with max {max_concurrent} workers"
        )
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=max_concurrent
        ) as executor:
            futures = {
                executor.submit(process_single_query, i): i for i in range(len(queries))
            }

            for future in concurrent.futures.as_completed(futures):
                try:
                    idx, result, error = future.result()
                    results[idx] = result
                    errors[idx] = error
                    logger.info(f"Completed query {idx+1}/{len(queries)}")
                except Exception as e:
                    idx = futures[future]
                    logger.error(f"Error processing query {idx}: {e}")
                    errors[idx] = {
                        "error_type": "Processing error",
                        "message": str(e),
                        "suggestion": "Check if the query is valid",
                    }
    else:
        # Process queries sequentially
        logger.info(f"Processing {len(queries)} queries sequentially")
        for i in range(len(queries)):
            try:
                idx, result, error = process_single_query(i)
                results[idx] = result
                errors[idx] = error
                logger.info(f"Completed query {i+1}/{len(queries)}")
            except Exception as e:
                logger.error(f"Error processing query {i}: {e}")
                errors[i] = {
                    "error_type": "Processing error",
                    "message": str(e),
                    "suggestion": "Check if the query is valid",
                }

    # Return appropriate result format
    if return_error:
        return results, errors
    return results
