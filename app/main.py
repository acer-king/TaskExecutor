from fastapi import FastAPI, HTTPException

import aiodocker
import subprocess
import logging

from app.config import settings
from app.api.endpoints import task_handler

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # Add tasks to be executed before the application starts
    logging.info("Running startup tasks...")
    try:
        docker = aiodocker.Docker()
        for image in (await docker.images.list()):
            if settings.default_docker_img in image["RepoTags"]:
                logging.info("python image does exist")
                return
        logging.info("pulling docker image python:3.9-slim from dockerhub")
        subprocess.run(["docker", "image", "pull", settings.default_docker_img], check=True)
    except Exception as e:
        logging.error(f"Error on Pulling docker image: {e}")
        raise HTTPException(status_code=500, detail="Error running external script")


app.include_router(task_handler.router, tags=["task_handler"])
