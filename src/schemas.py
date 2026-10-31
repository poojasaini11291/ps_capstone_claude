from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict


StatusEnum = Literal["todo", "in_progress", "done"]


class TaskCreate(BaseModel):
    title: str
    description: str
    status: StatusEnum = "todo"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: str
