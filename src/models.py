from sqlalchemy import Column, Integer, String

from src.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    status = Column(String(20), nullable=False, default="todo")
