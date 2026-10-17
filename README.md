# Quick Arithmetic

A locally runnable calculator web application built with FastAPI and a small HTML, CSS, and JavaScript frontend. It supports addition, subtraction, multiplication, and division without storing data.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn src.main:app --reload
```

Open http://127.0.0.1:8000 in a browser.

## Run tests

```powershell
python -m pip install -r requirements-test.txt
pytest
```

The calculator uses decimal arithmetic and keeps all values in the current page/request. No database is required.