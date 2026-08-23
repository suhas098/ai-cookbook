from fastapi import APIRouter

from app.config import settings

router = APIRouter(tags=["ops"])


@router.get("/health")
def health() -> dict:
    """Liveness probe: is the process up and able to respond at all."""
    return {"status": "ok"}


@router.get("/ready")
def ready() -> dict:
    """Readiness probe: is the app ready to serve traffic.

    Trivial here since there are no dependencies to check (no DB, no cache).
    A real service would ping its database / downstream deps here and return
    503 if any are unavailable.
    """
    return {"status": "ready"}


@router.get("/version")
def version() -> dict:
    """Build/version info - useful for confirming what's actually deployed."""
    return {
        "app_name": settings.app_name,
        "version": settings.version,
        "env": settings.env,
    }
