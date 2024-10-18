from pydantic import BaseModel


class UserMessageRequest(BaseModel):
    msg: str
