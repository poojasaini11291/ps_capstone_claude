from typing import List, Optional
from sqlalchemy.orm import Session

from src.models import Task
from src.schemas import TaskCreate, TaskUpdate


def create_task(db: Session, task_data: TaskCreate) -> Task:
    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session) -> List[Task]:
    return db.query(Task).all()


def get_task(db: Session, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(db: Session, task: Task, update_data: TaskUpdate) -> Task:
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
