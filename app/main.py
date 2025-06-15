from contextlib import asynccontextmanager
from typing import AsyncGenerator

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

from app.model.model import load_model
from app.routers.predictions import router as predictions_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[dict, None]:
    """Prepare before app starts and clean up after it stops."""
    redis_connection = redis.from_url("redis://redis", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_connection)

    model = load_model()

    yield {"model": model}

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
