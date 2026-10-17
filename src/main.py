from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.routers.calculator import router as calculator_router

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="Calculator")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(calculator_router, tags=["calculator"])


@app.get("/", include_in_schema=False)
def calculator_page() -> FileResponse:
	return FileResponse(STATIC_DIR / "index.html")
