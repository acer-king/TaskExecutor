import asyncio
from app.config import settings
from app.schemas import TaskRequest
from app.docker_manager import DockerManager
from fastapi import HTTPException


class TaskExecutor:
    def __init__(self):
        self.docker_manager = DockerManager()

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
