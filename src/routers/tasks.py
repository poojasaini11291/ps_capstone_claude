from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas import TaskCreate, TaskUpdate, TaskResponse
import src.crud as crud

router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)) -> TaskResponse:
    return crud.create_task(db=db, task_in=task_in)


@router.get("/", response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db)) -> list[TaskResponse]:
    return crud.get_tasks(db=db)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)) -> TaskResponse:
    task = crud.get_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int, task_in: TaskUpdate, db: Session = Depends(get_db)
) -> TaskResponse:
    task = crud.update_task(db=db, task_id=task_id, task_in=task_in)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> Response:
    task = crud.delete_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    # N-02: must return Response(status_code=204) explicitly — decorator alone is insufficient
    return Response(status_code=204)
