# OSMate

OSMate is a FastAPI server that serves an LLM-based agent. 
The server provides a REST API that allows the user to send natural language inputs to perform simple command line tasks on the server-side.
The name OSMate is a combination of the words "OS" and "Mate". The "OS" stands for Operating System, and "Mate" is a colloquial term for a friend or a companion.

## Pre-requisites

- Project is developed using Python 3.10.
- [Poetry](https://python-poetry.org/) is used for managing dependencies.
- Create a `.env` file with the `OPEN_AI_API_KEY`, in the root directory of the project.
- refer to `.env.example` for the format of the `.env` file.

## Features
- Asynchronous FastAPI server that processes JSON-based requests and responses.
- The server acts a gateway to an agent that can perform command line commands, like: navigating file system, CRUD operations on files and more.
- Once the task is complete, the steps taken by LLM can also be checked.
- The server internally uses a ReAct agent from LangGraph to perform the tasks.

## Available Endpoints

- `GET /` - Returns a list of available routes.
- `POST /agent` - Process a user message using the LLMService.
- `GET /steps/{session_id}` - Get the steps taken for a given session.
- `GET /docs` - Access the Swagger API documentation.

## Running the server
You can run the server using either `hypercorn` or `uvicorn`.

### Using Poetry
Make sure you have Poetry installed and added to path.
Then, install the dependencies using Poetry:
```sh
poetry install
```
### Using Hypercorn
Run the server with Hypercorn, with following command
```sh
poetry run hypercorn app/main:app --bind :8080
```

### Using Uvicorn
```sh
poetry run uvicorn main:app --host 0.0.0.0 --port 8080
```

#### Note on Hypercorn
Sometime with Hypercorn you may face this error:
```sh
hypercorn.utils.NoAppError: Cannot load application from 'app/main:app', module not found.
```
In this case, please type the following in your terminal and run the Hypercorn command again:
```sh
export PYTHONPATH=$PWD
```
## Contributing

Pull requests are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/)
