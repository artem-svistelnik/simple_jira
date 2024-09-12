import os


class DbConfig:
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "postgres")
    DB_CONFIG = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    DB_POOL_SIZE: int = 100
    DB_POOL_MAX_OVERFLOW: int = 30
    DB_COMMAND_TIMEOUT: int = 60
    DB_ISOLATION_LEVEL: str = "REPEATABLE READ"
    SQLALCHEMY_QUERY_DEBUG: bool = False


db_conf = DbConfig()
