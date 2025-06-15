from contextlib import asynccontextmanager
from typing import AsyncGenerator

import redis.asyncio as redis
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter
from pydantic import ValidationError

from app.model.model import load_model
from app.routers.monitoring import Monitoring
from app.routers.monitoring import router as monitoring_router
from app.routers.predictions import router as predictions_router
from app.settings import Settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[dict, None]:
    """Prepare before app starts and clean up after it stops."""
    settings = Settings()

    redis_connection = redis.from_url(f"redis://{settings.redis_host}", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_connection)

    model = load_model()
    Monitoring.readiness = True

    yield {"model": model}

    Monitoring.readiness = False

    del model
    await redis_connection.aclose()
    await redis_connection.connection_pool.disconnect()


app = FastAPI(
    title="Housing prices dashboard",
    description="House prices prediction API",
    docs_url="/",
    lifespan=lifespan,
)


app.include_router(predictions_router, prefix="/predictions")
app.include_router(monitoring_router, prefix="/monitoring")


@app.exception_handler(ValidationError)
async def exception_handler(_: Request, exc: ValidationError) -> JSONResponse:
    """Exception handler for pydantic ValidationError"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=str(exc),
    )
