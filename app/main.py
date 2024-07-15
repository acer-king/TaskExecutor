from fastapi import FastAPI, HTTPException, Depends
from typing_extensions import Annotated

from app.schemas import TaskRequest, TaskResponse
from app.task_executor import TaskExecutor
from app.dependency import get_task_executor

import aiodocker
import subprocess
import logging

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # Add tasks to be executed before the application starts
    logging.info("Running startup tasks...")
    try:
        docker = aiodocker.Docker()
        for image in (await docker.images.list()):
            if "python:3.9-slim" in image["RepoTags"]:
                logging.info("python image does exist")
                return
        logging.info("pulling docker image python:3.9-slim from dockerhub")
        subprocess.run(["docker", "image", "pull", "python:3.9-slim"], check=True)
    except Exception as e:
        logging.error(f"Error on Pulling docker image: {e}")
        raise HTTPException(status_code=500, detail="Error running external script")


@app.post("/execute_task", response_model=TaskResponse)
async def execute_task(task: TaskRequest, task_executor: Annotated[TaskExecutor, Depends(get_task_executor)]):
    result = await task_executor.execute(task)
    return TaskResponse(status="success", output=result)
