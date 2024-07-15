from fastapi import Depends, APIRouter
from typing_extensions import Annotated

from app.models.schemas import TaskRequest, TaskResponse
from app.service.task_executor import TaskExecutor
from app.api.deps import get_task_executor

router = APIRouter()


@router.post("/execute_task", response_model=TaskResponse)
async def execute_task(task: TaskRequest, task_executor: Annotated[TaskExecutor, Depends(get_task_executor)]):
    result = await task_executor.execute(task)
    return TaskResponse(status="success", output=result)
