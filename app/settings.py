from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Class for storing env variables, should be used as singleton though `get_settings`"""

    private_key: str = ""
    redis_host: str = ""

    class Config:
        """Config class"""

        env_prefix = "HOUSING_PRICES_"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Settings getter, cached"""
    return Settings()
