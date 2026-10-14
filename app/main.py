"""FastAPI application entrypoint.

Serves:
  - JSON API under /api
  - Interactive API docs at /docs (Swagger UI)
  - A static React front end at / (no build step required)
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api import health, items

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(
    title="FastAPI Web App",
    description="Minimal FastAPI + React starter",
    version="0.1.0",
)

# API routes
app.include_router(health.router, prefix="/api")
app.include_router(items.router, prefix="/api")

# Static assets (JS/CSS referenced from index.html)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    """Serve the React front end."""
    return FileResponse(STATIC_DIR / "index.html")
