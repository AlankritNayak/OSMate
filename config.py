import os
import json
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    open_ai_api_key: str

    class Config:
        ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
        env_file = f"{ROOT_DIR}/.env"