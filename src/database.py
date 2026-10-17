import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Default database path is ./tasks.db (relative to working directory, i.e. project root).
# Override via DATABASE_URL environment variable if set (DR-003).
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./tasks.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
