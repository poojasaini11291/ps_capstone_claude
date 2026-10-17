from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.schemas import TaskCreate, TaskUpdate, TaskResponse
from src import crud

router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)


@router.get("/", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} does not exist",
        )
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} does not exist",
        )
    return crud.update_task(db, task, task_update)


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} does not exist",
        )
    crud.delete_task(db, task)
    return {"message": f"Task with ID {task_id} has been deleted"}
