from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str
    description: str
    status: Literal["todo", "in_progress", "done"] = "todo"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal["todo", "in_progress", "done"]] = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: str
