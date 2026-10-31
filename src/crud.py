from sqlalchemy.orm import Session

from src.models import Task
from src.schemas import TaskCreate, TaskUpdate


def create_task(db: Session, task_in: TaskCreate) -> Task:
    db_task = Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session) -> list[Task]:
    return db.query(Task).all()


def get_task(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(db: Session, task_id: int, task_in: TaskUpdate) -> Task | None:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        return None
    # N-01: use exclude_unset=True to apply only the fields supplied in the request
    for field, value in task_in.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int) -> Task | None:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        return None
    db.delete(task)
    db.commit()
    return task
