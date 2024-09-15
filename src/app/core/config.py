import os

from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "simple-jira"
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:8080",
        "https://localhost:8080",
        "http://localhost",
        "https://localhost",
    ]
    SERVER_PORT: int = 8080
    SERVER_HOST: str = "0.0.0.0"
    RELOAD_ON_CHANGE: bool = True
    BASE_URL: str = "http://0.0.0.0:8080"
    ROOT_PATH: str = ""
    SECRET_KEY: str = "secret"
    JWT_SECRET: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_LIFETIME: int = 3600

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
