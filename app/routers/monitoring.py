from typing import Any

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse


class Monitoring:
    """Singleton for service monitoring status"""

    readiness = False

    def __new__(cls, *args: Any, **kwargs: Any) -> "Monitoring":
        raise RuntimeError("Monitoring is a singleton")


router = APIRouter(tags=["monitoring"])


@router.get("/readiness")
async def get_readiness() -> JSONResponse:
    """Check if the service is ready"""
    if Monitoring.readiness:
        return JSONResponse(status_code=200, content={"status": "OK"})

    raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE)
