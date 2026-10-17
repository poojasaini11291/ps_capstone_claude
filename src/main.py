from fastapi import FastAPI

from src.database import engine, Base
from src.routers.tasks import router as tasks_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API")

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
