"""
Contains service provides for dependency injection.
"""

from functools import lru_cache
from llm_service import LLMService


@lru_cache()
def get_llm_service():
    """
    Provides an instance of the LLMService class.
    :return: LLMService: An instance of the LLMService class.
    """
    try:
        return LLMService()
    except Exception as e:
        # Log the error or raise a custom exception
        raise RuntimeError(f"Failed to initialize LLMService: {str(e)}") from e
