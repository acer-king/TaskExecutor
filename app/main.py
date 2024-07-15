from fastapi import FastAPI, Depends
from typing_extensions import Annotated

from app.schemas import TaskRequest, TaskResponse
from app.task_executor import TaskExecutor
from app.dependency import get_task_executor

app = FastAPI()



@app.post("/execute_task", response_model=TaskResponse)
async def execute_task(task: TaskRequest, task_executor: Annotated[TaskExecutor, Depends(get_task_executor)]):
    result = await task_executor.execute(task)
    return TaskResponse(status="success", output=result)
