import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.config import settings
from app.routers import health, tasks

logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(settings.app_name)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("%s starting up (env=%s, version=%s)", settings.app_name, settings.env, settings.version)
    yield
    logger.info("%s shutting down", settings.app_name)


app = FastAPI(title=settings.app_name, version=settings.version, lifespan=lifespan)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Structured-ish request logging.

    Every request logs method, path, status, and duration. This is the
    minimum viable observability for a service - the first thing you'd wire
    up to a log aggregator (CloudWatch, Loki, Datadog) in a real deployment.
    """
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "%s %s -> %s (%.1fms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


app.include_router(health.router)
app.include_router(tasks.router)


@app.get("/")
def root() -> dict:
    return {"message": f"{settings.app_name} is running", "docs": "/docs"}
