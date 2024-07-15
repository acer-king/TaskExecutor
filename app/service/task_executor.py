import asyncio
from typing import Annotated

from fastapi import HTTPException
from fastapi import Depends

from app.config import settings
from app.models.schemas import TaskRequest
from app.service.docker_manager import DockerManager


class TaskExecutor:
    def __init__(self, docker_manager: Annotated[DockerManager, Depends(DockerManager)]):
        self.docker_manager = docker_manager

    async def execute(self, task: TaskRequest) -> str:
        """
        execute task inside docker container with resources specified in task.
        :param task:
        :return:
        """
        try:
            result = await asyncio.wait_for(self.docker_manager.run_container(task.code, task.resources),
                                            settings.default_time_out
                                            )
            if "Traceback" in result and "Error" in result:
                raise HTTPException(status_code=422, detail=result)
            return result
        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail='timeout')
