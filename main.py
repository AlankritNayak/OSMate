from fastapi import FastAPI
from models.requests import UserMessageRequest

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/agent")
async def process_user_message(user_message: UserMessageRequest):
    return {"message": f"User message: {user_message.msg}"}
