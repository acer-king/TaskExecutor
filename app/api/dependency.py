from app.service.task_executor import TaskExecutor
from app.service.docker_manager import DockerManager


async def get_task_executor():
    """
    return instance of TaskExecutor
    :return:
    """
    docker_mgr = DockerManager()
    task_executor = TaskExecutor(docker_mgr)
    return task_executor
