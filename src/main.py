from fastapi import FastAPI
from database import create_tables
from routers.tasks import router as tasks_router

create_tables()

app = FastAPI(title="Task Management API")

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
