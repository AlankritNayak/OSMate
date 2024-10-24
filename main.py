"""
Defines the FastAPI application and its routes.
"""

import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from models.requests import UserMessageRequest
from models.models import LLMResponse
from llm_service import LLMService
from providers import get_llm_service
from config import get_steps_file

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    """
    Handles validation errors.
    :return: JSONResponse: A JSON response containing the error message.
    """
    return JSONResponse(status_code=400, content={"msg": exc.errors()[0]["msg"]})


@app.get("/")
def root():
    """
    Returns a list of available routes.
    :return:
        dict: A dictionary containing the available routes.
    """
    return {
        "available_endpoints": [
            "/agent",
            "/steps/{session_id}",
            "/docs",
        ]
    }


@app.post(
    "/agent",
    response_model=LLMResponse,
    description="Process a user message using the LLMService.",
)
async def process_user_message(
    user_message: UserMessageRequest, llm_service: LLMService = Depends(get_llm_service)
):
    """
    Processes a user message using the LLMService.
    :param user_message:
    :param llm_service:
    :return: LLMResponse: A dictionary containing the result of processing the user message.
    """
    try:
        llm_service_response = await llm_service.execute(user_message.msg)
        return llm_service_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/steps/{session_id}", description="Get the steps for a given session.")
async def get_steps(session_id: str):
    """
    Retrieves the steps for a given session.
    :param session_id:
    :return: A txt file containing all the steps performed in a session.
    """
    try:
        steps_file = get_steps_file(session_id)
        if os.path.exists(steps_file):
            return FileResponse(steps_file)
        raise HTTPException(
            status_code=404, detail="Steps are not available for the given session."
        )
    except OSError as e:
        raise HTTPException(
            status_code=500, detail=f"File access error: {str(e)}"
        ) from e
