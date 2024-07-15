from pydantic import BaseModel
from pydantic import Field
from app.config import settings


class Resources(BaseModel):
    cpu: str = Field(pattern=r"^[0-9]+$", default=settings.default_cpus)
    gpu: str = Field(pattern=r"^[0-9]+$", default=settings.default_gpus)
    ram: str = Field(pattern=r"^[0-9]+MB$", default=settings.default_ram)
    storage: str = Field(pattern=r"^[0-9]+GB$", default=settings.default_storage)


class TaskRequest(BaseModel):
    task_type: str
    code: str
    resources: Resources


class TaskResponse(BaseModel):
    status: str
    output: str
