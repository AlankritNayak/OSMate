"""
Contains request models.
"""

from pydantic import BaseModel, field_validator


class UserMessageRequest(BaseModel):
    """
    Represents a users natural language message.
    """

    msg: str

    @classmethod
    @field_validator("msg")
    def ensure_not_empty(cls, v):
        """
        Ensures the message is not empty.
        """
        if not v.strip():
            raise ValueError("Message cannot be empty.")
        return v

    @classmethod
    @field_validator("msg")
    def ensure_not_all_digits(cls, v):
        """
        Ensures the message is not all digits.
        """
        if v.isdigit():
            raise ValueError("Message cannot be all digits.")
        return v
