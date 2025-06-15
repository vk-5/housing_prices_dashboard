import datetime

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.settings import Settings, get_settings

ALGORITHM = "HS256"

security = HTTPBearer()


def create_token(expires_in_days: int = 365) -> str:
    """Creates JWT tokens"""
    settings = get_settings()
    expire = datetime.datetime.utcnow() + datetime.timedelta(days=expires_in_days)
    payload = {"exp": expire}
    return jwt.encode(payload, settings.private_key, algorithm=ALGORITHM)


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security), settings: Settings = Depends(get_settings)
) -> None:
    """Verifies JWT tokens"""
    token = credentials.credentials

    try:
        _ = jwt.decode(token, settings.private_key, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token malformed",
        )
