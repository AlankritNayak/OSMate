"""
Contains environment variable and other configurations.
"""

import os
from pydantic_settings import BaseSettings
from pydantic import field_validator
from pydantic import SecretStr


class Settings(BaseSettings):
    """
    Contains environment variables.
    """

    open_ai_api_key: str = ""

    @classmethod
    @field_validator("open_ai_api_key", mode="before")
    def check_open_ai_api_key(cls, value: str):
        """
        Ensures that the 'open_ai_api_key' is provided and not empty.
        """
        if not value or len(value.strip()) == 0:
            raise ValueError(
                "The OpenAI API key (open_ai_api_key) must be set in the env file."
            )
        return value

    class Config:
        """
        Contains configuration settings
        """

        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        env_file = f"{ROOT_DIR}/.env"


settings = Settings()

_LOG_DIR = os.path.join(Settings.Config.ROOT_DIR, "logs")


def get_log_dir() -> str:
    """
    Returns the log directory, creating it if it doesn't exist.
    :return: str: path to log directory.
    """
    try:
        if not os.path.exists(_LOG_DIR):
            os.makedirs(_LOG_DIR)
        return _LOG_DIR
    except OSError as e:
        raise RuntimeError(f"Failed to create log directory: {str(e)}") from e


def get_steps_file(session_id: str) -> str:
    """
    Returns the step file for a given session id.
    :param session_id:
    :return: str: path to the step file.
    """
    return os.path.join(get_log_dir(), f"{session_id}_steps.txt")


def get_llm_key() -> SecretStr:
    """
    Returns the OpenAI API key.
    :return: SecretStr: OpenAI API key.
    """
    return SecretStr(settings.open_ai_api_key)
