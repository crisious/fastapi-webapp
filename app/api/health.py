"""Service health endpoint."""
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    """Liveness probe."""
    return {"status": "ok", "service": "fastapi-webapp", "version": "0.1.0"}
