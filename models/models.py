"""
Contains models used in the application.
"""

from pydantic import BaseModel


class LLMResponse(BaseModel):
    """
    Represents a response from the LLM model.
    """

    session_id: str
    msg: str
