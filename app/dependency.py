from app.task_executor import TaskExecutor


async def get_task_executor():
    """
    return instance of TaskExecutor
    :return:
    """
    task_executor = TaskExecutor()
    return task_executor
